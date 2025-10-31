from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class ItemType(Base):
    __tablename__ = "item_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    items = relationship("Item", back_populates="item_type", lazy="selectin")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    item_type_id = Column(Integer, ForeignKey("item_types.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    item_type = relationship("ItemType", back_populates="items", lazy="selectin")
    grocery_items = relationship("GroceryItem", back_populates="item", lazy="selectin")


class Grocery(Base):
    __tablename__ = "groceries"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(
        Integer, nullable=False, default=1
    )  # Assuming family_id refers to a family entity, family table can be added later (default to 1 for now)
    grocery_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    grocery_items = relationship(
        "GroceryItem",
        back_populates="grocery",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class GroceryItem(Base):
    __tablename__ = "grocery_items"
    id = Column(Integer, primary_key=True, index=True)
    grocery_id = Column(
        Integer,
        ForeignKey("groceries.id", ondelete="CASCADE"),
        nullable=False,
    )
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    purchased = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    grocery = relationship("Grocery", back_populates="grocery_items", lazy="selectin")
    item = relationship("Item", back_populates="grocery_items", lazy="selectin")
