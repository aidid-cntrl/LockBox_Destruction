import asyncio

from fastapi import APIRouter,HTTPException
from numpy import double


router = APIRouter(prefix ='/debt',tags=['DEBT'])

balance = 250
debt = 500
id = 1
paid = False

@router.patch("/Payment")
async def debt_payment(account_id:int, payment:float):
    print("came to endpoint 1")

    global id,balance,debt,paid

    if id != account_id or paid is True or balance <=0:

        print("came to endpoint 2")

        raise HTTPException(status_code=404, detail=f"something went wrong, debt:{debt}, balance{balance},paid:{paid}")
    
    else:
        print("came to endpoint 3")
        await asyncio.sleep(2)
        balance -= payment
        debt -= payment

        if debt == 0:
           paid = True
 
        return{"message":"successfully paid the debt", "current debt":debt, "current balance":balance}
