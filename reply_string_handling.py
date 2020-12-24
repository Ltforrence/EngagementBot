# tweepy-bots/EngagementBot/reply_string_handling.py
import tweepy
import logging
import os
import json


logger = logging.getLogger()


#This will be called at the beginning of the program running each time
def get_reply_strings():
    print("Getting Reply strings")



#This will be called every time a new reply string is added or removed
def set_reply_strings(reply_strings):
    print("Setting Reply strings")