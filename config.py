starknet_rpc = "https://starknet-mainnet.infura.io/v3/f4281cedd4254996bf77b083db6b79f6"

cairo_version = 0

MIN_SLEEP_TIME = 1300
MAX_SLEEP_TIME = 4000

MIN_TRANSACTION = 10
MAX_TRANSACTION = 16

MIN_AMOUNT_ETH = 0.0005
MAX_AMOUNT_ETH = 0.001

MIN_AMOUNT_USDC = 0
MAX_AMOUNT_USDC = 0

ALL_BALANCE = True  # Берет 93% всего баланса

RETRY_COUNT = 3

MAX_GWEI = 15

# Шансы должны быть распределены так чтобы общая сумма получась 1.0 = 100%
TASKS_CHANCE = {"zklend": 0.6, "jediswap": 0.2, "dmail": 0.2}
