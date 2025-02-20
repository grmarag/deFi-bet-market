from solcx import compile_standard, install_solc
from web3 import Web3

class PredictionMarket:
    def __init__(self, web3: Web3, contract_address: str = None, abi: list = None, bytecode: str = None):
        self.web3 = web3
        self.abi = abi
        self.bytecode = bytecode
        self.contract = None
        if contract_address and abi:
            self.contract = self.web3.eth.contract(address=contract_address, abi=abi)

    @staticmethod
    def compile_contract(contract_path: str, solc_version: str = "0.8.0"):
        install_solc(solc_version)
        with open(contract_path, "r") as file:
            contract_source_code = file.read()
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {
                "PredictionMarket.sol": {
                    "content": contract_source_code
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            }
        }, solc_version=solc_version)
        contract_interface = compiled_sol["contracts"]["PredictionMarket.sol"]["PredictionMarket"]
        abi = contract_interface["abi"]
        bytecode = contract_interface["evm"]["bytecode"]["object"]
        return abi, bytecode

    def deploy(self, question: str, deployer_address: str, private_key: str, gas: int = 3000000):
        if not self.bytecode or not self.abi:
            raise ValueError("Contract not compiled. Please compile the contract first.")
        contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        nonce = self.web3.eth.get_transaction_count(deployer_address)
        transaction = contract.constructor(question).build_transaction({
            'from': deployer_address,
            'nonce': nonce,
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price
        })
        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        self.contract = self.web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=self.abi
        )
        return tx_receipt.contractAddress

    def bet(self, voter_address: str, private_key: str, vote: bool, amount_wei: int, gas: int = 200000):
        nonce = self.web3.eth.get_transaction_count(voter_address)
        txn = self.contract.functions.bet(vote).build_transaction({
            'from': voter_address,
            'value': amount_wei,
            'nonce': nonce,
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price
        })
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def close_bets(self, owner_address: str, private_key: str, gas: int = 200000):
        nonce = self.web3.eth.get_transaction_count(owner_address)
        txn = self.contract.functions.closeBets().build_transaction({
            'from': owner_address,
            'nonce': nonce,
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price
        })
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def resolve(self, owner_address: str, private_key: str, outcome: bool, gas: int = 200000):
        nonce = self.web3.eth.get_transaction_count(owner_address)
        txn = self.contract.functions.resolve(outcome).build_transaction({
            'from': owner_address,
            'nonce': nonce,
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price
        })
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def withdraw(self, user_address: str, private_key: str, gas: int = 200000):
        nonce = self.web3.eth.get_transaction_count(user_address)
        txn = self.contract.functions.withdraw().build_transaction({
            'from': user_address,
            'nonce': nonce,
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price
        })
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_details(self):
        return {
            "owner": self.contract.functions.owner().call(),
            "question": self.contract.functions.question().call(),
            "betsOpen": self.contract.functions.betsOpen().call(),
            "resolved": self.contract.functions.resolved().call(),
            "totalYes": self.contract.functions.totalYes().call(),
            "totalNo": self.contract.functions.totalNo().call()
        }