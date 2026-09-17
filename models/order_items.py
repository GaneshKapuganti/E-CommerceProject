from sqlalchemy import Column,BigInteger,Numeric,ForeignKey,CheckConstraint
from database import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(BigInteger,primary_key=True,index=True)
    order_id = Column(BigInteger,ForeignKey("orders.id"),nullable=False,index=True)
    product_id = Column(BigInteger,ForeignKey("products.id"),nullable=False,index=True)
    quantity = Column(BigInteger,nullable=False)
    unit_price = Column(Numeric(10, 2),nullable=False)

    __table_args__ = (
        CheckConstraint(
            "quantity >= 1",
            name="check_order_item_quantity"
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="check_order_item_unit_price"
        ),
    )