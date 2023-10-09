from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body

import psycopg2 
from psycopg2.extras import RealDictCursor
from time import sleep

from pydantic import BaseModel
from typing import Optional
from random import randrange

import database
from sqlalchemy.orm import Session

database.create_db()
db = database.get_db() 

class Post(BaseModel) : 
    title: str
    content: str 
    published: bool = True 
    rating: Optional[int] = None 
    
while True : 
    try : 
        conn = psycopg2.connect(
            host='localhost',
            dbname='Database-Ark', 
            user='postgres', 
            password='forgotansh1',
            cursor_factory=RealDictCursor 
            )
        cursor = conn.cursor() 
        print("the database connection is successful!!")
        break 
    except Exception as e : 
        print(e) 
        sleep(5)
    
app = FastAPI() 

#------------------------------GET ALL POST--------------------------
@app.get(
    path='/post', 
    status_code=status.HTTP_200_OK)
async def get_all_post(db: Session = Depends(database.get_db)): 
    data = database.crud.get_all_posts(db=db)
    if data : return data
    else : raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="the table is empty!!")

#------------------------------CREATE A POST --------------------------
@app.post(
    path='/post', 
    status_code=status.HTTP_201_CREATED)
async def create_a_post(post: Post): 
    cursor.execute(
        query='''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
        vars=(post.title, post.content, post.published))
    data = cursor.fetchone()
    conn.commit()
    return data

#---------------------------GET A POST BY ID --------------------------
@app.get(
    path='/post/{id}', 
    status_code=status.HTTP_302_FOUND)
async def get_one(id: int, db: Session = Depends(database.get_db)): 
    data = database.crud.get_post_by_id(id, db)
    if data : return data    
    else : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Given {id} is not found")

#------------------------DELETE A POST BY ID --------------------------
@app.delete(
    path='/post/{id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_by_id(id: int):
    cursor.execute(
        query='''DELETE FROM posts where id = %s RETURNING *''', 
        vars=(id, ))
    
    data = cursor.fetchone()
     
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Given id {id} is not found")
    
    conn.commit() 


#-------------------------UPDATE A POST BY ID ------------------------
@app.put(
    path="/post/{id}",
    status_code=status.HTTP_200_OK)
async def update_post_by_id(id: int, post: Post): 
    cursor.execute(
        query='''UPDATE posts 
                SET title = %s, content = %s, published = %s 
                where id = %s returning *''', 
        vars=(post.title, post.content, post.published, id))
    data = cursor.fetchone()
    
    if data == None : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"the given id {id} is not found!!")    
    
    conn.commit() 
    return data