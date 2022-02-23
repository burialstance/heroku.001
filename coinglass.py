import asyncio
import aiohttp


async def fetch_data(client, period: str = "5m"):
    url = f"https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period={period}"
    async with client.get(url) as resp:
        return await resp.json()


async def iter_data(period: str = "5m"):
    async with aiohttp.ClientSession() as client:
        while True:
            yield await fetch_data(client, period=period)
            asyncio.sleep(1)
