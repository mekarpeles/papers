from waltz import web, track

class NotFound:
    def GET(self, err=None):
        raise web.notfound('404')
