import os
import shutil
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from database import get_db
from services import product_service

from schemas import Product

router = APIRouter()
IMAGES_DIR = "imagenes/"
ABS_IMAGES_DIR = os.path.abspath(IMAGES_DIR)
PRODUCT_NOT_FOUND_ERROR = "Product not found"

if not os.path.exists(ABS_IMAGES_DIR):
    os.makedirs(ABS_IMAGES_DIR)

@router.post("/products/", response_model=Product)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await product_service.create_product(db, name, description, price, category_id, image, IMAGES_DIR)

@router.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_service.get_products(db, skip, limit)

@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=PRODUCT_NOT_FOUND_ERROR)
    return product

@router.patch("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    updated_product = await product_service.update_product(db, product_id, name, description, price, category_id, image, IMAGES_DIR)
    if updated_product is None:
        raise HTTPException(status_code=404, detail=PRODUCT_NOT_FOUND_ERROR)
    return updated_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not product_service.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail=PRODUCT_NOT_FOUND_ERROR)
    return {"ok": True}