from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base() 

class Posts(Base) : 
    __tablename__ = "posts" 
    
    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String, nullable=False) 
    content = Column(String, nullable=False) 
    published = Column(Boolean, server_default="true", nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False) 
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False) 
    user = relationship("Users")        # here Users is a class name
    

class Users(Base): 
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True) 
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False) 
    phone_number = Column(String)
    
class Vote(Base): 
    __tablename__ = "votes" 
    
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), primary_key=True) 
    post_id = Column(Integer, ForeignKey(column="posts.id", ondelete="CASCADE"), primary_key=True)
    

    
    