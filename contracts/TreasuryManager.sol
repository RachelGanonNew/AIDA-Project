// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title TreasuryManager
 * @dev Hathor Nano Contract for automated treasury management
 * @notice This contract enables automated treasury rebalancing and asset management
 */
contract TreasuryManager is ReentrancyGuard, Ownable {
    
    struct Asset {
        address token;
        uint256 balance;
        uint256 targetAllocation;
        bool isActive;
    }
    
    struct RebalancingAction {
        address token;
        uint256 amount;
        bool isBuy; // true for buy, false for sell
        uint256 slippageTolerance;
    }
    
    // State variables
    mapping(address => Asset) public assets;
    address[] public assetList;
    address public daoAddress;
    address public dexRouter; // DEX router for swaps
    uint256 public rebalancingThreshold; // Minimum deviation to trigger rebalancing
    bool public rebalancingEnabled;
    
    // Events
    event AssetAdded(address indexed token, uint256 targetAllocation);
    event AssetRemoved(address indexed token);
    event TargetAllocationUpdated(address indexed token, uint256 newAllocation);
    event RebalancingExecuted(address indexed token, uint256 amount, bool isBuy);
    event TreasuryRebalanced(uint256 totalValue);
    
    // Modifiers
    modifier onlyDAO() {
        require(msg.sender == daoAddress, "Only DAO can call this function");
        _;
    }
    
    modifier onlyDAOOrOwner() {
        require(msg.sender == daoAddress || msg.sender == owner(), "Only DAO or owner can call this function");
        _;
    }
    
    modifier assetExists(address token) {
        require(assets[token].isActive, "Asset not found");
        _;
    }
    
    constructor(
        address _daoAddress,
        address _dexRouter,
        uint256 _rebalancingThreshold
    ) {
        daoAddress = _daoAddress;
        dexRouter = _dexRouter;
        rebalancingThreshold = _rebalancingThreshold;
        rebalancingEnabled = true;
    }
    
    /**
     * @dev Add a new asset to the treasury
     * @param token Token address
     * @param targetAllocation Target allocation percentage (basis points)
     */
    function addAsset(address token, uint256 targetAllocation) 
        external 
        onlyDAOOrOwner 
    {
        require(token != address(0), "Invalid token address");
        require(targetAllocation <= 10000, "Invalid allocation percentage");
        require(!assets[token].isActive, "Asset already exists");
        
        assets[token] = Asset({
            token: token,
            balance: 0,
            targetAllocation: targetAllocation,
            isActive: true
        });
        
        assetList.push(token);
        
        emit AssetAdded(token, targetAllocation);
    }
    
    /**
     * @dev Remove an asset from the treasury
     * @param token Token address
     */
    function removeAsset(address token) 
        external 
        onlyDAOOrOwner 
        assetExists(token) 
    {
        require(assets[token].balance == 0, "Asset has balance");
        
        assets[token].isActive = false;
        
        // Remove from asset list
        for (uint256 i = 0; i < assetList.length; i++) {
            if (assetList[i] == token) {
                assetList[i] = assetList[assetList.length - 1];
                assetList.pop();
                break;
            }
        }
        
        emit AssetRemoved(token);
    }
    
    /**
     * @dev Update target allocation for an asset
     * @param token Token address
     * @param newAllocation New target allocation percentage
     */
    function updateTargetAllocation(address token, uint256 newAllocation) 
        external 
        onlyDAOOrOwner 
        assetExists(token) 
    {
        require(newAllocation <= 10000, "Invalid allocation percentage");
        
        assets[token].targetAllocation = newAllocation;
        
        emit TargetAllocationUpdated(token, newAllocation);
    }
    
    /**
     * @dev Execute treasury rebalancing
     * @param actions Array of rebalancing actions
     */
    function rebalanceTreasury(RebalancingAction[] calldata actions) 
        external 
        onlyDAO 
        nonReentrant 
    {
        require(rebalancingEnabled, "Rebalancing disabled");
        
        for (uint256 i = 0; i < actions.length; i++) {
            RebalancingAction memory action = actions[i];
            
            require(assets[action.token].isActive, "Asset not active");
            
            if (action.isBuy) {
                // Buy more of the token
                _executeBuy(action.token, action.amount, action.slippageTolerance);
            } else {
                // Sell some of the token
                _executeSell(action.token, action.amount, action.slippageTolerance);
            }
            
            emit RebalancingExecuted(action.token, action.amount, action.isBuy);
        }
        
        emit TreasuryRebalanced(getTotalValue());
    }
    
    /**
     * @dev Execute a buy order
     * @param token Token to buy
     * @param amount Amount to buy
     * @param slippageTolerance Slippage tolerance in basis points
     */
    function _executeBuy(
        address token, 
        uint256 amount, 
        uint256 slippageTolerance
    ) internal {
        // This would integrate with a DEX like Uniswap
        // For now, just update the balance
        assets[token].balance += amount;
    }
    
    /**
     * @dev Execute a sell order
     * @param token Token to sell
     * @param amount Amount to sell
     * @param slippageTolerance Slippage tolerance in basis points
     */
    function _executeSell(
        address token, 
        uint256 amount, 
        uint256 slippageTolerance
    ) internal {
        require(assets[token].balance >= amount, "Insufficient balance");
        
        // This would integrate with a DEX like Uniswap
        // For now, just update the balance
        assets[token].balance -= amount;
    }
    
    /**
     * @dev Get current allocation percentages
     */
    function getCurrentAllocations() 
        external 
        view 
        returns (address[] memory tokens, uint256[] memory allocations) 
    {
        uint256 totalValue = getTotalValue();
        
        tokens = new address[](assetList.length);
        allocations = new uint256[](assetList.length);
        
        for (uint256 i = 0; i < assetList.length; i++) {
            address token = assetList[i];
            tokens[i] = token;
            
            if (totalValue > 0) {
                allocations[i] = (assets[token].balance * 10000) / totalValue;
            } else {
                allocations[i] = 0;
            }
        }
    }
    
    /**
     * @dev Get total treasury value (simplified - would use price feeds in production)
     */
    function getTotalValue() public view returns (uint256) {
        uint256 total = 0;
        
        for (uint256 i = 0; i < assetList.length; i++) {
            total += assets[assetList[i]].balance;
        }
        
        return total;
    }
    
    /**
     * @dev Check if rebalancing is needed
     */
    function needsRebalancing() external view returns (bool) {
        uint256 totalValue = getTotalValue();
        if (totalValue == 0) return false;
        
        for (uint256 i = 0; i < assetList.length; i++) {
            address token = assetList[i];
            uint256 currentAllocation = (assets[token].balance * 10000) / totalValue;
            uint256 targetAllocation = assets[token].targetAllocation;
            
            if (abs(currentAllocation, targetAllocation) > rebalancingThreshold) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * @dev Get rebalancing suggestions
     */
    function getRebalancingSuggestions() 
        external 
        view 
        returns (RebalancingAction[] memory suggestions) 
    {
        uint256 totalValue = getTotalValue();
        if (totalValue == 0) return new RebalancingAction[](0);
        
        // Count how many assets need rebalancing
        uint256 suggestionCount = 0;
        for (uint256 i = 0; i < assetList.length; i++) {
            address token = assetList[i];
            uint256 currentAllocation = (assets[token].balance * 10000) / totalValue;
            uint256 targetAllocation = assets[token].targetAllocation;
            
            if (abs(currentAllocation, targetAllocation) > rebalancingThreshold) {
                suggestionCount++;
            }
        }
        
        suggestions = new RebalancingAction[](suggestionCount);
        uint256 suggestionIndex = 0;
        
        for (uint256 i = 0; i < assetList.length; i++) {
            address token = assetList[i];
            uint256 currentAllocation = (assets[token].balance * 10000) / totalValue;
            uint256 targetAllocation = assets[token].targetAllocation;
            
            if (abs(currentAllocation, targetAllocation) > rebalancingThreshold) {
                uint256 targetBalance = (totalValue * targetAllocation) / 10000;
                uint256 currentBalance = assets[token].balance;
                
                suggestions[suggestionIndex] = RebalancingAction({
                    token: token,
                    amount: currentBalance > targetBalance ? 
                        currentBalance - targetBalance : 
                        targetBalance - currentBalance,
                    isBuy: currentBalance < targetBalance,
                    slippageTolerance: 200 // 2% default slippage
                });
                
                suggestionIndex++;
            }
        }
    }
    
    /**
     * @dev Emergency function to withdraw all assets
     */
    function emergencyWithdraw() external onlyOwner {
        rebalancingEnabled = false;
        
        for (uint256 i = 0; i < assetList.length; i++) {
            address token = assetList[i];
            uint256 balance = assets[token].balance;
            
            if (balance > 0) {
                if (token == address(0)) {
                    // ETH
                    payable(owner()).transfer(balance);
                } else {
                    // ERC20 token
                    IERC20(token).transfer(owner(), balance);
                }
                
                assets[token].balance = 0;
            }
        }
    }
    
    /**
     * @dev Update DAO address
     */
    function updateDAOAddress(address newDaoAddress) external onlyOwner {
        daoAddress = newDaoAddress;
    }
    
    /**
     * @dev Update DEX router
     */
    function updateDEXRouter(address newRouter) external onlyOwner {
        dexRouter = newRouter;
    }
    
    /**
     * @dev Update rebalancing threshold
     */
    function updateRebalancingThreshold(uint256 newThreshold) external onlyOwner {
        rebalancingThreshold = newThreshold;
    }
    
    /**
     * @dev Toggle rebalancing
     */
    function toggleRebalancing() external onlyOwner {
        rebalancingEnabled = !rebalancingEnabled;
    }
    
    /**
     * @dev Helper function to calculate absolute difference
     */
    function abs(uint256 a, uint256 b) internal pure returns (uint256) {
        return a > b ? a - b : b - a;
    }
    
    // Fallback function to receive ETH
    receive() external payable {}
} 