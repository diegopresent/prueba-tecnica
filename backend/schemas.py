from pydantic import BaseModel
from typing import List, Optional

# Esquema base para categorías
# Se utiliza la clase BaseModel de Pydantic para definir los esquemas
# y validar los datos de entrada y salida.
class CategoryBase(BaseModel):
    name: str

# Esquema para crear una nueva categoría en la base de datos.
class CategoryCreate(CategoryBase):
    pass

# Esquema para representar categorias.
class Category(CategoryBase):
    id: int

    class Config: # Configuración de Pydantic para el modelo 
        from_attributes = True # Permite que Pydantic use los atributos de la clase SQLAlchemy directamente.


# Esquema base para imágenes
class ImageBase(BaseModel):
    image_url: str
    product_id: Optional[int] = None # Relación opcional con el ID del producto al que pertenece la imagen.

# Esquema para crear una nueva imagen.
class ImageCreate(ImageBase):
    pass

# Esquema para representar imágenes.
# Hereda de ImageBase y agrega el ID de la imagen y la relación con el producto.
# También incluye un campo opcional para el ID del producto al que pertenece la imagen. Esto porque puede ser que la imagen no pertenezca a ningun producto.
class Image(ImageBase):
    id: int
    class Config: # Configuración de Pydantic para el modelo
        from_attributes = True # Permite que Pydantic use los atributos de la clase SQLAlchemy directamente.

# Esquema base para productos
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: Optional[int] = None # Relación opcional con el ID de la categoría a la que pertenece el producto.

# Esquema para crear un nuevo producto.
class ProductCreate(ProductBase):
    pass

# Esquema para actualizar un producto existente.
# Los campos opcionales permiten actualizar solo los campos que se deseen modificar.
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

# Esquema para representar un producto completo.
# Hereda de ProductBase y agrega el ID del producto y la relación con la categoría.
# También incluye una lista de imágenes asociadas al producto.
class Product(ProductBase):
    id: int
    category: Optional[Category] = None # Relación con la categoría del producto.
    images: List[Image] = [] # Lista de imágenes asociadas al producto.

    class Config: # Configuración de Pydantic para el modelo
        from_attributes = True # Permite que Pydantic use los atributos de la clase SQLAlchemy directamente.