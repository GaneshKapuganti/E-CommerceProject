from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.order import Order
from schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
    OrderListResponse
)


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)


# CREATE ORDER
@router.post(
    "",
    response_model=OrderResponse,
    status_code=201
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    new_order = Order(
        user_id=order.user_id,
        status=order.status,
        total_amount=order.total_amount
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


# GET ALL ORDERS
@router.get(
    "",
    response_model=OrderListResponse
)
def get_orders(
    user_id: int | None = None,
    status: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Order)

    if user_id is not None:
        query = query.filter(Order.user_id == user_id)

    if status is not None:
        query = query.filter(Order.status == status)

    total = query.count()

    orders = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": orders
    }


# GET ORDER BY ID
@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# UPDATE ORDER STATUS
@router.patch(
    "/{order_id}",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    order_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = order_data.status

    db.commit()
    db.refresh(order)

    return order