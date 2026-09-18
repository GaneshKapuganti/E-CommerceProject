from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.order_items import OrderItemCreate, OrderItemResponse, OrderItemListResponse
from services import order_items_service


router = APIRouter(prefix="/api/v1/order-items", tags=["Order_Items"])


@router.post("", response_model=OrderItemResponse, status_code=201)
def create_order_item(item: OrderItemCreate, db: Session = Depends(get_db)):
    return order_items_service.create_order_item(db, item)


@router.get("", response_model=OrderItemListResponse)
def get_order_items(
    order_id: int | None = None,
    product_id: int | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return order_items_service.list_order_items(db, limit, offset, order_id, product_id)


@router.get("/{order_item_id}", response_model=OrderItemResponse)
def get_order_item(order_item_id: int, db: Session = Depends(get_db)):
    return order_items_service.get_order_item(db, order_item_id)


@router.delete("/{order_item_id}", status_code=204)
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    order_items_service.delete_order_item(db, order_item_id)
    return None
