#-*- coding: utf-8 -*-

"""
    item
    ~~~~
    Fetching, voting, and commeting on items (journals)
"""

from waltz import web, render, session, User
from datetime import datetime
from lazydb import Db
from utils import record_vote, record_comment, canvote

class Item:
    def GET(self):
        i = web.input(pid=None, cid=None)
        if i.pid:
            try:
                db = Db('db/openjournal')
                papers = db.get('papers')
                paper = papers[int(i.pid)]
                if i.cid:
                    # XXX Revise to get comment with cid == i.cid, not
                    # i.cid'th element
                    comment = paper['comments'][int(i.cid)]
                    return render().comment(i.pid, i.comment, comment)
                return render().item(i.pid, paper)
            except IndexError:
                return "No such item exists, id out of range"
        raise web.seeother('/')

    def POST(self):
        """Organize/sort the comments according to votes, author,
        time, etc (heuristic)
        """
        i = web.input(pid=None, time=datetime.utcnow().ctime(),
                      comment="", username=session()['uname'], votes=0,
                      enabled=True, cid='0')
        if i.pid:
            if not session().logged:
                raise web.seeother('/login?redir=/item=?pid=%s' % i.pid)
            try:
                db = Db('db/openjournal')
                papers = db.get('papers') 
                paper = papers[int(i.pid)] #XXX get by key 'pid' instead
                
                if paper['comments']: i.cid = paper['comments'][-1]['cid']
                papers[int(i.pid)]['comments'].append(dict(i))
                db.put('papers', papers)
                record_comment(i.username, i.pid, i.cid)
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
                record_vote(u['username'], submitter_uname, i.pid)
            except IndexError:
                return "No such items exists to vote on"
        return render().index(ps, msg=msg)


