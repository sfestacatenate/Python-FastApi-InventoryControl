import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Warehouse
from app.schemas import ProductCreate
from app.services import product_service
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
def test_warehouse(db):
    warehouse = Warehouse(name="Test Warehouse", location="Test Location")
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse

def test_create_product(db, test_warehouse):
    product_data = ProductCreate(name="Test Product", description="Test Description", price=10.0, quantity=100)
    product = product_service.create_product(db, product=product_data, warehouse_id=test_warehouse.id)
    assert product.name == "Test Product"
    assert product.description == "Test Description"

def test_get_products(db):
    products = product_service.get_products(db, skip=0, limit=10)
    assert len(products) > 0

def test_get_product(db):
    product = product_service.get_products(db, skip=0, limit=1)[0]
    retrieved_product = product_service.get_product(db, product_id=product.id)
    assert retrieved_product.id == product.id

def test_update_product(db):
    product = product_service.get_products(db, skip=0, limit=1)[0]
    update_data = ProductCreate(name="Updated Product", description="Updated Description", price=20.0, quantity=200)
    updated_product = product_service.update_product(db, product_id=product.id, product=update_data)
    assert updated_product.name == "Updated Product"
    assert updated_product.description == "Updated Description"

def test_delete_product(db):
    product = product_service.get_products(db, skip=0, limit=1)[0]
    deleted_product = product_service.delete_product(db, product_id=product.id)
    assert deleted_product.id == product.id
    with pytest.raises(Exception):
        product_service.get_product(db, product_id=product.id)
