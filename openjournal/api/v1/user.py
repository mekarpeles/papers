#-*- coding: utf-8 -*-

"""
    api.v1.user
    ~~~~~~~~~~~

    User API and Academic user wrapper

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import re
from datetime import datetime
from waltz import User, session
from waltz.utils import Storage
from waltz.security import username_regex, passwd_regex

USERNAME_LEN = 2
PASSWD_LEN = 6
USERNAME_VALID = ""
PASSWD_VALID = '!@#$%^&+=_'
USERNAME_RE = username_regex % (USERNAME_VALID, USERNAME_LEN)
PASSWD_RE = passwd_regex % (PASSWD_VALID, PASSWD_LEN)

AUTH_ERR = {"malformed_creds": "Password must be at least %s " \
           "characters long and only contains numbers, letters, " \
           "or any of the following special characters: %s. " \
           "Please make sure your username is at least %s " \
           "characters long and only contains numbers, " \
           "letters, or underscores." % (PASSWD_LEN, PASSWD_VALID, USERNAME_LEN),
       "wrong_creds": "Incorrect username or password",
       "already_registered": "Sorry, username already registered"
       }

SESSION_DEFAULTS = {'logged': False,
                    'uname': ''
                    }

class Academic(User):
    
    class RegistrationException(Exception): pass

    @property
    def is_loggedin(self):
        return session().get('logged', False)

    def canvote(self, pid):
        """Predicate which returns a boolean which answers the
        question, can user (pkey username) vote for paper (pkey pid)
        """
        return int(pid) not in self.votes

    def authenticates(self, passwd):
        return self.easyauth(self, passwd)

    def login(self):
        """Constructs a dict of session variables for user u"""
        session().update({'logged': True,
                          'uname': self.username,
                          'email': self.email,
                          'created': self.created,
                          'bio': self.bio
                          })
        return self.is_loggedin

    @staticmethod
    def logout():
        """Invalidates and Academic's session and nullifies/defaults
        their client session data
        """
        session().update(SESSION_DEFAULTS)
        session().kill()

    @classmethod
    def validates(cls, username, passwd):
        """Determines if a username and password are valid.
        Returns a (boolean, msg) tuple
        
        usage:
        >>> validates("mek", "*****")
        (False, ["Incorrect username or password"])
        >>> a, _ = Academic.validates("mek", "*****")
        >>> a
        False
        >>> _, b = Academic.validates(i.username, i.passwd)
        >>> b
        ["Incorrect username or password"]
        """
        if not (username and passwd):
            return False
        if not (re.match(USERNAME_RE, username) and \
                    re.match(PASSWD_RE, passwd)):
            return False
        return True

    @classmethod
    def register(cls, username, passwd, **kwargs):
        if re.match(USERNAME_RE, username):
            if re.match(PASSWD_RE, passwd):
                try:
                    u = User.register(username, passwd, **kwargs)
                    return cls(u.username, user=u)
                except Exception:
                    raise cls.RegistrationException("already_registered")
        raise cls.RegistrationException('malformed_creds')

    @classmethod
    def defaults(cls):
        return {'karma': 0,
                'comments': [],
                'votes': [],
                'posts': [],
                'created': datetime.utcnow(),
                'bio': '',
                'email': ''
                }

## The following needs to be refactored:
    
def canvote(username, pid, cid=None):
    """Predicate which returns a boolean which answers the
    question, can user (pkey username) vote for paper (pkey pid)
    and/or a paper's comment (pkey (pid, cid))
    """
    return int(pid) not in User.get(username)['votes']

def inc_karma(user):
    """Aux func to assist User.update(username, func=?)"""
    user['karma'] += 1
    return user

def record_vote(votername, submittername, pid, cid=None):
    pid = int(pid)
    def inc_vote(user):
        """Closure which captures the scope of pid & cid (entity
        ids) and appends them to the voter's list of voted
        entities
        """
        if cid:
            user['votes'].append(cid) # ((pid,cid))?
        user['votes'].append(pid)
        return user

    voter = User.update(votername, func=inc_vote)
    submitter = User.update(submittername, func=inc_karma)
    return voter, submitter

def record_submission(submitter_name, pid, cid=None):
    """Pushes paper pid onto user's posts set. A submission can be a
    paper or a journal
    """
    u = User.get(submitter_name)
    if cid:
        u.comments.append((pid, cid))
    else:
        u.posts.append(pid)
    return User.replace(submitter_name, dict(u))

def get_karma(username):
    u = User(session()['uname'])
    if u:
        return u['karma']
    return 0

def has_voted(uname, pid):
    u = User(session()['uname'])
    if not u:
        return True
    return True if int(pid) in u.votes else False

def record_comment(commenter_name, pid, cid):
    """XXX add karma to comment voting later
    - you get 1 karma for commenting
    """
    pid, cid = map(int, (pid, cid))
    u = User.get(commenter_name)
    u['comments'].append((pid, cid))
    return User.replace(commenter_name, u)
