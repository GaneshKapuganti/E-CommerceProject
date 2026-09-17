from pydantic import BaseModel, ConfigDict

class OrderCreate(BaseModel):
    user_id: int
    status: str = "pending"
    total_amount: float


class OrderStatusUpdate(BaseModel):
    status: str


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[OrderResponse]