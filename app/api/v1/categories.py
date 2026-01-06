from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryOut
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryOut)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    return await CategoryService.create_category(
        db=db,
        name=category_in.name
    )

@router.get("/", response_model=list[CategoryOut])
async def list_categories(
    db: AsyncSession = Depends(get_db)
):
    return await CategoryService.list_categories(db)