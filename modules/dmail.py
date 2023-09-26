import random
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from modules.starknet_client import StarknetClient

from constants import DMAIL_CONTRACT
from utils import retry, check_gas, wait


class Dmail(StarknetClient):
    def __init__(self, id_account: int, private_key: str):
        super().__init__(id_account, private_key)

    @staticmethod
    async def generate_mail_data():
        domain_list = ["@gmail.com", "@dmail.ai"]

        domain_address = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(5, 10)))
        theme = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(10, 20)))

        return domain_address + random.choice(domain_list), theme

    @retry
    @check_gas
    @wait
    async def send_mail(self):
        logger.info(f"[{self.id_account}][{hex(self.address)}] [Dmail] send mail")

        email_address, theme = await self.generate_mail_data()

        mint_starknet_id_call = Call(
            to_addr=DMAIL_CONTRACT,
            selector=get_selector_from_name("transaction"),
            calldata=[email_address, theme],
        )

        tx_hash = await self.send_transaction([mint_starknet_id_call])
        return await self.verify_tx(tx_hash=tx_hash.transaction_hash)
