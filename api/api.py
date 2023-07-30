import mysql.connector

mydb = mysql.connector.connect(host="localhost",port="3306" ,  user="root",  password="admin")

cursor = mydb.cursor()

#print(cursor.execute("create database ali"))
print(cursor.execute("show databases"))
for x in cursor:
  print(x)