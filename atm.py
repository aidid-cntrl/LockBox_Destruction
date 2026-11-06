import asyncio
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy import select
from db import   get_db
from models import incoming_atm_request,Account,creating_account
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/atm', tags=['ATM'])

@router.put("/Create_account")
async def create_account(data:creating_account, db: AsyncSession = Depends(get_db)):

    account = (await db.execute(select(Account).where(data.id==Account.id)).with_for_update()).scalar_one_or_none()

    if account is None:
        new_account = Account(id=data.id, balance=data.balance)
        db.add(new_account)
        await db.commit()
        await db.refresh(Account)

    return {"message":"successfully created account", "details":data}
    

@router.patch("/Withdraw")
async def withdraw_funds(data:incoming_atm_request, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Account).where(data.id==Account.id).with_for_update())
    account = result.scalar_one_or_none()

    if account.id is None:
        raise HTTPException(status_code=404, detail ="no account matched")

    else:
        if account.balance == 0:
           raise HTTPException(status_code=404,detail="not enough money")
        elif account.balance < data.ammount:
            raise HTTPException(status_code=404,detail=f"not enough money, available balance:{account.balance}")
        else:

            print("before balance:", account.balance, "withdrawn:", account.withdrawn)

            account.balance -= data.ammount
            account.withdrawn += data.ammount

            print("after balance:", account.balance, "withdrawn:", account.withdrawn)

            await db.commit()
            await db.refresh(account)

            return {"message":"successfully withdrawn cash","withdrawn":data.ammount, "current balance": account.balance}

