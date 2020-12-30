import tweepy
import logging
from config import create_api
from dm_handling import handle_dms
from tweet_handling import handle_tweets
from reply_string_handling import get_user_settings
from follower_handling import handle_followers
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()

    settings = get_user_settings()

    #This is just a high number to start at that's tweet took place recently for me. You can just make this 1 in reality unless you are trying to pull 300 tweets first try
    since = 1341570120687226879
    while True:
        logger.info("Checking Followers")
        followers = handle_followers(api, settings)
        logger.info("Checking Tweets")
        since = handle_tweets(api, since, settings)
        logger.info("Checking DMs")
        handle_dms(api, followers, settings)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()