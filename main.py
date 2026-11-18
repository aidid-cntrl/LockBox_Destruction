
from contextlib import asynccontextmanager
from unittest.mock import Base

from fastapi import FastAPI 
from routers import transaction, users, wallets

from db import init_db,engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    #await init_db()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(transaction.router)

