#-*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~
    Waltz Lightweight webserver. Waltz around while never missing a beat.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import waltz
from waltz import web, track, session, render
import os
import random
import routes
from datetime import datetime
from lazydb import Db

urls = ('/submit/?', 'routes.item.Submit',
        '/item/?', 'routes.item.Item',
        '/upvote/?', 'routes.item.Vote',
        '/login/?', 'routes.auth.Login',
        '/logout/?', 'routes.auth.Logout',
        '/x/?', 'routes.auth.Register',
        '/404/?', 'routes.responses.NotFound',
        '/admin/?', 'routes.admin.Analytics',
        '/?', 'routes.index.Index',
        '(.*)', 'routes.responses.NotFound')

env = {'random': random,
       'time': lambda x: web.datestr(\
        datetime.strptime(x, "%a %b %d %H:%M:%S %Y"),
        now=datetime.utcnow())
       }
sessions = {'logged': False,
            'authattempt': 0,
            'uid': None,
            'uname': ''}
app = waltz.setup.dancefloor(urls, globals(), env=env, sessions=sessions,
                             db='%s/db/waltz' % os.getcwd(),
                             autoreload=False)

if __name__ == "__main__":
    app.run()
