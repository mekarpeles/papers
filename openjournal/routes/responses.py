from waltz import web, track

class NotFound:
    @track
    def GET(self, err=None):
        raise web.notfound('404')
