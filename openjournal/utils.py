#-*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~

    Misc utilities for formatting etc.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime

def str2datetime(s, fmt="%a %b %d %H:%M:%S %Y"):
    """Converts str timestamp to datetime"""
    return s if type(s) is datetime else \
        datetime.strptime(s, fmt)

def minutes_since(s, now=datetime.utcnow(),
                 fmt="%a %b %d %H:%M:%S %Y"):
    return (now - str2datetime(s)).seconds / 60.0

def decayscore(score, t):
    """http://www.seomoz.org/blog/reddit-stumbleupon-delicious-and-hacker-news-algorithms-exposed
    convert time to: hours since submission
    """
    return pow((score - 1) / (t + 2), 1.5)
