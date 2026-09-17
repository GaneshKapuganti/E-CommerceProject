from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from models.category import Category
from schemas.product import ProductCreate,ProductPatch,ProductResponse,ProductListResponse


router = APIRouter(prefix="/api/v1/products",tags=["Products"])

@router.post("",response_model=ProductResponse,status_code=201)
def create_product(product: ProductCreate,db: Session = Depends(get_db)):
    category = (db.query(Category).filter(Category.id == product.category_id).first())
    if category is None:
        raise HTTPException(status_code=404,detail="Category not found")
    new_product = Product(
        category_id=product.category_id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("",response_model=ProductListResponse)
def get_products(
    category_id: int | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):

    query = db.query(Product)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    if search is not None:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    total = query.count()
    products = (query.offset(offset).limit(limit).all())
    return {"total": total,"limit": limit,"offset": offset,"items": products}

@router.get("/{product_id}",response_model=ProductResponse)
def get_product(product_id: int,db: Session = Depends(get_db)):
    product = (db.query(Product).filter(Product.id == product_id).first())
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return product

@router.put("/{product_id}",response_model=ProductResponse)
def update_product(product_id: int,product_data: ProductCreate,db: Session = Depends(get_db)):
    product = (db.query(Product).filter(Product.id == product_id).first())
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    category = (db.query(Category).filter(Category.id == product_data.category_id).first())
    if category is None:
        raise HTTPException(status_code=404,detail="Category not found")
    product.category_id = product_data.category_id
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock_quantity = product_data.stock_quantity
    db.commit()
    db.refresh(product)
    return product

@router.patch("/{product_id}",response_model=ProductResponse)
def patch_product(product_id: int,product_data: ProductPatch,db: Session = Depends(get_db)):
    product = (db.query(Product).filter(Product.id == product_id)        .first())
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    if product_data.category_id is not None:
        category = (db.query(Category).filter(Category.id == product_data.category_id).first())
        if category is None:
            raise HTTPException(status_code=404,detail="Category not found")
        product.category_id = product_data.category_id
    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.stock_quantity is not None:
        product.stock_quantity = product_data.stock_quantity
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}",status_code=204)
def delete_product(product_id: int,db: Session = Depends(get_db)):
    product = (db.query(Product).filter(Product.id == product_id).first())
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    db.delete(product)
    db.commit()
    return None