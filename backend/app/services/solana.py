# import requests

# SOLANA_WALLET_ADDRESS = "BXKDAAAFYrPhkVRvyLHj2AQEa3PStHsBaWSY7errtEiM"

# def get_solana_balance_in_usd():
#     try:
#         # Step 1: Get SOL balance via public RPC
#         response = requests.post(
#             "https://api.mainnet-beta.solana.com",
#             json={
#                 "jsonrpc": "2.0",
#                 "id": 1,
#                 "method": "getBalance",
#                 "params": [SOLANA_WALLET_ADDRESS]
#             }
#         )
#         result = response.json()['result']['value']
#         sol_balance = result / 1e9  # Convert lamports to SOL

#         # Step 2: Get SOL price from CoinGecko
#         price_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
#         price_response = requests.get(price_url)
#         price_data = price_response.json()
#         sol_price = price_data['solana']['usd']

#         # Step 3: Calculate USD value
#         return sol_balance * sol_price

#     except Exception as e:
#         print("Solana fetch error:", e)
#         return 0.0


import requests

SOLANA_WALLET_ADDRESS = "BXKDAAAFYrPhkVRvyLHj2AQEa3PStHsBaWSY7errtEiM"

def get_solana_balance_in_usd():
    try:
        # ✅ Step 1: Get SOL balance
        response = requests.post(
            "https://api.mainnet-beta.solana.com",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [SOLANA_WALLET_ADDRESS]
            }
        )
        result = response.json().get('result', {}).get('value', 0)
        sol_balance = result / 1e9  # Convert lamports to SOL

        # ✅ Step 2: Get SOL price
        price_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        price_response = requests.get(price_url)
        price_data = price_response.json()

        sol_price = price_data.get('solana', {}).get('usd')
        if sol_price is None:
            raise ValueError("Could not get SOL price from CoinGecko")

        # ✅ Step 3: Return USD value
        return sol_balance * sol_price

    except Exception as e:
        print("Solana fetch error:", e)
        return 0.0
