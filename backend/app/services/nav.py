from .eth import get_eth_balance_in_usd
from .solana import get_solana_balance_in_usd

TOTAL_SHARES = 10000  # can later move to DB

def calculate_nav_snapshot():
    eth_usd = get_eth_balance_in_usd()
    sol_usd = get_solana_balance_in_usd()
    total_aum = eth_usd + sol_usd

    nav_per_share = total_aum / TOTAL_SHARES

    return {
        "eth_usd": round(eth_usd, 2),
        "sol_usd": round(sol_usd, 2),
        "total_aum": round(total_aum, 2),
        "nav_per_share": round(nav_per_share, 6)
    }
