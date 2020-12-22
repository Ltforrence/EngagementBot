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

def handle_dms(api):
    #This method will take all dms from the past 30 days read them and respond to them accordingly then delete them from my interface
    #if dm is HELP then it will give it instructions on what it can do. I will handle that first
    followers = api.followers()
    DMs = api.list_direct_messages()
    for dm in DMs:
        #if sender is following then proceed and reply accordingly
        #This may be a costly api call in the end so might not be worth it, but we'll see. It will save time and complexity
        temp_user = api.get_user(dm.message_create['sender_id'])
        if temp_user in followers:
            #reply to them
            send_dm(dm, api, temp_user)
        #Then delete the message. I think this only deletes it for the bot. thats what the documentation seemed to indicate, but we will see
        api.destroy_direct_message(dm.id)

def send_dm(dm, api, temp_user):
    #So this message will then interpret the message that was received and send one back
    #for now we will only handle the help command
    message = ""
    if dm.message_create['message_data']['text'] == "HELP":
        #construct help message reply
        message = "Help MENU to be implemented \nThank you for using Luke's Engagement Bot"
    else:
        message = "I'm sorry I don't understand that command, please reply 'HELP' if you would like more information about my functions"
    #put other options here obviously in an else if
    #if there was a message as in if it fit any of the options send the message back to sender. Otherwise do nothing
    if message != "":
        logger.info(f"Sending DM to {temp_user.name}")
        api.send_direct_message(dm.message_create['sender_id'], message)

def reply_tweets(api):
    #here we implement replying to some tweets
    user = api.me() #This is just a filler thing here.
    #I think what I wanna do is return from the previous one tweets I liked this time and then replying to them.



def main():
    api = create_api()
    while True:
        follow_followers(api)
        #okay so unfollow is going to be a somewhat costly method check wise
        #so instead of writing something better, I will just check if followers and following have the same number
        if check_follower_count(api):
            unfollow_unfollowers(api)

        like_tweets(api)
        reply_tweets(api)
        handle_dms(api)

        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()