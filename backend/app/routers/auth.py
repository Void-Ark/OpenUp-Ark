from fastapi import APIRouter, Depends, HTTPException, status
import schemas, database, password_token, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import timedelta


router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
) 

@router.post("/login", response_model=schemas.token)
def user_login(user_cred: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)) : 
    print(user_cred)
    user = database.crud.user_get_data_by_email(user_cred.username, db)
    if not (user and password_token.verify_password(user_cred.password, user.password)): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"the given email or password  is invalid!!" ) 
    
    access_token_expires = timedelta(minutes=30)
    access_token = oauth2.create_access_token({"user_id": user.id}, access_token_expires) 
    return {"access_token": access_token, "token_type": "bearer"}  

@router.get("/check")
def checking_current_user(current_user_id : schemas.tokenData = Depends(oauth2.get_current_user)) : 
    return current_user_id
 

