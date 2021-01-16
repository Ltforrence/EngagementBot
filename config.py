# tweepy-bots/EngagementBot/config.py
import tweepy
import logging
import os
import mysql.connector


#This is for showing logs of success to the console
logger = logging.getLogger()


def create_api():
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""



    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api




def connect_db():
    mydb = mysql.connector.connect(
        host="engagementbot2.ccs9ykexia3h.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd= "",
        database="engagementbot"
    )
    return mydb


#Putthing these in two different methods because I have to??? Not really sure if I need to even have this in config. Could get away with putting it elsewhere
#I don't think I really will need this method, but will leave it for now
def get_db_cursor(mydb):
    mycursor = mydb.cursor()

    return mycursor
    
