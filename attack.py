import asyncio

import httpx


url = "http://127.0.0.1:8000/atm/Withdraw"

async def hit_point(client,id,data):

    try:
       response = await client.patch(url, json = data)
       print(response)
       print(f"Req_id:{id}, status:{response.status_code}, {response.text}")

    except Exception as e: 
       print(f"Req_id:{id}, status:{response.status_code}")

async def main():

    async with httpx.AsyncClient() as client:

      ammount = 10
      tasks = []

      for i in range(1,11):

         ammount +=5

         data = {'id':1, 'ammount':ammount}

         tasks.append(hit_point(client,i,data))

      await asyncio.gather(*tasks)

if __name__ == "__main__":
   print("running")
   asyncio.run(main())