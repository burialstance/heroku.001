import asyncio
import aiohttp
from pydantic import BaseModel
from fastapi import APIRouter

from datetime import date, datetime, time, timedelta


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

router = APIRouter()

async def fetch_data(client):
    url = "https://data.messari.io/api/v1/assets/btc/metrics"
    async with client.get(url) as resp:
        return await resp.json()


async def get_data():
    async with aiohttp.ClientSession() as client:
        return await fetch_data(client)
           
