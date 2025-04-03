from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Definición de los modelos de la base de datos utilizando SQLAlchemy

# Modelo para la tabla de productos
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    # Clave foránea que referencia a la tabla de categorías
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relación con la tabla de categorías
    category = relationship("Category", back_populates="products")
    # Relación con la tabla de imágenes
    images = relationship("Image", back_populates="product")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(1000), nullable=False)
    # Clave foránea que referencia a la tabla de productos
    product_id = Column(Integer, ForeignKey("products.id"))

    # Relación con la tabla de productos
    product = relationship("Product", back_populates="images")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Relación con la tabla de productos
    products = relationship("Product", back_populates="category")