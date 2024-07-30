import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.schemas import WarehouseCreate
from app.services import warehouse_service
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

def test_create_warehouse(db):
    warehouse_data = WarehouseCreate(name="Test Warehouse", location="Test Location")
    warehouse = warehouse_service.create_warehouse(db, warehouse=warehouse_data)
    assert warehouse.name == "Test Warehouse"
    assert warehouse.location == "Test Location"

def test_get_warehouses(db):
    warehouses = warehouse_service.get_warehouses(db, skip=0, limit=10)
    assert len(warehouses) > 0

def test_get_warehouse(db):
    warehouse = warehouse_service.get_warehouses(db, skip=0, limit=1)[0]
    retrieved_warehouse = warehouse_service.get_warehouse(db, warehouse_id=warehouse.id)
    assert retrieved_warehouse.id == warehouse.id

def test_update_warehouse(db):
    warehouse = warehouse_service.get_warehouses(db, skip=0, limit=1)[0]
    update_data = WarehouseCreate(name="Updated Warehouse", location="Updated Location")
    updated_warehouse = warehouse_service.update_warehouse(db, warehouse_id=warehouse.id, warehouse=update_data)
    assert updated_warehouse.name == "Updated Warehouse"
    assert updated_warehouse.location == "Updated Location"

def test_delete_warehouse(db):
    warehouse = warehouse_service.get_warehouses(db, skip=0, limit=1)[0]
    deleted_warehouse = warehouse_service.delete_warehouse(db, warehouse_id=warehouse.id)
    assert deleted_warehouse.id == warehouse.id
    with pytest.raises(Exception):
        warehouse_service.get_warehouse(db, warehouse_id=warehouse.id)