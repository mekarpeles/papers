from waltz import User
from waltz.utils import Storage
from waltz.security import username_regex, passwd_regex

USERNAME_LEN = 2
PASSWD_LEN = 6
USERNAME_VALID = ""
PASSWD_VALID = '!@#$%^&+=_'
USERNAME_RE = username_regex % (USERNAME_VALID, USERNAME_LEN)
PASSWD_RE = passwd_regex % (PASSWD_VLID, PASSWD_LEN)

ERR = {"missing_creds": "Please provide all required fields",
       "malformed_creds": "Please make sure your password is at least %s " \
           "characters long and only contains numbers, letters, " \
           "or any of the following special characters: %s. " \
           "Please make sure your username is at least %s " \
           "characters long and only contains numbers, " \
           "letters, or underscores." % (passwd_len, passwd_valid, username_len),
       "wrong_creds": "Incorrect username or password"
       }

class Academic(Storage, User):
    """class Academic(User(Account))

    Academic An extension of the waltz.User class. It provides
    openjournal specific functions for updating user properties like
    karma, voting, bio, banning, etc.

    Consider a @raisectx decorator to wrap all Academic methods
    which captures and handles the exception following attempted
    access for User outside of the scope of a waltz/webpy route
    """

    def __init__(self, username):
        self.username = username
        u = User.get(self.username)
        try:
            for k, v in User.get(u).items():
                setattr(self, k, v)
        except:
            pass

    def __repr__(self):     
        return '<Academic ' + dict.__repr__(self) + '>'

    @classmethod
    def authenticates(cls, username, passwd):
        """Returns a boolean describing the success of
        authentication
        """
        return super(User, cls).easyauth(user, passwd)

    @classmethod
    def login(cls, u, session):
        """Constructs a dict of session variables for user u"""
        session().update({'logged': True,
                          'uname': u['username'],
                          'email': u['email'],
                          'created': u['created'],
                          'bio': u['bio']
                          })

    @classmethod
    def logout(cls, session):
        """Invalidates and Academic's session and nullifies/defaults their
        client session data"""
        session().update({'logged': False,
                          'uname': '',
                          'karma': 0,
                          })
        session().kill()

    @classmethod
    def validates(cls, username, passwd):
        """Determines if a username and password are valid.
        Returns a (boolean, msg) tuple

        usage:
            >>> Academic.validates("mek", "*****")
            (False, ["Incorrect username or password"])
            >>> a, _ = Academic.validates("mek", "*****")
            >>> a
            False
            >>> _, b = Academic.validates(i.username, i.passwd)
            >>> b
            ["Incorrect username or password"]
        """
        result = True
        errs = []
        if not (username and passwd):
            result = False
            errs.append(ERR["missing_cred"])
        if not (re.match(USERNAME_RE, i.username) and \
            re.match(PASSWD_RE, i.passwd)):
            result = False
            errs.append(ERR["invalid_cred"])
        return result, errs

    @staticmethod
    def canvote(username, pid, cid=None):
        """Predicate which returns a boolean which answers the
        question, can user (pkey username) vote for paper (pkey pid)
        and/or a paper's comment (pkey (pid, cid))
        """
        return pid not in User.get(username)['votes']

    @staticmethod
    def inc_karma(user):
        """Aux func to assist User.update(username, func=?)"""
        user['karma'] += 1
        return user

    @classmethod
    def record_vote(votername, submittername, pid, cid=None):
        def tally_vote(user):
            """Closure which captures the scope of pid & cid (entity
            ids) and appends them to the voter's list of voted
            entities
            """
            if cid:
                user['votes'].append(cid) # ((pid,cid))?
            user['votes'].append(pid)
            return user

        voter = User.update(votername, func=inc_vote)
        submitter = User.update(submittername, func=cls.inc_karma)
        return voter, submitter


    @classmethod
    def record_submission(submitter_name, pid, cid=None):
        """A submission can be a paper or a journal"""
        u = User.get(submitter_name)
        if cid:
            u['comments'].append((pid, cid))
        else:
            u['posts'].append(pid)
        return User.replace(submitter_name, u)
