import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.main import SessionLocal, engine
from app import models

models.Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

warehouse1 = models.Warehouse(name="Main Warehouse", location="City Center")
warehouse2 = models.Warehouse(name="Secondary Warehouse", location="Uptown")

product1 = models.Product(name="Product A", description="Description A", price=10.0, quantity=100, warehouse=warehouse1)
product2 = models.Product(name="Product B", description="Description B", price=20.0, quantity=200, warehouse=warehouse2)

customer1 = models.Customer(name="Customer 1", email="customer1@example.com", phone="123456789")
customer2 = models.Customer(name="Customer 2", email="customer2@example.com", phone="987654321")

order1 = models.Order(order_date="2023-07-20", customer=customer1)
order_item1 = models.OrderItem(order=order1, product=product1, quantity=10)
order_item2 = models.OrderItem(order=order1, product=product2, quantity=5)

db.add(warehouse1)
db.add(warehouse2)
db.add(product1)
db.add(product2)
db.add(customer1)
db.add(customer2)
db.add(order1)
db.add(order_item1)
db.add(order_item2)

db.commit()
db.close()
