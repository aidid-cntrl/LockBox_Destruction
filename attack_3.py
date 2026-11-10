import asyncio

import httpx

url = "http://127.0.0.1:8000/order/payment"
url_orders = "http://127.0.0.1:8000/order/orders"

async def hit_payment(client,data,index):

    try:

        response = await client.post(url, json=data)
        print(f"id:{index}, status:{response.status_code}, response:{response.text}")

    except Exception as e:

        print(f"id:{index}, error{e}")

async def get_orders(client,id):

    try:
        response = await client.get(url_orders,json=id)
        print(f"status:{response.status_code}, orders:{response.text}")

    except Exception as e:
        print(f"error:{e}")
    
    
async def main():
   
    async with httpx.AsyncClient() as client:

       payment = 50.0
       data = {'id':1, 'product':'chips','quantity':5, 'metric':'kg','payment':payment, 'overdraft':True}

       tasks = [hit_payment(client,data,i)for i in range(1,11)]

       await asyncio.gather(*tasks)

       id = 1

       await get_orders(client,id)

    
if __name__ == "__main__":
     print("running")
     asyncio.run(main())