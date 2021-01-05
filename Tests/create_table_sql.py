import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv("ROOT_PASSWORD"),
    database="testdb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE students (name VARCHAR(255), age INTEGER(10))")



###check if tables were actually created
#mycursor.execute("SHOW TABLES")
#
#for tb in mycursor:
#    print(tb)




