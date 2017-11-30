import base64, os
# from db import DB

class SessionStore:
    def __init__(self):
        self.SessionStore = {}
        return
    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode('utf-8')
        return rstr
    def createSession(self):
        sessionId = self.generateSessionId()
        self.SessionStore[sessionId] ={}
        return sessionId
    def getSession(self,sessionId ):
        if sessionId in self.SessionStore:
            return self.SessionStore[sessionId]
        else:      
            return None