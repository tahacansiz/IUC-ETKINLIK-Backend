from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True