import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.schemas import CustomerCreate
from app.services import customer_service
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

def test_create_customer(db):
    customer_data = CustomerCreate(name="Test Customer", email="test1@example.com", phone="1234567890")
    customer = customer_service.create_customer(db, customer=customer_data)
    assert customer.name == "Test Customer"
    assert customer.email == "test1@example.com"
    assert customer.phone == "1234567890"

def test_get_customers(db):
    customers = customer_service.get_customers(db, skip=0, limit=10)
    assert len(customers) > 0

def test_get_customer(db):
    customer = customer_service.get_customers(db, skip=0, limit=1)[0]
    retrieved_customer = customer_service.get_customer(db, customer_id=customer.id)
    assert retrieved_customer.id == customer.id

def test_update_customer(db):
    customer = customer_service.get_customers(db, skip=0, limit=1)[0]
    update_data = CustomerCreate(name="Updated Customer", email="updated@example.com", phone="0987654321")
    updated_customer = customer_service.update_customer(db=db, customer_id=customer.id, customer=update_data)
    assert updated_customer.name == "Updated Customer"
    assert updated_customer.email == "updated@example.com"
    assert updated_customer.phone == "0987654321"

def test_delete_customer(db):
    customer = customer_service.get_customers(db, skip=0, limit=1)[0]
    deleted_customer = customer_service.delete_customer(db=db, customer_id=customer.id)
    assert deleted_customer.id == customer.id
    with pytest.raises(Exception):
        customer_service.get_customer(db, customer_id=customer.id)
