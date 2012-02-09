#!/usr/bin/env python2.7

import random
import smtplib
from email.mime.text import MIMEText
import sys

import reddit

srcReddit = "aww"
corpus = ["I'm sorry",
          "I'm really really sorry",
          "I'm super sorry",
          "I'm very very sorry",
          ]

startWords = [sen.split(' ')[0] for sen in corpus]


def getRedditLink():
    print "Getting links from reddit..."
    r = reddit.Reddit(user_agent='auto_sorry')
    submissionGenerator = r.get_subreddit(srcReddit).get_hot(limit=20)
    urls = [x.url for x in submissionGenerator]

    return random.choice(urls)


def buildHMM(corpus):
    print "Building HMM from {0} sentences".format(len(corpus))
    hmm = {}

    # Build the count dictionary
    for sen in corpus:
        # For each sentence
        words = sen.split(' ')
        for i in range(len(words) - 1):
            # For each word
            word = words[i]
            nextWord = words[i + 1]

            hmm[word] = hmm.get(word, {})
            hmm[word][nextWord] = hmm[word].get(nextWord, 0.0) + 1

    # Normalize the counts
    for word in hmm.keys():
        for word2 in hmm[word].keys():
            hmm[word][word2] /= len(hmm[word])

    return hmm


def generateApology(hmm, startWords):
    def pickWord(currentWord, nextWords):
        if len(nextWords) > 0:
            # Do we have some words to choose from
            individualProbs = [nextWords[word] for word in nextWords.keys()]
            # Create a stacked probability list
            cumulativeProbs = [
                sum(individualProbs[:idx + 1])
                for idx in range(len(individualProbs))]

            # Pick a random value
            p = random.random()

            # Find the first index >= to p
            for idx in range(len(nextWords)):
                word = nextWords.keys()[idx]
                cp = cumulativeProbs[idx]

                if p > cp:
                    return word
            else:
                return nextWords.keys()[-1]
        else:
            # We don't know how to follow this word
            return None

    cw = random.choice(startWords)

    print "Generating apology starting with word '{0}'".format(cw)

    idx = 0
    maxWordLen = 10

    chain = [cw]

    while idx < maxWordLen:
        nw = pickWord(cw, hmm.get(cw, {}))

        if nw:
            chain += [nw]
            cw = nw
        else:
            break

        idx += 1

    return " ".join(chain)


def sendEmail(msg, link):
    print "Building email"
    message = "<html>{0}<br /><br /><a href=\"{1}\">{1}</a></html>".format(msg, link)

    msg = MIMEText(message, 'html')
    msg['Subject'] = "auto_sorry has generated an apology on behalf of {0}".format(sender)
    msg["From"] = sender
    msg["To"] = target
    msg["Reply-To"] = sender

    print "Sending email"
    server = smtplib.SMTP('localhost')
    server.sendmail(sender, target, msg.as_string())
    server.quit()


def main(sender, target):
    # Generate the message
    hmm = buildHMM(corpus)
    msg = generateApology(hmm, startWords)

    # Pick a random link
    link = getRedditLink()

    print '\n----------------------\n'

    print msg + "\n\n" + link + "\n"

    sendEmail(msg, link)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: python auto_sorry sender target"
    else:
        sender = sys.argv[1]
        target = sys.argv[2]

        main(sender, target)
