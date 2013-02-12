import os, sys
from paper import Paper

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

STOPWORDS = ['the', 'a', 'for', 'to', 'and', \
                 'with', 'without', 'within', 'more']    

class Search(object):
    def __init__(self, dbname=os.getcwd()+"/db/idx"):
        self.dbname = dbname

    def index(self):
        """Build openjournal search indices"""
        schema = Schema(attr=TEXT(stored=True),
                        pid=TEXT(stored=True))
        ix = create_in(self.dbname, schema)
        writer = ix.writer()
        
        def index_title(paper):
            writer.add_document(attr=unicode(prune(paper['title']).lower()),
                                pid=unicode(paper['pid']))

        def index_authors(paper):
            for author in p.authors:
                writer.add_document(attr=unicode(author.lower()),
                                    pid=unicode("XXX"))

        papers = Paper.getall()
        for uuid, p in enumerate(papers):
            index_title(p)
            #index_authors(p)
        writer.commit()

    def match(self, query):
        index = open_dir(self.dbname)
        searcher = index.searcher()
        query = unicode(prune(query).lower())
        q = QueryParser("attr", index.schema).parse(query)
        results = searcher.search(q)
        return results

def prune(txt, stopwords=STOPWORDS):
    """Remove any word from words which is a member of the set of
    stop_words
    """
    words = txt.split(" ")
    return ' '.join(filter(lambda word: word not in stopwords, words))
