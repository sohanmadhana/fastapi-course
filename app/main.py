from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

my_posts = [
    {
        'title':"favorite cars",
        "content": "Volkswagon passat",
        "id": 1
    },
    {
        'title':"favorite food",
        "content": "Pizza",
        "id": 2
    }
]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"]==id:
            return index

@app.get("/")
async def root():
    return {"message":"Hi!! This is my first project in python using FastAPI."}

@app.get("/posts")
async def get_posts():
    return {"data" : my_posts}

@app.get("/post/{id}")
def get_post_by_id(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"Post with id {id}. Not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id}. Not found.")
    return {"post" : post}

@app.post("/posts")
def create_post(new_post:Post):
    print(new_post)
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"post": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    return my_posts[-1]

@app.delete("/posts/{id}")
def delete_post(id:int, status_code=status.HTTP_204_NO_CONTENT):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return Response(status_code=status.HTTP_202_ACCEPTED,content=f"Post with id {id} is updated.")