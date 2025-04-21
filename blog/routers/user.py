from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import User as UserSchema, ShowUser as ShowUserSchema
from ..models import User as UserModel
from ..db import get_db
from passlib.context import CryptContext

router = APIRouter()

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated = "auto")

@router.post('/user', response_model = ShowUserSchema, tags=["users"])
def create_user(request:UserSchema,  db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = UserModel(name = request.name, email = request.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user', response_model =  List[ShowUserSchema], tags=["users"])
def show_user(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get('/user/{id}', response_model =  ShowUserSchema, tags=["users"])
def show_user(id:int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
