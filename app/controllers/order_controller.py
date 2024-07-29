from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from database.main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, customer_id: int, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order, customer_id=customer_id)

@router.get("/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id)

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.update_order(db=db, order_id=order_id, order=order)

@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return crud.delete_order(db=db, order_id=order_id)