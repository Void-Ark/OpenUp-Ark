from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import Session
from database import models
import schemas
from pydantic import EmailStr
import password_token

def get_all_posts(db: Session) : 
    stmt = select(models.Posts)
    result = db.execute(stmt)
    return result.scalars().all()

def get_post_by_id(id:int, db: Session) :
    stmt = select(models.Posts).where(models.Posts.id == id) 
    result = db.execute(stmt) 
    return result.scalar()

def create_a_post(post: schemas.PostCreate , db: Session, user_id: int):    # post schema is defined in main so lets make schema file later
    post_copy_dict = post.model_dump() 
    post_copy_dict['user_id'] = user_id
    stmt = insert(models.Posts).values(**post_copy_dict).returning(models.Posts)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar()

def delete_a_post_by_id(id: int, db: Session, user_id: int):
    stmt = delete(models.Posts).where(models.Posts.id == id).where(models.Posts.id == user_id).returning(models.Posts)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar() 

def update_a_post_by_id(id:int, post: schemas.PostUpdate, db:Session, user_id: int): 
    stmt = update(models.Posts).where(models.Posts.id == id).where(models.Posts.user_id == user_id).values(**post.model_dump()).returning(models.Posts) 
    result = db.execute(stmt)
    db.commit()
    return result.scalar()

def post_get_id_by_title(title: str, db: Session) : 
    stmt = select(models.Posts.id).where(models.Posts.title == title) 
    result = db.execute(stmt) 
    return result.scalar()

#=========================================================================================================================

def user_create(user: schemas.UserCreate, db: Session): 
    user.password = password_token.get_password_hash(user.password)
    stmt = insert(models.Users).values(**user.model_dump()).returning(models.Users)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar()
    
def user_update(id: int, user: schemas.UserUpdate, db: Session): 
    user.password = password_token.get_password_hash(user.password)
    stmt = update(models.Users).where(models.Users.id == id).values(**user.model_dump()).returning(models.Users)
    result = db.execute(stmt)
    db.commit() 
    return result.scalar()

def user_delete(id: int, db: Session): 
    stmt = delete(models.Users).where(models.Users.id == id).returning() 
    result = db.execute(stmt) 
    db.commit() 
    return result.scalar()

def user_get(id: int, db: Session): 
    stmt = select(models.Users).where(models.Users.id == id)
    result = db.execute(stmt) 
    return result.scalar()

def user_get_all(db: Session): 
    stmt = select(models.Users) #["id", "email", "created_at"])
    print(stmt)
    result = db.execute(stmt) 
    ret = result.scalars().all()
    print(ret)
    return ret

def user_get_password(id:int, db: Session) :
    stmt = select(models.Users.password).where(models.Users.id == id)
    result = db.execute(stmt) 
    return result.scalar()

def user_get_id_by_email(email: EmailStr, db: Session) : 
    stmt = select(models.Users.id).where(models.Users.email == email)
    result = db.execute(stmt) 
    return result.scalar() 

def user_get_data_by_email(email: EmailStr, db: Session) : 
    id = user_get_id_by_email(email, db)
    return user_get(id, db) if id else None
    
    