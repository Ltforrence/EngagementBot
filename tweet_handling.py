# tweepy-bots/EngagementBot/tweet_handling.py
import tweepy
import logging
import os

logger = logging.getLogger()


def handle_tweets(api, since, replies):

    #Now changing how timeline functions. Pulling only tweets that are newer than the newest one in the previoous try
    #making the initial count 50 because all the ones after that should be lower than 50 and in case its been off for awhile this will probably grab all tweets bot missed while off.
    #This include_rts does work which is pretty coolio
    timeline = api.home_timeline(since_id = since, count = 50, include_rts = False)

    since = like_tweets(api, since, timeline, replies)

    return since




def like_tweets(api, since, timeline, replies):
    #might have to put a if any tweets then do this for loop
    for tweet in timeline:
        if not tweet.favorited:
            print(f"{tweet.id} : {tweet.user.name} said {tweet.text}")
            api.create_favorite(tweet.id)
            ## check now if name is in tweet replys and get their tag
            tweet_reply_check(api, tweet, replies)
        if tweet.id > since:
            since = tweet.id
    
    return since

#In this method we will check the user to see if that user has replies turned on
def tweet_reply_check(api, tweet, replies):
    for us in replies:
        if tweet.user.id == us.username and us.reply == 1:
            reply_tweet(api, tweet, us)
    #If never returned true, return false
    return False


def reply_tweet(api, tweet, US):

    #print("Would reply to user " + tweet.user.name + " with "+ US.reply_string)
    print("Replying to user: "+ tweet.user.name)

    #This appears to be all you need to do in order to reply to another tweet
    api.update_status("@"+tweet.user.screen_name+" "+US.reply_string, tweet.id)

