import asyncio

from fastapi import APIRouter, FastAPI, HTTPException 


router = APIRouter(prefix='/atm', tags=['ATM'])

balance = 100

@router.patch("/Withdraw")
async def withdraw_funds(ammount: int):

    global balance

    if ammount > balance:
        raise HTTPException(status_code=404, detail ="not enough cash left")

    await asyncio.sleep(2)

    balance -= ammount

    return {"message":"successfully withdrawn cash" , "current balance": balance}

