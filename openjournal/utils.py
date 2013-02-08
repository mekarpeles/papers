from datetime import datetime
from waltz import User # should be moved elsewhere

def str2datetime(s, fmt="%a %b %d %H:%M:%S %Y"):
    """Converts str timestamp to datetime"""
    return s if type(s) is datetime else \
        datetime.strptime(s, fmt)

def canvote(u, pid):
    return pid not in u['votes']

def record_vote(yourname, submitter_name, pid, cid=None):
    """XXX Todo: expose as web api/v1/vote and require nonce?"""
    def inc_vote(user):
        user['votes'].append(pid)
        return user
    submitter = User.get(submitter_name)
    submitter['karma'] +=1
    User.replace(submitter_name, submitter)
    return User.update(yourname, func=inc_vote)
