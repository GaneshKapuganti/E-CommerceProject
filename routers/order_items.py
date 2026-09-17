from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.order_items import OrderItem
from models.order import Order
from models.product import Product
from schemas.order_items import OrderItemCreate,OrderItemResponse,OrderItemListResponse

router = APIRouter(prefix="/api/v1/order-items",tags=["Order_Items"])


# CREATE ORDER ITEM
@router.post("",response_model=OrderItemResponse,status_code=201)
def create_order_item(item: OrderItemCreate,db: Session = Depends(get_db)):
    order = (db.query(Order).filter(Order.id == item.order_id).first())
    if order is None:
        raise HTTPException(status_code=404,detail="Order not found")
    product = (db.query(Product).filter(Product.id == item.product_id).first())
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    new_item = OrderItem(order_id=item.order_id,product_id=item.product_id,quantity=item.quantity,unit_price=item.unit_price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("",response_model=OrderItemListResponse)
def get_order_items(order_id: int | None = None,product_id: int | None = None,limit: int = Query(20, ge=1, le=100),offset: int = Query(0, ge=0),db: Session = Depends(get_db)):
    query = db.query(OrderItem)
    if order_id is not None:
        query = query.filter(OrderItem.order_id == order_id)
    if product_id is not None:
        query = query.filter(OrderItem.product_id == product_id)
    total = query.count()
    items = (query.offset(offset).limit(limit).all())
    return {"total": total,"limit": limit,"offset": offset,"items": items}

@router.get("/{order_item_id}",response_model=OrderItemResponse)
def get_order_item(order_item_id: int,db: Session = Depends(get_db)):
    item = (db.query(OrderItem).filter(OrderItem.id == order_item_id).first())
    if item is None:
        raise HTTPException(status_code=404,detail="Order item not found")
    return item

@router.delete("/{order_item_id}",status_code=204)
def delete_order_item(order_item_id: int,db: Session = Depends(get_db)):
    item = (db.query(OrderItem).filter(OrderItem.id == order_item_id).first())
    if item is None:
        raise HTTPException(status_code=404,detail="Order item not found")
    db.delete(item)
    db.commit()
    return None