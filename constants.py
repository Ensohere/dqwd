import json

with open('data/private_keys.txt') as file:
    private_keys = [row.strip() for row in file]

with open('abis/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open('abis/zklend/abi.json') as file:
    ZKLEND_ABI = json.load(file)

with open('abis/jediswap/abi.json') as file:
    JEDISWAP_ABI = json.load(file)

with open('abis/dmail/abi.json') as file:
    DMAIL_ABI = json.load(file)

ARGENTX_PROXY_CLASS_HASH = 0x025EC026985A3BF9D0CC1FE17326B245DFDC3FF89B8FDE106542A3EA56C5A918
ARGENTX_IMPLEMENTATION_CLASS_HASH = 0x33434AD846CDD5F23EB73FF09FE6FDDD568284A0FB7D1BE20EE482F044DABE2
ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW = 0x01a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003

STARKNET_TOKENS = {
    "ETH": 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
    "USDC": 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
    "DAI": 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3
}

ZKLEND_CONTRACT = 0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05

ZKLEND_ETH_CONCTRACT = 0x01b5bd713e72fdc5d63ffd83762f81297f6175a5e0a4771cdadbc1dd5fe72cb1

JEDISWAP_CONTRACT = 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023

DMAIL_CONTRACT = 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309