from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryOut
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryOut)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new category"""
    category = await CategoryService.create_category(
        db=db,
        category_in=category_in
    )
    return CategoryOut.from_orm_model(category)


@router.get("/", response_model=List[CategoryOut])
async def list_categories(
    db: AsyncSession = Depends(get_db)
):
    """List all categories - matches frontend categories"""
    categories = await CategoryService.list_categories(db)
    return [CategoryOut.from_orm_model(c) for c in categories]


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a single category by ID"""
    category = await CategoryService.get_category_by_id(db, category_id)
    return CategoryOut.from_orm_model(category)