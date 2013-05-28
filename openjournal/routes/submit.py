from waltz import web, render, session
from datetime import datetime
from lazydb.lazydb import Db
from api.v1.search import Search
from api.v1.user import record_vote, record_submission


class Submit:
    def GET(self):
        if not session().logged:
            raise web.seeother('/register')
        return render().submit()

    def POST(self):
        if not session().logged:
            raise web.seeother('/register')

        i = web.input(authors="", url=None, title=None, comments=[],
                      year=None, enabled=True, subtitle='',
                      time=datetime.utcnow(), votes=1,
                      cite={'mla': '', 'apa': '', 'chicago': ''})
        db = Db('db/openjournal')

        def next_pid():
            papers = db.get('papers')
            return papers[-1]['pid'] + 1 if papers else 0

        i.submitter = session()['uname']
        if i.authors:
            i.authors = map(self.parse_author, i.authors.split(','))
        i.pid = next_pid()
        record_submission(i.submitter, i.pid)
        record_vote(i.submitter, i.submitter, i.pid)
        db.append('papers', dict(i))
        Search().index()
        raise web.seeother('/')

    def _authorize(self, name='', email='', institution=''):
        return {'name': name,
                'email': email,
                'institution': institution}

    def _handle_author(self, author_list):
        if author_list[-1] == ')':
            author_list += ' '
        author_list = author_list.replace('(),', '() ,')
        start = author_list.index(' (')
        stop = author_list.index(') ')
        name = author_list[:start]
        email = author_list[start+2:stop]
        institution = author_list[stop+1:]
        return self._authorize(name, email, institution)

    def parse_author(self, author):
        if author:
            if '(' and ')' in author:
                return self._handle_author(author)
            else:
                author = author.split()
                # if there's just one paren, it's probably a typo
                try:
                    author = author.replace('(', '')
                except:
                    pass
                name = author[0] + ' ' + author[1]
                email = filter(lambda x: '@' in x, author)
                try:
                    institution = author[3]
                except IndexError:
                    institution = ' '
                return self._authorize(name, email, institution)
        return self._authorize()
