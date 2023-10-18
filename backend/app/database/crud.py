from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import Session
from database import models
import schemas, auth

def get_all_posts(db: Session) : 
    stmt = select(models.Posts)
    result = db.execute(stmt)
    return result.scalars().all()

def get_post_by_id(id:int, db: Session) :
    stmt = select(models.Posts).where(models.Posts.id == id) 
    result = db.execute(stmt) 
    return result.scalar()

def create_a_post(post: schemas.PostCreate , db: Session):    # post schema is defined in main so lets make schema file later
    stmt = insert(models.Posts).values(**post.model_dump()).returning(models.Posts)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar()

def delete_a_post_by_id(id: int, db: Session):
    stmt = delete(models.Posts).where(models.Posts.id == id).returning(models.Posts)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar() 

def update_a_post_by_id(id:int, post: schemas.PostUpdate, db:Session): 
    stmt = update(models.Posts).where(models.Posts.id == id).values(**post.model_dump()).returning(models.Posts) 
    result = db.execute(stmt)
    db.commit()
    return result.scalar()


#=========================================================================================================================

def user_create(user: schemas.UserCreate, db: Session): 
    user.password = auth.get_password_hash(user.password)
    stmt = insert(models.Users).values(**user.model_dump()).returning(models.Users)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar()
    
def user_update(id: int, user: schemas.UserUpdate, db: Session): 
    user.password = auth.get_password_hash(user.password)
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
    stmt = select(models.Users)
    result = db.execute(stmt) 
    return result