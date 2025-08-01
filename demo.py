#!/usr/bin/env python3
"""
AIDA - AI-Driven DAO Analyst Demo Script
This script demonstrates the key features of the AIDA system
"""

import asyncio
import json
import requests
from datetime import datetime
import time

class AIDADemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.dao_address = "0x1234567890123456789012345678901234567890"
    
    def print_header(self, title):
        print("\n" + "="*60)
        print(f"🚀 {title}")
        print("="*60)
    
    def print_section(self, title):
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def demo_health_check(self):
        """Demo the health check endpoint"""
        self.print_header("AIDA System Health Check")
        
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ System is healthy and running")
                print(f"Response: {response.json()}")
            else:
                print("❌ System health check failed")
        except Exception as e:
            print(f"❌ Error connecting to system: {e}")
    
    def demo_dao_health_analysis(self):
        """Demo DAO health analysis"""
        self.print_header("DAO Health Analysis Demo")
        
        try:
            response = requests.get(f"{self.base_url}/api/dao/{self.dao_address}/health")
            if response.status_code == 200:
                data = response.json()
                
                self.print_section("Health Scores")
                print(f"Overall Health: {data['overall_health_score']:.1%}")
                print(f"Governance: {data['governance_score']:.1%}")
                print(f"Financial: {data['financial_score']:.1%}")
                print(f"Community: {data['community_score']:.1%}")
                
                self.print_section("Risk Factors")
                for risk in data['risk_factors'][:3]:
                    print(f"⚠️  {risk}")
                
                self.print_section("AI Recommendations")
                for rec in data['recommendations'][:3]:
                    print(f"💡 {rec}")
                    
            else:
                print("❌ Failed to get DAO health analysis")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_proposal_analysis(self):
        """Demo proposal analysis"""
        self.print_header("AI Proposal Analysis Demo")
        
        # Sample proposal data
        proposal_data = {
            "dao_address": self.dao_address,
            "proposal_id": "demo_prop_001",
            "title": "Treasury Diversification Strategy",
            "description": """
            This proposal aims to diversify our treasury holdings by allocating 20% of our 
            current USDC holdings to a mix of DeFi protocols including Aave, Compound, and 
            Uniswap. This will help us generate yield while maintaining liquidity for 
            operational expenses. The strategy includes:
            
            1. Allocate 10% to Aave lending pools
            2. Allocate 5% to Compound governance tokens
            3. Allocate 5% to Uniswap liquidity positions
            
            Expected annual yield: 8-12%
            Risk level: Medium
            Implementation timeline: 30 days
            """,
            "proposer": "0x1234567890123456789012345678901234567890"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/proposals/analyze",
                json=proposal_data
            )
            
            if response.status_code == 200:
                data = response.json()
                
                self.print_section("AI Prediction")
                print(f"Success Probability: {data['prediction']:.1%}")
                print(f"Confidence: {data['confidence']:.1%}")
                print(f"Risk Level: {data['risk_assessment']}")
                print(f"Sentiment: {'Positive' if data['sentiment_score'] > 0 else 'Negative'}")
                
                self.print_section("AI Summary")
                print(data['summary'])
                
                self.print_section("Key Points")
                for point in data['key_points'][:3]:
                    print(f"• {point}")
                
                self.print_section("AI Recommendations")
                for rec in data['recommendations'][:3]:
                    print(f"💡 {rec}")
                    
            else:
                print("❌ Failed to analyze proposal")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_treasury_analysis(self):
        """Demo treasury analysis"""
        self.print_header("Treasury Analysis Demo")
        
        try:
            response = requests.get(f"{self.base_url}/api/treasury/{self.dao_address}/analysis")
            if response.status_code == 200:
                data = response.json()
                
                self.print_section("Treasury Overview")
                print(f"Total Value: ${data['total_value_usd']:,.0f}")
                print(f"Diversification Score: {data['asset_diversification_score']:.1%}")
                print(f"Risk Score: {data['risk_score']:.1%}")
                print(f"Liquidity Score: {data['liquidity_score']:.1%}")
                
                self.print_section("Top Holdings")
                for holding in data['top_holdings'][:3]:
                    print(f"• {holding['symbol']}: ${holding['value_usd']:,.0f}")
                
                self.print_section("Risk Factors")
                for risk in data['risk_factors'][:3]:
                    print(f"⚠️  {risk}")
                
                self.print_section("AI Recommendations")
                for rec in data['recommendations'][:3]:
                    print(f"💡 {rec}")
                    
            else:
                print("❌ Failed to get treasury analysis")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_governance_metrics(self):
        """Demo governance metrics"""
        self.print_header("Governance Metrics Demo")
        
        try:
            response = requests.get(f"{self.base_url}/api/governance/{self.dao_address}/metrics")
            if response.status_code == 200:
                data = response.json()
                
                self.print_section("Key Metrics")
                print(f"Total Proposals: {data['total_proposals']}")
                print(f"Active Proposals: {data['active_proposals']}")
                print(f"Voter Participation: {data['average_voter_participation']:.1%}")
                print(f"Success Rate: {data['proposal_success_rate']:.1%}")
                
                self.print_section("Governance Trends")
                for trend, value in data['governance_trends'].items():
                    print(f"• {trend.replace('_', ' ').title()}: {value}")
                
                self.print_section("AI Predictions")
                predictions = data['predictions']
                print(f"Next Month Participation: {predictions['next_month_participation']:.1%}")
                print(f"Success Probability: {predictions['proposal_success_probability']:.1%}")
                print("Trending Topics:")
                for topic in predictions['trending_topics']:
                    print(f"  • {topic.replace('_', ' ').title()}")
                    
            else:
                print("❌ Failed to get governance metrics")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_cross_chain_analysis(self):
        """Demo cross-chain asset analysis"""
        self.print_header("Cross-Chain Asset Analysis Demo")
        
        try:
            response = requests.get(f"{self.base_url}/api/cross-chain/{self.dao_address}/assets")
            if response.status_code == 200:
                data = response.json()
                
                self.print_section("Cross-Chain Overview")
                print(f"Total Value: ${data['total_cross_chain_value']:,.0f}")
                
                self.print_section("Assets by Chain")
                for chain, assets in data['assets_by_chain'].items():
                    print(f"\n{chain.upper()}:")
                    for asset in assets:
                        print(f"  • {asset['symbol']}: ${asset['value_usd']:,.0f}")
                
                self.print_section("Risk Assessment")
                risk = data['risk_assessment']
                print(f"Risk Level: {risk['risk_level']}")
                print(f"Risk Score: {risk['risk_score']:.1%}")
                for risk_factor in risk['risk_factors'][:2]:
                    print(f"⚠️  {risk_factor}")
                
                self.print_section("Recommendations")
                for rec in data['recommendations'][:3]:
                    print(f"💡 {rec}")
                    
            else:
                print("❌ Failed to get cross-chain analysis")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_action_execution(self):
        """Demo automated action execution"""
        self.print_header("Automated Action Execution Demo")
        
        # Sample action data
        action_data = {
            "action_type": "treasury_rebalance",
            "dao_address": self.dao_address,
            "parameters": {
                "target_allocation": {
                    "USDC": 0.4,
                    "ETH": 0.3,
                    "UNI": 0.2,
                    "AAVE": 0.1
                },
                "slippage_tolerance": 0.02
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/actions/execute",
                json=action_data
            )
            
            if response.status_code == 200:
                data = response.json()
                
                self.print_section("Action Execution Result")
                print(f"Action ID: {data['action_id']}")
                print(f"Status: {data['status']}")
                print(f"Transaction Hash: {data['transaction_hash']}")
                print(f"Gas Used: {data['gas_used']}")
                
                if data['status'] == 'executed':
                    print("✅ Action executed successfully!")
                else:
                    print(f"❌ Action failed: {data['error_message']}")
                    
            else:
                print("❌ Failed to execute action")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run_full_demo(self):
        """Run the complete demo"""
        print("🎯 AIDA - AI-Driven DAO Analyst Demo")
        print("=" * 60)
        print("This demo showcases the key features of the AIDA system")
        print("Make sure the backend is running on http://localhost:8000")
        print("=" * 60)
        
        # Run all demos
        self.demo_health_check()
        time.sleep(1)
        
        self.demo_dao_health_analysis()
        time.sleep(1)
        
        self.demo_proposal_analysis()
        time.sleep(1)
        
        self.demo_treasury_analysis()
        time.sleep(1)
        
        self.demo_governance_metrics()
        time.sleep(1)
        
        self.demo_cross_chain_analysis()
        time.sleep(1)
        
        self.demo_action_execution()
        
        print("\n" + "="*60)
        print("🎉 Demo completed successfully!")
        print("="*60)
        print("\nKey Features Demonstrated:")
        print("✅ AI-powered proposal analysis and prediction")
        print("✅ Comprehensive DAO health assessment")
        print("✅ Treasury analysis and rebalancing suggestions")
        print("✅ Governance metrics and trends")
        print("✅ Cross-chain asset analysis")
        print("✅ Automated action execution via Hathor Nano Contracts")
        print("\nFor more information, visit: http://localhost:3000")

if __name__ == "__main__":
    demo = AIDADemo()
    demo.run_full_demo() 