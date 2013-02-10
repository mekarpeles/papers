from waltz import User

class Academic(User):
    """class Academic(User(Account))

    Academic An extension of the waltz.User class. It provides
    openjournal specific functions for updating user properties like
    karma, voting, bio, banning, etc.

    Consider a @raisectx decorator to wrap all Academic methods
    which captures and handles the exception following attempted
    access for User outside of the scope of a waltz/webpy route
    """

    @staticmethod
    def canvote(username, pid, cid=None):
        """Predicate which returns a boolean which answers the
        question, can user (pkey username) vote for paper (pkey pid)
        and/or a paper's comment (pkey (pid, cid))
        """
        return pid not in User.get(username)['votes']

    @staticmethod
    def inc_karma(user):
        """Aux func to assist User.update(username, func=?)"""
        user['karma'] += 1
        return user

    @classmethod
    def record_vote(votername, submittername, pid, cid=None):
        def tally_vote(user):
            """Closure which captures the scope of pid & cid (entity
            ids) and appends them to the voter's list of voted
            entities
            """
            if cid:
                user['votes'].append(cid) # ((pid,cid))?
            user['votes'].append(pid)
            return user

        voter = User.update(votername, func=inc_vote)
        submitter = User.update(submittername, func=cls.inc_karma)
        return voter, submitter


    @classmethod
    def record_submission(submitter_name, pid, cid=None):
        """A submission can be a paper or a journal"""
        u = User.get(submitter_name)
        if cid:
            u['comments'].append((pid, cid))
        else:
            u['posts'].append(pid)
        return User.replace(submitter_name, u)
