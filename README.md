# EngagementBot

### Info
This bot is a work in progress. Currently it functions, but the documentation on this site is limited and will be in the end updated so it is easily reproducible for anyone. 
The tests folder doesn't contain real "tests" its mostly just tests to make sure funtions work before I put them in my code. Maybe at some point I'll put in some unit testing or something. 
Eventually setup will tell you how to run everything and this doc will give an overview, but that is still a week or so away. I need to get this thing hosted somewhere soon, but for now it runs on my local so there are a lot of variables at play.


### Current Progress
I am about halfway through setting up database backing. I should finish that today if all goes to plan. Next I will work on scheduling tweets. 
All of my initial feature goals have been implemented and then some. You can see current functionality by dming it @EngagementBot
After it is hosted I will add some more DM functionality and add real tests for any new functionality

I have a bunch of planned features that are a bit insane in that no one would use them, but I now am excited about seeing how much this bot can do

Ideas for new features:
DM feature for user verification (allow users to dm the bot and ask me to be verified, which allows for some of the functionality to be turned on)
Future tweets -- Allow users to schedule a tweet for later in the day. Like the bot will reply to their tweet or retweet their tweet hours after it has been tweeted. This will have to use a new table or possible set up the api to work a certain way.
Have the bot unlike tweets when it unfollows (This will be petty, but kinda funny)
Lots of other small stuff



### Initial Readme info
This is what the initial goals were for the bot.

This is a twitter bot made using the python library Tweepy that will give my account some more engagement as a bit.

I have some private docs on my local machine that I will upload to show my progress and stuff, but heres some general information

All of the keys in test files are outdated. But useful to see because sometimes the name of a key from twitter is different and the format helps for identification.

This is my first twitter bot. I am making it because I am bored and want to explore what is possible with the twitter API and I really want my tweets to get more likes.


The plan:
Have the bot follow back anyone who follows it
Have the bot like all tweets the accounts it follows tweets
If you send it a DM, it will reply to all of your tweets as well with a custom message. "Great tweet _____" with the blank being whatever you dmed it
I would like this to be running constantly (or like at least once a minute)
Also I think with the DM functionality I could code in a few keywords that whenever I DM the bot it will do even more things



You will not be able to use this bot unless you change the keys in the config file
