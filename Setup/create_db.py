import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv("ROOT_PASSWORD") 
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE EngagementBot")


### this is how to check if the db was created successfully 
mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)