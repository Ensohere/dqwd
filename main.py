import asyncio
import random
from loguru import logger

from modules.zklend import ZkLend
from modules.jediswap import JediSwap
from modules.dmail import Dmail

from constants import private_keys, STARKNET_TOKENS
from config import (
    MIN_TRANSACTION,
    MAX_TRANSACTION,
    MIN_AMOUNT_ETH,
    MAX_AMOUNT_ETH,
    TASKS_CHANCE,
)


async def zklend(id_account, private_key):
    client = ZkLend(id_account=id_account, private_key=private_key)

    balance = await client.get_balance(STARKNET_TOKENS["ETH"])
    balance_wei = int(balance["balance_wei"] * 0.9)

    await client.deposit_zklend(balance_wei)
    await client.withdraw_zklend()


async def jediswap(id_account, private_key):
    client = JediSwap(id_account=id_account, private_key=private_key)

    random_value_eth = random.uniform(MIN_AMOUNT_ETH, MAX_AMOUNT_ETH)
    balance_wei_eth = int(random_value_eth * 10**18)
    await client.jedi_swap("ETH", "USDC", balance_wei_eth)

    balance_usdc = await client.get_balance(STARKNET_TOKENS["USDC"])
    balance_wei_eth_usdc = balance_usdc["balance_wei"]
    await client.jedi_swap("USDC", "ETH", balance_wei_eth_usdc)


async def dmail(id_account, private_key):
    client = Dmail(id_account=id_account, private_key=private_key)
    await client.send_mail()


def generate_task_sequence(num_tasks, task_chances):
    tasks = list(task_chances.keys())
    probabilities = list(task_chances.values())
    sequence = random.choices(tasks, probabilities, k=num_tasks)
    logger.info(f"Generated task sequence: {sequence}")
    return sequence


async def handle_wallet(id_account, private_key):
    TASKS_MAP = {"zklend": zklend, "jediswap": jediswap, "dmail": dmail}

    num_tasks = random.randint(MIN_TRANSACTION, MAX_TRANSACTION)
    logger.info(f"Total number of tasks to be executed: {num_tasks}")

    task_sequence = generate_task_sequence(num_tasks, TASKS_CHANCE)

    for task_name in task_sequence:
        await TASKS_MAP[task_name](id_account=id_account, private_key=private_key)


async def main():
    tasks = []
    for id_account, private_key in enumerate(private_keys, start=1):
        tasks.append(handle_wallet(id_account, private_key))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
