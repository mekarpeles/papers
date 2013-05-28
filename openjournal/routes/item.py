#-*- coding: utf-8 -*-

"""
    item
    ~~~~

    Fetching, voting, and commeting on items (journals)

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from waltz import web, render, session
from api.v1.user import Academic, record_vote, record_comment, canvote
from api.v1.paper import Paper

class Item:

    def GET(self):
        i = web.input(pid=None, cid=None, opt="")
        option = i.pop('opt')

        try: # getting the requested paper
            i.pid = int(i.pid)
            paper = Paper(i.pid)
            if not paper.enabled: raise
        except (TypeError, IndexError):
            raise web.notfound()

        try: # getting the specified comment
            i.cid = int(i.cid)
            comment = paper.comments[i.cid]
            if not comment['enabled']:
                raise IndexError
        except (TypeError, IndexError):
            return render().item(paper)

        if option and comment['username'] == session()['uname'] \
                and session()['logged']: # TODO: or session()['admin']
            if option == "delete":
                paper.activate_comment(i.cid, state=False)
                return render().item(paper)
            if option == "edit": return render().edit(i.pid, i.cid, comment)
        return render().comment(i.pid, i.cid, comment)

    def POST(self):
        """Organize/sort the comments according to votes, author,
        time, etc (heuristic)

        POST route to add a comment to a paper
        side effects:
        - handles votes / karma
        """
        i = web.input(pid=None, cid=None, comment="", opt="", enabled=True)
        option = i.pop('opt')

        try: # getting the requested paper
            i.pid = int(i.pid)
            paper = Paper(i.pid)
        except (TypeError, IndexError):
            # TODO: Log
            # IndexEror("No such paper") or 
            # TypeError("int() arg must be str or number, not 'NoneType'")
            raise web.notfound()

        if not i.comment:
            return render().item(paper)

        if not session().logged:
            raise web.seeother('/login?redir=/item?pid=%s' % i.pid)
        else:
            i.username = session()['uname']

        if option == "edit":
            try:
                paper.edit_comment(i.cid, content=i.comment, enabled=i.enabled)
                
            except (TypeError, ValueError) as e:
                # XXX Log error e
                return render().item(paper)
        else:
            i.cid = paper.add_comment(i.cid, session()['uname'], content=i.comment,
                              votes=paper.votes, enabled=i.enabled)
            record_comment(session()['uname'], i.pid, i.cid)
        return render().item(paper)


    @staticmethod
    def clear(pid):
        """Clear comments for an item"""
        paper = Paper(pid)
        paper.comments = []
        return paper.save()

class Comment:
    def GET(self):
        """Item().POST() should be refactored into Comment,
        routes.submit should be refactored into Item().POST()
        """
        pass

    def POST(self):
        pass

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
        i = web.input(pid=None, sort="popular")
        
        if not session().logged:
            raise web.seeother('/register')

        if i.pid:
            i.pid = int(i.pid)
            u = Academic(session()['uname'])
            p = Paper(i.pid)
            if canvote(u, i.pid):
                try:
                    # move set_vote to paper api
                    p.votes += 1
                    p.save()                    
                    record_vote(u['username'], p.submitter, i.pid)
                except IndexError:
                    return "No such items exists to vote on"
        raise web.seeother('/?sort=%s' % i.sort)
