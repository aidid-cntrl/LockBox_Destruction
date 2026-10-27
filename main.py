
from fastapi import FastAPI

import atm
import debt
import ghost_order


app = FastAPI()

app.include_router(atm.router)
app.include_router(debt.router)
app.include_router(ghost_order.router)