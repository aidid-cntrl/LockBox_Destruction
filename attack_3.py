import asyncio

import httpx

url = "http://127.0.0.1:8000/order/payment"
url_orders = "http://127.0.0.1:8000/order/orders"

async def hit_payment(client,data,payment_ammount,id):

    try:

        response = await client.post(url, json=data, params={'payment' : payment_ammount})
        print(f"id:{id}, status:{response.status_code}, response:{response.text}")

    except Exception as e:

        print(f"id:{id}, error{e}")

async def get_orders(client):

    try:
        response = await client.get(url_orders)
        print(f"status:{response.status_code}, orders:{response.text}")

    except Exception as e:
        print(f"error:{e}")
    
    
async def main():
   
    async with httpx.AsyncClient() as client:

       payment = 50.0
       data = {'product':'chips','quantity':'5', 'metric':'kg','payment':payment}

       tasks = [hit_payment(client,data,payment,i)for i in range(1,11)]

       await asyncio.gather(*tasks)

       await get_orders(client)

    
if __name__ == "__main__":
     print("running")
     asyncio.run(main())