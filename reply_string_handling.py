# tweepy-bots/EngagementBot/reply_string_handling.py
import tweepy
import logging
import os
import json
from User_Settings import User_Settings


logger = logging.getLogger()


#This will be called at the beginning of the program running each time
#For now this will return an array until I can think of a better data structure to user. More proving concept here
def get_user_settings():
    
    settings_dict = {}
    print("Getting User Settings")
    try:
        with open('user_strings.txt') as json_file:
            data = json.load(json_file)
            for u in data['user_settings']:
                #I know this is already a dictionary when read in and I could use that, but I like having an object
                settings_dict[u['username']] = User_Settings(u['username'], u['reply_string'], u['rt'], u['like'], u['reply'])
                #leaving this commented in for now because I can
                #reply_strings.append(User_Settings(u['username'], u['reply_string'], u['rt'], u['like'], u['reply']))
                #print(reply_dict[u['username']].username)
    except:
        print("File Empty") # okay so there is definitely a better file read in option but since I don't think this will be the final product anyway I just don't care right now
    finally:
        return settings_dict
            



#This will be called every time a new reply string is added or removed
def set_user_settings(settings_dict):
    print("Setting User Settings")
    data = {}
    data['user_settings'] = []
    
    for u in settings_dict.values():
        data['user_settings'].append({
            'username' : u.username,
            'reply_string' : u.reply_string,
            'rt': u.rt,
            'like': u.like,
            'reply': u.reply,
            'verified': u.verified
        })


    with open('user_strings.txt', 'w') as outfile:
        json.dump(data, outfile)



#This method will check if the user already exists in the reply strings. If they do we write all of it again. If a new one then we just do add_reply_string if already exists, do set_reply_strings
def new_string_dm(US, settings_dict):
    #This should be a nice new streamlined version of this method
    if US.username in settings_dict.keys():
        settings_dict[US.username].reply = 1
        settings_dict[US.username].reply_string = US.reply_string
    else:
        settings_dict[US.username] = US
    
    set_user_settings(settings_dict)




def remove_string_dm(temp_user, settings_dict):
    if temp_user.id in settings_dict.keys():
        print("Turning off replies for "+temp_user.name)
        settings_dict[temp_user.id].reply = 0
    else:
        print("User: "+temp_user.name+" did not have reply strings set up ever")
        #probably should like return this, but lol there is still so much to do here
    
    set_user_settings(settings_dict)


def user_like_off(temp_user, settings_dict):
    if temp_user.id in settings_dict.keys():
        if settings_dict[temp_user.id].like == 1:
            settings[temp_user.id].like = 0
            set_user_settings(settings_dict)
            return "Likes have been successfully turned off for your account! \nHave a nice day!"
        else: #likes were already off for this user
            return "Likes were already turned off for your account! If this is not the case please use our MESSAGE feature so EngagementBot can get better"
    else: #if we hit this then the user either does not follow or we have an issue (This issue could be caused by them being grandfathered into our current system (this will be fixed!!!))
        return "You do not have a Settings profile with us. Either there has been an issue or you do not yet follow us. If there is an issue, please contact us with the issue using the MESSAGE function.\nThank you!"


def user_like_on(temp_user, settings_dict):
    #check to see if the user is in the settings_dict 
    if temp_user.id in settings_dict.keys():
        if settings_dict[temp_user.id].like == 0:
            settings[temp_user.id].like = 1
            set_user_settings(settings_dict)
            return "Likes have been successfully turned on for your account! \nHave a nice day!"
        else: #likes were already off for this user
            return "Likes were already turned on for your account! If this is not the case please use our MESSAGE feature so EngagementBot can get better"
    else: #if we hit this then the user either does not follow or we have an issue (This issue could be caused by them being grandfathered into our current system (this will be fixed))
        return "You do not have a Settings profile with us. Either there has been an issue or you do not yet follow us. If there is an issue, please contact us with the issue using the MESSAGE function"



def user_rt_off(temp_user, settings_dict):
    if temp_user.id in settings_dict.keys():
        if settings_dict[temp_user.id].rt == 1:
            settings[temp_user.id].rt = 0
            set_user_settings(settings_dict)
            return "Likes have been successfully turned off for your account! \nHave a nice day!"
        else: #likes were already off for this user
            return "Likes were already turned off for your account! If this is not the case please use our MESSAGE feature so EngagementBot can get better"
    else: #if we hit this then the user either does not follow or we have an issue (This issue could be caused by them being grandfathered into our current system (this will be fixed!!!))
        return "You do not have a Settings profile with us. Either there has been an issue or you do not yet follow us. If there is an issue, please contact us with the issue using the MESSAGE function.\nThank you!"


def user_rt_on(temp_user, settings_dict):
    #check to see if the user is in the settings_dict 
    if temp_user.id in settings_dict.keys():
        if settings_dict[temp_user.id].rt == 0:
            settings[temp_user.id].rt = 1
            set_user_settings(settings_dict)
            return "Retweets have been successfully turned on for your account! \nHave a nice day!"
        else: #likes were already off for this user
            return "Retweets were already turned on for your account! If this is not the case please use our MESSAGE feature so EngagementBot can get better"
    else: #if we hit this then the user either does not follow or we have an issue (This issue could be caused by them being grandfathered into our current system (this will be fixed))
        return "You do not have a Settings profile with us. Either there has been an issue or you do not yet follow us. If there is an issue, please contact us with the issue using the MESSAGE function"