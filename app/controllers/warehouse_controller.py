from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..services import warehouse_service as service
from database.main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Warehouse)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return service.create_warehouse(db=db, warehouse=warehouse)

@router.get("/", response_model=list[schemas.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.get_warehouses(db, skip=skip, limit=limit)

@router.get("/{warehouse_id}", response_model=schemas.Warehouse)
def read_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    return service.get_warehouse(db, warehouse_id)

@router.put("/{warehouse_id}", response_model=schemas.Warehouse)
def update_warehouse(warehouse_id: int, warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return service.update_warehouse(db=db, warehouse_id=warehouse_id, warehouse=warehouse)

@router.delete("/{warehouse_id}", response_model=schemas.Warehouse)
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    return service.delete_warehouse(db=db, warehouse_id=warehouse_id)