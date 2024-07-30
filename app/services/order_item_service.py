from sqlalchemy.orm import Session
from .. import models, schemas
from ..exceptions import ErrorHandler

def get_order_item(db: Session, order_item_id: int):
    order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if order_item is None:
        raise ErrorHandler.not_found("Order item")
    return order_item

def get_order_items(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.OrderItem).offset(skip).limit(limit).all()
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def create_order_item(db: Session, order_item: schemas.OrderItemCreate, order_id: int):
    try:
        db_order_item = models.OrderItem(**order_item.model_dump(), order_id=order_id)
        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)
        return db_order_item
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def update_order_item(db: Session, order_item_id: int, order_item: schemas.OrderItemCreate):
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item is None:
        raise ErrorHandler.not_found("Order item")
    try:
        db_order_item.product_id = order_item.product_id
        db_order_item.quantity = order_item.quantity
        db.commit()
        db.refresh(db_order_item)
        return db_order_item
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def delete_order_item(db: Session, order_item_id: int):
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item is None:
        raise ErrorHandler.not_found("Order item")
    try:
        db.delete(db_order_item)
        db.commit()
        return db_order_item
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))