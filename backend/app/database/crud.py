from sqlalchemy import select, insert, delete, update, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import join, Select
select_from = Select.select_from

from database import models
import schemas
from pydantic import EmailStr
import password_token
from typing import Optional

def get_all_posts(limit: int, offset: int, search: Optional[str], 
        db: Session) : 
    #stmt = select(models.Posts).filter(models.Posts.title.contains(search)).limit(limit=limit).offset(offset=offset)
    #j = join(models.Posts, models.Vote, models.Posts.id == models.Vote.post_id, isouter=True)
    #stmt = select(func.count(models.Vote.post_id).label("votes"), models.Posts.id).select_from(j).group_by(models.Posts.id)
    stmt = select(models.Posts, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id)
    print(f"STMT: F{stmt}")
    result = db.execute(stmt)
    print("Returning Result")
    return tuple(map(lambda row: row._asdict(), result))
    #return [row._asdict() for row in result]

def get_post_by_id(id: int,
        db: Session) :
    stmt = select(models.Posts).where(models.Posts.id == id) 
    result = db.execute(stmt) 
    return result.scalar()

def create_a_post(post: schemas.PostCreate, user_id: int,
        db: Session):    # post schema is defined in main so lets make schema file later
    post_copy_dict = post.model_dump() 
    post_copy_dict['user_id'] = user_id
    stmt = insert(models.Posts).values(**post_copy_dict).returning(models.Posts)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar()

def delete_a_post_by_id(id: int, user_id: int, 
        db: Session):
    stmt = delete(models.Posts).where(models.Posts.id == id).where(models.Posts.user_id == user_id).returning(models.Posts)
    result = db.execute(stmt) 
    db.commit()
    return result.scalar() 

def update_a_post_by_id(id: int, post: schemas.PostUpdate, user_id: int, 
        db: Session): 
    stmt = update(models.Posts).where(models.Posts.user_id == user_id, models.Posts.id == id).values(**post.model_dump()).returning(models.Posts) 
    result = db.execute(stmt)
    db.commit()
    return result.scalar()

def post_get_id_by_title(title: str, 
        db: Session) : 
    stmt = select(models.Posts.id).where(models.Posts.title == title) 
    result = db.execute(stmt) 
    return result.scalar()

def get_all_posts_by_user_id(user_id: int, 
        db: Session): 
    stmt = select(models.Posts).where(models.Posts.user_id == user_id) 
    result = db.execute(stmt) 
    return result.scalars().all()

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
    
#========================================VOTES====================================================

def vote_find(post_id: int, user_id: int, db: Session) -> models.Vote|None : 
    stmt = select(models.Vote).where(models.Vote.user_id == user_id, models.Vote.post_id == post_id)
    result = db.execute(stmt)
    return result.scalar()

def vote_create(post_id: int, user_id: int, db: Session) : 
    stmt = insert(models.Vote).values(post_id=post_id, user_id=user_id).returning(models.Vote) 
    result = db.execute(stmt) 
    db.commit()
    return result.scalar() 

def vote_delete(post_id: int, user_id: int, db: Session) : 
    stmt = delete(models.Vote).where(models.Vote.post_id == post_id, models.Vote.user_id == user_id).returning(models.Vote) 
    result = db.execute(stmt) 
    db.commit()
    return result.scalar() 