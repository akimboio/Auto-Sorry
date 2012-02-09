#!/usr/local/pythenv/adam-api-product/bin/python

import os
import platform

# Make sure we actually have setuptools
try:
    from setuptools import setup
except ImportError:
    if platform.linux_distribution()[0] == "Ubuntu":
        os.system("apt-get update")
        os.system("apt-get -y install python-setuptools")
        from setuptools import setup
    else:
        print "You need to install python setuptools"
        exit()


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="Auto Sorry",
    author="Josh Marlow",
    author_email="josh.marlow@retickr.com",
    version="0.1",
    description=("Josh's script for generating apology emails to the team"),
    license="GPLv3",
    keywords="Fun",
    url="http://about.retickr.com/josh-marlow",
    long_description=read('README'),
    classifiers=[
        "Topic :: Fun",
        ],
    scripts=['auto_sorry.py'],
    data_files=[],
    dependency_links=[],
    install_requires=[
        "reddit"
        ],
)
