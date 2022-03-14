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

async def fetch_data(client, period: str = "5m"):
    url = f"https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period={period}"
    async with client.get(url) as resp:
        return await resp.json()


async def get_data(period: str = "5m"):
    async with aiohttp.ClientSession() as client:
        return [CoinData(**i) for i in await fetch_data(client, period=period)]
           
