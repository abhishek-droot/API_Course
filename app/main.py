from fastapi import FastAPI , Response , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional , List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine, SessionLocal, get_db


#what is the default Hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

@app.get("/")
def root():
    return {"message":"Welcome to my api"}
     
@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)
    posted = db.query(models.Post).all()
    return posted

@app.post("/createposts", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):                                   
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    return post

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: str , response: Response,db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts where id = %s """,(str(id),))
    #test_post = cursor.fetchone()
    #print(test_post)
    #post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} was not found")

    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ,db: Session = Depends(get_db)):
    # deleting post
    # find the index in the array that has reuired I
    # my_posts.pop(index)
    #cursor.execute(""" DELETE FROM posts where id = %s returning *""",(str(id),))
    #deleted_post = cursor.fetchone()
    #
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
             
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s  RETURNING *""",(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    #print(updated_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
     
    db.commit()

    return post_query.first()
    


#title str, content str, category , Boolean

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
     
    #hash the password - user.password
    #hash the password - user.passwpr
    
    hashed_password =  pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
     
    return new_user

