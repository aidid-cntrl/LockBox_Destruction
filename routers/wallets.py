

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import Users, Wallets
from schemas import incoming_wallet_request
from oauth2 import  get_current_user, verify_password


router = APIRouter(prefix='/wallets', tags=['Wallets'])

@router.post("/add_money")
async def add_money(data:incoming_wallet_request, db:AsyncSession = Depends(get_db), account:Users = Depends(get_current_user)):

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    else:
        wallets_account = await db.scalar(select(Wallets).where(Wallets.account_id==data.id).with_for_update())

        try:
            wallets_account.balance += data.payment # type: ignore
            await db.commit()
 
        except SQLAlchemyError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Could not update balance")
        
        return {f"Succesfully added money to account, current balance:{wallets_account.balance}, id:{wallets_account.account_id}"} # type: ignore

@router.get("/wallet_details")
async def wallet_details(id:int, db:AsyncSession = Depends(get_db), account:Users = Depends(get_current_user)):

    if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
    
    else:
        wallets_account = await db.scalar(select(Wallets).where(Wallets.account_id==id).with_for_update())
    
        if wallets_account is None:
                raise HTTPException(status_code=404, detail="No money in account add money")
    
        else:
            return{f"id:{wallets_account.account_id}, current balance:{wallets_account.balance}"}



