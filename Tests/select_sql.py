import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv("ROOT_PASSWORD"),
    database="testdb"
)


mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM students")

#gets all rows from the last exectued statement
myresult = mycursor.fetchall()

for row in myresult:
    print(row)


#what if you just want a specific column (I know this, but like ya just wanna document it for others)

mycursor.execute("SELECT age FROM students")

#gets all rows from the last exectued statement
myresult = mycursor.fetchall()

for row in myresult:
    print(row)


#again the video I am talking about is mentioning when you just want 1 (I assume you could also use top 1 but this is not bad)
#one interesting thing is that fetchone does not return the tuple of it, just each individually? Not exactly sure, but I guess fetchone returns each of the columns of the one row as its own entity which is useful!

mycursor.execute("SELECT * FROM students")

#gets all rows from the last exectued statement
myresult = mycursor.fetchone()

for row in myresult:
    print(row)