from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .schemas import Blog as BlogSchema, User as UserSchema, ShowUser as ShowUserSchema, ShowBlog as ShowBlogSchema
from .models import Blog as BlogModel, User as UserModel, Base
from .db import engine, SessionLocal
from . import models
from passlib.context import CryptContext

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", response_model = ShowBlogSchema, status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog/", response_model = ShowBlogSchema, tags=["blogs"])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs

@app.get("/blog/{id}", response_model = ShowBlogSchema, tags=["blogs"])
def show_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "Blog not found"}
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])   
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model = ShowBlogSchema, tags=["blogs"])
def update_blog(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return {"Updated_blog": blog}  

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated = auto)

@app.post('/user', response_model = ShowUserSchema, tags=["users"])
def create_user(request:UserSchema,  db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = UserModel(name = request.name, email = request.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user', response_model =  ShowUserSchema, tags=["users"])
def show_user(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@app.get('/user/{id}', response_model =  ShowUserSchema, tags=["users"])
def show_user(id:int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
