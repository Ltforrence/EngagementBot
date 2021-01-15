FROM python:3.7-alpine

COPY . .
RUN pip3 install tweepy
RUN pip3 install mysql-connector

CMD ["python3", "EngagementBot.py"]