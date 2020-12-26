# tweepy-bots/EngagementBot/reply_string_handling.py
import tweepy
import logging
import os
import json
from User_Settings import User_Settings


logger = logging.getLogger()


#This will be called at the beginning of the program running each time
#For now this will return an array until I can think of a better data structure to user. More proving concept here
def get_reply_strings():

    
    reply_strings = []
    print("Getting Reply strings")
    try:
        with open('user_strings.txt') as json_file:
            data = json.load(json_file)
            for u in data['user_settings']:
                reply_strings.append(User_Settings(u['username'], u['reply_string']))
    except:
        print("File Empty")
    finally:
        return reply_strings
            



#This will be called every time a new reply string is added or removed
def set_reply_strings(reply_strings):
    print("Setting Reply strings")
    data = {}
    data['user_settings'] = []
    
    for u in reply_strings:
        data['user_settings'].append({
            'username' : u.username,
            'reply_string' : u.reply_string
        })


    with open('user_strings.txt', 'w') as outfile:
        json.dump(data, outfile)



#Will likely not have to use the above method if this one works out(well I will still call it if someone is editing their reply string)
#This could totally just not work too, I may have to read in the file first then write the whole thing back? not sure how json files exactly look? We will see
#This should just append though ideally
def add_reply_string(US):
    print("Adding new Reply String")
    data = {}
    data['user_settings'] = []
    data['user_settings'].append({
            'username' : US.username,
            'reply_string' : US.reply_string
    })

    with open('user_strings.txt', 'a') as outfile:
        json.dump(data, outfile)


#This method will check if the user already exists in the reply strings. If they do we write all of it again. If a new one then we just do add_reply_string if already exists, do set_reply_strings
def new_string_dm(US, reply_strings):
    i = 0
    found = False
    if len(reply_strings) != 0:
        for u in reply_strings:
            #If they have the same username, then set it to the new User_Settings object. I believe this will work, but testing is needed
            if u.username == US.username:
                reply_strings[i] = US
                set_reply_strings(reply_strings)
                found = True
        i = i+1
        if not found:
            reply_strings.append(US)
            add_reply_string(US)
    else:
        reply_strings.append(US)
        add_reply_string(US)

