import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Customer
from app.schemas import Order, OrderCreate
from app.services import order_service
from app.constants import SQLALCHEMY_DATABASE_TEST_URL

engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
def test_customer(db):
    customer_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "1234567890"
    }
    customer = Customer(**customer_data)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def test_create_order(db, test_customer):
    order_data = OrderCreate(order_date="2023-01-01")
    order = order_service.create_order(db, order=order_data, customer_id=test_customer.id)
    assert order.order_date == "2023-01-01"
    assert order.customer_id == test_customer.id

def test_get_orders(db):
    orders = order_service.get_orders(db, skip=0, limit=10)
    assert len(orders) > 0

def test_get_order(db):
    order = order_service.get_orders(db, skip=0, limit=1)[0]
    retrieved_order = order_service.get_order(db, order_id=order.id)
    assert retrieved_order.id == order.id

def test_update_order(db):
    order = order_service.get_orders(db, skip=0, limit=1)[0]
    update_data = Order(id=order.id, order_date="2023-01-02", customer_id=order.customer_id)
    updated_order = order_service.update_order(db=db, order_id=order.id, order=update_data)
    assert updated_order.order_date == "2023-01-02"

def test_delete_order(db):
    order = order_service.get_orders(db, skip=0, limit=1)[0]
    deleted_order = order_service.delete_order(db=db, order_id=order.id)
    assert deleted_order.id == order.id
    with pytest.raises(Exception):
        order_service.get_order(db, order_id=order.id)
