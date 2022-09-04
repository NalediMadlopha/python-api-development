import time
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor

import psycopg2

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

class Post(BaseModel):
    title: str
    content: str
    published: bool


@app.get("/")
def root():
    return {"message": "Hello Naledi"}

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", str(id))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, str(id))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return Response(status_code=status.HTTP_410_GONE)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE post SET title = %s, content = %s, published =  %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return {"data": post}
