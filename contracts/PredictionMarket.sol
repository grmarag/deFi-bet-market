// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PredictionMarket {
    address public owner;
    string public question;
    bool public resolved;
    bool public outcome; // true for "yes", false for "no".
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
        require(msg.sender == owner, "Only owner can call this");
        _;
    }
    
    // Place a bet by sending ETH. Pass 'true' for yes, 'false' for no.
    function bet(bool _vote) public payable {
        require(betsOpen, "Bets are closed");
        require(msg.value > 0, "Must bet some ETH");
        if (_vote) {
            betsYes[msg.sender] += msg.value;
            totalYes += msg.value;
        } else {
            betsNo[msg.sender] += msg.value;
            totalNo += msg.value;
        }
    }
    
    // Close betting – only callable by the owner.
    function closeBets() public onlyOwner {
        betsOpen = false;
    }
    
    // Resolve the market with the outcome (true/false) – only callable by the owner.
    function resolve(bool _outcome) public onlyOwner {
        require(!resolved, "Market already resolved");
        require(!betsOpen, "Bets still open");
        outcome = _outcome;
        resolved = true;
    }
    
    // Withdraw winnings based on the outcome.
    function withdraw() public {
        require(resolved, "Market not resolved");
        uint256 payout = 0;
        if (outcome == true) {
            // "Yes" wins.
            if (betsYes[msg.sender] > 0) {
                uint256 userBet = betsYes[msg.sender];
                uint256 share = (userBet * (totalYes + totalNo)) / totalYes;
                payout = share;
                betsYes[msg.sender] = 0; // Prevent re‑entrancy.
            }
        } else {
            // "No" wins.
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