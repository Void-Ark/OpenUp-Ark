from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models, crud

# FORMAT =>  postgresql://<username>:<password>@<ip_address/host_name>/<database_name>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:forgotansh1@localhost/Database-Ark"

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_db() : 
    models.Base.metadata.create_all(bind=engine)
    
def get_db() : 
    db = sessionLocal()
    try : 
        yield db
    finally : 
        db.close() 


    