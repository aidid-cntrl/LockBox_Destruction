


send_money_url = "http://127.0.0.1:8000/transaction/send_money"

import asyncio
import json
import httpx


async def send_money(client,data):
        
        try:
            response = await client.post(send_money_url, json=data)
            print(response.json())
        
        except Exception as e:
            print(f"{e}")

async def main():
    async with httpx.AsyncClient() as client:
           
        send_money_tasks = []

        for i in range(10, 0, -1):

                if i>=2:
                    send_money_data = {f"id":i, "transfer_account_id":f"{i-1}", "email":f"Example{i}$@gmail.com", "password":f"Example${i}",
                                       "transfer_account_email":f"Example{i-1}$@gmail.com", "payment":50}
                    print(send_money_data)
                    send_money_tasks.append(send_money(client,send_money_data))

                elif i==1:
                    send_money_data = {f"id":i, "transfer_account_id":f"{10}", "email":f"Example{i}$@gmail.com", "password":f"Example${i}",
                                        "transfer_account_email":f"Example{i-1}$@gmail.com","payment":50}
                    print(send_money_data)
                    send_money_tasks.append(send_money(client,send_money_data))

        await asyncio.gather(*send_money_tasks)

asyncio.run(main())