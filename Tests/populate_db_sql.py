import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv("ROOT_PASSWORD"),
    database="testdb"
)


mycursor = mydb.cursor()


#creating the sql formula. Can run this with any data
sqlFormula = "INSERT INTO students (name, age) VALUES (%s, %s)"

#So we can create this student then just execute the formula with this student
students = [("Tommy", 25),
("bill", 25),
("ori", 25),
("andrea", 25),
("lorenzo", 25),
("billy bean", 25),]


mycursor.executemany(sqlFormula, students)

# For a single row use this
#mycursor.execute(sqlFormula, students)

mydb.commit() #no changes are made until this is called (Of course but like just gotta note it just in case we forget)