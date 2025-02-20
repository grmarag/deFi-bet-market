import os
from pathlib import Path

# Ethereum provider URL (defaults to local Ganache or geth).
ETH_PROVIDER_URL = os.getenv("ETH_PROVIDER_URL", "http://127.0.0.1:7545")

# Directory where Solidity contracts are located.
BASE_DIR = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = BASE_DIR / "contracts"