import tweepy

##The block of code below this is just for establishing the API object

API_Key = "OAmoZ5CiNjB6hSPtDxVlq5TZW"
API_Key_Secret = "horuA2aZ22c7xYb1rUoMqRmSJAcLTtp3iHlJFvYt99jS0gZkA8"

Access_Token = "1339728373854203906-5dbbOR2151OHEvepvBFM3AkhUvxr0L"
Access_Token_Secret = "Biyaq4wqVGsHJ7j6AU50uzMddcPfIlNflG4aSI929KTia"

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
