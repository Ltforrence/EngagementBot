# tweepy-bots/EngagementBot/reply_string_handling.py
import tweepy
import logging
import os
import json
from User_Settings import User_Settings
import mysql.connector


logger = logging.getLogger()


#This will be called at the beginning of the program running each time
#For now this will return an array until I can think of a better data structure to user. More proving concept here
def get_user_settings(mydb):
    
    settings_dict = {}
    print("Getting User Settings From DB")
    mycursor = mydb.cursor()

    #located in queries folder as Get_Current_User_Settings
    mycursor.execute("SELECT us.user_id, us.reply_string, us.retweet, us.likes, us.reply, us.verified FROM user u join user_settings us on u.user_id = us.user_id where u.current = 1")


    myresult = mycursor.fetchall()

    for row in myresult:
        settings_dict[row[0]] = User_Settings(row[0], row[1], row[2], row[3], row[4], row[5])


    return settings_dict
            

def add_user_history_event():
    print("Adding user history event")


def add_new_user(temp_user, settings_dict):
    print("Adding new user")
    #Run query to see if user already exists but is not current
        #change current to 1
        #check to make sure they have a user_settings object (They should, but just check in case)
    #else
        #add a new user with temp user stuff
        #add_new_user_settings()

    return settings_dict


def add_new_user_settings():
    print("Adding new user settings")
    #We know that this user settings doesn't exist so just run an insert statement!


def update_user_settings():
    print("Updating user settings")


def update_user_table():
    print("Updating user table")



def update_user(temp_user, settings_dict):
    print("Updating user")
    
    #if user is unfollowing
        #We run an update of the user table
    #if any other change
        #update_user_settings()

    #either way
    #add_user_history_event()

    #Commit it all

    #print message (in the thing you gotta check that it successfully went through!!!! ahhhhhhh

    return settings_dict






#These will be for reading from and writing to the most recent 
def get_since_id(mydb):
    print("Getting since ID from run_logs")
    #get the most recent run_logs row
    #make a new one with the current time as start/end time and the since_id_end as both start/end id and make number one greater than the previous one
    #return that since id


def set_run_logs(since, mydb):
    print("Setting since ID in run_logs")
    #Get the most recent run_logs row 
    #Run an update of it to change since_id_end and the time_end or whatever

    