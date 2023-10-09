from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import Posts

def get_all_posts(db: Session) : 
    stmt = select(Posts)
    result = db.execute(stmt)
    return result.scalars().all()

def get_post_by_id(id:int, db: Session) :
    stmt = select(Posts).where(Posts.id == id) 
    result = db.execute(stmt) 
    return result.scalar()

def create_a_post()