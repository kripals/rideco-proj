from typing import cast

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from grocery_api import models, schemas


def _model_dump(schema_obj, **kwargs):
    """Support Pydantic v1/v2 by checking available dump method."""
    if hasattr(schema_obj, "model_dump"):
        return schema_obj.model_dump(**kwargs)
    return schema_obj.dict(**kwargs)


# --------------------------------------------------------------------
# ITEM TYPES
# --------------------------------------------------------------------
def get_item_types(db: Session, skip: int = 0, limit: int = 50):
    return (
        db.query(models.ItemType)
        .options(selectinload(models.ItemType.items))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_item_type(db: Session, item_type: schemas.ItemTypeCreate):
    db_item_type = models.ItemType(**_model_dump(item_type))
    db.add(db_item_type)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_item_type)
    return db_item_type


# --------------------------------------------------------------------
# ITEMS
# --------------------------------------------------------------------
def get_items(db: Session, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Item)
        .options(selectinload(models.Item.item_type))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_item(db: Session, item: schemas.ItemCreate):
    item_type_exists = (
        db.query(models.ItemType)
        .filter(models.ItemType.id == item.item_type_id)
        .first()
    )
    if not item_type_exists:
        raise ValueError(f"Unknown item type id={item.item_type_id}")
    db_item = models.Item(**_model_dump(item))
    db.add(db_item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_item)
    return db_item


# --------------------------------------------------------------------
# GROCERIES
# --------------------------------------------------------------------
def get_groceries(db: Session, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Grocery)
        .options(
            selectinload(models.Grocery.grocery_items).selectinload(
                models.GroceryItem.item
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_grocery_by_id(db: Session, grocery_id: int):
    return (
        db.query(models.Grocery)
        .options(
            selectinload(models.Grocery.grocery_items).selectinload(
                models.GroceryItem.item
            )
        )
        .filter(models.Grocery.id == grocery_id)
        .first()
    )


def create_grocery(db: Session, grocery: schemas.GroceryCreate):
    db_grocery = models.Grocery(
        family_id=grocery.family_id,
        grocery_date=grocery.grocery_date,
    )
    if grocery.grocery_items:
        db_grocery.grocery_items = [
            models.GroceryItem(
                item_id=item.item_id,
                quantity=item.quantity,
                purchased=item.purchased,
            )
            for item in grocery.grocery_items
        ]
    db.add(db_grocery)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_grocery)
    grocery_id_int = cast(int, db_grocery.id)
    return get_grocery_by_id(db, grocery_id_int)


def update_grocery(db: Session, grocery_id: int, grocery: schemas.GroceryUpdate):
    db_grocery = (
        db.query(models.Grocery).filter(models.Grocery.id == grocery_id).first()
    )
    if not db_grocery:
        return None

    update_data = _model_dump(
        grocery,
        exclude_unset=True,
        exclude={"grocery_items"},
    )
    for key, value in update_data.items():
        setattr(db_grocery, key, value)
    db.commit()
    db.refresh(db_grocery)
    grocery_id_int = cast(int, db_grocery.id)
    return get_grocery_by_id(db, grocery_id_int)


def delete_grocery(db: Session, grocery_id: int):
    db_grocery = (
        db.query(models.Grocery).filter(models.Grocery.id == grocery_id).first()
    )
    if db_grocery:
        db.delete(db_grocery)
        db.commit()
    return db_grocery


# --------------------------------------------------------------------
# GROCERY ITEMS
# --------------------------------------------------------------------
def get_grocery_items(db: Session, skip: int = 0, limit: int = 50):
    return (
        db.query(models.GroceryItem)
        .options(selectinload(models.GroceryItem.item))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_grocery_items_by_grocery(
    db: Session, grocery_id: int, skip: int = 0, limit: int = 50
):
    return (
        db.query(models.GroceryItem)
        .options(selectinload(models.GroceryItem.item))
        .filter(models.GroceryItem.grocery_id == grocery_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_grocery_item(db: Session, grocery_id: int, item: schemas.GroceryItemCreate):
    grocery_exists = (
        db.query(models.Grocery).filter(models.Grocery.id == grocery_id).first()
    )
    if not grocery_exists:
        raise ValueError("Invalid grocery or item reference.")

    item_exists = db.query(models.Item).filter(models.Item.id == item.item_id).first()
    if not item_exists:
        raise ValueError("Invalid grocery or item reference.")

    db_item = models.GroceryItem(
        grocery_id=grocery_id,
        item_id=item.item_id,
        quantity=item.quantity,
        purchased=item.purchased,
    )
    db.add(db_item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_item)
    return db_item


def update_grocery_item(
    db: Session, grocery_item_id: int, item: schemas.GroceryItemUpdate
):
    db_item = (
        db.query(models.GroceryItem)
        .filter(models.GroceryItem.id == grocery_item_id)
        .first()
    )
    if not db_item:
        return None
    for key, value in _model_dump(item, exclude_unset=True).items():
        setattr(db_item, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_item)
    return db_item


def delete_grocery_item(db: Session, grocery_item_id: int):
    db_item = (
        db.query(models.GroceryItem)
        .filter(models.GroceryItem.id == grocery_item_id)
        .first()
    )
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
