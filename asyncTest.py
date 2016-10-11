import asyncio

async def get():
    print('get print!')


async def post():
    print('post start!')
    r = await get()
    print(r)
    print('post end!')

loop = asyncio.get_event_loop()
loop.run_until_complete(post())
loop.close()


