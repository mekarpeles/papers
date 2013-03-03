import waltz
from lazydb import Db
from routes.index import newest

def items():
    """A function which generates all rss items for this website"""
    papers = Db('db/openjournal').get('papers')
    items = []
    desc = "%s - %s votes, submitted by: %s @ %s" 
    for paper in filter(lambda x: x['enabled'], newest(papers)):
        description = desc % (paper['url'], paper['votes'],
                              paper['submitter'], paper['time'])
        items.append({'title': paper['title'],
                      'link': 'https://hackerlist.net:1443/item?pid=%s' % \
                          paper['pid'],
                      'description': description,
                      'date': paper['time'],
                      'guid': paper['pid']})
    return items
        
Rss = waltz.rss(items, **{'title': 'OpenJournal',
                          'description': 'My example waltz application',
                          'generator': 'hackerlist.net',
                          'link': 'http://hackerlist.net:1443',
                          'editor': 'mek',
                          'webmaster': 'm@hackerlist.net'
                          })
