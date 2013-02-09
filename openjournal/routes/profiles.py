from waltz import web, render, session, User

class Profile:
    def GET(self, username=""): 
        if username:
            try:
                user = User.get(username, safe=True)
                return render().profiles.index(user)
            except:
                pass
        raise web.seeother('/')

    def POST(self):
        """Edit Profile"""
        pass
