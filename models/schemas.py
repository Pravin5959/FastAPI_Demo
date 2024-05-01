from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    description: str
    price: int
    seller_id : int

class DisplaySeller(BaseModel):
    name: str
    email: str
    class Config:
        orm_mode = True

class DisplayProduct(BaseModel):
    name: str
    description: str
    seller : DisplaySeller
    class Config:
        orm_mode = True

class Seller(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : Optional[str] = None