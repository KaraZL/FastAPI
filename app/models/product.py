from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)
    in_stock: bool
