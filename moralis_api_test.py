# moralis_api_test.py - QA for Moralis vs. Infura (block data)
import requests
import json
from difflib import unified_diff

MORALIS_API = "https://deep-index.moralis.io/api/v2/block/18000000?chain=eth"
INFURA_API = "https://mainnet.infura.io/v3/7873ac918d4d495ab413161a02ea9a09"  # Use free key

headers = {"x-api-key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImM5NjM1NTIyLWU2NTgtNGU1My1hMjkwLTFkN2I0MjJhNWQ1NCIsIm9yZ0lkIjoiNDgwMjQ0IiwidXNlcklkIjoiNDk0MDY3IiwidHlwZUlkIjoiNmUwY2QzZGUtODRhNS00ZTNhLWI2ODQtNTA0ODhkZmNjZTA4IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NjI2MjQxNzYsImV4cCI6NDkxODM4NDE3Nn0.-B5qlxpLjJkjrHESIMi9Q2OFkqfPGxLJLQsUTeTox4w"}  # Get free at moralis.io

def fetch_moralis():
    r = requests.get(MORALIS_API, headers=headers)
    return r.json() if r.status_code == 200 else None

def fetch_infura():
    payload = {"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x1123F10", True],"id":1}
    r = requests.post(INFURA_API, json=payload)
    return r.json()['result'] if 'result' in r.json() else None

moralis = fetch_moralis()
infura = fetch_infura()

# Validate structure
expected_keys = ['hash', 'number', 'timestamp', 'transactions']
missing = [k for k in expected_keys if k not in moralis]
if missing:
    print(f"❌ Moralis missing keys: {missing}")

# Compare critical fields
diff = '\n'.join(unified_diff(
    [moralis['hash']], [infura['hash']],
    fromfile='Moralis', tofile='Infura'
))
print("✅ Match!" if not diff else f"⚠️ Discrepancy:\n{diff}")