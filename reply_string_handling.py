# tweepy-bots/EngagementBot/reply_string_handling.py
import tweepy
import logging
import os



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#This will be called at the beginning of the program running each time
def get_reply_strings(api):
    print("Getting Reply strings")



#This will be called every time a new reply string is added or removed
def set_reply_strings(reply_strings, api):
    print("Setting Reply strings")