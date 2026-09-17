from sqlalchemy import Column,BigInteger,String,Numeric,ForeignKey,DateTime,CheckConstraint
from database import Base


class Payment(Base):
    __tablename__ = "payments"
    id = Column(BigInteger,primary_key=True,index=True)
    order_id = Column(BigInteger,ForeignKey("orders.id"),nullable=False,index=True)
    amount = Column(Numeric(10, 2),nullable=False)
    payment_method = Column(String(30),nullable=False)
    status = Column(String(20),nullable=False,default="pending")
    transaction_id = Column(String(255),nullable=True,unique=True)
    paid_at = Column(DateTime(timezone=True),nullable=True)

    __table_args__ = (
        CheckConstraint(
            "amount >= 0",
            name="check_payment_amount"
        ),
    )