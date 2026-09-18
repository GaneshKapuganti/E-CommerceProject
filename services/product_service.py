from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import category as category_crud
from crud import product as product_crud
from models.product import Product
from schemas.product import ProductCreate, ProductPatch


def _ensure_category_exists(db: Session, category_id: int):
    if category_crud.get_by_id(db, category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")


def create_product(db: Session, product: ProductCreate) -> Product:
    _ensure_category_exists(db, product.category_id)

    return product_crud.create(
        db,
        product.category_id,
        product.name,
        product.description,
        product.price,
        product.stock_quantity,
    )


def list_products(
    db: Session,
    limit: int,
    offset: int,
    category_id: int | None,
    search: str | None,
    min_price: float | None,
    max_price: float | None,
) -> dict:
    total, items = product_crud.get_multi(
        db, limit, offset, category_id, search, min_price, max_price
    )
    return {"total": total, "limit": limit, "offset": offset, "items": items}


def get_product(db: Session, product_id: int) -> Product:
    product = product_crud.get_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def update_product(db: Session, product_id: int, data: ProductCreate) -> Product:
    product = get_product(db, product_id)
    _ensure_category_exists(db, data.category_id)

    return product_crud.update(
        db,
        product,
        data.category_id,
        data.name,
        data.description,
        data.price,
        data.stock_quantity,
    )


def patch_product(db: Session, product_id: int, data: ProductPatch) -> Product:
    product = get_product(db, product_id)

    category_id = data.category_id
    if category_id is not None:
        _ensure_category_exists(db, category_id)
    else:
        category_id = product.category_id

    return product_crud.update(
        db,
        product,
        category_id,
        data.name if data.name is not None else product.name,
        data.description if data.description is not None else product.description,
        data.price if data.price is not None else product.price,
        data.stock_quantity if data.stock_quantity is not None else product.stock_quantity,
    )


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    product_crud.delete(db, product)
