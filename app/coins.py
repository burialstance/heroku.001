import asyncio
import aiohttp
from pydantic import BaseModel
from fastapi import APIRouter

from datetime import date, datetime, time, timedelta

async def aiohttp_session():
    return aiohttp.ClientSession(
        
    )

class CoinData(BaseModel):
    symbol: str
    timestamp: datetime
    longAccount: float
    shortAccount: float
    longShortRatio: float

    def ratio(self):
        x = 1000
        ratio_long = self.longShortRatio - 1
        ratio_short = 1 - self.longShortRatio
        return str(round(x * (ratio_long if self.longShortRatio > 1 else ratio_short), 3))

    def status(self):
        return "success" if self.longShortRatio > 1 else "danger"



async def fetch_data(client: aiohttp.ClientSession, url: str, **kwargs):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
    }
    async with client.get(url, params=kwargs, headers=headers) as resp:
        return await resp.json()


async def get_data(url: str, **kwargs):
    async with aiohttp.ClientSession() as client:
        return await fetch_data(client, url)
