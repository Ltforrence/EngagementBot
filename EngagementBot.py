import tweepy
import logging
from config import create_api
from dm_handling import handle_dms
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

def like_tweets(api):
    #here we implement liking users tweets that follow us
    #What I have here right now is a pretty crude way of liking tweets. I just pulls the timeline and likes all tweets in it
    for tweet in tweepy.Cursor(api.home_timeline).items(20): #sooooo not exactly sure why more than 20 is the highest I can go right now because it should be 60
        if not tweet.favorited:
            api.create_favorite(tweet.id)
            print(f"{tweet.user.name} said {tweet.text}")


def reply_tweets(api):
    #here we implement replying to some tweets
    user = api.me() #This is just a filler thing here.
    #I think what I wanna do is return from the previous one tweets I liked this time and then replying to them.



def main():
    api = create_api()
    while True:
        followers = api.followers()
        follow_followers(api, followers)
        #okay so unfollow is going to be a somewhat costly method check wise
        #so instead of writing something better, I will just check if followers and following have the same number
        if check_follower_count(api):
            unfollow_unfollowers(api, followers)

        like_tweets(api)
        reply_tweets(api)
        handle_dms(api, followers)

        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()