from sqlalchemy import create_engine, inspect ,text , exc

import uvicorn
from fastapi import FastAPI , File, UploadFile
import uvicorn  
from pydantic import BaseModel

username = "root"
password = "admin"
hostname = "localhost:3306"  # or your MySQL server address
database_name = "my_database"

#db_url = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{database_name}"
db_url = "mysql+mysqlconnector://root:admin123@localhost:3306/my_database"
engine = create_engine(db_url)
mysql = engine.connect()
try:
    mysql.execute(text("create table hello ( username varchar(255) , email varchar(255) , avatar varchar(255) )"))
except Exception as e:
        print ("already exists")

## SEE TABLES AND DBS WITH INSPECTOR

#inspector = inspect(mysql)
#print(inspector.get_schema_names())
#print(inspector.get_table_names())

## EXECUTE COMMANDS DIRECTLY 

#for i in (mysql.execute(text("show databases"))):
#    print (i)
    
class User(BaseModel):
    username: str
    email: str 
    avatar: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users")
async def add_user(user: User):
    mysql = engine.connect()
    username = user.username
    email = user.email
    avatar = user.avatar
    query = text("insert into hello (username , email , avatar) values (:username , :email , :avatar)")
    param = {"username": username, "email": email, "avatar": avatar}
    result = mysql.execute(query , param)
    mysql.close()
    print(result)
    return 200
#@app.post("/users")


#print(cursor.execute("create database ali"))
#print(cursor.execute("show databases"))
#cursor
#for x in cursor:
#  print(x)

if __name__ =="__main__":
    uvicorn.run('api-sqlalchemy:app' , host='0.0.0.0' , port=8000 , reload=True )