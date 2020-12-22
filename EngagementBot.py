import tweepy
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api, followers):
    logger.info("Retrieving and following followers")
    for follower in followers:
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()

def unfollow_unfollowers(api):
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

def handle_dms(api, followers):
    #This method will take all dms from the past 30 days read them and respond to them accordingly then delete them from my interface
    #if dm is HELP then it will give it instructions on what it can do. I will handle that first
    DMs = api.list_direct_messages()
    for dm in DMs:
        #if sender is following then proceed and reply accordingly
        #This may be a costly api call in the end so might not be worth it, but we'll see. It will save time and complexity
        temp_user = api.get_user(dm.message_create['sender_id'])
        if temp_user in followers:
            #reply to them
            message = construct_message(dm, api, temp_user)
            send_dm(api, message, temp_user)
        #Then delete the message. I think this only deletes it for the bot. thats what the documentation seemed to indicate, but we will see
        api.destroy_direct_message(dm.id)

def construct_message(dm, api, temp_user):
    #So this message will then interpret the message that was received and send one back
    #for now we will only handle the help command

    message = ""
    recieved_text = dm.message_create['message_data']['text']
    if  recieved_text == "HELP":
        #construct help message reply
        message = "HELP MENU\nFunctions:\nREPLY: Engagement Bot will reply to your tweets with simple message and a one word name of your choice\nREPLY STRING: Engagement Bot will reply to your tweets with custom message you create\nREPLY STOP: End and delete your current reply settings\nMESSAGE: send message to Luke about issues or possible new functionality \nThank you for using Luke's Engagement Bot"
    elif recieved_text[0:4]=="HELP":
        #There should be a space after help so 5 onward
        if recieved_text[5:]=="REPLY":
            message = "REPLY:\nTo turn on reply messages send 'REPLY ____' with what you would like to be called as the blank. The standard reply message is 'Great Tweet _____'"
        elif recieved_text[5:]=="REPLY STRING":
            message = "REPLY STRING: To turn on fully custom reply messages send 'REPLY STRING ______________' with your full message as the blank. Please note you must be an authorized user to use this function."
        elif recieved_text[5:]=="MESSAGE":
            message = "MESSAGE: If you would like to send a message to the creator of this bot about something you want to be added or to tell him he did a great job, use this functionality by sending 'MESSAGE _______' with the blank being your message. Also, you can just message @ItBeLuke just thought this would be cooler to have"
        else:
            message = "I'm sorry I don't understand that command, please reply 'HELP' if you would like more information about my functions"
    elif recieved_text[0:7] == "MESSAGE":
        #okay so I will just have this write to a text file with all the info of this. Maybe it will just write a json object of this message, but for now I will just have it do nothing
        message = "Thank you for your message, \""+recieved_text[8:]+"\" will be sent to the creator of this bot"
        #oh shit I could just have this dm me lol. I will do that it will be way easier than just creating a text file of stuff. I will just do another call to 
        #not sure if this works for get_user, but we'll see
        send_dm(api, temp_user.screen_name+" said: '"+recieved_text[8:] +"' about your application", api.get_user("ItBeLuke"))
    elif recieved_text == "INFO":
        message
    else:
        message = "I'm sorry I don't understand that command, please reply 'HELP' if you would like more information about my functions"
    #put other options here obviously in an else if
    #if there was a message as in if it fit any of the options send the message back to sender. Otherwise do nothing
    return message



def send_dm(api, message, temp_user):
    if message != "":
        logger.info(f"Sending DM to {temp_user.name}")
        api.send_direct_message(temp_user.id, message)

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
            unfollow_unfollowers(api)

        like_tweets(api)
        reply_tweets(api)
        handle_dms(api, followers)

        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()