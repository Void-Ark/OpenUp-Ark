# from typing import annotated --> in future
from fastapi import FastAPI
from database import create_db
import routers

create_db()
app = FastAPI() 

app.include_router(router= routers.auth.router)

app.include_router(router= routers.users.router)

app.include_router(router= routers.posts.router)

