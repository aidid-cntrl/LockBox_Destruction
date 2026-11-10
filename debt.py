import asyncio
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import Account, Debt, incoming_debt_payment

router = APIRouter(prefix ='/debt',tags=['DEBT'])

@router.patch("/Payment")
async def debt_payment(data:incoming_debt_payment, db:AsyncSession = Depends(get_db)):

    debt_account = await db.scalar(select(Debt).where(Debt.id==data.id).with_for_update())
    main_account = await db.scalar(select(Account).where(Debt.id==data.id).with_for_update())


    if not debt_account:
        raise HTTPException(status_code=404, detail=f"no account found, debt")

    else:
        if data.payment<=0:
           raise HTTPException(status_code=404, detail=f"payment cannot be 0 or negative")
        else:
           debt_account.overdraft += data.payment

           if not main_account:
               raise HTTPException(status_code=404, detail=f"account has been deactivated")
           else:
                main_account.balance += data.payment

           await db.commit()
           return{"message":"successfully paid the debt", "current debt": debt_account.overdraft, "current balance":main_account.balance}
