from waltz import web, track, session, render
from lazydb.lazydb import Db

class Index:
    @track
    def GET(self):
        db = Db('db/openjournal')
        return render().index(db.get('papers'))

