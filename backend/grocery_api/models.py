from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class GroceryItem(Base):
    __tablename__ = "grocery_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    purchased = Column(Boolean, default=False)