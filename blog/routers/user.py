from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ..schemas import User as UserSchema, ShowUser as ShowUserSchema
from ..models import User as UserModel
from ..db import get_db
from passlib.context import CryptContext

router = APIRouter()

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")

@router.post('/user', response_model=ShowUserSchema, tags=["users"])
async def create_user(request: UserSchema, db: AsyncSession = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = UserModel(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    await db.commit()  # Async commit
    await db.refresh(new_user)  # Async refresh
    return new_user

@router.get('/user', response_model=List[ShowUserSchema], tags=["users"])
async def show_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()  # Get all users
    return users

@router.get('/user/{id}', response_model=ShowUserSchema, tags=["users"])
async def show_user(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == id))
    user = result.scalars().first()  # Get the first user
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
