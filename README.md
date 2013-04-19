# OpenJournal

![Build Status](https://travis-ci.org/mekarpeles/openjournal.png)


OpenJournal is an online community united around the concept of sharing, discussing, collaborating on and improving academic papers.

## Installation

    pip install -e .

## Running

    python main.py

## Developing

### Stack

OpenJournal was built using a modified version of Waltz running over web.py. The database (which will be replaced with a more stable solution) is currently LazyDB, a wrapper over the shelve flatfile db.

## How can I help?

* Submit articles http://hackerlist.net:1337/submit
* Contribute a feature

## Todo

* Map over all papers and add a 'submission' time field
* Add databasing (other than LazyDB)
* Implement search over papers (whoosh?)
* PDF semantic analyzer (decompose into search terms)
* Network with some schools re: partnerships
* Additional details at michaelkarpeles.com/#openjournal