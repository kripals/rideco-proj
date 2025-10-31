from typing import Dict, Set

from sqlalchemy.orm import Session, selectinload

from . import models

DEFAULT_DATA = {
    "Dairy": ["Milk", "Cheese", "Butter", "Yogurt"],
    "Bakery": ["Bread", "Bagels", "Croissants"],
    "Produce": ["Apples", "Bananas", "Carrots", "Tomatoes"],
    "Meat": ["Chicken", "Beef", "Fish"],
    "Pantry": ["Rice", "Pasta", "Flour", "Sugar", "Salt"],
    "Beverages": ["Tea", "Coffee", "Juice", "Water"],
}


def seed_item_types_and_items(db: Session) -> None:
    existing_types = (
        db.query(models.ItemType).options(selectinload(models.ItemType.items)).all()
    )
    type_by_name: Dict[str, models.ItemType] = {}
    items_by_type: Dict[str, Set[str]] = {}

    for item_type in existing_types:
        name = str(item_type.name)
        type_by_name[name] = item_type
        items_by_type[name] = {item.name for item in item_type.items}

    for type_name, items in DEFAULT_DATA.items():
        existing = type_by_name.get(type_name)
        if existing is None:
            new_item_type = models.ItemType(name=type_name)
            db.add(new_item_type)
            db.flush()  # Populate item_type.id for FK usage
            type_by_name[type_name] = new_item_type
            items_by_type[type_name] = set()
            item_type = new_item_type
        else:
            item_type = existing

        existing_items = items_by_type[type_name]
        for item_name in items:
            if item_name in existing_items:
                continue
            db.add(models.Item(name=item_name, item_type_id=item_type.id))
            existing_items.add(item_name)

    db.commit()
