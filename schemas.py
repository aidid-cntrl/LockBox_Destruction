import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import DateTime, ForeignKey, Numeric, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

#User's schemas

class incoming_account_request(BaseModel):

    model_config = ConfigDict(regex_engine="python-re")
    id: int
    password: str = Field(
        pattern=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must contain minimum 8 charecters including one uppcase, one lowercase, one digit, one special charecter")
    email: EmailStr
 
class outgoing_creating_account_request(BaseModel):

    id: int
    email: EmailStr
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


#Wallet's schemas

class incoming_wallet_request(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")
    id: int
    email:EmailStr
    password: str = Field(
        pattern=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must contain minimum 8 charecters including one uppcase, one lowercase, one digit, one special charecter")
    payment: Optional [Decimal] = Field(gt=0, decimal_places=2)

class outgoing_wallet_request(BaseModel):
    
    id: int
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)


#Transfer's schemas

class incoming_transfer_request (BaseModel):
     
     model_config = ConfigDict(regex_engine="python-re")
     id: int
     email: str
     transfer_account_id:int
     transfer_account_email:str
     password: str = Field(
        pattern=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must contain minimum 8 charecters including one uppcase, one lowercase, one digit, one special charecter")
     metric: str = Field(min_length=1, default="$")
     payment: Decimal = Field(gt=0)

class outgoing_transfer_request(BaseModel):
        id: int
        transfer_account_id: int
        metric: str = Field(min_length=2)
        payment: Decimal = Field(gt=0)
        success: bool

        model_config = ConfigDict(from_attributes=True)

class login(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")

    email: EmailStr
    password: str = Field(
        pattern=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must contain minimum 8 charecters including one uppcase, one lowercase, one digit, one special charecter")