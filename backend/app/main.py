# from typing import annotated --> in future
from fastapi import FastAPI
import database
import routers

database.create_db()
app = FastAPI() 

app.include_router(router= routers.users.router)

app.include_router(router= routers.posts.router)

