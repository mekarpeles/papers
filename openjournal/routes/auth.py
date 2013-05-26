#-*- coding: utf-8 -*-

"""
    routes.auth
    ~~~~~~~~~~~
"""

import re
import datetime
from waltz import web, render, session, exponential_backoff, User
from api.v1.user import Academic

def load_session(u, session):
    """Constructs a dict of session variables for user u"""
    session().update({'logged': True,
                      'uname': u['username'],
                      'email': u['email'],
                      'created': u['created'],
                      'bio': u['bio']
                      })

def invalidate_session(session):
    session().update({'logged': False,
                      'uname': '',
                      'karma': 0,
                      })
    session().kill()

class Login:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        return render().auth.login()

    def POST(self):
        """TODO: handle redir"""
        i = web.input(username='', passwd='', redir='')
        if Academic.validates(i.username, i.passwd):
            if Academic.authenticates(u, i.passwd):
                load_session(u, session)
                raise web.seeother('/')
            err = ""
        else:
            err = ""
        return render().auth.login(err=err)

class Register:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        return render().auth.register()

    def POST(self):
        def defusr():
            return {'karma': 0,
                    'comments': [],
                    'votes': [],
                    'posts': [],
                    'created': datetime.datetime.utcnow(),
                    'bio': '',
                    'email': ''}

        i = web.input(username='', passwd='', redir='')
        if validates(username, passwd):
            try: # login if creds are right
                u = User.get(
                if User.easyauth(u, i.passwd):
                    load_session(u, session)
                    raise web.seeother('/')
            except:
                pass
                    try:
                        u = User.register(i.username, i.passwd,
                                          **defusr())
                        load_session(u, session)
                        raise web.seeother('/')
                    except:
                        err = "Username unavailable"
                else:
                    err = passwd_err
            else:
                err = username_err
        else:
            err = "Please enter all required fields"
        return render().auth.register(err=err)

class Logout:
    def GET(self):
        """Invalidate session, etc"""
        i = web.input(redir='')
        invalidate_session(session)
        if i.redir:
            raise web.seeother(i.redir)
        raise web.seeother('/')
