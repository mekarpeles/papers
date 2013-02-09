from waltz import web, track, session, render
from lazydb.lazydb import Db
from datetime import datetime
from utils import str2datetime, decayscore, minutes_since

def popular(papers):
    def rank(paper):
        return decayscore(paper['votes'], minutes_since(paper['time']))
    return sorted(papers, key=lambda paper: rank(paper),
                  reverse=True)
def newest(papers):
    return sorted(papers, reverse=True,
                  key=lambda x: str2datetime(x['time']))

def comments(papers):
    return sorted(papers, reverse=True,
                  key=lambda x: len(x['comments']))

class Index:

    @track
    def GET(self):
        i = web.input(sort="popular", limit=30)
        db = Db('db/openjournal')
        papers = db.get('papers')

        try:
            papers = globals()[i.sort](papers)
        except:
            papers = popular(papers)
        return render().index(papers[:i.limit])

