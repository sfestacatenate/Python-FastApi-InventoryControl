from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..services import order_item_service as service
from database.main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, order_id: int, db: Session = Depends(get_db)):
    return service.create_order_item(db=db, order_item=order_item, order_id=order_id)

@router.get("/", response_model=list[schemas.OrderItem])
def read_order_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.get_order_items(db, skip=skip, limit=limit)

@router.get("/{order_item_id}", response_model=schemas.OrderItem)
def read_order_item(order_item_id: int, db: Session = Depends(get_db)):
    return service.get_order_item(db, order_item_id)

@router.put("/{order_item_id}", response_model=schemas.OrderItem)
def update_order_item(order_item_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return service.update_order_item(db=db, order_item_id=order_item_id, order_item=order_item)

@router.delete("/{order_item_id}", response_model=schemas.OrderItem)
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    return service.delete_order_item(db=db, order_item_id=order_item_id)