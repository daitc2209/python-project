from pydantic import BaseModel

class Favor(BaseModel):
    user_id: str
    product_id: str