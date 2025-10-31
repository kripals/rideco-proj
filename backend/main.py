import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

load_dotenv()

from grocery_api import crud, database, models, schemas
from grocery_api.seed import seed_item_types_and_items


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    with database.SessionLocal() as db:
        seed_item_types_and_items(db)
    yield


# --------------------------------------------------------------------
# APP INITIALIZATION
# --------------------------------------------------------------------
app = FastAPI(
    title="Grocery API",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,   # hides Schemas section
        "docExpansion": "none",            # collapse all endpoints by default
        "displayRequestDuration": True,    # show timing info
        "filter": True                     # adds a search bar
    },
)
api_v1 = APIRouter(prefix="/api/v1")

# Enable CORS for frontend access (restricted for production)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency for DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------------------------
# GLOBAL ERROR HANDLER
# --------------------------------------------------------------------
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "detail": "Internal Server Error"},
        )


# --------------------------------------------------------------------
# ROOT
# --------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Grocery API is running"}


# --------------------------------------------------------------------
# ITEM TYPES
# --------------------------------------------------------------------
@api_v1.get("/item_types", response_model=list[schemas.ItemType], tags=["Item Types"])
def read_item_types(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    item_types = crud.get_item_types(db)
    return item_types[skip : skip + limit]


@api_v1.post("/item_types", response_model=schemas.ItemType, tags=["Item Types"])
def create_item_type(item_type: schemas.ItemTypeCreate, db: Session = Depends(get_db)):
    return crud.create_item_type(db, item_type)


# --------------------------------------------------------------------
# ITEMS
# --------------------------------------------------------------------
@api_v1.get("/items", response_model=list[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return items[skip : skip + limit]


@api_v1.post("/items", response_model=schemas.Item, tags=["Items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)


# --------------------------------------------------------------------
# GROCERIES
# --------------------------------------------------------------------
@api_v1.get("/groceries", response_model=list[schemas.Grocery], tags=["Groceries"])
def read_groceries(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    groceries = crud.get_groceries(db)
    return groceries[skip : skip + limit]


@api_v1.get("/groceries/{grocery_id}", response_model=schemas.Grocery, tags=["Groceries"])
def read_grocery(grocery_id: int, db: Session = Depends(get_db)):
    grocery = crud.get_grocery_by_id(db, grocery_id)
    if not grocery:
        raise HTTPException(status_code=404, detail="Grocery not found")
    return grocery


@api_v1.post("/groceries", response_model=schemas.Grocery, tags=["Groceries"])
def create_grocery(grocery: schemas.GroceryCreate, db: Session = Depends(get_db)):
    return crud.create_grocery(db, grocery)


@api_v1.put("/groceries/{grocery_id}", response_model=schemas.Grocery, tags=["Groceries"])
def update_grocery(
    grocery_id: int, grocery: schemas.GroceryUpdate, db: Session = Depends(get_db)
):
    updated = crud.update_grocery(db, grocery_id, grocery)
    if not updated:
        raise HTTPException(status_code=404, detail="Grocery not found")
    return updated


@api_v1.delete("/groceries/{grocery_id}", tags=["Groceries"])
def delete_grocery(grocery_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_grocery(db, grocery_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Grocery not found")
    return {"status": "deleted"}


# --------------------------------------------------------------------
# GROCERY ITEMS
# --------------------------------------------------------------------
@api_v1.get("/grocery_items", response_model=list[schemas.GroceryItem], tags=["Grocery Items"])
def read_grocery_items(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    items = crud.get_grocery_items(db)
    return items[skip : skip + limit]


@api_v1.get(
    "/groceries/{grocery_id}/items",
    response_model=list[schemas.GroceryItem],
    tags=["Grocery Items"],
)
def read_grocery_items_by_grocery(grocery_id: int, db: Session = Depends(get_db)):
    return crud.get_grocery_items_by_grocery(db, grocery_id)


@api_v1.post(
    "/groceries/{grocery_id}/items",
    response_model=schemas.GroceryItem,
    tags=["Grocery Items"],
)
def create_grocery_item(
    grocery_id: int, item: schemas.GroceryItemCreate, db: Session = Depends(get_db)
):
    return crud.create_grocery_item(db, grocery_id, item)


@api_v1.put(
    "/grocery_items/{grocery_item_id}",
    response_model=schemas.GroceryItem,
    tags=["Grocery Items"],
)
def update_grocery_item(
    grocery_item_id: int, item: schemas.GroceryItemCreate, db: Session = Depends(get_db)
):
    updated = crud.update_grocery_item(db, grocery_item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Grocery item not found")
    return updated


@api_v1.delete("/grocery_items/{grocery_item_id}", tags=["Grocery Items"])
def delete_grocery_item(grocery_item_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_grocery_item(db, grocery_item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Grocery item not found")
    return {"status": "deleted"}


app.include_router(api_v1)
