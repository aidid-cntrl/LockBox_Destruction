import asyncio

import httpx


url =  "http://127.0.0.1:8000/debt/Payment?account_id=1&payment=50"

async def hit_point(client,request_id):

    try:
        print("in try")
        response = await client.patch(url)
        print(response)
        print(f"respose_id:{request_id}, status:{response.status_code}, response_message:{response.text}")

    except Exception as e:

        print(f"Error:{e}")


async def main():

    async with httpx.AsyncClient() as client:

        tasks = [hit_point(client,i)for i in range(1,11)]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("running")
    asyncio.run(main())

