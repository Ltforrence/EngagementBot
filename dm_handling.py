# tweepy-bots/EngagementBot/dm_handling.py
import tweepy
import logging
import os
from User_Settings import User_Settings
from reply_string_handling import new_string_dm, remove_string_dm



#This is for showing logs of success to the console
logger = logging.getLogger()

#This file is fully for handling dms and stuff!!!
#I really need to write some automated tests lol I am playing with fire



def handle_dms(api, followers, replies):
    #This method will take all dms from the past 30 days read them and respond to them accordingly then delete them from my interface
    #if dm is HELP then it will give it instructions on what it can do. I will handle that first
    DMs = api.list_direct_messages()
    for dm in DMs:
        #if sender is following then proceed and reply accordingly
        #This may be a costly api call in the end so might not be worth it, but we'll see. It will save time and complexity
        temp_user = api.get_user(dm.message_create['sender_id'])
        if temp_user in followers:
            #reply to them
            message = construct_message(dm, api, temp_user, replies)
            send_dm(api, message, temp_user)
        #Then delete the message. I think this only deletes it for the bot. thats what the documentation seemed to indicate, but we will see
        api.destroy_direct_message(dm.id)

def construct_message(dm, api, temp_user, replies):
    #So this message will then interpret the message that was received and send one back
    #for now we will only handle the help command

    message = ""
    recieved_text = dm.message_create['message_data']['text']
    if  recieved_text == "HELP":
        #construct help message reply
        message = "HELP MENU\n\nMany of these functions have their own help pages e.g. HELP REPLY will return a REPLY help message.\n\nFunctions:\n\nREPLY -- Engagement Bot will reply to your tweets with simple message and a one word name of your choice\n\nREPLY STRING -- Engagement Bot will reply to your tweets with custom message you create\n\nSTOP REPLY -- End and delete your current reply settings\n\nMESSAGE -- send message to Luke about issues or possible new functionality \n\nINFO -- Will give you info about bot's current progress \n\nThank you for using Luke's Engagement Bot"
    elif recieved_text[0:4].upper()=="HELP":
        #There should be a space after help so 5 onward
        if recieved_text[5:].upper()=="REPLY":
            #need to set whatever follows this to the new reply string
            #will also have to deal with truncating the message but that is for another day
            message = "REPLY:\nTo turn on reply messages send 'REPLY ____' with what you would like to be called as the blank. The standard reply message is 'Great Tweet _____'"
        elif recieved_text[5:].upper()=="REPLY STRING":
            message = "REPLY STRING: To turn on fully custom reply messages send 'REPLY STRING ______________' with your full message as the blank. Please note you must be an authorized user to use this function."
        elif recieved_text[5:].upper()=="MESSAGE":
            message = "MESSAGE: If you would like to send a message to the creator of this bot about something you want to be added or to tell him he did a great job, use this functionality by sending 'MESSAGE _______' with the blank being your message. Also, you can just message @ItBeLuke just thought this would be cooler to have"
        else:
            message = "I'm sorry I don't understand that command, please reply 'HELP' if you would like more information about my functions"
    elif recieved_text[0:5].upper()=="RT ON":
        #In this case you should turn retweets on for this user
        #I will need to add this to user Settings. Also will need to change the logic of how to do Replys because of this
        message = "You have turned on retweets for this account"
    elif recieved_text[0:6].upper()=="RT OFF":
        #Yeaaaaah so lets just change the user_settings object now...
        message = "You have turned off retweets for this account"
    elif recieved_text[0:10].upper() == "STOP REPLY":
        #turn off replies
        remove_string_dm(temp_user, replies)
        message = "Replies are now turned off for your account"
    elif recieved_text[0:12].upper() == "REPLY STRING":
        #These few lines are a failsafe in case a user doesn't send the correct info
        greeting = recieved_text[13:]
        if greeting == "":
            greeting = "Great tweet " + temp_user.name
        US = User_Settings(temp_user.id, greeting)
        new_string_dm(US, replies)
        message = "Congrats! You have changed your reply message to '" + recieved_text[13:] + "'"
    elif recieved_text[0:5].upper() == "REPLY":
        #These few lines are a failsafe in case a user doesn't send the correct info
        greeting = recieved_text[6:]
        if greeting == "":
            greeting = temp_user.name
        US = User_Settings(temp_user.id, "Great Tweet " + greeting)
        new_string_dm(US, replies)
        message = "Congrats! You have changed your reply message to 'Great Tweet " + recieved_text[6:] + "'"
    elif recieved_text[0:7].upper() == "MESSAGE":
        #okay so I will just have this write to a text file with all the info of this. Maybe it will just write a json object of this message, but for now I will just have it do nothing
        message = "Thank you for your message, \""+recieved_text[8:]+"\" will be sent to the creator of this bot"
        #oh shit I could just have this dm me lol. I will do that it will be way easier than just creating a text file of stuff. I will just do another call to 
        #not sure if this works for get_user, but we'll see
        send_dm(api, temp_user.screen_name+" said: '"+recieved_text[8:] +"' about your application", api.get_user("ItBeLuke"))
    elif recieved_text.upper() == "INFO":
        message = "By the time you read this Replies should be fully implemented and you can take advantage"
    else:
        message = "I'm sorry I don't understand that command, please reply 'HELP' if you would like more information about my functions"
    #put other options here obviously in an else if
    #if there was a message as in if it fit any of the options send the message back to sender. Otherwise do nothing
    return message



def send_dm(api, message, temp_user):
    if message != "":
        logger.info(f"Sending DM to {temp_user.name}")
        api.send_direct_message(temp_user.id, message)