from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.category import Category

class CategoryService:

    @staticmethod
    async def create_category(
        db: AsyncSession,
        name: str
    ) -> Category:

        result = await db.execute(
            select(Category).where(Category.name == name)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Category already exists")

        category = Category(name=name)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def list_categories(db: AsyncSession):
        result = await db.execute(select(Category))
        return result.scalars().all()
