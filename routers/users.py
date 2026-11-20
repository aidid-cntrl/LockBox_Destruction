
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select 
from db import get_db
from models import Users, Wallets
from schemas import incoming_account_request
from sqlalchemy.ext.asyncio import AsyncSession

from oauth2 import get_password_hash

router = APIRouter(prefix='/accounts', tags=['Accounts'])

@router.post("/create_account")
async def create_account(data: incoming_account_request, db:AsyncSession = Depends(get_db)):

    print("i am in endpoit Create_account")

    account =await db.scalar(select(Users).where(Users.email==data.email).with_for_update())

    if account:
    
        raise HTTPException(status_code=400, detail="Email already taken")
    
    else:

        try:
            hashed_password = get_password_hash(data.password)

            new_account=Users(id= data.id, email= data.email, password= hashed_password)
            
            db.add(new_account)
            await db.commit()
            await db.refresh(new_account)

            wallets_account = Wallets(account_id=data.id, balance=0)

            db.add(wallets_account)
            await db.commit()
            await db.refresh(wallets_account)

        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Could not register account")

        return {f"Successfully created user account and wallet's account, id:{new_account.id}, email:{new_account.email},created at:{new_account.created_at}, balance:{wallets_account.balance} "}