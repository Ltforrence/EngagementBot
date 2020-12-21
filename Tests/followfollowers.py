import tweepy
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()

def unfollow_unfollowers(api):
    logger.info("Retrieving and unfollowing unfollowers")
    followers = api.followers()
    for followling in tweepy.Cursor(api.friends).items():
        #instead of making an api call here I will just crosscheck a list of 
        if not followling in followers:
            logger.info(f"unfollowing {followling.name}")
            api.destroy_friendship(followling.id_str)

#This method will determine if you need to run unfollow unfollowers if the counts are not equal
def check_follower_count(api):
    #I don't know how to just check your own follower number without looking yourself up and getting a user object
    user = api.get_user('EngagementBot')
    #returns true if you should go into unfollowers
    return user.followers_count != user.friends_count


def main():
    api = create_api()
    while True:
        follow_followers(api)
        #okay so unfollow is going to be a somewhat costly method check wise
        #so instead of writing something better, I will just check if followers and following have the same number
        if check_follower_count(api):
            unfollow_unfollowers(api)
        logger.info("Waiting...")
        time.sleep(20)

if __name__ == "__main__":
    main()