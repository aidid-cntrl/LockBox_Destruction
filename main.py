
from fastapi import FastAPI

import atm
import debt


app = FastAPI()

app.include_router(atm.router)
app.include_router(debt.router)