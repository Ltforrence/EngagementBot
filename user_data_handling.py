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
    mycursor = mydb.cursor(buffered = True)
    #located in queries folder as Get_Current_User_Settings
    mycursor.execute("SELECT us.user_id, us.reply_string, us.retweet, us.likes, us.reply, us.verified FROM user u join user_settings us on u.user_id = us.user_id where u.current = 1")


    myresult = mycursor.fetchall()

    for row in myresult:
        settings_dict[row[0]] = User_Settings(row[0], row[1], row[2], row[3], row[4], row[5])


    return settings_dict
            

def add_user_history_event(mydb, temp_user, event, message):
    print("Adding user history event")
    mycursor = mydb.cursor(buffered = True)

    mycursor.execute("INSERT INTO user_history (user_id, event_time, event_string, event_type_id) VALUES(%s, %s, %s, %s)", [temp_user.id, datetime.datetime.now(), message, event])

    mydb.commit()


def add_new_user(mydb, temp_user, settings_dict):
    print("Adding new user")
    mycursor = mydb.cursor(buffered = True)

    mycursor.execute("SELECT * from user WHERE user_id = "+str(temp_user.id))

    #If the above returns anything then they exist
    if mycursor.rowcount == 1:
        #update user now since they already exist. Make current = 1
        settings_dict = update_user(mydb, temp_user, settings_dict, 1)
    else:
        #add new user
        mycursor.execute("INSERT INTO user (current, user_id, username, creation_date, Updated_date, since_id) VALUES(%s, %s, %s, %s, %s, %s)", [1, temp_user.id, temp_user.screen_name, datetime.datetime.now(), datetime.datetime.now(), 1346946600510386176])

        #add new user_settings 
        #add_new_user_settings(mydb, temp_user)
        mycursor.execute("INSERT INTO user_settings (user_id, likes, reply, retweet, verified, reply_string, updated_date) values(%s, %s, %s, %s, %s, %s, %s)", [temp_user.id, 1, 0, 0, 1, "", datetime.datetime.now()])


        add_user_history_event(mydb, temp_user, 1, "Following for the first time. Called from add_new_user")

        #commit both of them
        mydb.commit()

        #now get all user setttings
        settings_dict = get_user_settings(mydb)

    return settings_dict



#might end up using this but for now will just run this statement in add_new_user
def add_new_user_settings(mydb, temp_user):
    print("Adding new user settings")
    #We know that this user settings doesn't exist so just run an insert statement!

    mycursor = mydb.cursor(buffered = True)

    mycursor.execute()



def update_user_settings(mydb, us, temp_user, event):
    print("Updating user settings")


    mycursor = mydb.cursor(buffered = True)

    mycursor.execute("Update user_settings SET likes = %s, reply = %s, retweet=%s, verified = %s, reply_string = %s, updated_date = %s WHERE user_id = %s", [us.like, us.reply, us.rt, us.verified, us.reply_string, datetime.datetime.now(), us.username])


    message = "User "
    if event == 5:
        message = message + "turned on likes"
    elif event == 6:
        message = message + "turned off likes"
    elif event == 7:
        message = message + "turned on retweets"
    elif event == 8:
        message = message + "turned off retweets"
    elif event == 9:
        message = message + "turned on replies"
    elif event == 10:
        message = message + "turned off replies"
    elif event == 4:
        message = message + "changed reply string"

    add_user_history_event(mydb, temp_user, event, message)
    



    message = message + " from update_user_settings"
    
    mydb.commit()



def update_user(mydb, temp_user, settings_dict, event = 2):
    print("Updating user")
    
    #This will only be called if user is following or unfollowing

    #Technically it will also be called if a user changes their @name (I think will have to check logic) so eventually we will have to do that too. That will be event 3

    #Curr is what will be set to current in the db
    curr = 0
    message = "Unfollowing user from inside of update_user method. Really need to update this message later!"
    if event == 1:
        curr = 1 # if event = 1 that mean they are following and were already in the database
        message = "Following user from inside of update_user method."



    mycursor = mydb.cursor(buffered = True)

    mycursor.execute("UPDATE user SET current = %s, Updated_date = %s WHERE user_id = %s", [curr, datetime.datetime.now(), temp_user.id])

    #Commit it
    mydb.commit()



    #add_user_history_event() for following or unfollowing or name change if that does in fact come here??? who knows
    add_user_history_event(mydb, temp_user, event, message)

    #oh lol then you need to reget the settings dict because that user may have followed you before
    settings_dict = get_user_settings(mydb)
    return settings_dict






#These will be for reading from and writing to the most recent 
def get_last_runlog(mydb):
    #print("Getting since ID from run_logs")
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
    #print("Setting since ID in run_logs")
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



    