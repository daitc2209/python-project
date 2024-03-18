from pydantic import BaseModel, Field

class Order_details(BaseModel):
    order_id: str
    product_id: str
    amount:int
    discount: float = Field(default=0)
    price:float
    total:float