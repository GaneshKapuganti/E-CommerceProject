from sqlalchemy import Column,BigInteger,String,Text,Numeric,ForeignKey,CheckConstraint
from sqlalchemy.orm import relationship


from database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(BigInteger,primary_key=True,index=True)
    category_id = Column(BigInteger,ForeignKey("categories.id"),nullable=False,index=True)
    name = Column(String(150),nullable=False)
    description = Column(Text,nullable=True)
    price = Column(Numeric(10, 2),nullable=False)
    stock_quantity = Column(BigInteger,nullable=False)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="check_product_price"
        ),
        CheckConstraint(
            "stock_quantity >= 0",
            name="check_product_stock"
        ),
    )