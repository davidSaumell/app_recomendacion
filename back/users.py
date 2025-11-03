class User:

    def __init__(self, userid, password):
        self.set_userid(userid)
        self.set_password(password)

    def get_userid(self):
        return self.__userid
    
    def set_userid(self, userid):
        self.__userid = userid
    
    def get_password(self):
        return self.__password
    
    def set_password(self, password):
        self.__password = password