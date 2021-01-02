# tweepy-bots/EngagementBot/follower_handling.py
import tweepy
import logging
import time
from reply_string_handling import new_user_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def handle_followers(api, settings):
    followers = api.followers()

    follow_followers(api, followers, settings)
        #okay so unfollow is going to be a somewhat costly method
        #so instead of writing something better, for now I will just check if followers and following have the same number then do it if they do not
    if check_follower_count(api):
        unfollow_unfollowers(api, followers)

    return followers

def follow_followers(api, followers, settings):
    logger.info("Retrieving and following followers")
    for follower in followers:
        new_user_settings(follower, settings)
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()

def unfollow_unfollowers(api, followers):
    logger.info("Retrieving and unfollowing unfollowers")
    for followling in tweepy.Cursor(api.friends).items():   
        #instead of making an api call here I will just crosscheck a list of 
        if not followling in followers:
            logger.info(f"unfollowing {followling.name}")
            api.destroy_friendship(followling.id_str)

#This method will determine if you need to run unfollow unfollowers if the counts are not equal
def check_follower_count(api):
    #I don't know how to just check your own follower number without looking yourself up and getting a user object
    user = api.me()
    #returns true if you should go into unfollowers
    return user.followers_count != user.friends_count