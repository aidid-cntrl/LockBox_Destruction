


adding_money_url = "http://127.0.0.1:8000/wallets/add_money"
getting_wallet_account_details_url = "http://127.0.0.1:8000/wallets/wallet_details"

import asyncio
import json
from fastapi import HTTPException
import httpx


async def adding_money(client,data):

        try:
            print("i am in adding_money try")
            response = await client.post(adding_money_url, json=data)
            print(response.json())
        
        except Exception as e:
              print(f"{e}")

async def getting_account(client,i):

        try:    
            response = await client.get(f"http://127.0.0.1:8000/wallets/wallet_details?id={i}")
            print(response.json())

        except Exception as e:
            print(f"status:{e}")

              

async def main():
    async with httpx.AsyncClient() as client:
           
        adding_money_tasks = []
        getting_account_details_tasks = []

        for i in range(1,11):

                adding_money_data = {f"id":i, "email":f"Example{i}$@gmail.com", "password":f"Example${i}", "payment":50}
                print(adding_money_data)

                adding_money_tasks.append(adding_money(client,adding_money_data))
                getting_account_details_tasks.append(getting_account(client,i))

        await asyncio.gather(*adding_money_tasks)
        await asyncio.gather(*getting_account_details_tasks)

asyncio.run(main())