import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv("ROOT_PASSWORD"),
    database="engagementbot"
)

mycursor = mydb.cursor()
#User Table
mycursor.execute("CREATE TABLE User (current TINYINT, user_id BIGINT, username NVARCHAR(255), creation_date DATETIME, Updated_date DATETIME, since_id BIGINT)")

#User_Settings table
mycursor.execute("CREATE TABLE User_Settings (user_id BIGINT, likes TINYINT, reply TINYINT, retweet TINYINT, verified TINYINT, reply_string VARCHAR(255), upadted_date DATETIME)")

mycursor.execute("CREATE TABLE Run_Logs (since_id_start BIGINT, since_id_end BIGINT, session_id INT, session_time_start DATETIME, session_time_end DATETIME)")

#literally had to make it event_type_id because I didn't wanna define the ENUM now
mycursor.execute("CREATE TABLE User_History(user_id BIGINT, event_time DATETIME, event_string TEXT, event_type_id TINYINT)")

#I have not fully fleshed out this table so I will likely have to add to it in the future!
mycursor.execute("CREATE TABLE Error_Logs(user_id BIGINT, message BLOB)")


#Also will likely add a messages table that will contain all users messages that are sent to me!


#Also some other tables lol cause I am a literal crazy person... Its all in my one file that is not on github





###check if tables were actually created
mycursor.execute("SHOW TABLES")

for tb in mycursor:
    print(tb)
