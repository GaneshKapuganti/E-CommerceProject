from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)

    products = relationship("Product", back_populates="category")
