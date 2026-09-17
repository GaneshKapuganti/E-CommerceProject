from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    model_config = ConfigDict(from_attributes=True)

class OrderItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[OrderItemResponse]