from pydantic import BaseModel
from datetime import datetime 

class UserBase(BaseModel):
    username: str 
    email: str 

class UserCreate(UserBase):
    password: str 

class User(UserBase):
    #create_at: datetime

    class Config: 
        from_attributes = True 

