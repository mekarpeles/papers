# Papers

![Build Status](https://travis-ci.org/mekarpeles/openjournal.png)


**Papers** is an reddit/HackerNews-like interface for sharing, discussing, collaborating on and improving academic papers.

## Installation

    pip install -e .

## Running

    python main.py

## Developing

### Stack

**Papers** currently uses the Waltz web framework (web.py w/ batteries), soon to be replaced with Flask. The database (which will be replaced with a more stable solution) is currently LazyDB, a wrapper over the shelve flatfile db.

## Todo

See Issues.

* Map over all papers and add a 'submission' time field
* Add databasing (other than LazyDB)
* Implement search over papers (whoosh?)
* PDF semantic analyzer (decompose into search terms)
* Network with some schools re: partnerships
* Additional details at https://michaelkarpeles.com/rfcs/1-epic
