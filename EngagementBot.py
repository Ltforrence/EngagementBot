import tweepy
import logging
from config import create_api, connect_db, get_db_cursor
from dm_handling import handle_dms
from tweet_handling import handle_tweets
from reply_string_handling import get_user_settings, get_since_id, set_since_id
from follower_handling import handle_followers
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()

    ##The new code order coming in right here baby
    mydb = connect_db()

    settings = get_user_settings()

    #Now because we have to lol, we are gonna get and set this every time it changes in a file
    since = get_since_id()
    while True:
        logger.info("Checking Followers")
        followers = handle_followers(api, settings, mydb)
        logger.info("Checking Tweets")
        since = handle_tweets(api, since, settings, mydb)
        logger.info("Checking DMs")
        handle_dms(api, followers, settings, mydb)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()