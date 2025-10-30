from pydantic import BaseModel

class GroceryBase(BaseModel):
    name: str
    quantity: int
    purchased: bool = False

class GroceryCreate(GroceryBase):
    pass

class Grocery(GroceryBase):
    id: int
    class Config:
        orm_mode = True