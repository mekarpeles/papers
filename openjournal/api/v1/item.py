from datetime import datetime
from lazydb import Db

class Item(object):
    
    @staticmethod
    def db():
        return Db('openjournal')

    @classmethod
    def papers(cls):
        return cls.db().get('papers')

    @staticmethod
    def decay(score, t):
        """http://www.seomoz.org/blog/reddit-stumbleupon-delicious-and-hacker-news-algorithms-exposed
        convert time to: hours since submission
        """
        return pow((score - 1) / (t + 2), 1.5)        

    @classmethod
    def sort(cls, method="popular"):
        papers = cls.papers()
        def popular():
            return sorted(papers, key=lambda paper:decay(paper),
                          reverse=True)

    @classmethod
    def paginate(cls, papers, page=0, limit=30):
        """Paginates a list of papers

        >>> paginate(range(5), page=1, limit=2)
        [3, 4]
        """
        offset = page * limit
        end = offset + limit
        if offset > len(papers):
            return []
        if end > len(papers):
            return papers[offeset:]
        return papers[offset:end]

    @classmethod
    def score(pid, cid=None, decay=True):
        """Returns the score for a single paper (or a paper's
        comment). If you need to get the score (e.g. sorting/ranking)
        for multiple papers, consider applying the decay function
        directly to query all journals (with sorted() or map()).
        Otherwise, Item.score will get all papers from db every time.

        i.e./TLDR; Don't map/sorted over Item.score, instead map over
        cls.decay
        """
        return cls.decay(cls.papers()[pid]['score']
