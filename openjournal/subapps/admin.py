#-*- coding: utf-8 -*-

"""
    subapps.api
    ~~~~~~~~~~~
"""

from waltz import web

urls = ("/edit", "Edit")

class Edit:
    def GET (self):
        i = web.input()
        return i

subapp = web.application(urls, globals())
