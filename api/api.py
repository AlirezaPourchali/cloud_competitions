import mysql.connector

import uvicorn
from mysql.connector import errorcode
from fastapi import FastAPI , File, UploadFile
import uvicorn  
from pydantic import BaseModel
mydb = mysql.connector.connect(host="localhost",port="3306" ,  user="root",  password="admin")
cursor = mydb.cursor()

class Item(BaseModel):
    name: str
    description: str 
    price: float
    tax: float 


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
#@app.post("/users")


#print(cursor.execute("create database ali"))
#print(cursor.execute("show databases"))
#cursor
#for x in cursor:
#  print(x)
TABLES = {}
TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")


DB_NAME = "hellodb"
def create_database(cursor , name):
    try:
        cursor.execute(
            f"CREATE DATABASE {name} ")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        mydb.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")



cursor.close()
mydb.close()


if __name__ =="__main__":
    uvicorn.run('api:app' , host='0.0.0.0' , port=8000 , reload=True )