import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Customer
from app.schemas import OrderItemCreate, ProductCreate, OrderCreate
from app.services import order_item_service, product_service, order_service
from app.constants import SQLALCHEMY_DATABASE_TEST_URL

engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea il database temporaneo
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    """Crea una sessione di database per i test."""
    Session = TestingSessionLocal()
    try:
        yield Session
    finally:
        Session.close()

@pytest.fixture(scope="module")
def test_product(db):
    product_data = ProductCreate(name="Test Product", description="Test Description", price=10.0, quantity=100)
    product = product_service.create_product(db, product=product_data, warehouse_id=1)
    return product

@pytest.fixture(scope="module")
def test_order(db):
    customer = Customer(name="Test Customer", email="test@example.com", phone="1234567890")
    db.add(customer)
    db.commit()
    db.refresh(customer)
    order_data = OrderCreate(order_date="2023-01-01")
    order = order_service.create_order(db, order=order_data, customer_id=customer.id)
    return order

def test_create_order_item(db, test_order, test_product):
    order_item_data = OrderItemCreate(product_id=test_product.id, quantity=10)
    order_item = order_item_service.create_order_item(db, order_item=order_item_data, order_id=test_order.id)
    assert order_item.product_id == test_product.id
    assert order_item.quantity == 10

def test_get_order_items(db):
    order_items = order_item_service.get_order_items(db, skip=0, limit=10)
    assert len(order_items) > 0

def test_get_order_item(db):
    order_item = order_item_service.get_order_items(db, skip=0, limit=1)[0]
    retrieved_order_item = order_item_service.get_order_item(db, order_item_id=order_item.id)
    assert retrieved_order_item.id == order_item.id

def test_update_order_item(db):
    order_item = order_item_service.get_order_items(db, skip=0, limit=1)[0]
    update_data = OrderItemCreate(product_id=order_item.product_id, quantity=20)
    updated_order_item = order_item_service.update_order_item(db=db, order_item_id=order_item.id, order_item=update_data)
    assert updated_order_item.quantity == 20

def test_delete_order_item(db):
    order_item = order_item_service.get_order_items(db, skip=0, limit=1)[0]
    deleted_order_item = order_item_service.delete_order_item(db=db, order_item_id=order_item.id)
    assert deleted_order_item.id == order_item.id
    with pytest.raises(Exception):
        order_item_service.get_order_item(db, order_item_id=order_item.id)
