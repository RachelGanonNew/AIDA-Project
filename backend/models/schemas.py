from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ProposalStatus(str, Enum):
    ACTIVE = "active"
    PASSED = "passed"
    FAILED = "failed"
    EXECUTED = "executed"

class ActionType(str, Enum):
    PROPOSAL_EXECUTION = "proposal_execution"
    TREASURY_REBALANCE = "treasury_rebalance"
    TOKEN_TRANSFER = "token_transfer"
    CONTRACT_INTERACTION = "contract_interaction"

# Request Models
class ProposalAnalysisRequest(BaseModel):
    dao_address: str = Field(..., description="DAO contract address")
    proposal_id: str = Field(..., description="Unique proposal identifier")
    title: str = Field(..., description="Proposal title")
    description: str = Field(..., description="Full proposal description")
    proposer: str = Field(..., description="Address of proposal creator")
    voting_start: Optional[datetime] = Field(None, description="Voting start time")
    voting_end: Optional[datetime] = Field(None, description="Voting end time")

class ActionExecutionRequest(BaseModel):
    action_type: ActionType = Field(..., description="Type of action to execute")
    dao_address: str = Field(..., description="DAO contract address")
    proposal_id: Optional[str] = Field(None, description="Related proposal ID if applicable")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    gas_limit: Optional[int] = Field(None, description="Gas limit for transaction")

# Response Models
class DAOHealthResponse(BaseModel):
    dao_address: str
    overall_health_score: float = Field(..., ge=0, le=1, description="Overall health score (0-1)")
    governance_score: float = Field(..., ge=0, le=1, description="Governance health score (0-1)")
    financial_score: float = Field(..., ge=0, le=1, description="Financial health score (0-1)")
    community_score: float = Field(..., ge=0, le=1, description="Community health score (0-1)")
    risk_factors: List[str] = Field(default_factory=list, description="List of identified risk factors")
    recommendations: List[str] = Field(default_factory=list, description="AI-generated recommendations")
    last_updated: datetime
    analysis_confidence: float = Field(..., ge=0, le=1, description="Confidence in analysis (0-1)")

class ProposalAnalysisResponse(BaseModel):
    proposal_id: str
    dao_address: str
    prediction: float = Field(..., ge=0, le=1, description="Predicted probability of passing (0-1)")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in prediction (0-1)")
    summary: str = Field(..., description="AI-generated summary of the proposal")
    risk_assessment: RiskLevel = Field(..., description="Risk level assessment")
    key_points: List[str] = Field(default_factory=list, description="Key points from the proposal")
    recommendations: List[str] = Field(default_factory=list, description="AI recommendations")
    sentiment_score: float = Field(..., ge=-1, le=1, description="Sentiment analysis score (-1 to 1)")
    impact_analysis: Dict[str, Any] = Field(default_factory=dict, description="Impact analysis details")
    created_at: datetime

class ProposalSummaryResponse(BaseModel):
    proposal_id: str
    title: str
    summary: str = Field(..., description="AI-generated summary")
    key_points: List[str] = Field(default_factory=list, description="Key points")
    risk_level: RiskLevel
    estimated_impact: str = Field(..., description="Estimated impact on DAO")
    voting_recommendation: str = Field(..., description="AI voting recommendation")
    created_at: datetime

class ActionExecutionResponse(BaseModel):
    action_id: str
    action_type: ActionType
    dao_address: str
    status: str = Field(..., description="Execution status")
    transaction_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    execution_time: Optional[datetime] = Field(None, description="When action was executed")
    gas_used: Optional[int] = Field(None, description="Gas used for execution")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime

class TreasuryAnalysisResponse(BaseModel):
    dao_address: str
    total_value_usd: float = Field(..., description="Total treasury value in USD")
    asset_diversification_score: float = Field(..., ge=0, le=1, description="Diversification score (0-1)")
    risk_score: float = Field(..., ge=0, le=1, description="Risk assessment score (0-1)")
    liquidity_score: float = Field(..., ge=0, le=1, description="Liquidity score (0-1)")
    top_holdings: List[Dict[str, Any]] = Field(default_factory=list, description="Top asset holdings")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    recommendations: List[str] = Field(default_factory=list, description="AI recommendations")
    rebalancing_suggestions: List[Dict[str, Any]] = Field(default_factory=list, description="Rebalancing suggestions")
    last_updated: datetime

class GovernanceMetricsResponse(BaseModel):
    dao_address: str
    total_proposals: int = Field(..., description="Total number of proposals")
    active_proposals: int = Field(..., description="Currently active proposals")
    average_voter_participation: float = Field(..., ge=0, le=1, description="Average voter participation rate")
    proposal_success_rate: float = Field(..., ge=0, le=1, description="Historical proposal success rate")
    average_voting_duration: float = Field(..., description="Average voting duration in hours")
    top_voters: List[Dict[str, Any]] = Field(default_factory=list, description="Top voting addresses")
    governance_trends: Dict[str, Any] = Field(default_factory=dict, description="Governance trend analysis")
    predictions: Dict[str, Any] = Field(default_factory=dict, description="AI predictions for future governance")
    last_updated: datetime

class CrossChainAssetResponse(BaseModel):
    dao_address: str
    total_cross_chain_value: float = Field(..., description="Total value across all chains")
    assets_by_chain: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict, description="Assets grouped by chain")
    chain_breakdown: Dict[str, float] = Field(default_factory=dict, description="Value breakdown by chain")
    risk_assessment: Dict[str, Any] = Field(default_factory=dict, description="Cross-chain risk assessment")
    recommendations: List[str] = Field(default_factory=list, description="Cross-chain optimization recommendations")
    last_updated: datetime

class PredictionResponse(BaseModel):
    dao_address: str
    predictions: List[Dict[str, Any]] = Field(default_factory=list, description="List of predictions")
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="Confidence scores for predictions")
    factors_considered: List[str] = Field(default_factory=list, description="Factors considered in predictions")
    last_updated: datetime

# Utility Models
class AssetHolding(BaseModel):
    symbol: str
    address: str
    balance: float
    value_usd: float
    percentage: float = Field(..., ge=0, le=1, description="Percentage of total treasury")

class RiskFactor(BaseModel):
    factor: str
    severity: RiskLevel
    description: str
    impact_score: float = Field(..., ge=0, le=1, description="Impact score (0-1)")
    mitigation_suggestions: List[str] = Field(default_factory=list, description="Mitigation suggestions")

class GovernanceTrend(BaseModel):
    metric: str
    current_value: float
    previous_value: float
    trend_direction: str = Field(..., description="up, down, or stable")
    change_percentage: float = Field(..., description="Percentage change")
    significance: str = Field(..., description="high, medium, or low") 