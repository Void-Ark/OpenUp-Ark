from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session 
import schemas, database, oauth2
from typing import Optional

router = APIRouter(prefix='/posts', tags=['posts'])

#------------------------------GET ALL POST--------------------------
@router.get(
    path='/', 
    status_code=status.HTTP_200_OK, 
    response_model=list[schemas.PostOut])
async def get_all_post(db: Session = Depends(database.get_db), limit: int=4, skip: int=0, search: Optional[str]=''): 
    print("start")
    data = database.crud.get_all_posts(db=db, limit=limit, offset=skip, search=search)
    print("end")
    if data : return data
    else : raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="the table is empty!!")

#------------------------------CREATE A POST --------------------------
@router.post(
    path='/', 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.PostGet)
async def create_a_post(
    post: schemas.PostCreate, 
    db: Session = Depends(database.get_db), 
    current_user_id : schemas.tokenData = Depends(oauth2.get_current_user)
):        
    data = database.crud.create_a_post(post=post, db=db, user_id=current_user_id.id) 
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"the data is not acceptable may be because of some values become null which are set as not nullable (title, content)")
    return data

#---------------------------GET A POST BY ID --------------------------
@router.get(
    path='/{id}', 
    status_code=status.HTTP_302_FOUND, 
    response_model=schemas.PostGet)
async def get_one(id: int, db: Session = Depends(database.get_db)): 
    data = database.crud.get_post_by_id(id, db)
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Given {id} is not found")
    return data

#------------------------DELETE A POST BY ID --------------------------
@router.delete(
    path='/{id}', 
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user_id : schemas.tokenData = Depends(oauth2.get_current_user)
):     
    data = database.crud.delete_a_post_by_id(id=id, db=db, user_id=current_user_id.id) 
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"the given id {id} is not in database or you are not allowed to delete another user post")


#-------------------------UPDATE A POST BY ID ------------------------
@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK, 
    response_model=schemas.PostGet)
async def update_post_by_id(
    id: int, 
    post: schemas.PostUpdate, 
    db: Session = Depends(database.get_db), 
    current_user_id : schemas.tokenData = Depends(oauth2.get_current_user)
):
    data = database.crud.update_a_post_by_id(id=id, post=post, db=db, user_id=current_user_id.id)
    if data == None : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"the given id {id} is not found!! OR you are not allowed to delete another user post")    
    return data


