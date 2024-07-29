from sqlalchemy.orm import Session
from . import models, schemas
from .exceptions import ErrorHandler

# Warehouse CRUD
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

# Product CRUD
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
        db.delete(db_product)
        db.commit()
        return db_product
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

# Customer CRUD
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

# Order CRUD
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
        db_order = models.Order(**order.dict(), customer_id=customer_id)
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
        db.delete(db_order)
        db.commit()
        return db_order
    except Exception as e:
        raise ErrorHandler.internal_error(str(e))

# OrderItem CRUD
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
        db_order_item = models.OrderItem(**order_item.dict(), order_id=order_id)
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
