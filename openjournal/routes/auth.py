#-*- coding: utf-8 -*-

"""
    routes.auth
    ~~~~~~~~~~~
"""

import re
import datetime
from waltz import web, render, session, exponential_backoff, User
from api.v1.user import Academic, ERR as AUTH_ERR

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

def login(username, passwd):
    """Logs a user in and sets their session data. Assumes
    credentials have already validated via Academic.validates.
    """
    try:
        # assume user exists, try to fetch account
        u = Academic(username)
    except AttributeError:
        return False
    
    if Academic.authenticates(u, passwd):
        load_session(u, session)
        return True
    return False

class Login:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        return render().auth.login()

    def POST(self):
        """TODO: handle redir"""
        i = web.input(username='', passwd='', redir='/')
        if not (i.username and i.passwd):
            return render().auth.login(err=AUTH_ERR['missing_creds'])
        if not Academic.validates(i.username, i.passwd):
            return render().auth.login(err=AUTH_ERR['malformed_creds'])
        if login(i.username, i.passwd):
            raise web.seeother(i.redir)
        return render().auth.login(err=AUTH_ERR['wrong_creds'])
        

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

        i = web.input(username='', passwd='', redir='/')

        if Academic.validates(i.username, i.passwd):
            if login(i.username, i.passwd):
                raise web.seeother(i.redir)

            try: # attempting registration if login
                u = Academic.register(i.username, i.passwd, **defusr())
                load_session(u, session)
                raise web.seeother(i.redir)
            except Academic.RegistrationException as e:
                err = AUTH_ERR[str(e.message)]
            else: # If there's an uncaught error, assuming missing args for auth
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
