from sqlalchemy.orm import Session
from sqlalchemy import select, update

from schemas import CategoryCreate
from models import Category

# En esta clase se define la lógica de negocio para las categorías, como crear, obtener, actualizar y eliminar categorías.
# Se utiliza SQLAlchemy para interactuar con la base de datos y Pydantic para validar los datos de entrada y salida.

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Category).offset(skip).limit(limit)).scalars().all()

def get_category(db: Session, category_id: int):
    return db.execute(select(Category).filter(Category.id == category_id)).scalars().first()

def update_category(db: Session, category_id: int, category: CategoryCreate):
    db_category = get_category(db, category_id)
    if db_category is None:
        return None
    update_data = category.model_dump(exclude_unset=True)
    if update_data:
        db.execute(update(Category).where(Category.id == category_id).values(**update_data))
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if category is None:
        return False
    db.delete(category)
    db.commit()
    return True