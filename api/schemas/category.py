from pydantic import BaseModel

# Esta clase representa la base de datos de categorías.
# Se utiliza Pydantic para validar los datos de entrada y salida.
# La clase CategoryBase define los campos comunes para las categorías, mientras que CategoryCreate y Category
# definen los campos específicos para la creación y representación de categorías.
# La clase Config se utiliza para configurar la serialización y deserialización de los modelos de datos.

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True