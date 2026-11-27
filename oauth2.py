

import datetime
import os
from sqlite3 import IntegrityError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash
from sqlalchemy import select

from db import get_db
from models import Users
from sqlalchemy.ext.asyncio import AsyncSession

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES) # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user(db,email):

  user = await db.scalar(select(Users).where(Users.email==email))

  return user

async def authenticate_user(db,data):

    user = await get_user(db,data.email)

    if user is None:
       raise HTTPException(status_code=404, detail="Email not found")

    else:
        if verify_password(data.password, user.password) is False:
          raise HTTPException(status_code=404, detail="Password does not match")
       
        else:
           return user 

password_hash = PasswordHash.recommended()

def verify_password(plain_password, password):

    return password_hash.verify(plain_password, password)

async def create_token(data:dict, expire_time):

   expire_time_delta = datetime.datetime.now(datetime.UTC) + expire_time

   data.update({'exp':expire_time_delta})
   token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

   return token

async def get_current_user(token:str = Depends(oauth2_scheme),db:AsyncSession = Depends(get_db)):

   try:
      data = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore

      user = await get_user(db,data['sub'])

   except jwt.InvalidTokenError:

      raise HTTPException(status_code=401, detail="Unathorized credentials")

   if not user:
      raise HTTPException(status_code=404, detail="token doesnt work")
   else:
      return user

def get_password_hash(password):
   hashed_password = password_hash.hash(password)
   return hashed_password
   