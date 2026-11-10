import asyncio
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
import db
from models import Account, Debt, Order, incoming_order, viewing_order


router = APIRouter(prefix='/order', tags=['ORDER'])

@router.post("/payment")
async def order_payment(data:incoming_order, db:AsyncSession = Depends(get_db)):

    account = await db.scalar(select(Account).where(Account.id == data.id).with_for_update())

    if account is None:
        raise HTTPException(status_code=404, detail="account not found")

    elif account:

        if data.payment > account.balance:

            if data.overdraft is False:
                raise HTTPException(status_code=404, detail=f"don't have enough money. currect balance: {account.balance}")
            
            elif data.overdraft is True:
                    
                    account.balance -= data.payment
                 
                    await db.commit()
                 
                    result = await (confirmation(data,db))
                 
                    return result
                 
        else:
            account.balance -= data.payment

            await db.commit()

            result = await (confirmation(data,db))

            return result


@router.get("/orders")
async def orders(data:viewing_order, db: AsyncSession = Depends(get_db)):

    account = await db.scalar(select(Order).where(Order.id==data.id).with_for_update())

    if not account:
            raise HTTPException(status_code=404, detail="no account found")
    
    if (account.product or account.metric or account.quantity) is None:
    
            raise HTTPException(status_code=404, detail="order is not correct or found")
    
    else:
        return {"your order is":account}
 

async def confirmation(data,db):

    account = (await db.scalar(select(Account).where(Account.id == data.id).with_for_update()))
    overdraft_account = (await db.scalar(select(Debt).where(Debt.id==data.id).with_for_update()))

    if account is None:
           raise HTTPException(status_code=404,detail="account not found")
    else:

        if data.overdraft is False:
            new_order = Order(id=data.id, product=data.product, metric=data.metric,
                            quantity=data.quantity, payment=data.payment, overdraft=False)
            
        elif (data.overdraft is True) & (account.balance<0):
            new_order = Order(id=data.id, product=data.product, metric=data.metric,
                                quantity=data.quantity, payment=data.payment,
                                overdraft=True)

            if overdraft_account:
               overdraft_account.overdraft = account.balance

            else:
                new_debt= Debt(id=data.id, overdraft=account.balance)
                db.add(new_debt)
                await db.refresh(new_debt)
                await db.commit()



        elif (data.overdraft is True) & (account.balance>=0):
                new_order = Order(id=data.id, product=data.product, metric=data.metric,
                                        quantity=data.quantity, payment=data.payment,
                                        overdraft=False)
                     
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        balance = account.balance

        return {"message":"confirmed order", "balance":balance, "products":data}







