from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services import category_service
from schemas import Category, CategoryCreate

# En esta clase se definen las rutas para las categorías, incluyendo la creación, obtención, actualización y eliminación de categorías.
# Se utiliza FastAPI para definir las rutas y manejar las solicitudes HTTP, y SQLAlchemy para interactuar con la base de datos.

router = APIRouter()

CATEGORY_NOT_FOUND = "Category not found"

@router.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, category)

@router.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return category_service.get_categories(db, skip, limit)

@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    return category

@router.patch("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    updated_category = category_service.update_category(db, category_id, category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    return updated_category

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if not category_service.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    return {"ok": True}