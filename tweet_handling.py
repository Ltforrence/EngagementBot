# tweepy-bots/EngagementBot/tweet_handling.py
import tweepy
import logging
import os
from user_data_handling import set_run_logs

logger = logging.getLogger()


def handle_tweets(api, since, settings, mydb):

    #So since is read from the db from the end of the last session. Grabs all tweets newer than it. I assume the bot will never be off long enough for 50 tweets to happen, but eventually may have to bump this up in case
    timeline = api.home_timeline(since_id = since, count = 50, include_rts = False)

    since = like_tweets(api, since, timeline, settings, mydb)

    #have to return since so it is perpetuated to the next cycle
    return since




def like_tweets(api, since, timeline, settings, mydb):
    #timline is full of tweepy status objects
    for tweet in timeline:
        if not tweet.favorited:
            #Now we are checking to see if tweets should be liked based on the user's settings
            if tweet.user.id in settings.keys():
                if settings[tweet.user.id].like == 1:
                    print(f"{tweet.id} : {tweet.user.name} said {tweet.text}")
                    api.create_favorite(tweet.id)
                    ###Consider putting a user_history object here too just for fun (This would allow us to unlike all their tweets after they unfollow and other stuff for sure)
                tweet_reply_check(api, tweet, settings) # This only needs to go up here because if they don't exist in settings then they won't have replies turned on. The if user is in settings and its else will be removed from the final method here
            else:  #for now we need to have both of these because I don't have a settings set up for all of my users unfortunately... This will be fixed
                print(f"{tweet.id} : {tweet.user.name} said {tweet.text}")
                api.create_favorite(tweet.id)
            ## check now if name is in tweet replys and get their tag
        if tweet.id > since:
            since = tweet.id
            #set the since into the db
            set_run_logs(since, mydb)
    
    return since

#In this method we will check the user to see if that user has replies turned on
def tweet_reply_check(api, tweet, settings):
    #Now will do a check at the beginning of this to see if it starts with an @ and if it does, do not reply!
    if tweet.text[0:1] != "@":
        if tweet.user.id in settings.keys():
            if settings[tweet.user.id].reply == 1:
                try:
                    reply_tweet(api, tweet, settings[tweet.user.id])
                except tweepy.error.TweepError as e:
                    print(e) 
                    #Send to error logs here! There is nothing I know of that should actually fail here though
                except:
                    print("not sure what went wrong")
                    #also error logs here
    else:
        print("Not replying because tweet was a reply!")


def reply_tweet(api, tweet, US):
    print("Replying to user: "+ tweet.user.name)
    #This appears to be all you need to do in order to reply to another tweet
    api.update_status("@"+tweet.user.screen_name+" "+US.reply_string, tweet.id)

