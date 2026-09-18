from fastapi import HTTPException
from sqlalchemy.orm import Session
from crud import category as category_crud
from models.category import Category
from schemas.category import CategoryCreate


def create_category(db: Session, category: CategoryCreate) -> Category:
    if category_crud.get_by_name(db, category.name):
        raise HTTPException(status_code=400, detail="Category already exists")
    return category_crud.create(db, category.name, category.description)


def list_categories(db: Session, limit: int, offset: int) -> dict:
    total, items = category_crud.get_multi(db, limit, offset)
    return {"total": total, "limit": limit, "offset": offset, "items": items}


def get_category(db: Session, category_id: int) -> Category:
    category = category_crud.get_by_id(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def update_category(db: Session, category_id: int, data: CategoryCreate) -> Category:
    category = get_category(db, category_id)
    return category_crud.update(db, category, data.name, data.description)


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    category_crud.delete(db, category)
