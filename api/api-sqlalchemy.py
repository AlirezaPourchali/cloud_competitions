from sqlalchemy import create_engine,text 
import wget , os
import uvicorn
from fastapi import FastAPI 
from fastapi.responses import FileResponse
import uvicorn  
from pydantic import BaseModel

#from sqlalchemy.orm import sessionmaker
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


username = os.environ["API_MYSQL_USERNAME"]
password = os.environ["API_MYSQL_PASSWORD"]
hostname = os.environ["API_MYSQL_URL"]  # or your MySQL server address
port = os.environ["API_MYSQL_PORT"]
database_name = os.environ["API_MYSQL_DB"]
storage = os.environ["API_MYSQL_FILESYSTEM"]
table = os.environ["API_MYSQL_TABLE"]
#db_url = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{database_name}"
db_url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database_name}"
engine = create_engine(db_url)
mysql = engine.connect()
try:
    mysql.execute(text(f"create table {table} (id varchar(40) primary key , username varchar(255) , email varchar(255) , avatar varchar(255) )"))
except Exception as e:
        print ("already exists")
mysql.close()
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

    # or set @var = uuid();
    uuid = mysql.execute(text("select uuid()")).fetchall()
    id = uuid[0][0]
    
    query = text(f"insert into {table} (id , username , email , avatar) values (:id, :username , :email , :avatar)")
    param = {"id":id , "username": username, "email": email, "avatar": avatar}
    result = mysql.execute(query , param)
    #id = result.lastrowid
    mysql.commit()
    mysql.close()
    result.close()
    # dl
    try:
        wget.download(avatar , out=f"{storage}/{id}.jpg")
    except Exception as e:
        return e

    return {"user_id": f"{id}"}




@app.get("/users/{id}")
async def get_user(id):
    mysql = engine.connect()
    try: 
        query = text(f"select username , email from {table} where id = \"{id}\"")
        result = mysql.execute(query).fetchall()
        return {"username": f"{result[0][0]}" , "email": f"{result[0][1]}" }
    except Exception as e :
        return e

@app.get("/avatar/{id}")
async def get_user(id):
    return FileResponse(f"{storage}/{id}.jpg")

#print(cursor.execute("create database ali"))
#print(cursor.execute("show databases"))
#cursor
#for x in cursor:
#  print(x)

#if __name__ =="__main__":
#    uvicorn.run('api-sqlalchemy:app' , host='0.0.0.0' , port=8000 , reload=True )