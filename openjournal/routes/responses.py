from waltz import web

class NotFound:
    def GET(self, err=None):
        raise web.notfound('404')
