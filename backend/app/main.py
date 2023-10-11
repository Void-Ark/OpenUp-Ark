from fastapi import FastAPI, HTTPException, Response, Depends, status
from sqlalchemy.orm import Session
import database, schemas


database.create_db()
app = FastAPI() 

#------------------------------GET ALL POST--------------------------
@app.get(
    path='/post', 
    status_code=status.HTTP_200_OK, 
    response_model=list[schemas.PostGet])
async def get_all_post(db: Session = Depends(database.get_db)): 
    data = database.crud.get_all_posts(db=db)
    if data : return data
    else : raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="the table is empty!!")

#------------------------------CREATE A POST --------------------------
@app.post(
    path='/post', 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.Post)
async def create_a_post(
    post: schemas.PostCreate, 
    db: Session = Depends(database.get_db)):
        
    try : 
        data = database.crud.create_a_post(post=post, db=db) 
    except Exception as e : 
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"the data is not acceptable may be because of some values become null which are set as not nullable (title, content)")
    return data

#---------------------------GET A POST BY ID --------------------------
@app.get(
    path='/post/{id}', 
    status_code=status.HTTP_302_FOUND, 
    response_model=schemas.PostGet)
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
    status_code=status.HTTP_204_NO_CONTENT, 
    response_model=schemas.PostGet)
async def delete_post_by_id(
    id: int, 
    db: Session = Depends(database.get_db)):
     
    data = database.crud.delete_a_post_by_id(id=id, db=db) 
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"the given id {id} is not in database")
    return data 

#-------------------------UPDATE A POST BY ID ------------------------
@app.put(
    path="/post/{id}",
    status_code=status.HTTP_200_OK, 
    response_model=schemas.PostGet)
async def update_post_by_id(
    id: int, 
    post: schemas.PostUpdate, 
    db: Session = Depends(database.get_db)):
     
    try : 
        data = database.crud.update_a_post_by_id(id, post, db)
    except Exception as e : 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"may be the given id {id} is not found :{e}"
        )
    if data == None : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"the given id {id} is not found!!")    
    return data