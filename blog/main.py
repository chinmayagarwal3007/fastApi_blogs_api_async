from fastapi import FastAPI
from .models import Base
from .db import engine
from .routers import blog, user, authentication


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)


