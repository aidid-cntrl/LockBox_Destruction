from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
   pass

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(10,2), default = Decimal("100.00"))
    withdrawn: Mapped[Decimal] = mapped_column(Numeric(10,2), default = Decimal("0.00"))

class creating_account(BaseModel):
    id: int
    balance: Decimal = Field(gt = 0)

class incoming_atm_request(BaseModel):
    id:int
    ammount: Decimal = Field(gt = 5, decimal_places=2)
 
class outgoing_atm_request(BaseModel):

    balance: Decimal

    model_config = ConfigDict(from_attributes=True)

class Order(Base):
    __tablename__ = "orders"

    row_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    product: Mapped[str] = mapped_column(str(50))
    quantity: Mapped[float] = mapped_column(Numeric(10,2), default= 1)
    metric : Mapped[str] = mapped_column(str(10))
    payment : Mapped[float] = mapped_column(Numeric(10,2), default=0)
    overdraft : Mapped[bool] = mapped_column(default=None)

class incoming_order (BaseModel):

     id: int
     product: str = Field(min_length=3, max_length=20)
     quantity: float =  Field(gt=0)
     metric: str = Field(min_length=2)
     payment: Decimal = Field(gt=0)
     overdraft: bool = Field(default=False)


class viewing_order(BaseModel):

    id:int

class outgoing_order(BaseModel):
        id: int
        product: str = Field(min_length=3, max_length=20)
        quantity: float =  Field(gt=0)
        metric: str = Field(min_length=2)
        payment: Decimal = Field(gt=0)

        model_config = ConfigDict(from_attributes=True)

class Debt(Base):
    __tablename__="debts"

    row_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(ForeignKey("accounts.id"),nullable=False)
    overdraft: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0)

class incoming_debt_payment(BaseModel):
    
    id: int
    payment: Decimal = Field(decimal_places=2)

class outgoing_debt_payment(BaseModel):

    debt: Decimal

    model_config = ConfigDict(from_attributes=True)




