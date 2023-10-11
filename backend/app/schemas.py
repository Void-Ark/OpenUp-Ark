from pydantic import BaseModel, AwareDatetime

class Post(BaseModel) : 
    title: str
    content: str 
    published: bool = True
    
class PostCreate(BaseModel) : 
    title: str
    content: str 
    published: bool = True
    
class PostUpdate(BaseModel) : 
    title: str
    content: str 
    published: bool 
    
class PostGet(BaseModel) : 
    id : int
    title: str
    content: str 
    published: bool 
    created_at: AwareDatetime