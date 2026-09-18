from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import order as order_crud
from models.order import Order
from schemas.order import OrderCreate, OrderStatusUpdate


def create_order(db: Session, order: OrderCreate) -> Order:
    return order_crud.create(db, order.user_id, order.status, order.total_amount)


def list_orders(
    db: Session,
    limit: int,
    offset: int,
    user_id: int | None,
    status: str | None,
) -> dict:
    total, items = order_crud.get_multi(db, limit, offset, user_id, status)
    return {"total": total, "limit": limit, "offset": offset, "items": items}


def get_order(db: Session, order_id: int) -> Order:
    order = order_crud.get_by_id(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def update_order_status(db: Session, order_id: int, data: OrderStatusUpdate) -> Order:
    order = get_order(db, order_id)
    return order_crud.update_status(db, order, data.status)
