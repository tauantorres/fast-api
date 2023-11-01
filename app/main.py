# swagger : http://127.0.0.1:8000/posts/docs
# redoc : http://127.0.0.1:8000/redoc
# uvicorn  app.main:app --reload
# login == password == admin
# port : 5432

import uuid

from fastapi import FastAPI, Response, status, HTTPException

from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    id: Optional[str] = str(uuid.uuid4().hex)
    title: str
    content: str
    published: bool = True

posts = [
    {
        "id": "1",
        "title" : "FIRST",
        "content": "My first post",
        "published": True,
    },
    {
        "id": "2",
        "title" : "SECOND",
        "content": "My second post",
        "published": True,
    }
]

# get-all-posts
@app.get("/posts")
def get_posts():
    return {"posts": posts}

# creat-one-post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    posts.append(post.model_dump())
    return {
            "message": "Post created successfully",
            "post": post
        }

# get-one-post
@app.get("/posts/{id}")
def get_post(id: str):
    return find_post(id)

def find_post(id: str)-> dict:
    for post in posts:
        if post["id"] == id:
            return {"post": post}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f"Post with id [{id}] was not found.")

# delete-one-post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id [{id}] was not found.")
    posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT, 
                   content="Post deleted successfully.")

def find_index_post(id: str):
    for index, post in enumerate(posts):
        if post["id"] == id:
            return index
    return None

# update-one-post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: str, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id [{id}] was not found.")
    updated_post = post.model_dump()
    updated_post["id"] = id
    posts[index] = updated_post

    return {
            "message": f"Post with id [{id}] updated successfully",
            "post": updated_post
        }
