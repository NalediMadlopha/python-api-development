from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
def root():
    return {"message": "Hello Naledi"}


@app.get("/posts")
def get_post():
    return {"data": "This is your post"}


@app.post("/createposts")
def create_posts(post: Post):
    print(post.title)
    return {"data": "new"}
