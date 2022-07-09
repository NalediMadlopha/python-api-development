from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


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


@app.get("/")
def root():
    return {"message": "Hello Naledi"}


@app.get("/posts")
def get_post():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    my_posts.remove(post)
    
    return Response(status_code=status.HTTP_410_GONE)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    updated_post_dict = updated_post.dict()
    updated_post_dict["id"] = id
    my_posts[my_posts.index(post)] = updated_post_dict

    return {"message": updated_post_dict}
