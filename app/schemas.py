from pydantic import BaseModel

class WarehouseBase(BaseModel):
    name: str
    location: str

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    warehouse_id: int
    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    order_date: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    customer_id: int
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    quantity: int

class OrderItemCreate(OrderItemBase):
    product_id: int

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product_id: int
    class Config:
        orm_mode = True
