from sqlalchemy.orm import Session
from ..models import Blog as BlogModel


def get_all(db: Session):
    blogs = db.query(BlogModel).all()
    return blogs