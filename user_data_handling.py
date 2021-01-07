# tweepy-bots/EngagementBot/reply_string_handling.py
import tweepy
import logging
import os
import json
from User_Settings import User_Settings
import mysql.connector
import datetime


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


def add_new_user(temp_user, settings_dict, mydb):
    print("Adding new user")
    #Run query to see if user already exists but is not current
        #update_user_table()
            #this changes current to 1
        #check to make sure they have a user_settings object (They should, but just check in case)
    #else
        #add a new user with temp user stuff
        #add_new_user_settings()

    return settings_dict


def add_new_user_settings():
    print("Adding new user settings")
    #We know that this user settings doesn't exist so just run an insert statement!


def update_user_settings(screen_name, user_settings, settings_dict, mydb):
    print("Updating user settings")
    message = ""


    return message


def update_user_table():
    print("Updating user table")
    #Change current to 1 for this user


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
def get_last_runlog(mydb):
    print("Getting since ID from run_logs")
    #get the most recent run_logs row
    #make a new one with the current time as start/end time and the since_id_end as both start/end id and make number one greater than the previous one
    #return that since id
    mycursor = mydb.cursor(buffered = True) #have to do this because you get an error basically that you are requesting the same info again sometimes (I think I am actually wrong here. Results are lazilly loaded tho and mysql is complaining). I can't not request it unless I keep track of my last request which I don't wanna do at the moment. Maybe in the future
    mycursor.execute("SELECT since_id_end, session_id from run_logs ORDER BY session_id desc")

    #Just doing fetchone should get me the top one and should put em different
    myresult = mycursor.fetchone()

    #This should be the order they come to me in and since I only got one it should work
    since_id = myresult[0]
    session_id = myresult[1]

    #### now we create a new run_log entry
    run_log = [since_id, since_id, session_id+1, datetime.datetime.now(), datetime.datetime.now()]

    sqlFormula = "INSERT INTO run_logs (since_id_start, since_id_end, session_id, session_time_start, session_time_end) VALUES (%s, %s, %s, %s, %s)"


    mycursor.execute(sqlFormula, run_log)


    mydb.commit()

    return since_id



#Ultimately I am considering having this set once per minute even if the since_id has not changed, just so I can actually monitor bot downtime myself. I do really like to know that stuff. (if I do this I will just put since second and have it set to 0 when no value is passed in so I can just do that. Or tbh just keep passing in the same value it don't matter if since_id is updated without changing it)
def set_run_logs(since, mydb):
    print("Setting since ID in run_logs")
    #Get the most recent run_logs row 
    #Run an update of it to change since_id_end and the time_end or whatever

    mycursor = mydb.cursor(buffered = True)


    #I definitely do not need to run two executes here, but I will fix that when I am not tired!
    mycursor.execute("SELECT session_id from run_logs ORDER BY session_id desc")
    myresult = mycursor.fetchone() #has to be a single number
    session_id = myresult[0] #doing this because it yelled at me for not "reading" the result

    sqlformula = ("UPDATE run_logs SET since_id_end = %s, session_time_end = %s WHERE session_id = %s")

    data = [since, datetime.datetime.now(), session_id]

    mycursor.execute(sqlformula, data)

    mydb.commit()



    