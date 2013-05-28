#-*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~

    Main application for OpenJournal, built using the Waltz Lightweight webserver.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import os
import random
import datetime
import waltz
from waltz import web, User
from api.v1.user import SESSION_DEFAULTS, has_voted, get_karma
from utils import str2datetime
from configs.config import server

urls = ('/submit/?', 'routes.submit.Submit',
        '/item/?', 'routes.item.Item',
        '/upvote/?', 'routes.item.Vote',
        '/search/?', 'routes.search.Search',
        '/rss/?', 'routes.rss.Rss',
        '/admin', 'waltz.modules.Analytics',
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
       'karma': lambda: get_karma(waltz.session()['uname']),
       'voted': lambda pid: has_voted(waltz.session()['uname'], pid),
       'join': lambda x, y: y.join(x)
       }
sessions = SESSION_DEFAULTS
ssl = server['ssl'] if all(server['ssl']) else None
app = waltz.setup.dancefloor(urls, globals(), env=env, sessions=sessions,
                             db='%s/db/waltz' % os.getcwd(), ssl=ssl,
                             autoreload=False)

if __name__ == "__main__":
    app.run()
