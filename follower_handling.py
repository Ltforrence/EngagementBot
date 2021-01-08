# tweepy-bots/EngagementBot/follower_handling.py
import tweepy
import logging
import time
from user_data_handling import update_user, add_new_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


#This is what is called from main
def handle_followers(api, settings, mydb):
    followers = api.followers()

    follow_followers(api, followers, settings, mydb)
    #Checking to see if someone unfollowed is a costly method, so to not have to run it a lot, first we check to see if follower+count != follow_count 
    if check_follower_count(api):
        unfollow_unfollowers(api, followers, settings, mydb)

    return followers

def follow_followers(api, followers, settings, mydb):
    logger.info("Retrieving and following followers")
    for follower in followers:
        if not follower.following:
            #settings = new_user_settings(follower, settings) #if following for the first time create a user_settings object for them
            settings = add_new_user(mydb, follower, settings) #not sure if I need settings but we will see as we continue to implement here
            logger.info(f"Following {follower.name}")
            follower.follow()

def unfollow_unfollowers(api, followers, settings, mydb):
    logger.info("Retrieving and unfollowing unfollowers")
    for followling in tweepy.Cursor(api.friends).items():   
        #instead of making an api call here I will just crosscheck a list of 
        if not followling in followers:
            #We don't delete past users, just change them to not current
            settings = update_user(mydb, followling, settings)
            logger.info(f"unfollowing {followling.name}")
            #This is the actual unfollow method in tweepy
            api.destroy_friendship(followling.id_str)


#This method will determine if you need to run unfollow unfollowers if the counts are not equal
def check_follower_count(api):
    #I don't know how to just check your own follower number without looking yourself up and getting a user object
    user = api.me()
    #returns true if you should go into unfollowers
    return user.followers_count != user.friends_count