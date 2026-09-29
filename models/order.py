from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from models.enums import OrderStatus

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.pending)
    total_amount = Column(Float , nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")


