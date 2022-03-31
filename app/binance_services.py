import asyncio
import json

from binance import AsyncClient, DepthCacheManager, BinanceSocketManager


async def get_binance_data(symbol="BTCUSDT"):
    client = await AsyncClient.create()

    data = json.dumps(await client.get_symbol_ticker(symbol=symbol), indent=2)
    return data

async def main():

    # initialise the client
    client = await AsyncClient.create()

    # run some simple requests
    print(json.dumps(await client.get_exchange_info(), indent=2))

    print(json.dumps(await client.get_symbol_ticker(symbol="BTCUSDT"), indent=2))

    # initialise websocket factory manager
    bsm = BinanceSocketManager(client)

    # create listener using async with
    # this will exit and close the connection after 5 messages
    async with bsm.trade_socket('ETHBTC') as ts:
        for _ in range(5):
            res = await ts.recv()
            print(f'recv {res}')

    # get historical kline data from any date range

    # fetch 1 minute klines for the last day up until now
    klines = client.get_historical_klines("BNBBTC", AsyncClient.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    # use generator to fetch 1 minute klines for the last day up until now
    async for kline in await client.get_historical_klines_generator("BNBBTC", AsyncClient.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
        print(kline)

    # fetch 30 minute klines for the last month of 2017
    klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

    # fetch weekly klines since it listed
    klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

    # setup an async context the Depth Cache and exit after 5 messages
    async with DepthCacheManager(client, symbol='ETHBTC') as dcm_socket:
        for _ in range(5):
            depth_cache = await dcm_socket.recv()
            print(f"symbol {depth_cache.symbol} updated:{depth_cache.update_time}")
            print("Top 5 asks:")
            print(depth_cache.get_asks()[:5])
            print("Top 5 bids:")
            print(depth_cache.get_bids()[:5])

    # Vanilla options Depth Cache works the same, update the symbol to a current one
    options_symbol = 'BTC-210430-36000-C'
    async with OptionsDepthCacheManager(client, symbol=options_symbol) as dcm_socket:
        for _ in range(5):
            depth_cache = await dcm_socket.recv()
            count += 1
            print(f"symbol {depth_cache.symbol} updated:{depth_cache.update_time}")
            print("Top 5 asks:")
            print(depth_cache.get_asks()[:5])
            print("Top 5 bids:")
            print(depth_cache.get_bids()[:5])

    await client.close_connection()
