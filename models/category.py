from sqlalchemy import Column, Integer, String, Float, Text
from database import Base




class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String , nullable=False)
    description = Column(Text)
