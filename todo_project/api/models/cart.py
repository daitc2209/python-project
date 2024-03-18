from pydantic import BaseModel

class Cart(BaseModel):
    user_id: str
    product_id: str
    amount: int