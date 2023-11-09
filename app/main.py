# swagger : http://127.0.0.1:8000/posts/docs
# redoc : http://127.0.0.1:8000/redoc
# uvicorn  app.main:app --reload
# login == password == admin
# port : 5432
#===================================================================
# REGION : logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fmt = "%(asctime)s [%(levelname)s] %(message)s"
datefmt = "[%d-%m-%Y] [%H:%M:%S]"
formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

file_handler_error = logging.FileHandler(filename="app_error.log", 
                                         encoding="utf-8")
file_handler_error.setLevel(logging.ERROR)
file_handler_error.setFormatter(formatter)

file_handler = logging.FileHandler(filename="app.log",
                                    encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler_error)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
# ENDREGION logging
#===================================================================
import uuid
import psycopg
from psycopg.rows import dict_row 

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    id: Optional[int] = uuid.uuid4().hex
    title: str
    content: str
    published: bool = True

try:
    connection = psycopg.connect(host="localhost",
                                dbname="fastapi", 
                                user="postgres", 
                                password="admin")
    cursor = connection.cursor(row_factory=dict_row)
    logger.debug("Connection status: [\033[32mSUCCESS\033[0m]")

except Exception as error:
    logger.error(f"Connection status: [\033[31mFAILED\033[0m]. Error: {error}")
    exit()

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

# get-all-posts [DONE]
@app.get("/posts")
def get_posts():

    cursor.execute("""SELECT * FROM posts""")
    my_posts = cursor.fetchall()

    return {"posts": my_posts}

# creat-one-post [DONE]
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()

    return {
            "message": "Post created successfully",
            "post": new_post
            }


# get-one-post [DONE]
@app.get("/posts/{id}")
def get_post(id: int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        logger.error(f"Post with id [{id}] was not found.")
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id [{id}] was not found.")
    return {"post": post}


# delete-one-post [DONE]
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()

    if deleted_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id [{id}] was not found.")

    return JSONResponse(status_code = status.HTTP_200_OK, 
                        content={"message": "Post deleted successfully."})

def find_index_post(id: int):
    for index, post in enumerate(posts):
        if post["id"] == id:
            return index
    return None

# update-one-post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()

    if updated_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id [{id}] was not found.")
    return {
            "message": f"Post with id [{id}] updated successfully",
            "post": updated_post
        }
