from collections import defaultdict

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


def seed_item_types_and_items(db: Session):
    existing_types = (
        db.query(models.ItemType).options(selectinload(models.ItemType.items)).all()
    )
    type_by_name = {item_type.name: item_type for item_type in existing_types}
    items_by_type = defaultdict(
        set,
        {
            item_type.name: {item.name for item in item_type.items}
            for item_type in existing_types
        },
    )

    for type_name, items in DEFAULT_DATA.items():
        item_type = type_by_name.get(type_name)
        if item_type is None:
            item_type = models.ItemType(name=type_name)
            db.add(item_type)
            db.flush()  # Populate item_type.id for FK usage
            type_by_name[type_name] = item_type
            items_by_type[type_name] = set()

        existing_items = items_by_type[type_name]
        for item_name in items:
            if item_name in existing_items:
                continue
            db.add(models.Item(name=item_name, item_type_id=item_type.id))

    db.commit()
