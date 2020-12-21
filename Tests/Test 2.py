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

#Below this is just a small test of the last 20 tweets on my timeline
#At first run I just had my own tweets here, but it was successful and it did return 20 of them as I wanted.

timeline = api.home_timeline()
for tweet in timeline:
    print(f"{tweet.user.name} said {tweet.text}")
