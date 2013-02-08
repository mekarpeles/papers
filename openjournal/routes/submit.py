from waltz import web, render, session
from datetime import datetime
from lazydb.lazydb import Db

class Submit:
    def GET(self):
        if not session().logged:
            raise web.seeother('/register')
        return render().submit()

    def POST(self):
        if not session().logged:
            raise web.seeother('/register')

        i = web.input(authors="", url=None, title=None, comments=[],
                      year=None, enabled=False, subtitle='',
                      time=datetime.utcnow(), votes=0,
                      cite={'mla': '', 'apa': '', 'chicago': ''})
        db = Db('db/openjournal')

        def next_pid():
            papers = db.get('papers')
            return papers[-1]['pid'] + 1 if papers else 0

        i.submitter = session()['uname']
        if i.authors:
            i.authors = map(self.parse_author, i.authors.split(','))

        i.pid = next_pid()
        db.append('papers', dict(i))
        raise web.seeother('/')

    @staticmethod
    def parse_author(author):
        def authorize(name='', email='', institution=''):
            return {'name': name,
                    'email': email,
                    'institution': institution}
        
        if author: 
            start = author.index(' (')
            stop = author.index(') ')
            name = author[:start]
            email = author[start+2:stop]
            institution = author[stop+1:]
            return authorize(name, email, institution)
        return authorize()
