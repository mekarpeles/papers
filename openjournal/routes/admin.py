from waltz import db

class Analytics:
    def GET(self):
        """This should be migrated to its own route module.
        Also, Db call should be abstracted through an API"""
        return db().get('analytics')
