class User:

    def __init__(self, username, password, userid = -1):
        self.set_userid(userid)
        self.set_username(username)
        self.set_password(password)

    def get_userid(self):
        return self.__userid
    
    def set_userid(self, userid):
        self.__userid = userid

    def get_username(self):
        return self.__username
    
    def set_username(self, username):
        self.__username = username
    
    def get_password(self):
        return self.__password
    
    def set_password(self, password):
        self.__password = password