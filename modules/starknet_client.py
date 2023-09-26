from starknet_py.cairo.felt import decode_shortstring
from starknet_py.contract import Contract
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.networks import MAINNET
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

from loguru import logger
import aiohttp
from typing import Union, List

from config import starknet_rpc, cairo_version
from constants import (
    ARGENTX_PROXY_CLASS_HASH,
    ARGENTX_IMPLEMENTATION_CLASS_HASH,
    ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
    ERC20_ABI,
)


class StarknetClient:
    def __init__(self, id_account: int, private_key: str) -> None:
        self.id_account = id_account
        self.key_pair = KeyPair.from_private_key(private_key)
        self.client = FullNodeClient(node_url=starknet_rpc)
        # self.client = GatewayClient(MAINNET)
        self.address = self.get_address_argent()
        self.account = Account(
            address=self.address,
            client=self.client,
            key_pair=self.key_pair,
            chain=StarknetChainId.MAINNET,
        )

    def get_address_argent(self):
        if cairo_version == 0:
            selector = get_selector_from_name("initialize")

            calldata = [self.key_pair.public_key, 0]

            address = compute_address(
                class_hash=ARGENTX_PROXY_CLASS_HASH,
                constructor_calldata=[
                    ARGENTX_IMPLEMENTATION_CLASS_HASH,
                    selector,
                    len(calldata),
                    *calldata,
                ],
                salt=self.key_pair.public_key,
            )

            return address
        else:
            address = compute_address(
                class_hash=ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
                constructor_calldata=[self.key_pair.public_key, 0],
                salt=self.key_pair.public_key,
            )

            return address

    def get_contract(self, contract_address: int, abi: Union[dict, None] = None):
        if abi is None:
            abi = ERC20_ABI

        contract = Contract(address=contract_address, abi=abi, provider=self.account)

        return contract

    async def get_balance(self, contract_address: int) -> dict:
        contract = self.get_contract(contract_address)

        symbol_data = await contract.functions["symbol"].call()
        symbol = decode_shortstring(symbol_data.symbol)
        decimal = await contract.functions["decimals"].call()
        balance_wei = await contract.functions["balanceOf"].call(self.address)

        balance = balance_wei.balance / 10**decimal.decimals

        return {
            "balance_wei": balance_wei.balance,
            "balance": balance,
            "symbol": symbol,
            "decimal": decimal.decimals,
        }

    async def send_transaction(self, calls: List[Call]):
        tx_params = await self.account.sign_invoke_transaction(
            calls=calls,
            auto_estimate=True,
            nonce=await self.account.get_nonce(),
        )

        sign_tx = await self.account.client.send_transaction(tx_params)
        return sign_tx

    async def verify_tx(self, tx_hash):
        await self.account.client.wait_for_tx(tx_hash=tx_hash, check_interval=10)
        logger.success(
            f"[{self.id_account}][{hex(self.address)}] https://starkscan.co/tx/{hex(tx_hash)}"
        )

    async def get_min_amount(self, amount: int, slippage: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coinlore.net/api/ticker/?id=80"
            ) as response:
                if response.status  == 200:
                    data = await response.json()
                    eth_price = float(data[0].get("price_usd"))
                    amount = int(eth_price * (1 - slippage / 100) * amount)
                    min_amount = int(amount * 10 * 6)
                    return min_amount
                else:
                    logger.error(f"Error with min amount | {response.status}")
