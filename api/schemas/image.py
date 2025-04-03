from pydantic import BaseModel # librería pydantic, que se utiliza para crear modelos de datos en Python.
from typing import Optional # librería typing, que se utiliza para especificar tipos de datos en Python.

class ImageBase(BaseModel):
    image_url: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    product_id: Optional[int] = None

    class Config:
        from_attributes = True