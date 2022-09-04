import time
import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='127.0.0.1', port='5432', database='fastapi', user='postgres',
                                password='dev123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)


my_posts = [
    {"id": 1, "title": "title 1", "content": "content 1"},
    {"id": 2, "title": "title 2", "content": "content 2"}
]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/")
def root():
    return {"message": "Hello Naledi"}

@app.get("/posts")
def get_posts(session: Session = Depends(get_db)):
    posts = session.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, session: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, session: Session = Depends(get_db)):
    post = session.query(models.Post).get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, session: Session = Depends(get_db)):
    post = session.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    post.delete(synchronize_session=False)
    session.commit()
    
    return Response(status_code=status.HTTP_410_GONE)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostUpdate, session: Session = Depends(get_db)):
    query = session.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    query.update(updated_post.dict(), synchronize_session=False)
    session.commit()

    return {"data": query.first()}
