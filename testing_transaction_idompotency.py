import asyncio
import uuid

from fastapi import HTTPException
import httpx

login_url = "http://127.0.0.1:8000/login/login"
transaction_url = "http://127.0.0.1:8000/transaction/send_money"

async def transaction_endpoint(client,data,headers):

    data = await client.post(transaction_url, json=data, headers=headers)

    if data is None:
        raise HTTPException(status_code=401, detail="response no found")

    print(data.json())

    return data

async def login_endpoint(client,data):

    token = await client.post(login_url, json=data)

    return token.json()

async def main():
    async with httpx.AsyncClient() as client:

        login_data_1 = {"email":"Example1$@gmail.com", "password":"Example$1"}
        login_data_2 = {"email":"Example2$@gmail.com", "password":"Example$2"}

        token_1 = await login_endpoint(client, login_data_1)
        token_2 = await login_endpoint(client, login_data_2)

        tasks =[]

        idempotency_key_1 = str(uuid.uuid4())
        idempotency_key_2 = str(uuid.uuid4())

        for i in range(1,6):

            data_1 = {"transfer_account_id":2, "transfer_account_email":f"Example{2}$@gmail.com", "payment":100}
            data_2 = {"transfer_account_id":1, "transfer_account_email":f"Example{1}$@gmail.com", "payment":100}

            print(idempotency_key_1)
            print(idempotency_key_2)

            headers_1 = {"Authorization": f"Bearer {token_1}",
                         "Idempotency-key":f"{idempotency_key_1}"}
            headers_2 = {"Authorization": f"Bearer {token_2}",
                         "Idempotency-key":f"{idempotency_key_2}"}

            data_recived_1 = transaction_endpoint(client, data_1, headers_1)
            data_recived_2 = transaction_endpoint(client, data_2, headers_2)

            if i % 2 == 0:
                tasks.append(data_recived_1)
                tasks.append(data_recived_2)
            else:
                tasks.append(data_recived_2)
                tasks.append(data_recived_1)

        results = await asyncio.gather(*tasks)

        success = sum(1 for i in results if i.status_code == 200)

        print(f"Total success:{success}")

asyncio.run(main())





            