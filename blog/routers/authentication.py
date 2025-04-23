from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import Login as LoginSchema, Token
from ..db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import User
from passlib.context import CryptContext
from datetime import timedelta
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["authentication"]
)

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")

@router.post("/login", response_model=Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.username))
    user = result.scalars().first()

    if not user or not pwd_cxt.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
