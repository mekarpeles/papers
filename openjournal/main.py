
import web
from lazydb.lazydb import Db

#-*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~
    Waltz Lightweight webserver. Waltz around while never missing a beat.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import web
from reloader import PeriodicReloader
import random

urls = ('/submit', 'Submit',
        '/', 'Index',
        '/404', 'NotFound',
        '(.*)', 'NotFound')


app = web.application(urls, globals(), autoreload=False)

_globals = {'ctx': web.ctx,
            'random': random}
slender  = web.template.render('templates/', globals=_globals)
render  = web.template.render('templates/', base='base', globals=_globals)

class Index:
    def GET(self):
        papers = Db('db/openjournal').get('papers')
        return render.index(papers)

class Vote:
    def GET(self):
        """Research http://news.ycombinator.com/item?id=1781013 how
        hacker news voting works and emulate
        """
        pass

class Submit:
    def GET(self):
        return render.submit()

    def POST(self):
        i = web.input(authors=None, url=None, title=None, year=None, enabled=False,
                      cite={'mla': '', 'apa': '', 'chicago': ''}, submitter='', subtitle='')
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
    #if SERVER['DEBUG_MODE']:
    PeriodicReloader()
    app.run()
