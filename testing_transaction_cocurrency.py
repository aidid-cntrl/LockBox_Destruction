import asyncio

from fastapi import HTTPException
import httpx

login_url = "http://127.0.0.1:8000/login/login"
transaction_url = "http://127.0.0.1:8000/transaction/send_money"


async def transaction_endpoint(client,data,headers):

    data = await client.post(transaction_url, json=data, headers=headers)

    if data is None:
        raise HTTPException(status_code=401, detail="response no found")

    print(data.json())

    print("in transaction_endpoint")

    return data

async def login_endpoint(client,data):

    token = await client.post(login_url, json=data)
    
    print("in login_endpoint")

    print(token.json())

    return token.json()

async def main():
    async with httpx.AsyncClient() as client:

        login_data = {"email":"Example1$@gmail.com", "password":"Example$1"}

        token = await login_endpoint(client, login_data)

        tasks =[]

        for i in range(10,2,-1):

            data = {"transfer_account_id":i, "transfer_account_email":f"Example{i}$@gmail.com", "payment":100}

            headers = {"Authorization": f"Bearer {token}"}
            print(headers)

            data_recived = transaction_endpoint(client, data, headers)

            tasks.append(data_recived)

        await asyncio.gather(*tasks)

asyncio.run(main())





            