

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models import Users
from oauth2 import authenticate_user, create_token, get_current_user
from schemas import login
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/login', tags=['/Loging'])

@router.post("/login")
async def login_user(data:login, db:AsyncSession = Depends(get_db)):

    user = await authenticate_user(db,data)

    expire_time = timedelta(minutes=15)

    token = await create_token(data={'sub':user.email},expire_time=expire_time)

    return token

@router.get("/user_details")
async def user_details(current_user:Users = Depends(get_current_user)):

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    else: 
        return current_user