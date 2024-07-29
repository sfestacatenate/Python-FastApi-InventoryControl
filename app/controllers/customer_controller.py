from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..services import customer_service as service
from database.main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return service.create_customer(db=db, customer=customer)

@router.get("/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.get_customers(db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    return service.get_customer(db, customer_id)

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return service.update_customer(db=db, customer_id=customer_id, customer=customer)

@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return service.delete_customer(db=db, customer_id=customer_id)
