# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~

    This module is the middle man for handling/consolidating
    configurations for the openjournal project.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import ConfigParser
import os
import types

def getdef(self, section, option, default_value):
    try:
        return self.get(section, option)
    except:
        return default_value

path = os.path.dirname(__file__)
config = ConfigParser.ConfigParser()
config.read('%s/oj.cfg' % path)
config.getdef = types.MethodType(getdef, config)

server = {'ssl': (config.getdef('ssl', 'cert', ''),
                  config.getdef('ssl', 'key', ''))
          }
