import tweepy
import logging
from config import create_api
from dm_handling import handle_dms
from tweet_handling import handle_tweets
from reply_string_handling import get_reply_strings, set_reply_strings
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api, followers):
    logger.info("Retrieving and following followers")
    for follower in followers:
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

def main():
    api = create_api()

    replies = get_reply_strings(api)
    #initialize this
    check = True
    #This is just a high number to start at that's tweet took place recently for me. You can just make this 1
    since = 1341570120687226879
    while True:

        followers = api.followers()

        follow_followers(api, followers)

        #okay so unfollow is going to be a somewhat costly method
        #so instead of writing something better, for now I will just check if followers and following have the same number then do it if they do not
        if check_follower_count(api):
            unfollow_unfollowers(api, followers)

        since = handle_tweets(api, since)

        logger.info("Checking DMs")

        handle_dms(api, followers)

        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()