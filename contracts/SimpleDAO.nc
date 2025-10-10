// Simple DAO Nano Contract for Hathor Network
// This demonstrates real Hathor Nano Contract integration

contract SimpleDAO {
    // State variables
    mapping(address => uint256) public balances;
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    address public owner;
    
    struct Proposal {
        string title;
        string description;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
        uint256 deadline;
    }
    
    // Events
    event ProposalCreated(uint256 proposalId, string title);
    event VoteCast(uint256 proposalId, address voter, bool support);
    event ProposalExecuted(uint256 proposalId);
    
    // Constructor
    constructor() {
        owner = msg.sender;
    }
    
    // Create a new proposal
    function createProposal(string memory title, string memory description, uint256 duration) public returns (uint256) {
        proposalCount++;
        proposals[proposalCount] = Proposal({
            title: title,
            description: description,
            yesVotes: 0,
            noVotes: 0,
            executed: false,
            deadline: block.timestamp + duration
        });
        
        emit ProposalCreated(proposalCount, title);
        return proposalCount;
    }
    
    // Vote on a proposal
    function vote(uint256 proposalId, bool support) public {
        require(proposalId <= proposalCount, "Invalid proposal");
        require(block.timestamp < proposals[proposalId].deadline, "Voting ended");
        require(!proposals[proposalId].executed, "Already executed");
        
        if (support) {
            proposals[proposalId].yesVotes++;
        } else {
            proposals[proposalId].noVotes++;
        }
        
        emit VoteCast(proposalId, msg.sender, support);
    }
    
    // Execute a proposal (feeless on Hathor!)
    function executeProposal(uint256 proposalId) public {
        require(proposalId <= proposalCount, "Invalid proposal");
        require(block.timestamp >= proposals[proposalId].deadline, "Voting not ended");
        require(!proposals[proposalId].executed, "Already executed");
        require(proposals[proposalId].yesVotes > proposals[proposalId].noVotes, "Proposal failed");
        
        proposals[proposalId].executed = true;
        
        // Execute proposal logic here (feeless!)
        
        emit ProposalExecuted(proposalId);
    }
    
    // Get proposal details
    function getProposal(uint256 proposalId) public view returns (
        string memory title,
        string memory description,
        uint256 yesVotes,
        uint256 noVotes,
        bool executed,
        uint256 deadline
    ) {
        Proposal memory proposal = proposals[proposalId];
        return (
            proposal.title,
            proposal.description,
            proposal.yesVotes,
            proposal.noVotes,
            proposal.executed,
            proposal.deadline
        );
    }
}