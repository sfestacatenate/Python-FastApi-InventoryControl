from sqlalchemy import inspect
from database.main import engine

def test_tables_exist():
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    
    assert "warehouses" in tables
    assert "products" in tables
    assert "customers" in tables
    assert "orders" in tables
    assert "order_items" in tables