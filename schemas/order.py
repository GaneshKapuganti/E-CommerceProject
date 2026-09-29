from pydantic import BaseModel, ConfigDict

from models.enums import OrderStatus

class OrderCreate(BaseModel):
    user_id: int
    status: OrderStatus = OrderStatus.pending
    total_amount: float


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[OrderResponse]