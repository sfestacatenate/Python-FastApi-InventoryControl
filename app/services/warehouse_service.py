from sqlalchemy.orm import Session
from .. import models, schemas
from ..exceptions import ErrorHandler

def get_warehouse(db: Session, warehouse_id: int):
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise ErrorHandler.not_found("Warehouse")
    return warehouse

def get_warehouses(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Warehouse).offset(skip).limit(limit).all()
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    try:
        db_warehouse = models.Warehouse(name=warehouse.name, location=warehouse.location)
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def update_warehouse(db: Session, warehouse_id: int, warehouse: schemas.WarehouseCreate):
    db_warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if db_warehouse is None:
        raise ErrorHandler.not_found("Warehouse")
    try:
        db_warehouse.name = warehouse.name
        db_warehouse.location = warehouse.location
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def delete_warehouse(db: Session, warehouse_id: int):
    db_warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if db_warehouse is None:
        raise ErrorHandler.not_found("Warehouse")
    try:
        db.query(models.Product).filter(models.Product.warehouse_id == warehouse_id).delete()
        
        order_items_to_delete = db.query(models.OrderItem).join(models.Product).filter(models.Product.warehouse_id == warehouse_id).all()
        for order_item in order_items_to_delete:
            db.delete(order_item)

        orders_to_delete = db.query(models.Order).join(models.OrderItem).join(models.Product).filter(models.Product.warehouse_id == warehouse_id).all()
        for order in orders_to_delete:
            db.delete(order)

        db.delete(db_warehouse)
        db.commit()
        return db_warehouse
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))
