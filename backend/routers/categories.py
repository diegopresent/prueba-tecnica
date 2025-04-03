from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update

import models, schemas
from database import get_db

# Importa las dependencias necesarias para la creación de rutas y manejo de excepciones
router = APIRouter()

CATEGORY_NOT_FOUND_ERROR = "Category not found"

# Ruta para crear una categoría
# Esta ruta recibe un objeto de tipo CategoryCreate y lo guarda en la base de datos y devuelve el objeto creado.
# La función model_dump() de Pydantic se utiliza para convertir el objeto en un diccionario que SQLAlchemy puede entender.
# La función refresh() se utiliza para actualizar el objeto con los datos de la base de datos después de que se ha guardado.
# Esto es útil para obtener el ID generado automáticamente por la base de datos.
@router.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category) 
    return db_category

# Ruta para obtener una lista de categorías
# Esta ruta recibe dos parámetros opcionales: skip y limit, que se utilizan para paginar los resultados.
# La función scalars() se utiliza para obtener solo los resultados de la consulta y no los metadatos adicionales.
# La función all() se utiliza para obtener todos los resultados de la consulta.
# La función offset() se utiliza para omitir un número específico de resultados y la función limit() se utiliza para limitar el número de resultados devueltos.
@router.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.execute(select(models.Category).offset(skip).limit(limit)).scalars().all()
    return categories

# En este caso, se está seleccionando todos los registros de la tabla Category.
# La función scalars() se utiliza para obtener solo los resultados de la consulta y no los metadatos adicionales.
# La función first() se utiliza para obtener el primer resultado de la consulta.
# Si no se encuentra la categoría, se lanza una excepción HTTP 404 con un mensaje de error.
# La función filter() se utiliza para filtrar los resultados de la consulta.
# En este caso, se está filtrando por el ID de la categoría.
@router.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.execute(select(models.Category).filter(models.Category.id == category_id)).scalars().first()
    if category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND_ERROR)
    return category

# Ruta para actualizar una categoría
# Esta ruta recibe un ID de categoría y un objeto de tipo CategoryCreate y actualiza la categoría en la base de datos.
# La función model_dump() de Pydantic se utiliza para convertir el objeto en un diccionario que SQLAlchemy puede entender.
# La función exclude_unset=True se utiliza para excluir los campos que no se han establecido en el objeto.
# La función update() se utiliza para crear una consulta de actualización en SQLAlchemy.
# La función values() se utiliza para establecer los nuevos valores de la categoría.
@router.patch("/categories/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.execute(select(models.Category).filter(models.Category.id == category_id)).scalars().first()
    if db_category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND_ERROR)
    update_data = category.model_dump(exclude_unset=True)
    if update_data:
        db.execute(update(models.Category).where(models.Category.id == category_id).values(**update_data))
        db.commit()
        db.refresh(db_category)
    return db_category

# Ruta para eliminar una categoría
# Esta ruta recibe un ID de categoría y elimina la categoría de la base de datos.
# La función delete() se utiliza para eliminar la categoría de la base de datos.
# La función commit() se utiliza para guardar los cambios en la base de datos.
# La función scalars() se utiliza para obtener solo los resultados de la consulta y no los metadatos adicionales.
# La función first() se utiliza para obtener el primer resultado de la consulta.
@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.execute(select(models.Category).filter(models.Category.id == category_id)).scalars().first()
    if category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND_ERROR)
    db.delete(category)
    db.commit()
    return {"ok": True}