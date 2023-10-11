from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import Session
from database import models
import schemas

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