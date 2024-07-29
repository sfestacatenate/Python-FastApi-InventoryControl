from sqlalchemy.orm import Session
from .. import models, schemas
from ..exceptions import ErrorHandler

def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise ErrorHandler.not_found("Product")
    return product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Product).offset(skip).limit(limit).all()
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def create_product(db: Session, product: schemas.ProductCreate, warehouse_id: int):
    try:
        db_product = models.Product(**product.dict(), warehouse_id=warehouse_id)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise ErrorHandler.not_found("Product")
    try:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise ErrorHandler.not_found("Product")
    try:
        db.query(models.OrderItem).filter(models.OrderItem.product_id == product_id).delete()

        orders_to_delete = db.query(models.Order).join(models.OrderItem).filter(models.OrderItem.product_id == product_id).all()
        for order in orders_to_delete:
            db.delete(order)

        db.delete(db_product)
        db.commit()
        return db_product
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))