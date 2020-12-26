
#May add more values as they become relevant, but for now we only have 2

class User_Settings:
    def __init__(self, username, reply_string):
        self.username = username
        self.reply_string = reply_string
    

    #If ths user changes their reply string
    def set_reply_string(self, reply_string):
        self.reply_string = reply_string
    
    #If the user changes their username (@ sign) I am not 100 percent sure how this will go? Need to look into this
    def set_username(self, username):
        self.username = username


