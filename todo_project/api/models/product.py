
from typing import Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str]
    img: str
    discount: float = Field(default=0)
    quantity: int
    brand: str
    category: str
