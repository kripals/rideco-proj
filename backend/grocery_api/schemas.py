from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# --------------------------------------------------------------------
# ITEM TYPE
# --------------------------------------------------------------------
class ItemTypeBase(BaseModel):
    name: str


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemType(ItemTypeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------------------------------
# ITEM
# --------------------------------------------------------------------
class ItemBase(BaseModel):
    name: str
    item_type_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    created_at: datetime
    item_type: Optional[ItemType] = None

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------------------------------
# GROCERY ITEM
# --------------------------------------------------------------------
class GroceryItemBase(BaseModel):
    item_id: int
    quantity: int = 1
    purchased: bool = False


class GroceryItemCreate(GroceryItemBase):
    pass


class GroceryItem(GroceryItemBase):
    id: int
    grocery_id: int
    created_at: datetime
    item: Optional[Item] = None

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------------------------------
# GROCERY
# --------------------------------------------------------------------
class GroceryBase(BaseModel):
    family_id: int
    grocery_date: date


class GroceryCreate(GroceryBase):
    grocery_items: List[GroceryItemCreate] = Field(default_factory=list)


class GroceryUpdate(BaseModel):
    family_id: Optional[int] = None
    grocery_date: Optional[date] = None
    grocery_items: Optional[List[GroceryItemCreate]] = None


class Grocery(GroceryBase):
    id: int
    created_at: datetime
    grocery_items: List[GroceryItem] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
