import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

from models.schemas import (
    ProposalAnalysisRequest, 
    ProposalAnalysisResponse, 
    ProposalSummaryResponse,
    RiskLevel
)
from services.ai_service import AIService
from services.dao_service import DAOService

logger = logging.getLogger(__name__)

class ProposalService:
    def __init__(self):
        """Initialize proposal service"""
        self.ai_service = AIService()
        self.dao_service = DAOService()
        
        # Mock storage for proposals (in production, would use database)
        self.proposals = {}
        self.analyses = {}
    
    async def analyze_proposal(self, request: ProposalAnalysisRequest) -> ProposalAnalysisResponse:
        """
        Analyze a governance proposal using AI
        """
        try:
            # Get DAO context for analysis
            dao_data = await self.dao_service._get_dao_data(request.dao_address)
            
            # Perform comprehensive AI analysis
            ai_analysis = await self.ai_service.analyze_proposal(
                request.description,
                request.proposer,
                dao_data
            )
            
            # Create analysis response
            analysis_response = ProposalAnalysisResponse(
                proposal_id=request.proposal_id,
                dao_address=request.dao_address,
                prediction=ai_analysis['prediction']['prediction'],
                confidence=ai_analysis['confidence'],
                summary=ai_analysis['summary'],
                risk_assessment=RiskLevel(ai_analysis['risk_assessment']['risk_level']),
                key_points=ai_analysis['key_points'],
                recommendations=ai_analysis['recommendations'],
                sentiment_score=ai_analysis['sentiment_score'],
                impact_analysis=ai_analysis['impact_analysis'],
                created_at=datetime.utcnow()
            )
            
            # Store analysis for later retrieval
            self.analyses[request.proposal_id] = analysis_response.dict()
            
            return analysis_response
        except Exception as e:
            logger.error(f"Error analyzing proposal: {e}")
            raise
    
    async def get_proposal_summary(self, proposal_id: str) -> ProposalSummaryResponse:
        """
        Get AI-generated summary of a proposal
        """
        try:
            # Check if we have stored analysis
            if proposal_id in self.analyses:
                analysis = self.analyses[proposal_id]
                
                return ProposalSummaryResponse(
                    proposal_id=proposal_id,
                    title=analysis.get('title', 'Proposal Analysis'),
                    summary=analysis['summary'],
                    key_points=analysis['key_points'],
                    risk_level=analysis['risk_assessment'],
                    estimated_impact=self._get_impact_description(analysis['impact_analysis']),
                    voting_recommendation=self._generate_voting_recommendation(analysis),
                    created_at=datetime.utcnow()
                )
            
            # If no stored analysis, generate a mock summary
            return await self._generate_mock_summary(proposal_id)
        except Exception as e:
            logger.error(f"Error getting proposal summary: {e}")
            raise
    
    async def get_proposal_predictions(self, dao_address: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get AI predictions for upcoming proposals
        """
        try:
            # Mock predictions based on historical data
            predictions = []
            
            # Generate mock upcoming proposals
            mock_proposals = [
                {
                    'id': f'prop_{i}',
                    'title': f'Proposal {i}: {self._get_mock_proposal_title(i)}',
                    'predicted_success': 0.65 + (i * 0.05),
                    'confidence': 0.7 + (i * 0.02),
                    'estimated_impact': 'medium',
                    'trending_topic': self._get_trending_topic(i)
                }
                for i in range(1, limit + 1)
            ]
            
            for proposal in mock_proposals:
                predictions.append({
                    'proposal_id': proposal['id'],
                    'title': proposal['title'],
                    'predicted_success_rate': proposal['predicted_success'],
                    'confidence': proposal['confidence'],
                    'estimated_impact': proposal['estimated_impact'],
                    'trending_topic': proposal['trending_topic'],
                    'key_factors': self._get_prediction_factors(proposal['predicted_success']),
                    'recommendation': self._get_prediction_recommendation(proposal['predicted_success'])
                })
            
            return predictions
        except Exception as e:
            logger.error(f"Error getting proposal predictions: {e}")
            return []
    
    async def store_analysis(self, request: ProposalAnalysisRequest):
        """
        Store proposal analysis in background
        """
        try:
            # Store proposal data
            self.proposals[request.proposal_id] = {
                'dao_address': request.dao_address,
                'title': request.title,
                'description': request.description,
                'proposer': request.proposer,
                'voting_start': request.voting_start,
                'voting_end': request.voting_end,
                'created_at': datetime.utcnow()
            }
            
            logger.info(f"Stored proposal analysis for {request.proposal_id}")
        except Exception as e:
            logger.error(f"Error storing proposal analysis: {e}")
    
    def _get_impact_description(self, impact_analysis: Dict[str, Any]) -> str:
        """Generate impact description from analysis"""
        try:
            impacts = []
            for impact_type, data in impact_analysis.items():
                if isinstance(data, dict) and 'score' in data:
                    score = data['score']
                    if score > 0.7:
                        impacts.append(f"High {impact_type.replace('_', ' ')} impact")
                    elif score > 0.4:
                        impacts.append(f"Medium {impact_type.replace('_', ' ')} impact")
                    else:
                        impacts.append(f"Low {impact_type.replace('_', ' ')} impact")
            
            if impacts:
                return "; ".join(impacts)
            return "Moderate overall impact"
        except Exception as e:
            logger.error(f"Error generating impact description: {e}")
            return "Impact analysis unavailable"
    
    def _generate_voting_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Generate voting recommendation based on analysis"""
        try:
            prediction = analysis.get('prediction', 0.5)
            risk_level = analysis.get('risk_assessment', 'medium')
            sentiment = analysis.get('sentiment_score', 0)
            
            if prediction > 0.7 and sentiment > 0.3:
                return "Strong recommendation to vote YES - high success probability with positive sentiment"
            elif prediction > 0.6 and risk_level == 'low':
                return "Recommend voting YES - good success probability with low risk"
            elif prediction < 0.4 or sentiment < -0.3:
                return "Recommend voting NO - low success probability or negative sentiment"
            elif risk_level == 'high':
                return "Exercise caution - high risk proposal, consider additional research"
            else:
                return "Neutral recommendation - consider all factors carefully"
        except Exception as e:
            logger.error(f"Error generating voting recommendation: {e}")
            return "Consider the proposal carefully before voting"
    
    async def _generate_mock_summary(self, proposal_id: str) -> ProposalSummaryResponse:
        """Generate mock summary for demonstration"""
        return ProposalSummaryResponse(
            proposal_id=proposal_id,
            title="Sample Governance Proposal",
            summary="This proposal aims to improve the DAO's governance structure by implementing new voting mechanisms and treasury management strategies.",
            key_points=[
                "Introduces new voting mechanism",
                "Updates treasury allocation strategy",
                "Improves governance transparency"
            ],
            risk_level=RiskLevel.MEDIUM,
            estimated_impact="Medium impact on governance and treasury management",
            voting_recommendation="Consider voting YES after reviewing detailed analysis",
            created_at=datetime.utcnow()
        )
    
    def _get_mock_proposal_title(self, index: int) -> str:
        """Generate mock proposal titles"""
        titles = [
            "Treasury Diversification Strategy",
            "Governance Token Distribution Update",
            "Smart Contract Security Enhancement",
            "Community Incentive Program",
            "Cross-Chain Integration Proposal",
            "DeFi Protocol Partnership",
            "Voting Mechanism Optimization",
            "Treasury Yield Farming Strategy",
            "Governance Framework Update",
            "Emergency Fund Establishment"
        ]
        return titles[(index - 1) % len(titles)]
    
    def _get_trending_topic(self, index: int) -> str:
        """Get trending topic for proposal"""
        topics = [
            "treasury_management",
            "governance_updates",
            "security_enhancement",
            "community_engagement",
            "cross_chain_integration",
            "defi_partnerships",
            "voting_optimization",
            "yield_farming",
            "framework_updates",
            "emergency_funds"
        ]
        return topics[(index - 1) % len(topics)]
    
    def _get_prediction_factors(self, success_rate: float) -> List[str]:
        """Get key factors affecting prediction"""
        factors = []
        
        if success_rate > 0.7:
            factors.extend(["High community support", "Clear proposal objectives", "Low risk assessment"])
        elif success_rate > 0.5:
            factors.extend(["Moderate community interest", "Standard proposal type", "Medium risk"])
        else:
            factors.extend(["Limited community engagement", "Complex proposal", "High risk factors"])
        
        return factors
    
    def _get_prediction_recommendation(self, success_rate: float) -> str:
        """Get recommendation based on prediction"""
        if success_rate > 0.7:
            return "High likelihood of success - consider supporting"
        elif success_rate > 0.5:
            return "Moderate success probability - review carefully"
        else:
            return "Low success probability - may need revision"
    
    async def get_proposal_history(self, dao_address: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get historical proposal data"""
        try:
            # Mock historical data
            history = []
            for i in range(limit):
                proposal_date = datetime.utcnow() - timedelta(days=i * 7)
                success = i % 3 != 0  # Mock success pattern
                
                history.append({
                    'proposal_id': f'hist_prop_{i}',
                    'title': f'Historical Proposal {i}',
                    'status': 'passed' if success else 'failed',
                    'voter_participation': 0.65 + (i * 0.02),
                    'created_at': proposal_date,
                    'voting_duration': 72 + (i * 2),
                    'total_votes': 850 + (i * 10)
                })
            
            return history
        except Exception as e:
            logger.error(f"Error getting proposal history: {e}")
            return []
    
    async def get_proposal_analytics(self, proposal_id: str) -> Dict[str, Any]:
        """Get detailed analytics for a specific proposal"""
        try:
            # Mock analytics data
            return {
                'proposal_id': proposal_id,
                'voting_trends': {
                    'hourly_participation': [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45],
                    'sentiment_over_time': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    'prediction_accuracy': 0.85
                },
                'community_engagement': {
                    'total_voters': 1250,
                    'unique_addresses': 980,
                    'average_vote_weight': 0.15,
                    'top_voter_impact': 0.25
                },
                'risk_metrics': {
                    'volatility_score': 0.3,
                    'complexity_score': 0.6,
                    'controversy_score': 0.4
                },
                'comparison_data': {
                    'similar_proposals': 5,
                    'average_success_rate': 0.68,
                    'benchmark_performance': 'above_average'
                }
            }
        except Exception as e:
            logger.error(f"Error getting proposal analytics: {e}")
            return {} 