
from fastapi import FastAPI

import atm


app = FastAPI()

app.include_router(atm.router)