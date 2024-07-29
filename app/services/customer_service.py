from sqlalchemy.orm import Session
from .. import models, schemas
from ..exceptions import ErrorHandler

def get_customer(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is None:
        raise ErrorHandler.not_found("Customer")
    return customer

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Customer).offset(skip).limit(limit).all()
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def create_customer(db: Session, customer: schemas.CustomerCreate):
    try:
        db_customer = models.Customer(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise ErrorHandler.not_found("Customer")
    try:
        db_customer.name = customer.name
        db_customer.email = customer.email
        db_customer.phone = customer.phone
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise ErrorHandler.not_found("Customer")
    try:
        db.delete(db_customer)
        db.commit()
        return db_customer
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))
