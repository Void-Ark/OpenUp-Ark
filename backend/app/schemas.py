from pydantic import BaseModel, AwareDatetime, EmailStr

class Post(BaseModel) : 
    title: str
    content: str 
    published: bool = True
class PostCreate(Post) : pass 
class PostUpdate(Post) : pass
class PostGet(Post) : 
    id : int
    created_at: AwareDatetime
    
#-------------------------------------------------------------------

class User(BaseModel): 
    email: EmailStr
    password: str 
class UserCreate(User): pass 
class UserUpdate(User): pass
 
class UserGet(BaseModel):  
    id: int 
    email: EmailStr
    created_at: AwareDatetime 