#-*- coding: utf-8 -*-

"""
    item
    ~~~~
    Fetching, voting, and commeting on items (journals)
"""

from waltz import web, render, session, User
from datetime import datetime
from lazydb import Db

class Item:
    def GET(self):
        i = web.input(pid=None, comment=None)        
        if i.pid:
            try:
                db = Db('db/openjournal')
                papers = db.get('papers')
                paper = papers[int(i.pid)]
                if i.comment:
                    comment = paper['comments'][int(i.comment)]
                    return render().comment(i.pid, i.comment, comment)
                return render().item(i.pid, paper)
            except IndexError:
                return "No such item exists, id out of range"
        raise web.seeother('/')

    def POST(self):
        """Organize/sort the comments according to votes, author,
        time, etc (heuristic)

        XXX Add voting + karma to comments
        """
        i = web.input(pid=None, time=datetime.utcnow().ctime(),
                      comment="", user="Anonymous", votes=0)
        if i.pid:
            try:
                db = Db('db/openjournal')
                papers = db.get('papers') 
                paper = papers[int(i.pid)]
                papers[int(i.pid)]['comments'].append(dict(i))
                db.put('papers', papers)
                return render().item(i.pid, paper)
            except IndexError:
                return "No such item exists, id out of range"
        raise web.seeother('/')        

    @staticmethod
    def clear(pid):
        """Clear comments for an item"""
        db = Db('db/openjournal')
        papers = db.get('papers')
        papers[int(pid)]['comments'] = []
        return db.put('papers', papers)

class Vote:
    def GET(self):
        """Research http://news.ycombinator.com/item?id=1781013 how
        hacker news voting works and emulate

        XXX Restrict voting to session().logged users + element id
        must not already exist in user['votes'] set.

        XXX Requires accounting + record keeping

        XXX Preserve the web.ctx GET query params to preserve sorting
        / ordering

        Algo:
        1. Add karma to paper['submitter'] if vote
        2. Record vote in user['votes'] set by id
        - calc unique vote id via some linear combination of paper pid
          (and or comment id [cid], if it exists)
        """
        msg = None
        i = web.input(pid=None)

        if not session().logged:
            raise web.seeother('/register')

        db = Db('db/openjournal')
        ps = db.get('papers')
        u = User.get(session()['uname'])
        if i.pid and canvote(u, i.pid):
            try:
                ps[int(i.pid)]['votes'] += 1
                db.put('papers', ps)
                submitter_uname = ps[int(i.pid)]['submitter']
                submitter = User.get(submitter_uname)
                submitter['karma'] +=1
                User.replace(submitter_uname, submitter)
                record_vote(u, i.pid)
            except IndexError:
                return "No such items exists to vote on"
        return render().index(ps, msg=msg)

def canvote(u, pid):
    return pid not in u['votes']

def record_vote(u, pid, cid=None):
    def inc_vote(user):
        user['votes'].append(pid)
        return user
    return User.update(u['username'], func=inc_vote)
