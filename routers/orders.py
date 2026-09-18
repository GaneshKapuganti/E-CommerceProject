from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate, OrderListResponse
from services import order_service


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)


@router.get("", response_model=OrderListResponse)
def get_orders(
    user_id: int | None = None,
    status: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return order_service.list_orders(db, limit, offset, user_id, status)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(db, order_id)


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order_status(order_id: int, order_data: OrderStatusUpdate, db: Session = Depends(get_db)):
    return order_service.update_order_status(db, order_id, order_data)
