from sqlalchemy.orm import Session
from . import models, schemas

# Warehouse CRUD
def get_warehouse(db: Session, warehouse_id: int):
    return db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()

def get_warehouses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()

def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    db_warehouse = models.Warehouse(name=warehouse.name, location=warehouse.location)
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def update_warehouse(db: Session, warehouse_id: int, warehouse: schemas.WarehouseCreate):
    db_warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if db_warehouse:
        db_warehouse.name = warehouse.name
        db_warehouse.location = warehouse.location
        db.commit()
        db.refresh(db_warehouse)
    return db_warehouse

def delete_warehouse(db: Session, warehouse_id: int):
    db_warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if db_warehouse:
        db.delete(db_warehouse)
        db.commit()
    return db_warehouse

# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate, warehouse_id: int):
    db_product = models.Product(**product.dict(), warehouse_id=warehouse_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Customer CRUD
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        db_customer.name = customer.name
        db_customer.email = customer.email
        db_customer.phone = customer.phone
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# Order CRUD
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate, customer_id: int):
    db_order = models.Order(**order.dict(), customer_id=customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.order_date = order.order_date
        db_order.customer_id = order.customer_id
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

# OrderItem CRUD
def get_order_item(db: Session, order_item_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()

def get_order_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.OrderItem).offset(skip).limit(limit).all()

def create_order_item(db: Session, order_item: schemas.OrderItemCreate, order_id: int):
    db_order_item = models.OrderItem(**order_item.dict(), order_id=order_id)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def update_order_item(db: Session, order_item_id: int, order_item: schemas.OrderItemCreate):
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item:
        db_order_item.product_id = order_item.product_id
        db_order_item.quantity = order_item.quantity
        db.commit()
        db.refresh(db_order_item)
    return db_order_item

def delete_order_item(db: Session, order_item_id: int):
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item:
        db.delete(db_order_item)
        db.commit()
    return db_order_item
