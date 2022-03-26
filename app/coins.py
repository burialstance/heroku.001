import asyncio
import aiohttp
from pydantic import BaseModel
from fastapi import APIRouter
import os

from datetime import date, datetime, time, timedelta

def aiohttp_session():
    return aiohttp.ClientSession(
        
    )


async def fetch_data(client: aiohttp.ClientSession, url: str, **kwargs):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ.get("X-CMC_PRO_API_KEY")
    }
    async with client.get(url, params=kwargs, headers=headers) as resp:
        return await resp.json()


async def get_data(url: str, **kwargs):
    async with aiohttp_session() as client:
        return await fetch_data(client, url)
