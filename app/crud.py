# crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    db_warehouse = models.Warehouse(name=warehouse.name, location=warehouse.location)
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def get_warehouses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()

# Aggiungi funzioni CRUD per Product, Customer, Order, OrderItem
