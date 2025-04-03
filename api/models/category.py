from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# Esta clase representa la tabla de categorías en la base de datos.
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    products = relationship("Product", back_populates="category")