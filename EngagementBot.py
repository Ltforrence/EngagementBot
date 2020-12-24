import tweepy
import logging
from config import create_api
from dm_handling import handle_dms
from tweet_handling import handle_tweets
from reply_string_handling import get_reply_strings, set_reply_strings
from follower_handling import handle_followers
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()

    replies = get_reply_strings()
    #initialize this
    check = True
    #This is just a high number to start at that's tweet took place recently for me. You can just make this 1
    since = 1341570120687226879

    reply_strings = get_reply_strings()
    while True:

        followers = handle_followers

        since = handle_tweets(api, since)

        logger.info("Checking DMs")

        handle_dms(api, followers)

        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()