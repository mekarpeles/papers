#-*- coding: utf-8 -*-

"""
    openjournal
    ~~~~~~~~~~~
"""

from distutils.core import setup

setup(
    name='openjournal',
    version='0.0.2',
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
        'waltz >= 0.1.698',
        'paste >= 1.7.5.1',
        'lepl >= 5.1.3',
        'whoosh >= 2.4.1',
        'requests >= 1.1.0',
        'pypdf',
        'markdown'
    ],
    description="OpenJournal is a community for sharing academic papers.",
    long_description=open('README.md').read(),
)
