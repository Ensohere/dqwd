from loguru import logger
import time

from modules.starknet_client import StarknetClient
from constants import JEDISWAP_CONTRACT, JEDISWAP_ABI, STARKNET_TOKENS
from utils import retry, check_gas, wait


class JediSwap(StarknetClient):
    def __init__(self, id_account: int, private_key: str):
        super().__init__(id_account, private_key)

        self.contract = self.get_contract(
            contract_address=JEDISWAP_CONTRACT, abi=JEDISWAP_ABI
        )

    async def get_min_amount_out(self, amount, slippage, path: list):
        min_amount_out_data = (
            await self.contract.functions["get_amounts_out"]
            .prepare(amountIn=amount, path=path)
            .call()
        )

        min_amount_out = min_amount_out_data.amounts

        return int(min_amount_out[1] - (min_amount_out[1] / 100 * slippage))

    @retry
    @check_gas
    @wait
    async def jedi_swap(
        self, from_token: str, to_token: str, amount_wei: int, slippage=2
    ):
        logger.info(
            f"[{self.id_account}][{hex(self.address)}] Swap on Jediswap - {from_token} -> {to_token} | {amount_wei} {from_token}"
        )

        path = [STARKNET_TOKENS[from_token], STARKNET_TOKENS[to_token]]
        min_amount_out = await self.get_min_amount_out(amount_wei, slippage, path)

        approve_contract = self.get_contract(STARKNET_TOKENS[from_token])

        approve_call = approve_contract.functions["approve"].prepare(
            JEDISWAP_CONTRACT, amount_wei
        )

        swap_call = self.contract.functions["swap_exact_tokens_for_tokens"].prepare(
            amount_wei, min_amount_out, path, self.address, int(time.time()) + 18000
        )

        tx_hash = await self.send_transaction([approve_call, swap_call])
        return await self.verify_tx(tx_hash=tx_hash.transaction_hash)
