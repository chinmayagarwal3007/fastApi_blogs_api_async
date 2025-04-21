from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .schemas import Blog as BlogSchema, User as UserSchema
from .models import Blog as BlogModel, User as UserModel
from .db import engine, SessionLocal

app = FastAPI()

BlogModel.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog/")
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs

@app.get("/blog/{id}")
def show_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "Blog not found"}
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return {"Updated_blog": blog}  

@app.post('/user')
def create_user(request:UserSchema,  db: Session = Depends(get_db)):
    new_user = UserModel(request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
