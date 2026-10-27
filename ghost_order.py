import asyncio
from fastapi import HTTPException
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix='/order', tags=['ORDER'])

balance = 500 
products = []

class order(BaseModel):

    product:str
    quantity:float
    metric:str
    payment:float

@router.post("/payment")
async def order_payment(data:order):

    global balance,products

    if data.payment > balance:
        raise HTTPException(status_code=404, detail="don't have enough money")

    else:
        balance -= data.payment

        result = await (confirmation(data))

        return result

        


@router.get("/orders")
async def orders():

    global products

    if products:
      return products
    
    else:
        raise HTTPException(status_code=404, detail="no orders found")
 

async def confirmation(data):

    global products,balance

    return {"message":"confirmed order", "balance":balance, "products":data}

    products.append(data)







