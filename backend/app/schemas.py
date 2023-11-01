from typing import Optional
from pydantic import BaseModel, AwareDatetime, EmailStr


    
#-------------------------------------------------------------------

class UserBase(BaseModel): 
    email: EmailStr
    password: str 
class UserCreate(UserBase): pass 
class UserUpdate(UserBase): pass
class UserLogin(UserBase): pass 
class UserSignIn(UserBase): pass 

class UserGet(BaseModel):  
    id: int 
    email: EmailStr
    created_at: AwareDatetime 
    
#-----------------------------------------------------------------
    
class token(BaseModel) :
    access_token: str 
    token_type: str
    
class tokenData(BaseModel) : 
    id: int
    
#----------------------------------------------------------------
class PostBase(BaseModel) : 
    title: str
    content: str 
    published: bool = True
class PostCreate(PostBase) : pass 
class PostUpdate(PostBase) : pass
class PostGet(PostBase) : 
    id : int
    user_id: int 
    created_at: AwareDatetime