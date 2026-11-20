

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from db import get_db
from models import Transfers, Users, Wallets
from schemas import incoming_transfer_request
from sqlalchemy.ext.asyncio import AsyncSession

from oauth2 import get_current_user, get_password_hash, verify_password


router = APIRouter(prefix='/transaction',tags=['Transaction'])

@router.post("/send_money")
async def send_money(data:incoming_transfer_request, db:AsyncSession = Depends(get_db), sendee_account:Users = Depends(get_current_user)):

    receiver_account = await db.scalar(select(Users).where((Users.id==data.transfer_account_id)&(Users.email==data.transfer_account_email)).with_for_update())

    if sendee_account is None:
        raise HTTPException(status_code=404, detail="Your account doesn't exist.")

    elif verify_password(data.password,sendee_account.password) is False:
          raise HTTPException(status_code=404, detail="Your password doesn't match.")

    elif receiver_account is None:
            raise HTTPException(status_code=404, detail="Receiver's account doesn't exist.")

    else:
        sendee_wallet_account = await db.scalar(select(Wallets).where(Wallets.account_id==data.id).with_for_update())
        receiver_wallet_account = await db.scalar(select(Wallets).where(Wallets.account_id==data.transfer_account_id).with_for_update())

        if sendee_wallet_account is None: 
                raise HTTPException(status_code=404, detail="Your account doesn't have enough money.")
        
        if sendee_wallet_account.balance < data.payment: 
                        raise HTTPException(status_code=404, detail="Your account doesn't have enough money.")
        
        if receiver_wallet_account is None:
              
              new_transaction = Wallets(account_id=data.transfer_account_id, balance=0)

              db.add(new_transaction)
              await db.commit()
              await db.refresh(new_transaction)

        else:
              sendee_wallet_account.balance -= data.payment
              receiver_wallet_account.balance += data.payment

              new_transaction = Transfers(account_id=data.id, transfer_account_id=data.transfer_account_id, payment=data.payment, success=True)

              db.add(new_transaction)
              await db.commit()
              await db.refresh(new_transaction)

              return {f"Successfully sent money, current balance:{sendee_wallet_account.balance}"} 
         
    


