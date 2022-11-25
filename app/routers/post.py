from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional , List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models,schemas, utils
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=["Posts"]
    #group name
)

@router.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)
    posted = db.query(models.Post).all()
    return posted

@router.post("/createposts", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):                                   
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#@router.get("/posts/latest")
#def get_latest_post():
    post = my_post[len(my_post)-1]
    return post

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: str , response: Response,db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts where id = %s """,(str(id),))
    #test_post = cursor.fetchone()
    #print(test_post)
    #post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} was not found")

    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/posts/{id}", response_model=schemas.Post)
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
    