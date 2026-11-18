


creating_account_url = "http://127.0.0.1:8000/accounts/create_account"
getting_account_details_url = "http://127.0.0.1:8000/accounts/account_details"

import asyncio
import json
from fastapi import HTTPException
import httpx


async def creating_account(client,data):

        try:
            print("i am in creating_account try")
            response = await client.post(creating_account_url, json=data)
            print(response.json())
        
        except Exception as e:
              print(f"status:{response.status_code}")

async def getting_account(client,i):

        try:    
            response = await client.get(f"http://127.0.0.1:8000/accounts/account_details?id={i}")
            print(response.json())

        except Exception as e:
            print(f"status:{response.status_code}")

              

async def main():
    async with httpx.AsyncClient() as client:
           
        creating_account_tasks = []
        getting_account_details_tasks = []

        for i in range(1,11):

                creating_account_data = {f"id":i, "email":f"Example{i}$@gmail.com", "password":f"Example${i}"}
                print(creating_account_data)

                creating_account_tasks.append(creating_account(client,creating_account_data))
                getting_account_details_tasks.append(getting_account(client,i))

        await asyncio.gather(*creating_account_tasks)
        await asyncio.gather(*getting_account_details_tasks)

asyncio.run(main())