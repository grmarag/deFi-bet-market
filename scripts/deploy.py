import os
from web3 import Web3
from src.market import PredictionMarket
from src.config import ETH_PROVIDER_URL, CONTRACTS_DIR

def main():
    w3 = Web3(Web3.HTTPProvider(ETH_PROVIDER_URL))
    if not w3.is_connected():
        print("Web3 not connected. Check your ETH_PROVIDER_URL.")
        return
    
    deployer_address = input("Enter deployer address: ").strip()
    private_key = input("Enter deployer private key: ").strip()
    question = input("Enter the market question: ").strip()
    
    contract_path = os.path.join(CONTRACTS_DIR, "PredictionMarket.sol")
    abi, bytecode = PredictionMarket.compile_contract(contract_path)
    market = PredictionMarket(w3, abi=abi, bytecode=bytecode)
    
    print("Deploying contract...")
    contract_address = market.deploy(question, deployer_address, private_key)
    print(f"Contract deployed at: {contract_address}")

if __name__ == "__main__":
    main()