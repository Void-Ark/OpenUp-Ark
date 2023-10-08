from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional
from random import randrange

class Post(BaseModel) : 
    title: str
    content: str 
    published: bool = True 
    rating: Optional[int] = None 
    
DATA = [
    {'id':101 , 'title': 'first post', "content": 'data of first post', "published": True, "rating": 32},
    {'id':102 , 'title': 'second post', "content": 'data of second post', "published": False, "rating": 100},
    {'id':103 , 'title': 'third post', "content": 'data of third post', "published": True},
]

app = FastAPI() 

@app.get(
    path='/post', 
    status_code=status.HTTP_200_OK)
async def get_all_post() : 
    return {"data": DATA}

@app.post(
    path='/post', 
    status_code=status.HTTP_201_CREATED) 
async def create_a_post(post: Post): 
    data = post.model_dump()
    data['id'] = randrange(3, 2034972034)
    DATA.append(data) 
    return DATA

@app.get(
    path='/post/{id}', 
    status_code=status.HTTP_302_FOUND)
async def get_one(id: int): 
    for i in DATA : 
        if i['id'] == id : 
            return i 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Given {id} is not found")

@app.delete(
    path='/post/{id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_by_id(id: int):
    for i in DATA : 
        if i['id'] == id : 
            DATA.remove(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Given id {id} is not found")

@app.put(
    path="/post/{id}",
    status_code=status.HTTP_200_OK
)
async def update_post_by_id(id: int, post: Post): 
    print(post, type(post))
    for i in DATA : 
        if i['id'] == id : 
            i['content'] = post.content
            i['title'] = post.title 
            return i
    HTTPException(status_code=status.HTTP_404_NOT_FOUND)    