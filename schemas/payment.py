from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    status: str = "pending"
    transaction_id: str | None = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: str
    transaction_id: str | None = None
    paid_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class PaymentListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[PaymentResponse]