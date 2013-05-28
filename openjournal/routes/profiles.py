from waltz import web, render, session
from api.v1.user import Academic

class Profile:
    def GET(self, username=""): 
        if username:
            try:
                user = Academic.get(username, safe=True)
                return render().profiles.index(user)
            except:
                pass
        raise web.seeother('/')

    def POST(self):
        """Edit Profile"""
        pass
