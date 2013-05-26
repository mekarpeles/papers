from waltz import render, web
from api.v1.search import Search as S
from api.v1.paper import Paper

class Search:
    def GET(self):
        i = web.input(search="")
        results = []
        if i.search:
            papers = Paper.getall()
            matches = S().match(i.search)
            pids = [int(x['pid']) for x in matches]
            results = [p for p in papers if p['pid'] in pids]
        return render().search(i.search, results)

    def POST(self):
        return self.GET()
