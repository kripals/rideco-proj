from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from grocery_api import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Grocery API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items", response_model=list[schemas.Grocery])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.post("/items", response_model=schemas.Grocery)
def create_item(item: schemas.GroceryCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.put("/items/{item_id}", response_model=schemas.Grocery)
def update_item(item_id: int, item: schemas.GroceryCreate, db: Session = Depends(get_db)):
    return crud.update_item(db, item_id, item)

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    crud.delete_item(db, item_id)
    return {"status": "deleted"}