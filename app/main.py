from fastapi import FastAPI
from database.main import engine
from . import models
from .controllers import warehouse_controller, product_controller, customer_controller, order_controller, order_item_controller

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(warehouse_controller.router, prefix="/warehouses", tags=["warehouses"])
app.include_router(product_controller.router, prefix="/products", tags=["products"])
app.include_router(customer_controller.router, prefix="/customers", tags=["customers"])
app.include_router(order_controller.router, prefix="/orders", tags=["orders"])
app.include_router(order_item_controller.router, prefix="/order_items", tags=["order_items"])
