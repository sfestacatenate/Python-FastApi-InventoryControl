# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.post("/warehouses/", response_model=schemas.Warehouse)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return crud.create_warehouse(db=db, warehouse=warehouse)

@app.get("/warehouses/", response_model=list[schemas.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    warehouses = crud.get_warehouses(db, skip=skip, limit=limit)
    return warehouses

# Aggiungi le altre rotte CRUD per Product, Customer, Order, OrderItem
