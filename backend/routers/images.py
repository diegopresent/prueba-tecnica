import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import select

import models, schemas
from database import get_db

router = APIRouter()
IMAGES_DIR = "imagenes/"
ABS_IMAGES_DIR = os.path.abspath(IMAGES_DIR)

if not os.path.exists(ABS_IMAGES_DIR):
    os.makedirs(ABS_IMAGES_DIR)

@router.post("/images/", response_model=schemas.Image)
async def create_image(
    image: UploadFile = File(...),
    product_id: int = Form(...),
    db: Session = Depends(get_db)
):
    image_path = os.path.join(IMAGES_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    db_image = models.Image(image_url=image_path, product_id=product_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@router.get("/images/", response_model=List[schemas.Image])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = db.execute(select(models.Image).offset(skip).limit(limit)).scalars().all()
    return images

@router.get("/images/{image_id}", response_model=schemas.Image)
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = db.execute(select(models.Image).filter(models.Image.id == image_id)).scalars().first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@router.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.execute(select(models.Image).filter(models.Image.id == image_id)).scalars().first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
    return {"ok": True}