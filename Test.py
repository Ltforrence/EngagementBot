import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("OAmoZ5CiNjB6hSPtDxVlq5TZW", 
    "horuA2aZ22c7xYb1rUoMqRmSJAcLTtp3iHlJFvYt99jS0gZkA8")
auth.set_access_token("1339728373854203906-5dbbOR2151OHEvepvBFM3AkhUvxr0L", 
    "Biyaq4wqVGsHJ7j6AU50uzMddcPfIlNflG4aSI929KTia")

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK") #Well this worked so thats coolio
except:
    print("Error during authentication")

