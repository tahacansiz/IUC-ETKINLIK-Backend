from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    """Schema for creating a category"""
    name: str
    iconName: str | None = Field(default=None, alias="icon_name")
    colorHex: str | None = Field(default=None, alias="color_hex")
    
    class Config:
        populate_by_name = True


class CategoryOut(BaseModel):
    """Schema for category response - matches frontend CategoryModel"""
    id: str
    name: str
    iconName: str | None = Field(default=None, serialization_alias="iconName")
    colorHex: str | None = Field(default=None, serialization_alias="colorHex")

    class Config:
        from_attributes = True
        populate_by_name = True
    
    @classmethod
    def from_orm_model(cls, category) -> "CategoryOut":
        """Convert SQLAlchemy model to Pydantic schema"""
        return cls(
            id=str(category.id),
            name=category.name,
            iconName=category.icon_name,
            colorHex=category.color_hex
        )