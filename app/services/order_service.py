from sqlalchemy.orm import Session
from .. import models, schemas
from ..exceptions import ErrorHandler

def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise ErrorHandler.not_found("Order")
    return order

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Order).offset(skip).limit(limit).all()
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def create_order(db: Session, order: schemas.OrderCreate, customer_id: int):
    try:
        db_order = models.Order(**order.model_dump(), customer_id=customer_id)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise ErrorHandler.not_found("Order")
    try:
        db_order.order_date = order.order_date
        db_order.customer_id = order.customer_id
        db.commit()
        db.refresh(db_order)
        return db_order
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise ErrorHandler.not_found("Order")
    try:
        db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()

        db.delete(db_order)
        db.commit()
        return db_order
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))