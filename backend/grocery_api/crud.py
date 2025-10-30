from sqlalchemy.orm import Session
from grocery_api import models, schemas

def get_items(db: Session):
    return db.query(models.GroceryItem).all()

def create_item(db: Session, item: schemas.GroceryCreate):
    db_item = models.GroceryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.GroceryCreate):
    db_item = db.query(models.GroceryItem).filter(models.GroceryItem.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.GroceryItem).filter(models.GroceryItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item