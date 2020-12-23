# tweepy-bots/EngagementBot/tweet_handling.py
import tweepy
import logging
import os




def handle_tweets(api, since):
    since = like_tweets(api, since)

    reply_tweets(api)

    return since




def like_tweets(api, since):
    #Now changing how timeline functions. Pulling only tweets that are newer than the newest one in the previoous try
    #Could do since + 1 here, but it is nice to see the reassurance of the most recent tweet every time, 
    timeline = api.home_timeline(since_id = since)
    #might have to put a if any tweets then do this for loop
    for tweet in timeline:
        if not tweet.favorited:
            print(f"{tweet.id} : {tweet.user.name} said {tweet.text}")
            api.create_favorite(tweet.id)
        if tweet.id > since: 
            since = tweet.id
    
    return since


def reply_tweets(api):
    #here we implement replying to some tweets
    user = api.me() #This is just a filler thing here.
    #I think what I wanna do is return from the previous one tweets I liked this time and then replying to them.
