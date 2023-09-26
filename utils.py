import asyncio
from functools import wraps
from web3 import AsyncWeb3
from loguru import logger
import random
import time

from config import MAX_GWEI, MIN_SLEEP_TIME, MAX_SLEEP_TIME, RETRY_COUNT

ETH_RPC = "https://eth.getblock.io/8926182a-45f0-44c0-bc4f-006060e1235a/mainnet/"


def check_gas(func):
    async def wrapper(*args, **kwargs):
        while True:
            w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(ETH_RPC))
            gas = await w3.eth.gas_price
            gas_gwei = w3.from_wei(gas, "gwei")

            if gas_gwei > MAX_GWEI:
                logger.warning(
                    f"The GAS price is high -> {gas_gwei.__round__(4)} Gwei | waiting for it to drop below < {MAX_GWEI} Gwei"
                )
                await asyncio.sleep(120)
            else:
                break

        return await func(*args, **kwargs)

    return wrapper


def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries < RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                time.sleep(10)
                retries += 1

    return wrapper


def wait(func):
    async def sleep(*args, **kwargs):
        random_time = random.randint(MIN_SLEEP_TIME, MAX_SLEEP_TIME)
        logger.debug(f"Sleeping for {random_time} seconds...")
        await asyncio.sleep(random_time)
        await func(*args, **kwargs)

    return sleep
