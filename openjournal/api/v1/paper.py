#-*- coding: utf-8 -*-

"""
    api.v1.paper
    ~~~~~~~~~~~~

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import os
from datetime import datetime
from waltz import Storage
from lazydb import Db

class Paper(Storage):

    def __init__(self, pid, paper=None):
        self.pid = int(pid)
        paper = paper if paper else self.get(self.pid)        
        for k, v in paper.items():
            setattr(self, k, v)
    
    def __repr__(self):     
        return '<Paper ' + dict.__repr__(self) + '>'

    @staticmethod
    def db(dbname=os.getcwd()+"/db/openjournal"):
        return Db(dbname)

    @classmethod
    def getall(cls):
        return [Paper(paper['pid'], paper=paper) for \
                    paper in cls.db().get('papers')]
    
    @classmethod
    def get(cls, pid):
        papers = cls.getall()
        if type(pid) is int:
            try:
                return papers[pid]
            except IndexError as e:
                raise IndexError("No paper with pid %s. Details: %s" % (pid, e))
        raise ValueError("Paper.get(pid) invoked with invalid or " \
                             "non-existing id: %s" % pid)
        
    @staticmethod
    def decay(score, t):
        """seomoz.org/blog/reddit-stumbleupon-delicious-and-\
        hacker-news-algorithms-exposed convert time to: hours since
        submission
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

    def activate(self, state=True):
        self.enabled = state
        return self.save()

    def save(self):
        papers = self.getall()
        papers[self.pid] = dict(self)
        return self.db().put('papers', papers)

    def add_comment(self, cid, author, content="", time=None,
                    votes=0, enabled=True):
        if not content:
            raise ValueError("Comment must be a str with len() > 0")
        cid = 0 if not self.comments else int(self.comments[-1]['cid']) + 1
        time = time if time else datetime.utcnow().ctime()
        self.comments.append({'pid': self.pid,
                              'cid': cid,
                              'enabled': enabled,
                              'time': time,
                              'username': author,
                              'comment': content,
                              'edits': []
                              })
        self.save()
        return cid

    def edit_comment(self, cid, content="", time=None, **comment):
        """**comment includes
        """
        if not content:
            raise ValueError("Comment must be a str with len() > 0")
        try:
            cid = int(cid)
        except (TypeError, ValueError) as e:            
            raise # case cid is None or invalid literal w/ base 10
        time = time if time else datetime.utcnow().ctime()
        for index, comment in enumerate(self.comments):
            if self.comments[index]['cid'] == cid:
                c = self.comments[cid]
                if not 'edits' in c:
                    c['edits'] = [time]
                else:
                    c['edits'] += [time]
                c['comment'] = content
                c.update(comment)
                self.comments[cid] = c
        self.save()

    def activate_comment(self, cid, state=True):
        try:
            cid = int(cid)
        except (TypeError, ValueError) as e:            
            raise # case cid is None or invalid literal w/ base 10
        for index, comment in enumerate(self.comments):
            if self.comments[index]['cid'] == cid:
                self.comments[cid]['enabled'] = state
        self.save()
        
class Comment(Storage):
    def __init__(self, pid, cid, comment=None):
        comment = comment if comment else self.get(pid, cid)
        for k, v in comment.items():
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
        raise ValueError("Comment.get(pid) invoked with invalid or non-existant " \
                             "<pid: %s> or <cid: %s>" % (cid, pid))

    def __repr__(self):     
        return '<Paper ' + dict.__repr__(self) + '>'

