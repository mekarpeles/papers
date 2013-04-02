#-*- coding: utf-8 -*-

"""

"""

import os
from datetime import datetime
from lazydb import Db

class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
    
        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'
    
    """
    def __getattr__(self, key): 
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __setattr__(self, key, value): 
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __repr__(self):     
        return '<Storage ' + dict.__repr__(self) + '>'

class Paper(Storage):

    def __init__(self, pid):
        self.pid = pid
        for k, v in self.get(pid).items():
            setattr(self, k, v)
    
    def __repr__(self):     
        return '<Paper ' + dict.__repr__(self) + '>'

    @staticmethod
    def db(dbname=os.getcwd()+"/db/openjournal"):
        return Db(dbname)

    @classmethod
    def getall(cls):
        return cls.db().get('papers')
    
    @classmethod
    def get(cls, pid):
        papers = cls.getall()
        if pid:
            try:
                return papers[pid]
            except IndexError as e:
                raise IndexError("No paper with pid %s. Details: %s" % (pid, e))
        raise ValueError("Paper.get(pid) invoked with invald or non-existing id: %s" % pid)
        
    @staticmethod
    def decay(score, t):
        """seomoz.org/blog/reddit-stumbleupon-delicious-and-hacker-news-algorithms-exposed
        convert time to: hours since submission
        """
        return pow((score - 1) / (t + 2), 1.5)

    @classmethod
    def sort(cls, method="popular"):
        papers = cls.papers()
        def popular():
            return sorted(papers, key=lambda paper:decay(paper),
                          reverse=True)

    @classmethod
    def paginate(cls, papers, page=0, limit=30):
        """Paginates a list of papers

        >>> paginate(range(5), page=1, limit=2)
        [3, 4]
        """
        offset = page * limit
        end = offset + limit
        if offset > len(papers):
            return []
        if end > len(papers):
            return papers[offeset:]
        return papers[offset:end]

    @classmethod
    def score(pid, cid=None, decay=True):
        """Returns the score for a single paper (or a paper's
        comment). If you need to get the score (e.g. sorting/ranking)
        for multiple papers, consider applying the decay function
        directly to query all journals (with sorted() or map()).
        Otherwise, Item.score will get all papers from db every time.

        i.e./TLDR; Don't map/sorted over Item.score, instead map over
        cls.decay
        """
        return cls.decay(cls.papers())[pid]['score']

class Comment(Storage):
    def __init__(self, pid, cid):
        for k, v in self.get(pid, cid).items():
            setattr(self, k, v)

    def edit(self, comment):
        """XXX Update timestamp? Version Control comment revs / edits?"""
        try:
            self.comment = comment
            self.save()
        except Exception as e:
            raise Exception("Failed to save, rolling back transaction." \
                                "Details: %s" % e)

    def delete(self):
        try:
            self.enabled = False
            self.save()
        except Exception as e:
            raise Exception("Failed to save, rolling back transaction." \
                                "Details: %s" % e)

    def save(self):
        papers = self.db().get('papers')
        papers[self.pid]['comments'][self.cid] = self.items()
        self.db().puts('papers', papers)

    @staticmethod
    def db(dbname=os.getcwd()+"/db/openjournal"):
        return Db(dbname)
    
    @classmethod
    def get(cls, pid, cid):
        papers = cls.db().get('papers')
        if pid and cid:
            try:
                paper = papers[pid]
                try:
                    return paper['comments'][cid]
                except IndexError as e:
                    raise IndexError("Paper with pid %s has no comment " \
                                         "with cid: %s. Details: %s" %
                                     (pid, cid, e))
            except IndexError as e:
                raise IndexError("No paper with pid %s. Details: %s" % (pid, e))
        raise ValueError("Comment.get(pid) invoked with invald or non-existant " \
                             "<pid: %s> or <cid: %s>" % (cid, pid))

    def __repr__(self):     
        return '<Paper ' + dict.__repr__(self) + '>'

