import aiohttp
import asyncio


async def make_request1():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://onliner.by/") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ 1го запроса")
            print("=" * 18)


async def make_request2():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://kufar.by/") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ 2го запроса")
            print("=" * 18)


async def make_request3():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://google.com/") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ 3-го запроса")
            print("=" * 18)


async def make_request4():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://wikipedia.org") as resp:
            print(await resp.text())


async def make_request5():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://microsoft.com") as resp:
            print(await resp.text())


async def make_request6():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://apple.com") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ ")
            print("=" * 18)


async def make_request7():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://abw.by") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ ")
            print("=" * 18)


async def make_request8():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://youtube.com/") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ ")
            print("=" * 18)


async def make_request9():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://telegram.org") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ ")
            print("=" * 18)


async def make_request10():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://av.by") as resp:
            print(await resp.text())
            print("=" * 18)
            print(" КОНЕЦ ")
            print("=" * 18)


async def amain():
    await asyncio.gather(
        make_request1(),
        make_request2(),
        make_request3(),
        make_request4(),
        make_request5(),
        make_request6(),
        make_request7(),
        make_request8(),
        make_request9(),
        make_request10(),
    )


asyncio.run(amain())
