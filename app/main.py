from fastapi import FastAPI , Response , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional , List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post , user

#what is the default Hashing algorithm


models.Base.metadata.create_all(bind=engine)  

app = FastAPI()


#request Get method url



while True:

    try:
        conn = psycopg2.connect(host='localhost', database='newapi', user='postgres',password='1234567890', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)

my_post = [{"title":"title of Post 1", "content": "content of post 1", "id": 1},
{"title":"favourite foods","content":"I like Pizza", "id":2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
    
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message":"Welcome to my api"}
     



#title str, content str, category , Boolean


     
