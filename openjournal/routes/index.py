from waltz import web, track, session, render
from datetime import datetime
from math import ceil
from lazydb.lazydb import Db
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
        i = web.input(sort="popular", limit=30, page=0)
        db = Db('db/openjournal')
        papers = db.get('papers')
        limit = int(i.limit)
        page = int(i.page)
        pages = int(ceil(float(len(papers)) / limit))
        try:
            papers = globals()[i.sort](papers)
        except:
            papers = popular(papers)
        start = page * limit
        end = start + limit
        return render().index(papers[start:end], pages, i.page,
                              sort=i.sort, limit=limit)

