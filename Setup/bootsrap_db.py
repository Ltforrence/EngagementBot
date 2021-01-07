import mysql.connector
import os
import datetime
from config import create_api
from reply_string_handling import get_user_settings


#This was for my personal bootstrapping because of how I used to set everything up!

#api = create_api()
#
#us = get_user_settings()
#
#User_Settings = []
#
#Users = []
#
#
#for key in us.keys():
#    if key != 1129823604 and key != 718475920194068480:
#        User_Settings.append([us[key].username, us[key].like, us[key].reply, us[key].rt, us[key].verified, us[key].reply_string, datetime.datetime.now()])
#        #Do the get here
#        user = api.get_user(us[key].username)
#        print(user.screen_name)
#        Users.append([1, us[key].username, user.screen_name, datetime.datetime.now(), datetime.datetime.now(), 1346946600510386176])


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv("ROOT_PASSWORD"),
    database="engagementbot"
)
##
##
## DISCLAIMER: This file will likely not make that much sense for you to use! There is no real data to bootstrap for you since test accounts would have real corresponding ids on twitter and could cause issues for you. I initially thought users would need this to duplicate my application but they don't need it. I just need it because my system was set up weird to start
##
## I am only not putting in everything to test what this data looks like for me.

mycursor = mydb.cursor()

#current TINYINT, user_id BIGINT, username NVARCHAR(255), creation_date DATETIME, Updated_date DATETIME, since_id BIGINT
sqlFormula = "INSERT INTO User (current, user_id, username, creation_date, updated_date, since_id) VALUES (%s, %s, %s, %s, %s, %s)"
#Users = [[1, 1129823604, "ItBeLuke", datetime.datetime.now(), datetime.datetime.now(), 1346488989675610115], [1, 718475920194068480, "Geese_Boy", datetime.datetime.now(), datetime.datetime.now(), 1346488989675610115] ]

mycursor.executemany(sqlFormula, Users)

#some test data for everyone

#user_id BIGINT, likes TINYINT, reply TINYINT, retweet TINYINT, verified TINYINT, reply_string VARCHAR(255), upadted_date DATETIME)"
sqlFormula = "INSERT INTO User_Settings (user_id, likes, reply, retweet, verified, reply_string, updated_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#User_Settings = [[718475920194068480, 1, 1, 0, 1, "Great Tweet The Algorithm", datetime.datetime.now()], [1129823604, 1, 1, 0, 1, "Great Tweet The Algorithm", datetime.datetime.now()]]

mycursor.executemany(sqlFormula, User_Settings)

mydb.commit()

#Again some test data for everyone

#since_id_start BIGINT, since_id_end BIGINT, session_id INT, session_time_start DATETIME, session_time_end DATETIME
sqlFormula = "INSERT INTO Run_Logs (name, age) VALUES (%s, %s, %s, %s, %s)"


#Again some test data for everyone

#user_id BIGINT, event_time DATETIME, event_string TEXT, event_type_id TINYINT
sqlFormula = "INSERT INTO User_History (name, age) VALUES (%s, %s, %s, %s)"


#Again some test data for everyone

#user_id BIGINT, message BLOB
sqlFormula = "INSERT INTO Error_Logs (name, age) VALUES (%s, %s)"


#Again some test data for everyone











#This is what I had to do because I had everything stored in json and had to send it into the system
#If this second one is not commented out for you it should be! Sorry about that





