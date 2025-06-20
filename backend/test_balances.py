
from dotenv import load_dotenv
load_dotenv()


from app.services.eth import get_eth_balance_in_usd
from app.services.solana import get_solana_balance_in_usd

print("ETH in USD:", get_eth_balance_in_usd())
print("SOL in USD:", get_solana_balance_in_usd())
