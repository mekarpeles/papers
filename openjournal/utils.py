from datetime import datetime
import re

r = re.compile(r"(http://[^ ]+)")

def linkify(txt):
    print r.sub(r'<a href="\1">\1</a>', txt)

def str2datetime(s, fmt="%a %b %d %H:%M:%S %Y"):
    """Converts str timestamp to datetime"""
    return s if type(s) is datetime else \
        datetime.strptime(s, fmt)

def minutes_since(s, now=datetime.utcnow(),
                 fmt="%a %b %d %H:%M:%S %Y"):
    return (now - str2datetime(s)).seconds / 60.0

def decayscore(score, t):
    """http://www.seomoz.org/blog/reddit-stumbleupon-delicious-and-hacker-news-algorithms-exposed
    convert time to: hours since submission
    """
    return pow((score - 1) / (t + 2), 1.5)

# Pardon the poor coding style -- below should be moved to api/v1/user
from waltz import User

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

def record_submission(submitter_name, pid):
    """Move to openjoural specific user api.
    Pushes pid onto user's posts set
    """
    u = User.get(submitter_name)
    u['posts'].append(pid)
    return User.replace(submitter_name, u)

def record_comment(commenter_name, pid, cid):
    """XXX add karma to comment voting later
    - you get 1 karma for commenting
    """
    u = User.get(commenter_name)
    u['comments'].append((pid, cid))
    return User.replace(commenter_name, u)
    
