from waltz import web, track, session, render
from lazydb.lazydb import Db
from datetime import datetime
from utils import str2datetime

def popular(papers):
    return sorted(papers, key=lambda x: int(x['votes']),
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

