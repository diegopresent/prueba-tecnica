import os
import shutil
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from models import Product
from models import Image

async def create_product(db: Session, name: str, description: str, price: float, category_id: int, image: UploadFile, images_dir: str):
    db_product = Product(name=name, description=description, price=price, category_id=category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    image_path = os.path.join(images_dir, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    db_image = Image(image_url=image_path, product_id=db_product.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Product).offset(skip).limit(limit)).scalars().all()

def get_product(db: Session, product_id: int):
    return db.execute(select(Product).filter(Product.id == product_id)).scalars().first()

async def update_product(db: Session, product_id: int, name: Optional[str], description: Optional[str], price: Optional[float], category_id: Optional[int], image: Optional[UploadFile], images_dir: str):
    db_product = get_product(db, product_id)
    if db_product is None:
        return None

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
        db.execute(update(Product).where(Product.id == product_id).values(**update_data))
        db.commit()
        db.refresh(db_product)

    if image:
        image_path = os.path.join(images_dir, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        db_image = Image(image_url=image_path, product_id=product_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_product)

    return db_product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product is None:
        return False
    db.delete(product)
    db.commit()
    return True