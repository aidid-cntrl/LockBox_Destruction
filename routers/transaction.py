

from sqlite3 import OperationalError

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from db import get_db
from models import Transfers, Users, Wallets
from schemas import incoming_transfer_request
from sqlalchemy.ext.asyncio import AsyncSession

from oauth2 import get_current_user


router = APIRouter(prefix='/transaction',tags=['Transaction'])

@router.post("/send_money")
async def send_money(data:incoming_transfer_request, db:AsyncSession = Depends(get_db), sendee_account:Users = Depends(get_current_user)):

    receiver_account = await db.scalar(select(Users).where((Users.id==data.transfer_account_id)&(Users.email==data.transfer_account_email)))

    if sendee_account is None:
        raise HTTPException(status_code=404, detail="Your account doesn't exist.")
    
    elif receiver_account is None:
            raise HTTPException(status_code=404, detail="Receiver's account doesn't exist.")

    elif receiver_account.id == sendee_account.id:
                raise HTTPException(status_code=404, detail="Receiver's account can't be same as your account")

    else:
        sendee_wallet_account = await db.scalar(select(Wallets).where(Wallets.account_id==sendee_account.id))
        
        if sendee_wallet_account.balance < data.payment: # type: ignore
                        raise HTTPException(status_code=404, detail="Your account doesn't have enough money.")

        else:
            try:
                if sendee_account.id<receiver_account.id:
                        smaller_id = sendee_account.id
                        bigger_id = receiver_account.id
                else:
                        smaller_id = receiver_account.id
                        bigger_id = sendee_account.id

                if smaller_id == sendee_account.id:
                    sendee_wallet_account = await db.scalar(update(Wallets).
                                                            where(Wallets.account_id==sendee_account.id).
                                                            values(balance = Wallets.balance-data.payment).returning(Wallets))
                    
                    receiver_wallet_account = await db.scalar(update(Wallets).
                                                            where(Wallets.account_id==receiver_account.id).
                                                            values(balance = Wallets.balance+data.payment).returning(Wallets))
                
                if bigger_id == sendee_account.id:
                    receiver_wallet_account = await db.scalar(update(Wallets).
                                                where(Wallets.account_id==receiver_account.id).
                                                values(balance = Wallets.balance+data.payment).returning(Wallets))

                    sendee_wallet_account = await db.scalar(update(Wallets).
                                                    where(Wallets.account_id==sendee_account.id).
                                                    values(balance = Wallets.balance-data.payment).returning(Wallets))

                new_transaction = Transfers(account_id=sendee_account.id, transfer_account_id=data.transfer_account_id, payment=data.payment, success=True)
                db.add(new_transaction)
                await db.commit()
                await db.refresh(new_transaction)

            except SQLAlchemyError:
              await db.rollback()
              raise HTTPException(status_code=500, detail="Couldn't send money")

            
            return {f"Successfully sent money, id:{sendee_wallet_account.account_id}, current balance:{sendee_wallet_account.balance}, sent to:{receiver_wallet_account.account_id}, ammount:{data.payment}"} # type: ignore
         
    


