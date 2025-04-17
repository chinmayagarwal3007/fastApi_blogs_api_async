from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .schemas import Blog as BlogSchema
from .models import Blog as BlogModel
from .db import engine, SessionLocal

app = FastAPI()

BlogModel.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog")
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