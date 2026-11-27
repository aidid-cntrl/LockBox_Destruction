import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import DateTime, ForeignKey, Numeric, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
   pass

class Users(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password:Mapped[str] = mapped_column(nullable=False)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True) ,server_default=func.now())

class Wallets(Base):
    __tablename__="Wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("Users.id"),nullable=False)
    metric: Mapped[str] = mapped_column(default='$', nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0)

class Transfers(Base):
    __tablename__ = "Transfers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)
    transfer_account_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)
    metric : Mapped[str] = mapped_column(String(10), default='$')
    payment : Mapped[float] = mapped_column(Numeric(10,2), default=0)
    processed_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True) ,server_default=func.now())
    idempotency_key: Mapped[str] = mapped_column(nullable=True, unique=True)
    success: Mapped[bool] = mapped_column(default=False)