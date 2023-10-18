from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session 
import schemas 
import database

router = APIRouter(prefix='/users', tags=['users'])

#----------------------------------------- CREATE A USER ------------------------------------------------
@router.post(
    path='/', 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.UserGet)
def user_create(
    user: schemas.UserCreate, 
    db : Session = Depends(database.get_db)
): 
    data = database.crud.user_create(user=user, db=db) 
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"the data is not acceptable may be because of some values become null which are set as not nullable (email, password)")
    return data

#-------------------------------------------GET A USER-------------------------------------------------------
@router.get(
    path='/{id}', 
    status_code=status.HTTP_302_FOUND, 
    response_model=schemas.UserGet)
async def user_get_by_id(id: int, db: Session = Depends(database.get_db)): 
    data = database.crud.user_get(id, db)
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Given {id} is not found")
    return data 

#--------------------------------- DELETE A USER ------------------------------------------------------
@router.delete(
    path='/{id}', 
    status_code=status.HTTP_204_NO_CONTENT) 
def user_delete_by_id(id: int, db: Session = Depends(database.get_db)): pass