import os
import shutil
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import select, update

import models, schemas
from database import get_db

router = APIRouter()
IMAGES_DIR = "imagenes/"
ABS_IMAGES_DIR = os.path.abspath(IMAGES_DIR)

if not os.path.exists(ABS_IMAGES_DIR): # esto verifica si el directorio existe
    os.makedirs(ABS_IMAGES_DIR) # esto crea el directorio si no existe 

PRODUCT_NOT_FOUND_ERROR = "Product not found"

@router.post("/products/", response_model=schemas.Product)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db_product = models.Product(name=name, description=description, price=price, category_id=category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    image_path = os.path.join(IMAGES_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    db_image = models.Image(image_url=image_path, product_id=db_product.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_product

@router.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.execute(select(models.Product).offset(skip).limit(limit)).scalars().all()
    return products

@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.execute(select(models.Product).filter(models.Product.id == product_id)).scalars().first()
    if product is None:
        raise HTTPException(status_code=404, detail=PRODUCT_NOT_FOUND_ERROR) # Usa la constante
    return product

@router.patch("/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_product = db.execute(select(models.Product).filter(models.Product.id == product_id)).scalars().first()
    if db_product is None:
        raise HTTPException(status_code=404, detail=PRODUCT_NOT_FOUND_ERROR) # Usa la constante

    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if price is not None:
        update_data["price"] = price
    if category_id is not None:
        update_data["category_id"] = category_id


    if update_data:
        db.execute(update(models.Product).where(models.Product.id == product_id).values(**update_data))
        db.commit()
        db.refresh(db_product)

    if image:
        image_path = os.path.join(IMAGES_DIR, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer) 

        # db_image = db.execute(select(models.Image).filter(models.Image.product_id == product_id)).scalars().first()
        # if db_image:
        #     db_image.image_url = image_path
        # else:
        db_image = models.Image(image_url=image_path, product_id=product_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_product)

    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.execute(select(models.Product).filter(models.Product.id == product_id)).scalars().first()
    if product is None:
        raise HTTPException(status_code=404, detail=PRODUCT_NOT_FOUND_ERROR) # Usa la constante
    db.delete(product)
    db.commit()
    return {"ok": True}