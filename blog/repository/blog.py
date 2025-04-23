from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Blog as BlogModel

async def get_all(db: AsyncSession):
    result = await db.execute(select(BlogModel))
    blogs = result.scalars().all()  # Fetch all the blogs asynchronously
    return blogs