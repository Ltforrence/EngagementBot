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

def like_tweets(api, since):
    #Now changing how timeline functions. Pulling only tweets that are newer than the newest one in the previoous try
    #Could do since + 1 here, but it is nice to see the reassurance of the most recent tweet every time, 
    timeline = api.home_timeline(since_id = since)
    print(f"since: {since}")

    #might have to put a if any tweets then do this for loop
    for tweet in timeline:
        print(f"{tweet.id} : {tweet.user.name} said {tweet.text}")
        if not tweet.favorited:
            print("Liking Above tweet")
            api.create_favorite(tweet.id)
        if tweet.id > since: 
            since = tweet.id
    
    return since


def reply_tweets(api):
    #here we implement replying to some tweets
    user = api.me() #This is just a filler thing here.
    #I think what I wanna do is return from the previous one tweets I liked this time and then replying to them.



def main():
    api = create_api()
    #initialize this
    check = True
    #This is just a high number to start at that's tweet took place recently for me. You can just make this 1
    since = 1341570120687226879
    while True:
        #only check for list of followers every minute so we can update more often, but check everything else every 30 seconds
        if check:
            #only do all this code every other time
            followers = api.followers()
            follow_followers(api, followers)

            #okay so unfollow is going to be a somewhat costly method
            #so instead of writing something better, for now I will just check if followers and following have the same number then do it if they do not
            if check_follower_count(api):
                unfollow_unfollowers(api, followers)

            #So I am also putting this in here so we can do dms every 30 seconds
            since = like_tweets(api, since)
            reply_tweets(api)

            check = False
        else:
            logger.info("Checking DMs")
            check = True




        handle_dms(api, followers)

        logger.info("Waiting...")
        time.sleep(30)

if __name__ == "__main__":
    main()