import asyncio
import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import httpx

from models.schemas import ActionExecutionRequest, ActionExecutionResponse, ActionType

logger = logging.getLogger(__name__)

class HathorService:
    def __init__(self):
        """Initialize Hathor service"""
        self.node_url = "https://node1.testnet.hathor.network/"
        self.evm_bridge_url = "https://evm-bridge.testnet.hathor.network/"
        
        # Mock Nano Contract addresses (in production, these would be deployed contracts)
        self.nano_contracts = {
            'proposal_executor': '0x1234567890123456789012345678901234567890',
            'treasury_manager': '0x2345678901234567890123456789012345678901',
            'governance_voter': '0x3456789012345678901234567890123456789012'
        }
        
        # Mock transaction hashes for demonstration
        self.mock_tx_hashes = [
            '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            '0xbcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab',
            '0xcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abc'
        ]
    
    async def execute_action(self, request: ActionExecutionRequest) -> ActionExecutionResponse:
        """
        Execute automated action using Hathor Nano Contracts
        """
        try:
            action_id = str(uuid.uuid4())
            
            # Validate action parameters
            await self._validate_action_parameters(request)
            
            # Execute based on action type
            if request.action_type == ActionType.PROPOSAL_EXECUTION:
                result = await self._execute_proposal(request)
            elif request.action_type == ActionType.TREASURY_REBALANCE:
                result = await self._execute_treasury_rebalance(request)
            elif request.action_type == ActionType.TOKEN_TRANSFER:
                result = await self._execute_token_transfer(request)
            elif request.action_type == ActionType.CONTRACT_INTERACTION:
                result = await self._execute_contract_interaction(request)
            else:
                raise ValueError(f"Unsupported action type: {request.action_type}")
            
            # Create response
            response = ActionExecutionResponse(
                action_id=action_id,
                action_type=request.action_type,
                dao_address=request.dao_address,
                status=result['status'],
                transaction_hash=result.get('transaction_hash'),
                execution_time=result.get('execution_time'),
                gas_used=result.get('gas_used'),
                error_message=result.get('error_message'),
                created_at=datetime.utcnow()
            )
            
            # Log execution
            await self._log_action_execution(response)
            
            return response
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return ActionExecutionResponse(
                action_id=str(uuid.uuid4()),
                action_type=request.action_type,
                dao_address=request.dao_address,
                status="failed",
                error_message=str(e),
                created_at=datetime.utcnow()
            )
    
    async def _validate_action_parameters(self, request: ActionExecutionRequest):
        """Validate action parameters"""
        if not request.dao_address:
            raise ValueError("DAO address is required")
        
        if request.action_type == ActionType.PROPOSAL_EXECUTION:
            if not request.proposal_id:
                raise ValueError("Proposal ID is required for proposal execution")
        
        if request.action_type == ActionType.TREASURY_REBALANCE:
            if 'target_allocation' not in request.parameters:
                raise ValueError("Target allocation is required for treasury rebalancing")
    
    async def _execute_proposal(self, request: ActionExecutionRequest) -> Dict[str, Any]:
        """Execute a governance proposal"""
        try:
            # Mock proposal execution using Nano Contract
            contract_address = self.nano_contracts['proposal_executor']
            
            # Simulate contract interaction
            execution_data = {
                'contract_address': contract_address,
                'method': 'executeProposal',
                'parameters': {
                    'proposalId': request.proposal_id,
                    'daoAddress': request.dao_address,
                    'executor': '0x1234567890123456789012345678901234567890'
                }
            }
            
            # Mock transaction execution
            tx_hash = self._generate_mock_tx_hash()
            gas_used = 150000  # Mock gas usage
            
            return {
                'status': 'executed',
                'transaction_hash': tx_hash,
                'execution_time': datetime.utcnow(),
                'gas_used': gas_used,
                'execution_data': execution_data
            }
        except Exception as e:
            logger.error(f"Error executing proposal: {e}")
            return {
                'status': 'failed',
                'error_message': str(e)
            }
    
    async def _execute_treasury_rebalance(self, request: ActionExecutionRequest) -> Dict[str, Any]:
        """Execute treasury rebalancing"""
        try:
            contract_address = self.nano_contracts['treasury_manager']
            target_allocation = request.parameters.get('target_allocation', {})
            
            # Validate target allocation
            total_percentage = sum(target_allocation.values())
            if abs(total_percentage - 1.0) > 0.01:
                raise ValueError("Target allocation percentages must sum to 100%")
            
            # Simulate rebalancing execution
            execution_data = {
                'contract_address': contract_address,
                'method': 'rebalanceTreasury',
                'parameters': {
                    'daoAddress': request.dao_address,
                    'targetAllocation': target_allocation,
                    'slippageTolerance': request.parameters.get('slippage_tolerance', 0.02)
                }
            }
            
            tx_hash = self._generate_mock_tx_hash()
            gas_used = 200000  # Higher gas for complex operation
            
            return {
                'status': 'executed',
                'transaction_hash': tx_hash,
                'execution_time': datetime.utcnow(),
                'gas_used': gas_used,
                'execution_data': execution_data
            }
        except Exception as e:
            logger.error(f"Error executing treasury rebalance: {e}")
            return {
                'status': 'failed',
                'error_message': str(e)
            }
    
    async def _execute_token_transfer(self, request: ActionExecutionRequest) -> Dict[str, Any]:
        """Execute token transfer"""
        try:
            # Validate transfer parameters
            required_params = ['recipient', 'amount', 'token_address']
            for param in required_params:
                if param not in request.parameters:
                    raise ValueError(f"Parameter '{param}' is required for token transfer")
            
            # Simulate transfer execution
            execution_data = {
                'method': 'transfer',
                'parameters': {
                    'recipient': request.parameters['recipient'],
                    'amount': request.parameters['amount'],
                    'tokenAddress': request.parameters['token_address'],
                    'daoAddress': request.dao_address
                }
            }
            
            tx_hash = self._generate_mock_tx_hash()
            gas_used = 65000  # Standard transfer gas
            
            return {
                'status': 'executed',
                'transaction_hash': tx_hash,
                'execution_time': datetime.utcnow(),
                'gas_used': gas_used,
                'execution_data': execution_data
            }
        except Exception as e:
            logger.error(f"Error executing token transfer: {e}")
            return {
                'status': 'failed',
                'error_message': str(e)
            }
    
    async def _execute_contract_interaction(self, request: ActionExecutionRequest) -> Dict[str, Any]:
        """Execute generic contract interaction"""
        try:
            contract_address = request.parameters.get('contract_address')
            method = request.parameters.get('method')
            
            if not contract_address or not method:
                raise ValueError("Contract address and method are required")
            
            # Simulate contract interaction
            execution_data = {
                'contract_address': contract_address,
                'method': method,
                'parameters': request.parameters.get('method_parameters', {}),
                'daoAddress': request.dao_address
            }
            
            tx_hash = self._generate_mock_tx_hash()
            gas_used = request.parameters.get('estimated_gas', 100000)
            
            return {
                'status': 'executed',
                'transaction_hash': tx_hash,
                'execution_time': datetime.utcnow(),
                'gas_used': gas_used,
                'execution_data': execution_data
            }
        except Exception as e:
            logger.error(f"Error executing contract interaction: {e}")
            return {
                'status': 'failed',
                'error_message': str(e)
            }
    
    async def get_cross_chain_assets(self, dao_address: str) -> Dict[str, Any]:
        """
        Get cross-chain asset analysis via Hathor EVM Bridge
        """
        try:
            # Mock cross-chain data
            cross_chain_assets = {
                'ethereum': [
                    {
                        'symbol': 'ETH',
                        'address': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
                        'balance': 200,
                        'value_usd': 400000,
                        'bridge_status': 'active'
                    },
                    {
                        'symbol': 'USDC',
                        'address': '0xA0b86a33E6441b8c4C8C8C8C8C8C8C8C8C8C8C8C8',
                        'balance': 500000,
                        'value_usd': 500000,
                        'bridge_status': 'active'
                    }
                ],
                'polygon': [
                    {
                        'symbol': 'MATIC',
                        'address': '0x0000000000000000000000000000000000001010',
                        'balance': 10000,
                        'value_usd': 8000,
                        'bridge_status': 'active'
                    }
                ],
                'arbitrum': [
                    {
                        'symbol': 'ARB',
                        'address': '0x912CE59144191C1204E64559FE8253a0e49E6548',
                        'balance': 5000,
                        'value_usd': 5000,
                        'bridge_status': 'pending'
                    }
                ]
            }
            
            # Calculate totals
            total_value = sum(
                sum(asset['value_usd'] for asset in chain_assets)
                for chain_assets in cross_chain_assets.values()
            )
            
            # Generate chain breakdown
            chain_breakdown = {}
            for chain, assets in cross_chain_assets.items():
                chain_value = sum(asset['value_usd'] for asset in assets)
                chain_breakdown[chain] = chain_value / total_value if total_value > 0 else 0
            
            # Risk assessment
            risk_assessment = await self._assess_cross_chain_risk(cross_chain_assets)
            
            # Generate recommendations
            recommendations = await self._generate_cross_chain_recommendations(
                cross_chain_assets, risk_assessment
            )
            
            return {
                'dao_address': dao_address,
                'total_cross_chain_value': total_value,
                'assets_by_chain': cross_chain_assets,
                'chain_breakdown': chain_breakdown,
                'risk_assessment': risk_assessment,
                'recommendations': recommendations,
                'last_updated': datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error getting cross-chain assets: {e}")
            raise
    
    async def _assess_cross_chain_risk(self, cross_chain_assets: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Assess cross-chain risks"""
        risks = []
        risk_score = 0.0
        
        # Bridge risks
        for chain, assets in cross_chain_assets.items():
            for asset in assets:
                if asset['bridge_status'] == 'pending':
                    risks.append(f"Pending bridge transaction for {asset['symbol']} on {chain}")
                    risk_score += 0.2
        
        # Concentration risks
        total_value = sum(
            sum(asset['value_usd'] for asset in chain_assets)
            for chain_assets in cross_chain_assets.values()
        )
        
        for chain, assets in cross_chain_assets.items():
            chain_value = sum(asset['value_usd'] for asset in assets)
            if chain_value / total_value > 0.7:
                risks.append(f"High concentration on {chain} chain")
                risk_score += 0.3
        
        # Liquidity risks
        for chain, assets in cross_chain_assets.items():
            for asset in assets:
                if asset['value_usd'] > 100000 and asset['symbol'] not in ['USDC', 'USDT', 'DAI']:
                    risks.append(f"Large illiquid position in {asset['symbol']} on {chain}")
                    risk_score += 0.1
        
        return {
            'risk_score': min(1.0, risk_score),
            'risk_factors': risks,
            'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low'
        }
    
    async def _generate_cross_chain_recommendations(self, cross_chain_assets: Dict[str, List[Dict[str, Any]]], 
                                                   risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate cross-chain optimization recommendations"""
        recommendations = []
        
        if risk_assessment['risk_score'] > 0.7:
            recommendations.append("Consider consolidating assets to reduce cross-chain complexity")
        
        # Check for pending transactions
        pending_count = sum(
            sum(1 for asset in assets if asset['bridge_status'] == 'pending')
            for assets in cross_chain_assets.values()
        )
        
        if pending_count > 0:
            recommendations.append(f"Monitor {pending_count} pending bridge transactions")
        
        # Diversification recommendations
        chain_count = len(cross_chain_assets)
        if chain_count > 3:
            recommendations.append("Consider reducing the number of chains to simplify management")
        elif chain_count < 2:
            recommendations.append("Consider diversifying across multiple chains for better risk distribution")
        
        if not recommendations:
            recommendations.append("Cross-chain allocation appears optimal")
        
        return recommendations
    
    def _generate_mock_tx_hash(self) -> str:
        """Generate mock transaction hash"""
        import random
        return random.choice(self.mock_tx_hashes)
    
    async def _log_action_execution(self, response: ActionExecutionResponse):
        """Log action execution for monitoring"""
        logger.info(f"Action executed: {response.action_id} - {response.action_type} - {response.status}")
        
        if response.status == 'failed':
            logger.error(f"Action failed: {response.error_message}")
    
    async def get_nano_contract_status(self, contract_address: str) -> Dict[str, Any]:
        """Get Nano Contract status and health"""
        try:
            # Mock contract status
            return {
                'contract_address': contract_address,
                'status': 'active',
                'last_activity': datetime.utcnow(),
                'total_transactions': 150,
                'success_rate': 0.98,
                'gas_efficiency': 0.85,
                'deployment_date': datetime.utcnow() - timedelta(days=30)
            }
        except Exception as e:
            logger.error(f"Error getting contract status: {e}")
            return {}
    
    async def estimate_gas_cost(self, action_type: ActionType, parameters: Dict[str, Any]) -> int:
        """Estimate gas cost for action execution"""
        try:
            # Mock gas estimation
            base_costs = {
                ActionType.PROPOSAL_EXECUTION: 150000,
                ActionType.TREASURY_REBALANCE: 200000,
                ActionType.TOKEN_TRANSFER: 65000,
                ActionType.CONTRACT_INTERACTION: 100000
            }
            
            base_cost = base_costs.get(action_type, 100000)
            
            # Adjust based on complexity
            complexity_multiplier = 1.0
            if 'complexity' in parameters:
                complexity_multiplier = parameters['complexity']
            
            return int(base_cost * complexity_multiplier)
        except Exception as e:
            logger.error(f"Error estimating gas cost: {e}")
            return 100000  # Default estimate 