import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

from models.schemas import TreasuryAnalysisResponse
from services.ai_service import AIService

logger = logging.getLogger(__name__)

class TreasuryService:
    def __init__(self):
        """Initialize treasury service"""
        self.ai_service = AIService()
    
    async def analyze_treasury(self, dao_address: str) -> TreasuryAnalysisResponse:
        """
        Comprehensive treasury analysis
        """
        try:
            # Get treasury data
            treasury_data = await self._get_treasury_data(dao_address)
            
            # Perform AI analysis
            ai_analysis = await self.ai_service.analyze_treasury_health(treasury_data)
            
            # Get top holdings
            top_holdings = ai_analysis.get('top_holdings', [])
            
            # Identify risk factors
            risk_factors = await self._identify_treasury_risks(treasury_data, ai_analysis)
            
            # Generate rebalancing suggestions
            rebalancing_suggestions = await self._generate_rebalancing_suggestions(
                treasury_data, ai_analysis
            )
            
            return TreasuryAnalysisResponse(
                dao_address=dao_address,
                total_value_usd=treasury_data['total_value'],
                asset_diversification_score=ai_analysis['diversification_score'],
                risk_score=ai_analysis['risk_score'],
                liquidity_score=ai_analysis['liquidity_score'],
                top_holdings=top_holdings,
                risk_factors=risk_factors,
                recommendations=ai_analysis['recommendations'],
                rebalancing_suggestions=rebalancing_suggestions,
                last_updated=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error analyzing treasury: {e}")
            raise
    
    async def _get_treasury_data(self, dao_address: str) -> Dict[str, Any]:
        """Get comprehensive treasury data"""
        # Mock treasury data - in production this would come from blockchain
        return {
            'total_value': 2500000,  # $2.5M
            'assets': [
                {
                    'symbol': 'USDC',
                    'address': '0xA0b86a33E6441b8c4C8C8C8C8C8C8C8C8C8C8C8C8',
                    'balance': 1000000,
                    'value_usd': 1000000,
                    'percentage': 0.4,
                    'price_usd': 1.0,
                    'market_cap': 25000000000,
                    'volume_24h': 5000000000
                },
                {
                    'symbol': 'ETH',
                    'address': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
                    'balance': 400,
                    'value_usd': 800000,
                    'percentage': 0.32,
                    'price_usd': 2000,
                    'market_cap': 240000000000,
                    'volume_24h': 15000000000
                },
                {
                    'symbol': 'UNI',
                    'address': '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
                    'balance': 5000,
                    'value_usd': 400000,
                    'percentage': 0.16,
                    'price_usd': 80,
                    'market_cap': 4800000000,
                    'volume_24h': 200000000
                },
                {
                    'symbol': 'AAVE',
                    'address': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9',
                    'balance': 2000,
                    'value_usd': 300000,
                    'percentage': 0.12,
                    'price_usd': 150,
                    'market_cap': 2100000000,
                    'volume_24h': 150000000
                }
            ],
            'historical_data': {
                'value_30_days_ago': 2300000,
                'value_7_days_ago': 2450000,
                'value_24_hours_ago': 2480000,
                'daily_change': 0.008,  # 0.8%
                'weekly_change': 0.022,  # 2.2%
                'monthly_change': 0.087  # 8.7%
            },
            'performance_metrics': {
                'volatility_30d': 0.15,
                'sharpe_ratio': 1.2,
                'max_drawdown': -0.08,
                'annualized_return': 0.25
            }
        }
    
    async def _identify_treasury_risks(self, treasury_data: Dict[str, Any], 
                                     ai_analysis: Dict[str, Any]) -> List[str]:
        """Identify specific treasury risks"""
        risk_factors = []
        
        # Concentration risks
        if ai_analysis['diversification_score'] < 0.3:
            risk_factors.append("High asset concentration - consider diversifying holdings")
        
        # Volatility risks
        if treasury_data['performance_metrics']['volatility_30d'] > 0.2:
            risk_factors.append("High volatility detected - consider stablecoin allocation")
        
        # Liquidity risks
        if ai_analysis['liquidity_score'] < 0.6:
            risk_factors.append("Low liquidity - ensure sufficient liquid assets")
        
        # Market risks
        if treasury_data['historical_data']['daily_change'] < -0.05:
            risk_factors.append("Recent significant decline - monitor market conditions")
        
        # Size risks
        if treasury_data['total_value'] < 100000:
            risk_factors.append("Small treasury size - consider growth strategies")
        
        # Add AI-identified risks
        if 'risk_factors' in ai_analysis:
            risk_factors.extend(ai_analysis['risk_factors'])
        
        if not risk_factors:
            risk_factors.append("No significant risks identified")
        
        return risk_factors[:5]  # Limit to top 5 risks
    
    async def _generate_rebalancing_suggestions(self, treasury_data: Dict[str, Any], 
                                              ai_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate rebalancing suggestions"""
        suggestions = []
        
        # Diversification suggestions
        if ai_analysis['diversification_score'] < 0.4:
            suggestions.append({
                'type': 'diversification',
                'action': 'Increase asset diversity',
                'description': 'Consider adding more assets to reduce concentration risk',
                'priority': 'high',
                'estimated_impact': 'Reduce concentration risk by 30%'
            })
        
        # Risk management suggestions
        if ai_analysis['risk_score'] > 0.7:
            suggestions.append({
                'type': 'risk_management',
                'action': 'Increase stablecoin allocation',
                'description': 'Allocate more funds to stablecoins to reduce volatility',
                'priority': 'high',
                'estimated_impact': 'Reduce risk score by 20%'
            })
        
        # Liquidity suggestions
        if ai_analysis['liquidity_score'] < 0.6:
            suggestions.append({
                'type': 'liquidity',
                'action': 'Maintain liquid reserves',
                'description': 'Ensure sufficient liquid assets for operations',
                'priority': 'medium',
                'estimated_impact': 'Improve liquidity score by 25%'
            })
        
        # Performance optimization
        if treasury_data['performance_metrics']['sharpe_ratio'] < 1.0:
            suggestions.append({
                'type': 'performance',
                'action': 'Optimize risk-adjusted returns',
                'description': 'Review asset allocation for better risk-adjusted performance',
                'priority': 'medium',
                'estimated_impact': 'Improve Sharpe ratio by 15%'
            })
        
        return suggestions
    
    async def get_treasury_performance(self, dao_address: str, period: str = '30d') -> Dict[str, Any]:
        """Get treasury performance metrics"""
        try:
            treasury_data = await self._get_treasury_data(dao_address)
            
            return {
                'dao_address': dao_address,
                'period': period,
                'total_value': treasury_data['total_value'],
                'performance_metrics': treasury_data['performance_metrics'],
                'historical_changes': treasury_data['historical_data'],
                'asset_performance': await self._get_asset_performance(treasury_data['assets']),
                'benchmark_comparison': await self._get_benchmark_comparison(treasury_data),
                'risk_metrics': {
                    'var_95': 0.08,  # Value at Risk 95%
                    'expected_shortfall': 0.12,
                    'beta': 0.85,
                    'correlation_with_eth': 0.72
                }
            }
        except Exception as e:
            logger.error(f"Error getting treasury performance: {e}")
            raise
    
    async def _get_asset_performance(self, assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get individual asset performance"""
        performance_data = []
        
        for asset in assets:
            # Mock performance data
            performance_data.append({
                'symbol': asset['symbol'],
                'current_value': asset['value_usd'],
                'daily_change': 0.02 + (hash(asset['symbol']) % 10) / 100,  # Mock change
                'weekly_change': 0.05 + (hash(asset['symbol']) % 15) / 100,
                'monthly_change': 0.10 + (hash(asset['symbol']) % 20) / 100,
                'volatility': 0.15 + (hash(asset['symbol']) % 10) / 100,
                'contribution_to_portfolio': asset['percentage']
            })
        
        return performance_data
    
    async def _get_benchmark_comparison(self, treasury_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare treasury performance to benchmarks"""
        return {
            'vs_eth': {
                'performance': 0.95,  # 95% of ETH performance
                'risk': 0.85,  # 85% of ETH risk
                'sharpe_ratio': 1.1  # Better risk-adjusted returns
            },
            'vs_defi_index': {
                'performance': 1.15,  # 15% better than DeFi index
                'risk': 0.9,  # 90% of DeFi index risk
                'sharpe_ratio': 1.3  # Much better risk-adjusted returns
            },
            'vs_stablecoins': {
                'performance': 1.25,  # 25% better than stablecoins
                'risk': 2.1,  # Higher risk than stablecoins
                'sharpe_ratio': 0.8  # Lower risk-adjusted returns
            }
        }
    
    async def get_treasury_alerts(self, dao_address: str) -> List[Dict[str, Any]]:
        """Get treasury alerts and notifications"""
        try:
            treasury_data = await self._get_treasury_data(dao_address)
            alerts = []
            
            # Value change alerts
            daily_change = treasury_data['historical_data']['daily_change']
            if abs(daily_change) > 0.05:  # 5% change
                alerts.append({
                    'type': 'value_change',
                    'severity': 'high' if abs(daily_change) > 0.1 else 'medium',
                    'message': f"Treasury value changed by {daily_change:.1%} in 24 hours",
                    'timestamp': datetime.utcnow(),
                    'action_required': abs(daily_change) > 0.1
                })
            
            # Risk alerts
            if treasury_data['performance_metrics']['volatility_30d'] > 0.2:
                alerts.append({
                    'type': 'risk',
                    'severity': 'medium',
                    'message': "High volatility detected - consider risk management",
                    'timestamp': datetime.utcnow(),
                    'action_required': True
                })
            
            # Liquidity alerts
            total_stablecoins = sum(
                asset['value_usd'] for asset in treasury_data['assets'] 
                if asset['symbol'] in ['USDC', 'USDT', 'DAI']
            )
            stablecoin_ratio = total_stablecoins / treasury_data['total_value']
            
            if stablecoin_ratio < 0.2:  # Less than 20% stablecoins
                alerts.append({
                    'type': 'liquidity',
                    'severity': 'medium',
                    'message': "Low stablecoin allocation - consider increasing liquidity",
                    'timestamp': datetime.utcnow(),
                    'action_required': False
                })
            
            return alerts
        except Exception as e:
            logger.error(f"Error getting treasury alerts: {e}")
            return []
    
    async def get_treasury_forecast(self, dao_address: str, days: int = 30) -> Dict[str, Any]:
        """Get treasury value forecast"""
        try:
            treasury_data = await self._get_treasury_data(dao_address)
            
            # Mock forecast data
            current_value = treasury_data['total_value']
            volatility = treasury_data['performance_metrics']['volatility_30d']
            expected_return = treasury_data['performance_metrics']['annualized_return'] / 365 * days
            
            # Generate forecast scenarios
            scenarios = {
                'optimistic': current_value * (1 + expected_return + volatility),
                'base_case': current_value * (1 + expected_return),
                'pessimistic': current_value * (1 + expected_return - volatility)
            }
            
            return {
                'dao_address': dao_address,
                'forecast_period': days,
                'current_value': current_value,
                'scenarios': scenarios,
                'confidence_interval': {
                    'lower_bound': scenarios['pessimistic'],
                    'upper_bound': scenarios['optimistic']
                },
                'key_assumptions': [
                    'Market conditions remain stable',
                    'No major protocol changes',
                    'Current asset allocation maintained'
                ]
            }
        except Exception as e:
            logger.error(f"Error getting treasury forecast: {e}")
            raise 