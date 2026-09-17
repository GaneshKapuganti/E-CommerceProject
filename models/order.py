from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(20) , nullable=False)
    total_amount = Column(Float , nullable=False)


