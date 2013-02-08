from waltz import web, render, session, exponential_backoff, User
import re
import datetime

username_len = 2
passwd_len = 6
passwd_valid = '!@#$%^&+=_'
username_regex = r'[A-Za-z0-9_]{%s,}' % username_len
passwd_regex = r'[A-Za-z0-9%s]{%s,}' % (passwd_valid, passwd_len)
passwd_err = "Please make sure your password is at least %s " \
    "characters long and only contains numbers, letters, " \
    "or any of the following special characters: %s" % (passwd_len,
                                                        passwd_valid)
username_err = "Please make sure your username is at least %s " \
    "characters long and only contains numbers, " \
    "letters, or underscores." % username_len

def loadsession(u):
    """Constructs a dict of session variables for user u"""
    session().update({'logged': True,
                      'uname': u['username'],
                      'email': u['email'],
                      'created': u['created'],
                      'bio': u['bio']
                      })

class Login:
    """Requires stateful exponential backoff to prevent rate limiting"""
    def GET(self):
        return render().auth.login()

    def POST(self):
        """TODO: handle redir"""
        i = web.input(username='', passwd='', redir='')
        if i.username and i.passwd:
            try:
                u = User.get(i.username)
                if User.easyauth(u, i.passwd):
                    loadsession(u)
                    raise web.seeother('/')
            except:
                raise
            err = "Incorrect username or password"
        else:
            err = "Please provide all required fields"
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
        if i.username and i.passwd:            
            if re.match(username_regex, i.username):
                if re.match(passwd_regex, i.passwd):
                    try:
                        # treat as login if creds are right
                        u = User.get(i.username)
                        if User.easyauth(u, i.passwd):
                            loadsession(u)
                            raise web.seeother('/')
                    except:
                        pass

                    try:
                        u = User.register(i.username, i.passwd,
                                          **defusr())
                        loadsession(u)
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
        session().update({'logged': False,
                          'uname': '',
                          'karma': 0,
                          })
        session().kill()
        if i.redir:
            raise web.seeother(i.redir)
        raise web.seeother('/')
