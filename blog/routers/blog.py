from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Blog as BlogSchema, ShowBlog as ShowBlogSchema
from ..models import Blog as BlogModel
from ..db import get_db
from ..repository import blog as blog_repo

router = APIRouter(
tags=["blogs"],
prefix="/blog"
)

@router.get("/", response_model = List[ShowBlogSchema])
def get_all(db: Session = Depends(get_db)):
    return blog_repo.get_all(db)

@router.post("/", response_model = ShowBlogSchema, status_code=status.HTTP_201_CREATED)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{id}", response_model = ShowBlogSchema)
def show_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "Blog not found"}
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)   
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model = ShowBlogSchema)
def update_blog(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return {"Updated_blog": blog}  