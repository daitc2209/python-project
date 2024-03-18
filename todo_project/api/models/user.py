from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str 
    password: str
    email: EmailStr
    role: str = Field(default="user")
    name: Optional[str]
    address: str
    createdAt: datetime = Field(default=datetime.now())