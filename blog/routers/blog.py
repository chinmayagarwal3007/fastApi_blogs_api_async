from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schemas import Blog as BlogSchema, ShowBlog as ShowBlogSchema, User as UserSchema
from ..models import Blog as BlogModel
from ..db import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    tags=["blogs"],
    prefix="/blog"
)

@router.get("/", response_model=List[ShowBlogSchema])
async def get_all(db: AsyncSession = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    result = await db.execute(select(BlogModel))
    blogs = result.scalars().all()
    return blogs

@router.post("/", response_model=ShowBlogSchema, status_code=status.HTTP_201_CREATED)
async def create(request: BlogSchema, db: AsyncSession = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    new_blog = BlogModel(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

@router.get("/{id}", response_model=ShowBlogSchema)
async def show_blog(id: int, db: AsyncSession = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    result = await db.execute(select(BlogModel).where(BlogModel.id == id))
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: AsyncSession = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    result = await db.execute(select(BlogModel).where(BlogModel.id == id))
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    await db.delete(blog)
    await db.commit()

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowBlogSchema)
async def update_blog(id: int, request: BlogSchema, db: AsyncSession = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    result = await db.execute(select(BlogModel).where(BlogModel.id == id))
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    blog.title = request.title
    blog.body = request.body
    await db.commit()
    await db.refresh(blog)
    return {"Updated_blog": blog}
