import aiohttp 


async def fetch_data(period: str = "5m"):
    url = f"https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period={period}"
    async with client.get(url) as resp:
        return await resp.json()

    
