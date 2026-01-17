from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.category import Category
from app.schemas.category import CategoryCreate

class CategoryService:

    @staticmethod
    async def create_category(
        db: AsyncSession,
        category_in: CategoryCreate = None,
        name: str = None,
        icon_name: str = None,
        color_hex: str = None
    ) -> Category:
        """Create a new category - matches frontend CategoryModel"""
        # Support both CategoryCreate schema and individual params
        if category_in:
            name = category_in.name
            icon_name = category_in.iconName
            color_hex = category_in.colorHex

        result = await db.execute(
            select(Category).where(Category.name == name)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Kategori zaten mevcut")

        category = Category(
            name=name,
            icon_name=icon_name,
            color_hex=color_hex
        )
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def list_categories(db: AsyncSession):
        """List all categories"""
        result = await db.execute(select(Category))
        return result.scalars().all()

    @staticmethod
    async def get_category_by_id(db: AsyncSession, category_id: str):
        """Get category by ID"""
        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Kategori bulunamadı")
        return category
