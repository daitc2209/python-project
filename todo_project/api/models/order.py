from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
class Order(BaseModel):
    user_id: str
    address_delivery: str
    code_order: str = Field(default=None)
    createdAt: datetime = Field(default=datetime.now())
    email: str
    name: str
    phone: str 
    state_checkout: int = Field(default=0)
    state_order: int = Field(default=0)
    amount: int
    note: str
    total_money: float