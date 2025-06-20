import os
import requests

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY") 

ETH_WALLET_ADDRESS = "0x052e3082ED423F790D4D8A4756DC45A9CAf3D544"

def get_eth_balance_in_usd():
    try:
        # Step 1: Get ETH balance in Wei
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={ETH_WALLET_ADDRESS}&tag=latest&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url)
        data = response.json()
        eth_balance_wei = int(data['result'])
        eth_balance_eth = eth_balance_wei / 1e18

        # Step 2: Get ETH price from CoinGecko
        price_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        price_response = requests.get(price_url)
        price_data = price_response.json()
        eth_price = price_data['ethereum']['usd']

        # Step 3: Calculate USD value
        return eth_balance_eth * eth_price

    except Exception as e:
        print("ETH fetch error:", e)
        return 0.0
