from pydantic import BaseModel, Field
from typing import Optional

class OrderCreate(BaseModel):
    product_name: str
    price: float
    internal_note: str

class OrderResponse(BaseModel):
    product_name: str
    price: float