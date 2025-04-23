from fastapi import FastAPI
from .models import Base
from .db import engine
from .routers import blog, user, authentication
import asyncio

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Create tables asynchronously
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
