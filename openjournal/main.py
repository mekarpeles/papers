#-*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~
    Waltz Lightweight webserver. Waltz around while never missing a beat.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import waltz
from waltz import web, track, session, render, User
import os
import random
import routes
import datetime
from utils import str2datetime
from lazydb import Db

urls = ('/submit/?', 'routes.submit.Submit',
        '/item/?', 'routes.item.Item',
        '/upvote/?', 'routes.item.Vote',
        '/search/?', 'routes.search.Search',
        '/admin', 'subapps.admin.Edit',
        '/login/?', 'routes.auth.Login',
        '/register/?', 'routes.auth.Register',
        '/logout/?', 'routes.auth.Logout',
        '/users/(.*)/?', 'routes.profiles.Profile',
        '/x/?', 'routes.auth.Register',
        '/404/?', 'routes.responses.NotFound',
        '/admin/?', 'routes.admin.Analytics',
        '/?', 'routes.index.Index',
        '(.*)', 'routes.responses.NotFound')

env = {'random': random,
       'time': lambda x: web.datestr(str2datetime(x),
                                     now=datetime.datetime.utcnow()),
       'karma': lambda: User.get(session()['uname'])['karma'],
       'voted': lambda pid: str(pid) in \
           User.get(session()['uname'])['votes'],
       }
sessions = {'logged': False,
            'uid': None,
            'uname': ''}
app = waltz.setup.dancefloor(urls, globals(), env=env, sessions=sessions,
                             db='%s/db/waltz' % os.getcwd(),
                             autoreload=False)

if __name__ == "__main__":
    app.run()
