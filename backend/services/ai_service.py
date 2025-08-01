import openai
import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from typing import Dict, List, Any, Tuple, Optional
import asyncio
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        """Initialize AI service with OpenAI and ML models"""
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize ML models
        self.proposal_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Model training data (in production, this would come from database)
        self.training_data = self._load_training_data()
        self._train_models()
    
    def _load_training_data(self) -> pd.DataFrame:
        """Load training data for ML models"""
        # Mock training data - in production this would come from historical DAO data
        data = {
            'proposal_text': [
                "Increase treasury allocation to DeFi protocols",
                "Reduce governance token supply",
                "Add new validator to the network",
                "Update smart contract parameters",
                "Distribute rewards to token holders",
                "Implement new security measures",
                "Change voting mechanism",
                "Allocate funds for development",
                "Update tokenomics model",
                "Implement cross-chain bridge"
            ],
            'proposer_reputation': [0.8, 0.6, 0.9, 0.7, 0.5, 0.8, 0.4, 0.7, 0.6, 0.8],
            'proposal_complexity': [0.6, 0.8, 0.4, 0.7, 0.3, 0.9, 0.8, 0.5, 0.7, 0.6],
            'community_sentiment': [0.7, 0.3, 0.8, 0.5, 0.9, 0.6, 0.2, 0.7, 0.4, 0.7],
            'financial_impact': [0.8, 0.9, 0.3, 0.6, 0.7, 0.5, 0.8, 0.6, 0.8, 0.5],
            'passed': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
        }
        return pd.DataFrame(data)
    
    def _train_models(self):
        """Train ML models with historical data"""
        try:
            # Prepare features
            X_text = self.vectorizer.fit_transform(self.training_data['proposal_text'])
            X_numeric = self.training_data[['proposer_reputation', 'proposal_complexity', 
                                          'community_sentiment', 'financial_impact']].values
            
            # Combine features
            X_combined = np.hstack([X_text.toarray(), X_numeric])
            y = self.training_data['passed']
            
            # Train model
            self.proposal_classifier.fit(X_combined, y)
            logger.info("ML models trained successfully")
        except Exception as e:
            logger.error(f"Error training models: {e}")
    
    async def analyze_proposal(self, proposal_text: str, proposer_address: str, 
                             dao_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive proposal analysis using AI
        """
        try:
            # Parallel processing for different analysis types
            tasks = [
                self._analyze_sentiment(proposal_text),
                self._generate_summary(proposal_text),
                self._assess_risk(proposal_text, dao_context),
                self._predict_outcome(proposal_text, proposer_address, dao_context),
                self._analyze_impact(proposal_text, dao_context)
            ]
            
            results = await asyncio.gather(*tasks)
            
            return {
                'sentiment_score': results[0],
                'summary': results[1],
                'risk_assessment': results[2],
                'prediction': results[3],
                'impact_analysis': results[4],
                'confidence': self._calculate_confidence(results),
                'key_points': await self._extract_key_points(proposal_text),
                'recommendations': await self._generate_recommendations(results, dao_context)
            }
        except Exception as e:
            logger.error(f"Error in proposal analysis: {e}")
            raise
    
    async def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of proposal text"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Analyze the sentiment of the given DAO proposal text and return a score between -1 (very negative) and 1 (very positive). Return only the numeric score."},
                    {"role": "user", "content": f"Analyze the sentiment of this proposal: {text[:1000]}"}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            score = float(response.choices[0].message.content.strip())
            return max(-1.0, min(1.0, score))  # Clamp between -1 and 1
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return 0.0
    
    async def _generate_summary(self, text: str) -> str:
        """Generate concise summary of proposal"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at summarizing DAO governance proposals. Create a clear, concise summary in 2-3 sentences that captures the key points and intent."},
                    {"role": "user", "content": f"Summarize this proposal: {text[:1500]}"}
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Unable to generate summary at this time."
    
    async def _assess_risk(self, text: str, dao_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk level and factors"""
        try:
            context_info = f"DAO Treasury: ${dao_context.get('treasury_value', 0):,.0f}, Active Proposals: {dao_context.get('active_proposals', 0)}"
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a risk assessment expert for DAO governance. Analyze the risk level (low/medium/high) and identify specific risk factors. Return JSON format: {\"risk_level\": \"low/medium/high\", \"risk_factors\": [\"factor1\", \"factor2\"], \"risk_score\": 0.0-1.0}"},
                    {"role": "user", "content": f"Assess risk for this proposal in context: {context_info}\n\nProposal: {text[:1000]}"}
                ],
                max_tokens=200,
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result
        except Exception as e:
            logger.error(f"Error in risk assessment: {e}")
            return {"risk_level": "medium", "risk_factors": ["Analysis unavailable"], "risk_score": 0.5}
    
    def _predict_outcome(self, text: str, proposer_address: str, dao_context: Dict[str, Any]) -> Dict[str, float]:
        """Predict proposal outcome using ML model"""
        try:
            # Extract features
            text_features = self.vectorizer.transform([text]).toarray()
            
            # Mock features (in production, these would be calculated from real data)
            proposer_reputation = dao_context.get('proposer_reputation', 0.5)
            complexity = len(text.split()) / 100  # Simple complexity metric
            sentiment = dao_context.get('avg_sentiment', 0.0)
            financial_impact = dao_context.get('financial_impact_score', 0.5)
            
            numeric_features = np.array([[proposer_reputation, complexity, sentiment, financial_impact]])
            
            # Combine features
            features = np.hstack([text_features, numeric_features])
            
            # Make prediction
            prediction = self.proposal_classifier.predict_proba(features)[0][1]
            confidence = self.proposal_classifier.predict_proba(features).max()
            
            return {
                'prediction': float(prediction),
                'confidence': float(confidence)
            }
        except Exception as e:
            logger.error(f"Error in outcome prediction: {e}")
            return {'prediction': 0.5, 'confidence': 0.5}
    
    async def _analyze_impact(self, text: str, dao_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential impact of proposal"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing DAO governance proposal impacts. Analyze the potential impact on treasury, governance, community, and technical aspects. Return JSON format with impact scores (0-1) and descriptions."},
                    {"role": "user", "content": f"Analyze impact of this proposal: {text[:1000]}"}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            logger.error(f"Error in impact analysis: {e}")
            return {
                "treasury_impact": {"score": 0.5, "description": "Moderate impact"},
                "governance_impact": {"score": 0.5, "description": "Moderate impact"},
                "community_impact": {"score": 0.5, "description": "Moderate impact"}
            }
    
    async def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from proposal"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract 3-5 key points from this DAO proposal. Return as a JSON array of strings."},
                    {"role": "user", "content": f"Extract key points: {text[:1000]}"}
                ],
                max_tokens=200,
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return ["Key points extraction unavailable"]
    
    async def _generate_recommendations(self, analysis_results: List, dao_context: Dict[str, Any]) -> List[str]:
        """Generate AI recommendations based on analysis"""
        try:
            context = f"Sentiment: {analysis_results[0]}, Risk: {analysis_results[2]}, Prediction: {analysis_results[3]}"
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Based on the analysis results, provide 2-3 actionable recommendations for DAO members. Focus on voting guidance and risk mitigation."},
                    {"role": "user", "content": f"Generate recommendations based on: {context}"}
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            recommendations = response.choices[0].message.content.strip().split('\n')
            return [rec.strip() for rec in recommendations if rec.strip()]
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Consider the proposal carefully before voting"]
    
    def _calculate_confidence(self, results: List) -> float:
        """Calculate overall confidence in analysis"""
        try:
            # Weight different factors
            sentiment_confidence = 0.8
            risk_confidence = 0.7
            prediction_confidence = results[3].get('confidence', 0.5)
            
            # Weighted average
            confidence = (sentiment_confidence + risk_confidence + prediction_confidence) / 3
            return min(1.0, max(0.0, confidence))
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5
    
    async def analyze_treasury_health(self, treasury_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze treasury health and provide recommendations"""
        try:
            # Calculate diversification score
            assets = treasury_data.get('assets', [])
            total_value = sum(asset.get('value_usd', 0) for asset in assets)
            
            if total_value == 0:
                return {"error": "No treasury data available"}
            
            # Calculate diversification (Herfindahl-Hirschman Index)
            concentrations = [(asset.get('value_usd', 0) / total_value) ** 2 for asset in assets]
            hhi = sum(concentrations)
            diversification_score = 1 - hhi  # Higher is better
            
            # Calculate risk score based on asset volatility
            risk_score = self._calculate_treasury_risk(assets)
            
            # Calculate liquidity score
            liquidity_score = self._calculate_liquidity_score(assets)
            
            # Generate AI recommendations
            recommendations = await self._generate_treasury_recommendations(
                diversification_score, risk_score, liquidity_score, assets
            )
            
            return {
                'diversification_score': diversification_score,
                'risk_score': risk_score,
                'liquidity_score': liquidity_score,
                'recommendations': recommendations,
                'top_holdings': sorted(assets, key=lambda x: x.get('value_usd', 0), reverse=True)[:5]
            }
        except Exception as e:
            logger.error(f"Error in treasury analysis: {e}")
            raise
    
    def _calculate_treasury_risk(self, assets: List[Dict[str, Any]]) -> float:
        """Calculate treasury risk score"""
        try:
            # Mock risk calculation (in production, would use real volatility data)
            risk_scores = {
                'USDC': 0.1, 'USDT': 0.1, 'DAI': 0.1,  # Stablecoins
                'ETH': 0.6, 'BTC': 0.7,  # Major cryptos
                'UNI': 0.8, 'AAVE': 0.8, 'COMP': 0.8  # DeFi tokens
            }
            
            total_value = sum(asset.get('value_usd', 0) for asset in assets)
            if total_value == 0:
                return 0.5
            
            weighted_risk = 0
            for asset in assets:
                symbol = asset.get('symbol', 'UNKNOWN')
                value = asset.get('value_usd', 0)
                risk = risk_scores.get(symbol, 0.5)
                weighted_risk += (value / total_value) * risk
            
            return min(1.0, weighted_risk)
        except Exception as e:
            logger.error(f"Error calculating treasury risk: {e}")
            return 0.5
    
    def _calculate_liquidity_score(self, assets: List[Dict[str, Any]]) -> float:
        """Calculate liquidity score"""
        try:
            # Mock liquidity calculation
            liquidity_scores = {
                'USDC': 1.0, 'USDT': 1.0, 'DAI': 1.0,  # High liquidity
                'ETH': 0.9, 'BTC': 0.9,  # High liquidity
                'UNI': 0.7, 'AAVE': 0.6, 'COMP': 0.6  # Medium liquidity
            }
            
            total_value = sum(asset.get('value_usd', 0) for asset in assets)
            if total_value == 0:
                return 0.5
            
            weighted_liquidity = 0
            for asset in assets:
                symbol = asset.get('symbol', 'UNKNOWN')
                value = asset.get('value_usd', 0)
                liquidity = liquidity_scores.get(symbol, 0.5)
                weighted_liquidity += (value / total_value) * liquidity
            
            return min(1.0, weighted_liquidity)
        except Exception as e:
            logger.error(f"Error calculating liquidity score: {e}")
            return 0.5
    
    async def _generate_treasury_recommendations(self, diversification: float, risk: float, 
                                               liquidity: float, assets: List[Dict[str, Any]]) -> List[str]:
        """Generate treasury management recommendations"""
        recommendations = []
        
        if diversification < 0.3:
            recommendations.append("Consider diversifying treasury holdings to reduce concentration risk")
        
        if risk > 0.7:
            recommendations.append("High risk detected - consider increasing stablecoin allocation")
        
        if liquidity < 0.6:
            recommendations.append("Low liquidity detected - ensure sufficient liquid assets for operations")
        
        if not recommendations:
            recommendations.append("Treasury appears well-balanced - maintain current allocation strategy")
        
        return recommendations 