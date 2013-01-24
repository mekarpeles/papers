#-*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~
    Waltz Lightweight webserver. Waltz around while never missing a beat.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import waltz
from waltz import web, track, session, render
from lazydb.lazydb import Db
import random

urls = ('/submit', 'Submit',
        '/item/([0-9]+)/?', 'Item',
        '/upvote/?', 'Vote',
        '/', 'Index',
        '/404', 'NotFound',
        '(.*)', 'NotFound')

env = {'random': random}
sessions = {'logged': False,
            'uid': -1,
            'name': ''}
app = waltz.setup.dancefloor(urls, globals(), env=env, sessions=sessions, autoreload=False)

db = Db('db/openjournal')
papers = lambda: db.get('papers')

class Index:
    def GET(self):
        return render().index(papers())

class Vote:
    def GET(self):
        """Research http://news.ycombinator.com/item?id=1781013 how
        hacker news voting works and emulate
        """
        i = web.input(pid=None)
        if i.pid:
            ps = papers()
            
            try:
                ps[int(i.pid)]['votes'] += 1
                db.put('papers', ps)
            except IndexError:
                return "No such items exists to vote on"
            return render().index(ps)

class Item:
    def GET(self, pid=None):
        if pid:            
            try:
                return papers()[int(pid)]
            except IndexError:
                return "No such item exists, id out of range"
        raise web.seeother('/')

class Submit:
    def GET(self):
        return render().submit()

    def POST(self):
        i = web.input(authors=None, url=None, title=None, year=None,
                      enabled=False, submitter='', subtitle='',
                      cite={'mla': '', 'apa': '', 'chicago': ''})
        if i.authors:
            clean_authors = []
            dirty_authors = i.authors.split(',')
            for author in dirty_authors:
                opn = author.index(' (')
                cls = author.index(') ')
                name = author[:opn]
                email = author[opn+2:cls]
                inst = author[cls+1:]
                clean_authors.append({'name': name,
                                      'email': email,
                                      'institution': inst})
            i.authors = clean_authors
        db = Db('db/openjournal')
        db.append('papers', dict(i))
        raise web.seeother('/')
                  
class NotFound:
    def GET(self, err=None):
        raise web.notfound('')

if __name__ == "__main__":
    app.run()
