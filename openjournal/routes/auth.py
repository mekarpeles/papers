from waltz import web, render, session, exponential_backoff

class Login:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        pass

class Register:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        pass

class Logout:
    def GET(self):
        """Invalidate session, etc"""
        i = web.input(redir='')
        session().logged = False
        session().uid = None
        session().uname = ''
        session().kill()
        if i.redir:
            raise web.seeother(i.redir)
        return "Logged out"
