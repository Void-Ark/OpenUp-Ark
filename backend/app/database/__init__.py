from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import models, crud
from config import settings 

USERNAME = settings.database_username 
PASSWORD = settings.database_password 
HOST_NAME = settings.database_hostname 
NAME = settings.database_name

# FORMAT =>  postgresql://<username>:<password>@<ip_address/host_name>/<database_name>
SQLALCHEMY_DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST_NAME}/{NAME}"
#print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def create_db() : 
    models.Base.metadata.create_all(bind=engine)
    
def get_db() : 
    db = sessionLocal()
    try : 
        yield db
    finally : 
        db.close() 