from pydantic import BaseModel, EmailStr, Field, validator
import datetime
import re
from typing import Optional, List
import uuid

class UserBase(BaseModel):
    cpf: str
    name: str
    birth_date: datetime.date
    email: EmailStr

    @validator('cpf')
    def validate_cpf(cls, v):
        if not re.match(r'^\d{11}$', v):
            raise ValueError('CPF must be exactly 11 digits')
        return v

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    is_admin: bool

    class Config:
        from_attributes = True

class DebtBase(BaseModel):
    amount: float = Field(gt=0)
    due_date: datetime.date
    owner_cpf: str

class DebtCreate(DebtBase):
    pass

class DebtResponse(DebtBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    cpf: Optional[str] = None
    is_admin: Optional[bool] = False

class Login(BaseModel):
    cpf: str
    password: str

class Score(BaseModel):
    score: int
    
class MessageResponse(BaseModel):
    message: str