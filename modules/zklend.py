from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

from modules.starknet_client import StarknetClient
from constants import ZKLEND_CONTRACT, ZKLEND_ETH_CONCTRACT, STARKNET_TOKENS
from utils import retry, check_gas, wait


class ZkLend(StarknetClient):
    def __init__(self, id_account: int, private_key: str):
        super().__init__(id_account, private_key)

    async def get_deposit_amount(self):
        zklend_eth_contract = self.get_contract(ZKLEND_ETH_CONCTRACT)

        amount_data = await zklend_eth_contract.functions['balanceOf'].call(self.address)
        amount = amount_data.balance

        return amount

    @retry
    @check_gas
    @wait
    async def deposit_zklend(self, amount_wei):
        logger.info(f'[{self.id_account}][{self.address}] [ZKLEND] Deposit {amount_wei} ETH')

        approve_contract = self.get_contract(STARKNET_TOKENS["ETH"])

        approve_call = approve_contract.functions["approve"].prepare(
            ZKLEND_CONTRACT,
            amount_wei
        )

        deposit_call = Call(
            to_addr=ZKLEND_CONTRACT,
            selector=get_selector_from_name("deposit"),
            calldata=[STARKNET_TOKENS["ETH"], amount_wei],
        )

        tx_hash = await self.send_transaction([approve_call, deposit_call])
        return await self.verify_tx(tx_hash=tx_hash.transaction_hash)

    @retry
    @check_gas
    @wait
    async def withdraw_zklend(self):
        amount = await self.get_deposit_amount()

        logger.info(f'[{self.id_account}][{self.address}] [ZKLEND] Withdraw')

        if amount > 0:
            withdraw_all_call = Call(
                to_addr=ZKLEND_CONTRACT,
                selector=get_selector_from_name("withdraw_all"),
                calldata=[STARKNET_TOKENS["ETH"]],
            )

            tx_hash = await self.send_transaction([withdraw_all_call])
            return await self.verify_tx(tx_hash=tx_hash.transaction_hash)
        else:
            logger.error(f"[{self.id_account}][{hex(self.address)}] Deposit not found")