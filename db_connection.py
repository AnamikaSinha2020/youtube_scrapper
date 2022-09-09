import mysql.connector

mydb = mysql.connector.connect(
  host="database-1.clejtyeseawc.us-east-1.rds.amazonaws.com",
  user="admin",
  password="Pass1234"
)


cursor = mydb.cursor()
