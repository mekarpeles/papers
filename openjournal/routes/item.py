from waltz import web, render, session
from datetime import datetime
from lazydb.lazydb import Db

JS = lambda msg: "<script type='text/javascript'>alert(\"%s\");</script>" % msg
db = Db('db/openjournal')

class Item:
    def GET(self):
        i = web.input(pid=None, comment=None)
        if i.pid:            
            try:
                papers = db.get('papers')
                paper = papers[int(i.pid)]
                if i.comment:
                    comment = paper['comments'][int(i.comment)]
                    return render().comment(i.pid, comment)
                return render().item(i.pid, paper)
            except IndexError:
                return "No such item exists, id out of range"
        raise web.seeother('/')

    def POST(self):
        """Organize/sort the comments according to votes, author,
        time, etc (heuristic)
        """
        i = web.input(pid=None, time=datetime.utcnow().ctime(),
                      comment="", user="Anonymous", votes=0)
        if i.pid:
            try:
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
        papers = db.get('papers')
        papers[int(pid)]['comments'] = []
        return db.put('papers', papers)

class Vote:
    def GET(self):
        """Research http://news.ycombinator.com/item?id=1781013 how
        hacker news voting works and emulate
        """
        msg = None
        i = web.input(pid=None)
        db = Db('db/openjournal')
        if i.pid:
            ps = db.get('papers')
            if not session().logged:
                msg = JS("Must be logged in to vote")
            else:
                try:
                    ps[int(i.pid)]['votes'] += 1
                    db.put('papers', ps)
                except IndexError:
                    return "No such items exists to vote on"
            return render().index(ps, msg=msg)

class Submit:
    def GET(self):
        return render().submit()

    def POST(self):
        i = web.input(authors=None, url=None, title=None, comments=[],
                      year=None, enabled=False, submitter='',
                      subtitle='', time=datetime.utcnow(),
                      cite={'mla': '', 'apa': '', 'chicago': ''})
        i.authors = map(parse_author, i.authors.split(','))

        # abstract db out of routes
        db = Db('db/openjournal')
        db.append('papers', dict(i))
        raise web.seeother('/')

    @staticmethod
    def parse_author(authors):
        def author(name='', email='', institution=''):
            return {'name': name,
                    'email': email,
                    'institution': institution}
        
        if author: 
            start = author.index(' (')
            stop = author.index(') ')
            name = author[:start]
            email = author[start+2:stop]
            institution = author[stop+1:]
            return author(name, email, institution)
        return author()
