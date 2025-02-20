import pytest
from web3 import Web3, EthereumTesterProvider
from src.market import PredictionMarket

# Fixture to create an EthereumTester instance.
@pytest.fixture
def eth_tester_instance():
    from eth_tester import EthereumTester
    return EthereumTester()

# Fixture to create a Web3 instance using the EthereumTesterProvider.
@pytest.fixture
def web3_instance(eth_tester_instance):
    w3 = Web3(EthereumTesterProvider(eth_tester_instance))
    return w3

# Fixture to retrieve the default private keys from EthereumTester.
@pytest.fixture
def default_private_keys(eth_tester_instance):
    # Use to_hex() since the keys are PrivateKey objects.
    return [key.to_hex() for key in eth_tester_instance.backend.account_keys]

# Fixture to compile the contract.
@pytest.fixture
def compiled_contract(tmp_path, web3_instance):
    # Write a temporary contract file.
    contract_code = '''
    pragma solidity ^0.8.0;

    contract PredictionMarket {
        address public owner;
        string public question;
        bool public resolved;
        bool public outcome;
        mapping(address => uint256) public betsYes;
        mapping(address => uint256) public betsNo;
        uint256 public totalYes;
        uint256 public totalNo;
        bool public betsOpen;
        
        constructor(string memory _question) {
            owner = msg.sender;
            question = _question;
            betsOpen = true;
            resolved = false;
        }
        
        modifier onlyOwner() {
            require(msg.sender == owner, "Only owner");
            _;
        }
        
        function bet(bool _vote) public payable {
            require(betsOpen, "Bets are closed");
            require(msg.value > 0, "Must bet some ETH");
            if(_vote) {
                betsYes[msg.sender] += msg.value;
                totalYes += msg.value;
            } else {
                betsNo[msg.sender] += msg.value;
                totalNo += msg.value;
            }
        }
        
        function closeBets() public onlyOwner {
            betsOpen = false;
        }
        
        function resolve(bool _outcome) public onlyOwner {
            require(!resolved, "Already resolved");
            require(!betsOpen, "Bets still open");
            outcome = _outcome;
            resolved = true;
        }
        
        function withdraw() public {
            require(resolved, "Market not resolved");
            uint256 payout = 0;
            if (outcome == true) {
                if (betsYes[msg.sender] > 0) {
                    uint256 userBet = betsYes[msg.sender];
                    uint256 share = (userBet * (totalYes + totalNo)) / totalYes;
                    payout = share;
                    betsYes[msg.sender] = 0;
                }
            } else {
                if (betsNo[msg.sender] > 0) {
                    uint256 userBet = betsNo[msg.sender];
                    uint256 share = (userBet * (totalYes + totalNo)) / totalNo;
                    payout = share;
                    betsNo[msg.sender] = 0;
                }
            }
            require(payout > 0, "Nothing to withdraw");
            payable(msg.sender).transfer(payout);
        }
    }
    '''
    contract_file = tmp_path / "PredictionMarket.sol"
    contract_file.write_text(contract_code)
    abi, bytecode = PredictionMarket.compile_contract(str(contract_file))
    return abi, bytecode

# Fixture to deploy the contract using auto-signing by EthereumTesterProvider.
@pytest.fixture
def deployed_market(web3_instance, compiled_contract):
    abi, bytecode = compiled_contract
    market = PredictionMarket(web3_instance, abi=abi, bytecode=bytecode)
    deployer = web3_instance.eth.accounts[0]
    # Deploy contract using a direct transaction (EthereumTesterProvider auto-signs)
    contract = web3_instance.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor("Test Market").transact({'from': deployer})
    tx_receipt = web3_instance.eth.wait_for_transaction_receipt(tx_hash)
    market.contract = web3_instance.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    return market

def test_deploy_market(web3_instance, compiled_contract, default_private_keys):
    abi, bytecode = compiled_contract
    market = PredictionMarket(web3_instance, abi=abi, bytecode=bytecode)
    deployer = web3_instance.eth.accounts[0]
    # Use the correct private key for the deployer account.
    deployer_key = default_private_keys[0]
    contract_address = market.deploy("Test Market", deployer, deployer_key)
    assert web3_instance.is_address(contract_address)

def test_bet_and_withdraw(deployed_market, web3_instance, default_private_keys):
    market = deployed_market
    voter = web3_instance.eth.accounts[1]
    owner = web3_instance.eth.accounts[0]
    # Use the correct private keys for voter and owner.
    voter_key = default_private_keys[1]
    owner_key = default_private_keys[0]
    
    # Place a bet from the voter.
    market.bet(voter, voter_key, True, 1000)
    
    # Owner closes bets and resolves the market with outcome True.
    market.close_bets(owner, owner_key)
    market.resolve(owner, owner_key, True)
    
    # Voter withdraws winnings.
    market.withdraw(voter, voter_key)
    
    # Check market details.
    details = market.get_details()
    assert details["resolved"] is True