import os
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Image

async def create_image(db: Session, image: UploadFile, product_id: int, images_dir: str):
    image_path = os.path.join(images_dir, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    db_image = Image(image_url=image_path, product_id=product_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Image).offset(skip).limit(limit)).scalars().all()

def get_image(db: Session, image_id: int):
    return db.execute(select(Image).filter(Image.id == image_id)).scalars().first()

def delete_image(db: Session, image_id: int):
    image = get_image(db, image_id)
    if image is None:
        return False
    db.delete(image)
    db.commit()
    return True