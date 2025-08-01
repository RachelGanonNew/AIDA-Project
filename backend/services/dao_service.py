import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
import logging

from models.database import get_db, DAO, DAOHealthReport, Proposal
from models.schemas import DAOHealthResponse, GovernanceMetricsResponse
from services.ai_service import AIService

logger = logging.getLogger(__name__)

class DAOService:
    def __init__(self):
        """Initialize DAO service"""
        self.ai_service = AIService()
    
    async def analyze_dao_health(self, dao_address: str) -> DAOHealthResponse:
        """
        Comprehensive DAO health analysis
        """
        try:
            # Get DAO data
            dao_data = await self._get_dao_data(dao_address)
            
            # Analyze different aspects
            governance_score = await self._analyze_governance_health(dao_data)
            financial_score = await self._analyze_financial_health(dao_data)
            community_score = await self._analyze_community_health(dao_data)
            
            # Calculate overall health score
            overall_score = (governance_score + financial_score + community_score) / 3
            
            # Identify risk factors
            risk_factors = await self._identify_risk_factors(dao_data, governance_score, financial_score, community_score)
            
            # Generate recommendations
            recommendations = await self._generate_health_recommendations(
                overall_score, governance_score, financial_score, community_score, risk_factors
            )
            
            # Calculate confidence
            confidence = self._calculate_health_confidence(dao_data)
            
            return DAOHealthResponse(
                dao_address=dao_address,
                overall_health_score=overall_score,
                governance_score=governance_score,
                financial_score=financial_score,
                community_score=community_score,
                risk_factors=risk_factors,
                recommendations=recommendations,
                last_updated=datetime.utcnow(),
                analysis_confidence=confidence
            )
        except Exception as e:
            logger.error(f"Error analyzing DAO health: {e}")
            raise
    
    async def _get_dao_data(self, dao_address: str) -> Dict[str, Any]:
        """Get comprehensive DAO data"""
        # Mock data - in production this would come from blockchain and database
        return {
            'address': dao_address,
            'name': 'Sample DAO',
            'treasury_value': 2500000,  # $2.5M
            'total_members': 1250,
            'active_members': 850,
            'total_proposals': 45,
            'active_proposals': 3,
            'passed_proposals': 32,
            'failed_proposals': 10,
            'avg_voter_participation': 0.68,
            'avg_voting_duration': 72,  # hours
            'treasury_assets': [
                {'symbol': 'USDC', 'value_usd': 1000000, 'percentage': 0.4},
                {'symbol': 'ETH', 'value_usd': 800000, 'percentage': 0.32},
                {'symbol': 'UNI', 'value_usd': 400000, 'percentage': 0.16},
                {'symbol': 'AAVE', 'value_usd': 300000, 'percentage': 0.12}
            ],
            'recent_activity': {
                'proposals_last_30_days': 8,
                'votes_last_30_days': 1250,
                'treasury_changes_last_30_days': 3
            },
            'governance_parameters': {
                'quorum': 0.1,  # 10%
                'voting_period': 168,  # hours
                'execution_delay': 24  # hours
            }
        }
    
    async def _analyze_governance_health(self, dao_data: Dict[str, Any]) -> float:
        """Analyze governance health score"""
        try:
            # Calculate various governance metrics
            proposal_success_rate = dao_data['passed_proposals'] / max(dao_data['total_proposals'], 1)
            voter_participation = dao_data['avg_voter_participation']
            activity_level = min(dao_data['recent_activity']['proposals_last_30_days'] / 10, 1.0)
            
            # Weight the factors
            governance_score = (
                proposal_success_rate * 0.3 +
                voter_participation * 0.4 +
                activity_level * 0.3
            )
            
            return min(1.0, max(0.0, governance_score))
        except Exception as e:
            logger.error(f"Error analyzing governance health: {e}")
            return 0.5
    
    async def _analyze_financial_health(self, dao_data: Dict[str, Any]) -> float:
        """Analyze financial health score"""
        try:
            # Analyze treasury health using AI service
            treasury_data = {
                'assets': dao_data['treasury_assets'],
                'total_value': dao_data['treasury_value']
            }
            
            treasury_analysis = await self.ai_service.analyze_treasury_health(treasury_data)
            
            # Calculate financial health based on treasury analysis
            diversification = treasury_analysis.get('diversification_score', 0.5)
            risk_score = treasury_analysis.get('risk_score', 0.5)
            liquidity = treasury_analysis.get('liquidity_score', 0.5)
            
            # Weight the factors (lower risk is better, so we invert it)
            financial_score = (
                diversification * 0.4 +
                (1 - risk_score) * 0.4 +
                liquidity * 0.2
            )
            
            return min(1.0, max(0.0, financial_score))
        except Exception as e:
            logger.error(f"Error analyzing financial health: {e}")
            return 0.5
    
    async def _analyze_community_health(self, dao_data: Dict[str, Any]) -> float:
        """Analyze community health score"""
        try:
            # Calculate community metrics
            member_activity_rate = dao_data['active_members'] / max(dao_data['total_members'], 1)
            recent_engagement = min(dao_data['recent_activity']['votes_last_30_days'] / 1000, 1.0)
            
            # Mock community sentiment (in production, would analyze social media, forums, etc.)
            community_sentiment = 0.7  # Mock value
            
            # Weight the factors
            community_score = (
                member_activity_rate * 0.4 +
                recent_engagement * 0.4 +
                community_sentiment * 0.2
            )
            
            return min(1.0, max(0.0, community_score))
        except Exception as e:
            logger.error(f"Error analyzing community health: {e}")
            return 0.5
    
    async def _identify_risk_factors(self, dao_data: Dict[str, Any], 
                                   governance_score: float, financial_score: float, 
                                   community_score: float) -> List[str]:
        """Identify risk factors based on analysis"""
        risk_factors = []
        
        # Governance risks
        if governance_score < 0.6:
            risk_factors.append("Low voter participation rate")
        if dao_data['avg_voter_participation'] < 0.5:
            risk_factors.append("Insufficient quorum participation")
        if dao_data['recent_activity']['proposals_last_30_days'] < 3:
            risk_factors.append("Low governance activity")
        
        # Financial risks
        if financial_score < 0.6:
            risk_factors.append("Treasury concentration risk")
        if dao_data['treasury_value'] < 100000:  # Less than $100k
            risk_factors.append("Low treasury value")
        
        # Community risks
        if community_score < 0.6:
            risk_factors.append("Declining community engagement")
        if dao_data['active_members'] / dao_data['total_members'] < 0.5:
            risk_factors.append("Low active member ratio")
        
        # Add some mock risk factors for demonstration
        if not risk_factors:
            risk_factors.append("No significant risks identified")
        
        return risk_factors
    
    async def _generate_health_recommendations(self, overall_score: float, 
                                             governance_score: float, financial_score: float, 
                                             community_score: float, risk_factors: List[str]) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if overall_score < 0.7:
            recommendations.append("Consider implementing governance incentives to increase participation")
        
        if governance_score < 0.6:
            recommendations.append("Review and potentially lower quorum requirements")
            recommendations.append("Implement proposal templates to improve quality")
        
        if financial_score < 0.6:
            recommendations.append("Diversify treasury holdings to reduce concentration risk")
            recommendations.append("Consider establishing a treasury management policy")
        
        if community_score < 0.6:
            recommendations.append("Launch community engagement initiatives")
            recommendations.append("Improve communication channels and transparency")
        
        # Add AI-generated recommendations
        if risk_factors:
            recommendations.append(f"Address identified risks: {', '.join(risk_factors[:2])}")
        
        if not recommendations:
            recommendations.append("DAO appears healthy - maintain current practices")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _calculate_health_confidence(self, dao_data: Dict[str, Any]) -> float:
        """Calculate confidence in health analysis"""
        # Mock confidence calculation based on data completeness
        data_completeness = 0.8  # Mock value
        analysis_quality = 0.9   # Mock value
        
        confidence = (data_completeness + analysis_quality) / 2
        return min(1.0, max(0.0, confidence))
    
    async def get_governance_metrics(self, dao_address: str) -> GovernanceMetricsResponse:
        """Get comprehensive governance metrics"""
        try:
            dao_data = await self._get_dao_data(dao_address)
            
            # Calculate metrics
            total_proposals = dao_data['total_proposals']
            active_proposals = dao_data['active_proposals']
            avg_participation = dao_data['avg_voter_participation']
            success_rate = dao_data['passed_proposals'] / max(total_proposals, 1)
            avg_duration = dao_data['avg_voting_duration']
            
            # Mock top voters data
            top_voters = [
                {'address': '0x1234...', 'votes': 45, 'percentage': 0.15},
                {'address': '0x5678...', 'votes': 38, 'percentage': 0.12},
                {'address': '0x9abc...', 'votes': 32, 'percentage': 0.10}
            ]
            
            # Mock governance trends
            governance_trends = {
                'participation_trend': 'increasing',
                'proposal_quality': 'improving',
                'voting_efficiency': 'stable'
            }
            
            # Mock AI predictions
            predictions = {
                'next_month_participation': 0.72,
                'proposal_success_probability': 0.68,
                'trending_topics': ['treasury_management', 'governance_updates']
            }
            
            return GovernanceMetricsResponse(
                dao_address=dao_address,
                total_proposals=total_proposals,
                active_proposals=active_proposals,
                average_voter_participation=avg_participation,
                proposal_success_rate=success_rate,
                average_voting_duration=avg_duration,
                top_voters=top_voters,
                governance_trends=governance_trends,
                predictions=predictions,
                last_updated=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error getting governance metrics: {e}")
            raise
    
    async def store_dao_health_report(self, dao_address: str, health_data: DAOHealthResponse):
        """Store DAO health report in database"""
        try:
            # This would store the health report in the database
            # For now, just log it
            logger.info(f"Stored health report for DAO {dao_address}")
        except Exception as e:
            logger.error(f"Error storing health report: {e}")
    
    async def get_dao_by_address(self, dao_address: str) -> Optional[Dict[str, Any]]:
        """Get DAO information by address"""
        try:
            # Mock DAO data - in production would query database
            return {
                'address': dao_address,
                'name': 'Sample DAO',
                'description': 'A sample DAO for demonstration purposes',
                'treasury_address': '0x1234567890123456789012345678901234567890',
                'governance_token': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',
                'created_at': datetime.utcnow() - timedelta(days=365)
            }
        except Exception as e:
            logger.error(f"Error getting DAO: {e}")
            return None 