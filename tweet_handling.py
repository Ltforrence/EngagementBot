# tweepy-bots/EngagementBot/tweet_handling.py
import tweepy
import logging
import os

logger = logging.getLogger()


def handle_tweets(api, since):

    #Now changing how timeline functions. Pulling only tweets that are newer than the newest one in the previoous try
    #making the initial count 50 because all the ones after that should be lower than 50 and in case its been off for awhile this will probably grab all tweets bot missed while off.
    #This include_rts does work which is pretty coolio
    timeline = api.home_timeline(since_id = since, count = 50, include_rts = False)

    since = like_tweets(api, since, timeline)

    reply_tweets(api, timeline)

    return since




def like_tweets(api, since, timeline):
    #might have to put a if any tweets then do this for loop
    for tweet in timeline:
        if not tweet.favorited:
            print(f"{tweet.id} : {tweet.user.name} said {tweet.text}")
            api.create_favorite(tweet.id)
            ## check now if name is in tweet replys and get their tag
            
        if tweet.id > since:
            since = tweet.id
    
    return since


def reply_tweets(api, timeline):
    #here we implement replying to some tweets
    user = api.me() #This is just a filler thing here.
    #I think what I wanna do is return from the previous one tweets I liked this time and then replying to them.

