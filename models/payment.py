from sqlalchemy import Column,BigInteger,String,Numeric,ForeignKey,DateTime,CheckConstraint,Enum
from sqlalchemy.orm import relationship
from database import Base
from models.enums import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"
    id = Column(BigInteger,primary_key=True,index=True)
    order_id = Column(BigInteger,ForeignKey("orders.id"),nullable=False,index=True)
    amount = Column(Numeric(10, 2),nullable=False)
    payment_method = Column(String(30),nullable=False)
    status = Column(Enum(PaymentStatus, name="payment_status"),nullable=False,default=PaymentStatus.pending)
    transaction_id = Column(String(255),nullable=True,unique=True)
    paid_at = Column(DateTime(timezone=True),nullable=True)

    order = relationship("Order", back_populates="payments")

    __table_args__ = (
        CheckConstraint(
            "amount >= 0",
            name="check_payment_amount"
        ),
    )