import asyncio
import aiohttp
from pydantic import BaseModel
from fastapi import APIRouter

from datetime import date, datetime, time, timedelta

def aiohttp_session():
    return aiohttp.ClientSession(
        
    )


async def fetch_data(client: aiohttp.ClientSession, url: str, **kwargs):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
    }
    async with client.get(url, params=kwargs, headers=headers) as resp:
        return await resp.json()


async def get_data(url: str, **kwargs):
    async with aiohttp_session() as client:
        return await fetch_data(client, url)
