import asyncio

import httpx


url =  "http://127.0.0.1:8000/debt/Payment"

async def hit_point(client,request_id,data):

    try:
        response = await client.patch(url, json=data)
        print(response)
        print(f"respose_id:{request_id}, status:{response.status_code}, response_message:{response.text}")

    except Exception as e:

        print(f"Error:{e}")


async def main():

    async with httpx.AsyncClient() as client:

        data = {'id':3, 'payment':50}

        tasks = [hit_point(client,i,data)for i in range(1,11)]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("running")
    asyncio.run(main())

