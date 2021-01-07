# tweepy-bots/EngagementBot/dm_handling.py
import tweepy
import logging
import os
from User_Settings import User_Settings
from reply_string_handling import new_user_reply, user_reply_off, set_user_settings, user_like_off, user_like_on, user_rt_off, user_rt_on
from user_data_handling import add_new_user, update_user

#This file is the worst.
#For this I am truly sorry
#It is my greatest sin

#This is for showing logs of success to the console
logger = logging.getLogger()

#This file is fully for handling dms and stuff!!!
#I really need to write some automated tests lol I am playing with fire



def handle_dms(api, followers, settings, mydb):
    #This method will take all dms from the past 30 days read them and respond to them accordingly then delete them from my interface
    #if dm is HELP then it will give it instructions on what it can do. I will handle that first
    DMs = api.list_direct_messages()
    for dm in DMs:
        #if sender is following then proceed and reply accordingly
        #This may be a costly api call in the end so might not be worth it, but we'll see. It will save time and complexity
        temp_user = api.get_user(dm.message_create['sender_id'])
        if temp_user in followers:
            #reply to them
            message = construct_message(dm, api, temp_user, settings, mydb)
            send_dm(api, message, temp_user)
        #Then delete the message. I think this only deletes it for the bot. thats what the documentation seemed to indicate, but we will see
        api.destroy_direct_message(dm.id)



def construct_message(dm, api, temp_user, settings, mydb):
    #So this message will then interpret the message that was received and send one back
    #for now we will only handle the help command

    message = ""
    recieved_text = dm.message_create['message_data']['text']
    if  recieved_text.upper() == "HELP":
        #construct help message reply
        message = "HELP MENU\n\nMany of these functions have their own help pages e.g. HELP REPLY will return a REPLY help message.\n\nFunctions:\n\nREPLY ON-- Engagement Bot will reply to your tweets with simple message and your current screen name!\n\nREPLY STRING -- Engagement Bot will reply to your tweets with custom message you create\n\REPLY OFF -- End and delete your current reply settings\nLIKE ON/OFF -- Will turn on or off the feature that EngagementBot likes all of your tweets\nRT ON/OFF -- Will turn on or off the feature that has EngagementBot retweet all your tweets\n\nMESSAGE -- send message to Luke about issues or possible new functionality \n\nINFO -- Will give you info about bot's current progress \n\nThank you for using Luke's Engagement Bot"


    elif recieved_text[0:4].upper()=="HELP":
        #There should be a space after help so 5 onward
        if recieved_text[5:].upper()=="REPLY":
            #need to set whatever follows this to the new reply string
            #will also have to deal with truncating the message but that is for another day
            message = "REPLY:\nTo turn on reply messages send 'REPLY ON' the reply that will be tweeted to all of your tweets is 'Great Tweet <name>'\n\nTo turn reply tweets off, send REPLY OFF."
        elif recieved_text[5:].upper()=="REPLY STRING":
            message = "REPLY STRING: To turn on fully custom reply messages send 'REPLY STRING ______________' with your full message as the blank. Please note you must be an authorized user to use this function."
        elif recieved_text[5:].upper()=="MESSAGE":
            message = "MESSAGE: If you would like to send a message to the creator of this bot about something you want to be added or to tell him he did a great job, use this functionality by sending 'MESSAGE _______' with the blank being your message. Also, you can just message @ItBeLuke just thought this would be cooler to have"
        else:
            message = "I'm sorry I don't understand that command, please reply 'HELP' if you would like more information about my functions"


    elif recieved_text[0:7].upper()=="LIKE ON":
        #yay we did it this looks okay!
        message = user_like_on(temp_user, settings)


    elif recieved_text[0:8].upper()=="LIKE OFF":
        #Yeaaaaah so lets just change the user_settings object now...
        message = user_like_off(temp_user, settings)


    elif recieved_text.upper() == "REPLY ON":
        #This is now changed to be just a standard reply because for the long run we don't want unverified users to be able to put whatever name in here
        greeting = "Great Tweet " + temp_user.name
        new_user_reply(temp_user, greeting, settings)
        message = "Congrats! You have changed your reply message to '" + greeting + "'"


    elif recieved_text[0:10].upper() == "REPLY OFF":
        #turn off replies
        message = user_reply_off(temp_user, settings)


    elif recieved_text[0:10].upper() == "RT ON":
        #turn on retweets
        message = user_rt_on(temp_user, settings)


    elif recieved_text[0:6].upper()=="RT OFF":
        #turn off retweets
        message = user_rt_off(temp_user, settings)


    elif recieved_text[0:12].upper() == "REPLY STRING":
        #These few lines are a failsafe in case a user doesn't send the correct info
        greeting = recieved_text[13:]
        if greeting == "":
            greeting = "Great tweet " + temp_user.name
        new_user_reply(temp_user, greeting, settings)
        message = "Congrats! You have changed your reply message to '" + recieved_text[13:] + "'"


    elif recieved_text[0:7].upper() == "MESSAGE":
        #okay so I will just have this write to a text file with all the info of this. Maybe it will just write a json object of this message, but for now I will just have it do nothing
        message = "Thank you for your message, \""+recieved_text[8:]+"\" will be sent to the creator of this bot"
        #oh shit I could just have this dm me lol. I will do that it will be way easier than just creating a text file of stuff. I will just do another call to 
        #not sure if this works for get_user, but we'll see
        send_dm(api, temp_user.screen_name+" said: '"+recieved_text[8:] +"' about your application", api.get_user("ItBeLuke"))


    elif recieved_text.upper() == "INFO":
        message = "Replies are fully implemented. Trying to make a user_settings object for everyone. Likes/Retweets ON/OFF are also implemented, but will not work until you have at some point turned on Replies lol\nI know this is silly, but soon that will be fixed. That is my next project"


    else:
        message = "I'm sorry I don't understand that command, please reply 'HELP' if you would like more information about my functions"

        
    #put other options here obviously in an else if
    #if there was a message as in if it fit any of the options send the message back to sender. Otherwise do nothing
    return message



def send_dm(api, message, temp_user):
    if message != "":
        logger.info(f"Sending DM to {temp_user.name}")
        api.send_direct_message(temp_user.id, message)