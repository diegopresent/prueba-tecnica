from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update

import models, schemas
from database import get_db

router = APIRouter()

CATEGORY_NOT_FOUND_ERROR = "Category not found"

@router.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.execute(select(models.Category).offset(skip).limit(limit)).scalars().all()
    return categories

@router.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.execute(select(models.Category).filter(models.Category.id == category_id)).scalars().first()
    if category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND_ERROR)
    return category

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

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.execute(select(models.Category).filter(models.Category.id == category_id)).scalars().first()
    if category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND_ERROR)
    db.delete(category)
    db.commit()
    return {"ok": True}