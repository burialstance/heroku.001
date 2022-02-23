import asyncio
import aiohttp
from fastapi import APIRouter

router = APIRouter()

async def fetch_data(client, period: str = "5m"):
    url = f"https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period={period}"
    async with client.get(url) as resp:
        return await resp.json()


async def get_data(period: str = "5m"):
    async with aiohttp.ClientSession() as client:
        return await fetch_data(client, period=period)
           

async def iter_data():
    while True:
        yield await get_data()




