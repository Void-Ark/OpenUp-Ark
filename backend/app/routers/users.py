from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session 
import schemas, oauth2, database
from typing import Sequence


router = APIRouter(prefix='/users', tags=['users'])


#----------------------------------------- GET ALL USERS -----------------------------------------------
@router.get(
    path='/', 
    status_code=status.HTTP_200_OK, 
    response_model=list[schemas.UserGet]) 
def get_all(db: Session = Depends(database.get_db)) -> list[schemas.UserGet]: 
    data = database.crud.user_get_all(db=db) 
    if not data : raise HTTPException(
                                status_code=status.HTTP_204_NO_CONTENT, 
                                detail=f"there is no content!")
    return data                                                                 # type: ignore # not able to resolve 

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



#--------------------------------- DELETE A USER ------------------------------------------------------
@router.delete(
    path='/', 
    status_code=status.HTTP_204_NO_CONTENT) 
def user_delete_by_id(
    db: Session = Depends(database.get_db), 
    current_user_id : schemas.tokenData = Depends(oauth2.get_current_user)
): 
    data = database.crud.user_delete(id=current_user_id.id, db=db)
    if data : 
        print("user deleted successfully", data)
    else : 
        print("User not found")

#---------------------------------All POST OF A USER------------------------------------------------------
@router.get(
    path='/posts', 
    status_code=status.HTTP_200_OK)
def user_all_posts(
    db: Session = Depends(database.get_db), 
    current_user: schemas.tokenData = Depends(oauth2.get_current_user)
):
    data = database.crud.get_all_posts_by_user_id(db=db, user_id=current_user.id) 
    if not data : 
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"There is no post under user id: {current_user.id}")
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