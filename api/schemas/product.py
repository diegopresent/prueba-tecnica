from pydantic import BaseModel
from typing import List, Optional
from .category import Category
from .image import Image

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    id: int
    category: Optional[Category] = None
    images: List[Image] = []

    class Config:
        from_attributes = True