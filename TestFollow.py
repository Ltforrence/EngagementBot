import tweepy

##The block of code below this is just for establishing the API object

API_Key = "AU4J5aMJ66yuUke52beTQoa8P"
API_Key_Secret = "udw4GdVTo2AKWYQ2S6XoCN66nFIAJYd0bjAwcRIRq7hrcBIu7P"

Access_Token = "1339728373854203906-wptrPawR6KhONBSZ9mw4dPvHMqv5Xj"
Access_Token_Secret = "pWRPDki9F9JDPnvhl8df1aT7Ahu887Fa1U5cxv3cyza1G"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_Key, API_Key_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

##This is the end of the the establishing of the API Object here.



#This is testing following

api.create_friendship("francousmck")

#This did not work on first try
#it says I cannot post
#I believe this may be an issue with my account because it was read only to start