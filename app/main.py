from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from database.main import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, warehouse_id: int, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product, warehouse_id=warehouse_id)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, customer_id: int, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order, customer_id=customer_id)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.post("/order_items/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, order_id: int, db: Session = Depends(get_db)):
    return crud.create_order_item(db=db, order_item=order_item, order_id=order_id)

@app.get("/order_items/", response_model=list[schemas.OrderItem])
def read_order_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    order_items = crud.get_order_items(db, skip=skip, limit=limit)
    return order_items
