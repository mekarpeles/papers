#-*- coding: utf-8 -*-

"""
    routes.auth
    ~~~~~~~~~~~

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from waltz import web, render, session
from api.v1.user import Academic, AUTH_ERR

def login(username, passwd):
    try:
        u = Academic(username)
        if u.authenticates(passwd):
            return u.login()
    except:
        return False

class Login:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        return render().auth.login()

    def POST(self):
        """TODO: handle redir"""
        i = web.input(username='', passwd='', redir='/')

        if not Academic.validates(i.username, i.passwd):
            return render().auth.login(err=AUTH_ERR['malformed_creds'])

        if login(i.username, i.passwd):
            raise web.seeother(i.redir)

        return render().auth.login(err=AUTH_ERR['wrong_creds'])


class Register:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        if session().logged:
            raise web.seeother('/')
        return render().auth.register()

    def POST(self):
        i = web.input(username='', passwd='', redir='/')

        if session().logged:
            raise web.seeother(i.redir)

        if not Academic.validates(i.username, i.passwd):
            return render().auth.login(err=AUTH_ERR['malformed_creds'])

        # attempting login first
        if login(i.username, i.passwd):
            raise web.seeother(i.redir)

        try:
            u = Academic.register(i.username, i.passwd, **Academic.defaults())
            u.login()
            raise web.seeother(i.redir)
        except Academic.RegistrationException as e:
            err = AUTH_ERR[str(e.message)]
        return render().auth.register(err=err)

class Logout:
    def GET(self):
        """Invalidate session, etc"""
        i = web.input(redir='/')
        Academic.logout()
        raise web.seeother(i.redir)
