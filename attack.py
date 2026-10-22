import asyncio

import httpx


url = "http://127.0.0.1:8000/atm/Withdraw?ammount=100"

async def hit_point(client,id):

    try:
       response = await client.patch(url)
       print(response)
       print(f"Req_id:{id}, status:{response.status_code}, {response.text}")

    except Exception as e: 
       print(f"Req_id:{id}, status:{response.status_code}")

async def main():

    async with httpx.AsyncClient() as client:

      tasks = [hit_point(client,i) for i in range(1,11)]

      await asyncio.gather(*tasks )

if __name__ == "__main__":
   print("running")
   asyncio.run(main())