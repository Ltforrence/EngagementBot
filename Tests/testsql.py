import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv("ROOT_PASSWORD") 
)

print(mydb)