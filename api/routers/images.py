import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from database import get_db
from services import image_service

from schemas import Image

router = APIRouter()
IMAGES_DIR = "imagenes/"
ABS_IMAGES_DIR = os.path.abspath(IMAGES_DIR)

if not os.path.exists(ABS_IMAGES_DIR):
    os.makedirs(ABS_IMAGES_DIR)

@router.post("/images/", response_model=Image)
async def create_image(
    image: UploadFile = File(...),
    product_id: int = Form(...),
    db: Session = Depends(get_db)
):
    return await image_service.create_image(db, image, product_id, IMAGES_DIR)

@router.get("/images/", response_model=List[Image])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return image_service.get_images(db, skip, limit)

@router.get("/images/{image_id}", response_model=Image)
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image(db, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@router.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    if not image_service.delete_image(db, image_id):
        raise HTTPException(status_code=404, detail="Image not found")
    return {"ok": True}