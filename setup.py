#-*- coding: utf-8 -*-

"""
    openjournal
    ~~~~~~~~~~~
"""

from distutils.core import setup

setup(
    name='openjournal',
    version='0.0.1',
    url='http://github.com/mekarpeles/openjournal',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'openjournal',
        'openjournal.subapps',
        'openjournal.routes',
        ],
    platforms='any',
    scripts=[],
    license='LICENSE',
    install_requires=[
        'waltz >= 0.1.68',
        'lepl >= 5.1.3',
        'whoosh >= 2.4.1',
        'pypdf',
        'markdown'
    ],
    description="OpenJournal is a community for sharing academic papers.",
    long_description=open('README.md').read(),
)
