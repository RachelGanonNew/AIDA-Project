// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ProposalExecutor
 * @dev Hathor Nano Contract for automated proposal execution
 * @notice This contract enables one-click execution of approved DAO proposals
 */
contract ProposalExecutor {
    
    struct Proposal {
        uint256 id;
        address proposer;
        string title;
        string description;
        uint256 votingStart;
        uint256 votingEnd;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
        bool passed;
        mapping(address => bool) hasVoted;
    }
    
    struct ExecutionAction {
        address target;
        uint256 value;
        bytes data;
        string description;
    }
    
    // State variables
    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => ExecutionAction[]) public proposalActions;
    uint256 public proposalCount;
    address public daoAddress;
    address public owner;
    
    // Events
    event ProposalCreated(uint256 indexed proposalId, address indexed proposer, string title);
    event ProposalExecuted(uint256 indexed proposalId, address indexed executor);
    event ActionExecuted(uint256 indexed proposalId, address indexed target, bool success);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyDAO() {
        require(msg.sender == daoAddress, "Only DAO can call this function");
        _;
    }
    
    modifier proposalExists(uint256 proposalId) {
        require(proposalId > 0 && proposalId <= proposalCount, "Proposal does not exist");
        _;
    }
    
    modifier proposalNotExecuted(uint256 proposalId) {
        require(!proposals[proposalId].executed, "Proposal already executed");
        _;
    }
    
    constructor(address _daoAddress) {
        daoAddress = _daoAddress;
        owner = msg.sender;
    }
    
    /**
     * @dev Create a new proposal
     * @param title Proposal title
     * @param description Proposal description
     * @param votingDuration Duration of voting period in seconds
     */
    function createProposal(
        string memory title,
        string memory description,
        uint256 votingDuration
    ) external onlyDAO returns (uint256) {
        proposalCount++;
        uint256 proposalId = proposalCount;
        
        Proposal storage proposal = proposals[proposalId];
        proposal.id = proposalId;
        proposal.proposer = msg.sender;
        proposal.title = title;
        proposal.description = description;
        proposal.votingStart = block.timestamp;
        proposal.votingEnd = block.timestamp + votingDuration;
        proposal.executed = false;
        proposal.passed = false;
        
        emit ProposalCreated(proposalId, msg.sender, title);
        return proposalId;
    }
    
    /**
     * @dev Add execution action to a proposal
     * @param proposalId ID of the proposal
     * @param target Target contract address
     * @param value ETH value to send
     * @param data Calldata for the action
     * @param description Description of the action
     */
    function addExecutionAction(
        uint256 proposalId,
        address target,
        uint256 value,
        bytes memory data,
        string memory description
    ) external onlyDAO proposalExists(proposalId) {
        ExecutionAction memory action = ExecutionAction({
            target: target,
            value: value,
            data: data,
            description: description
        });
        
        proposalActions[proposalId].push(action);
    }
    
    /**
     * @dev Execute a passed proposal
     * @param proposalId ID of the proposal to execute
     */
    function executeProposal(uint256 proposalId) 
        external 
        onlyDAO 
        proposalExists(proposalId) 
        proposalNotExecuted(proposalId) 
    {
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp >= proposal.votingEnd, "Voting period not ended");
        require(proposal.yesVotes > proposal.noVotes, "Proposal not passed");
        
        proposal.executed = true;
        proposal.passed = true;
        
        // Execute all actions
        ExecutionAction[] storage actions = proposalActions[proposalId];
        for (uint256 i = 0; i < actions.length; i++) {
            ExecutionAction memory action = actions[i];
            
            (bool success, ) = action.target.call{value: action.value}(action.data);
            
            emit ActionExecuted(proposalId, action.target, success);
        }
        
        emit ProposalExecuted(proposalId, msg.sender);
    }
    
    /**
     * @dev Vote on a proposal
     * @param proposalId ID of the proposal
     * @param support True for yes, false for no
     */
    function vote(uint256 proposalId, bool support) external onlyDAO {
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp >= proposal.votingStart, "Voting not started");
        require(block.timestamp < proposal.votingEnd, "Voting ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        
        proposal.hasVoted[msg.sender] = true;
        
        if (support) {
            proposal.yesVotes++;
        } else {
            proposal.noVotes++;
        }
    }
    
    /**
     * @dev Get proposal details
     * @param proposalId ID of the proposal
     */
    function getProposal(uint256 proposalId) 
        external 
        view 
        proposalExists(proposalId) 
        returns (
            uint256 id,
            address proposer,
            string memory title,
            string memory description,
            uint256 votingStart,
            uint256 votingEnd,
            uint256 yesVotes,
            uint256 noVotes,
            bool executed,
            bool passed
        ) 
    {
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.id,
            proposal.proposer,
            proposal.title,
            proposal.description,
            proposal.votingStart,
            proposal.votingEnd,
            proposal.yesVotes,
            proposal.noVotes,
            proposal.executed,
            proposal.passed
        );
    }
    
    /**
     * @dev Get execution actions for a proposal
     * @param proposalId ID of the proposal
     */
    function getProposalActions(uint256 proposalId) 
        external 
        view 
        proposalExists(proposalId) 
        returns (ExecutionAction[] memory) 
    {
        return proposalActions[proposalId];
    }
    
    /**
     * @dev Check if an address has voted on a proposal
     * @param proposalId ID of the proposal
     * @param voter Address to check
     */
    function hasVoted(uint256 proposalId, address voter) 
        external 
        view 
        proposalExists(proposalId) 
        returns (bool) 
    {
        return proposals[proposalId].hasVoted[voter];
    }
    
    /**
     * @dev Update DAO address (only owner)
     * @param newDaoAddress New DAO address
     */
    function updateDAOAddress(address newDaoAddress) external onlyOwner {
        daoAddress = newDaoAddress;
    }
    
    /**
     * @dev Transfer ownership (only owner)
     * @param newOwner New owner address
     */
    function transferOwnership(address newOwner) external onlyOwner {
        owner = newOwner;
    }
    
    // Fallback function to receive ETH
    receive() external payable {}
} 