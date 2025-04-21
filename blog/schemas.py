from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body: str
    

class BlogConfig(Blog):
    class Confing():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[BlogConfig] = []
    class Confing():
        orm_mode = True
    
class ShowUserSchemaWithoutBlogs(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUserSchemaWithoutBlogs
    class Confing():
        orm_mode = True

