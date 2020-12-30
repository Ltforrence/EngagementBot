
#Will be adding more stuff as we go because it is necessary to have basically the whole profile here
#May need to add a since at some point!!! because we 

class User_Settings:
    def __init__(self, username, reply_string, rt = 0, like = 1, reply = 1, verified = 1):
        self.username = username
        self.reply_string = reply_string
        self.rt = rt
        self.like = like
        self.reply = reply
        self.verified = verified #Currently all users are verified lol. This will change as time goes on

    

    #If ths user changes their reply string
    def set_reply_string(self, reply_string):
        self.reply_string = reply_string
    
    #If the user changes their username (@ sign) I am not 100 percent sure how this will go? Need to look into this
    def set_username(self, username):
        self.username = username


