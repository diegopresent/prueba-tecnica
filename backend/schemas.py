from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ImageBase(BaseModel):
    image_url: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    id: int
    category: Category
    images: List[Image] = []

    class Config:
        from_attributes = True