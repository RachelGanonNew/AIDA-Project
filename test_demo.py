#!/usr/bin/env python3
"""
AIDA - Comprehensive Test Demo Script
This script tests all functionality of the AIDA system
"""

import asyncio
import json
import requests
import time
from datetime import datetime
import sys

class AIDATestDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.dao_address = "0x1234567890123456789012345678901234567890"
        self.test_results = []
    
    def print_header(self, title):
        print("\n" + "="*60)
        print(f"🧪 {title}")
        print("="*60)
    
    def print_section(self, title):
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def log_test(self, test_name, success, details=""):
        result = "✅ PASS" if success else "❌ FAIL"
        print(f"{result} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_health_check(self):
        """Test the health check endpoint"""
        self.print_header("Testing Health Check")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code == 200
            self.log_test("Health Check", success, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {e}")
            return False
    
    def test_dao_health_analysis(self):
        """Test DAO health analysis"""
        self.print_header("Testing DAO Health Analysis")
        
        try:
            response = requests.get(f"{self.base_url}/api/dao/{self.dao_address}/health", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("DAO Health Analysis", True, f"Overall Health: {data['overall_health_score']:.1%}")
                
                # Test individual scores
                scores = ['governance_score', 'financial_score', 'community_score']
                for score in scores:
                    if score in data and 0 <= data[score] <= 1:
                        self.log_test(f"{score.replace('_', ' ').title()}", True)
                    else:
                        self.log_test(f"{score.replace('_', ' ').title()}", False, "Invalid score range")
                
                # Test recommendations
                if 'recommendations' in data and isinstance(data['recommendations'], list):
                    self.log_test("AI Recommendations", True, f"{len(data['recommendations'])} recommendations")
                else:
                    self.log_test("AI Recommendations", False, "Missing or invalid recommendations")
            else:
                self.log_test("DAO Health Analysis", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("DAO Health Analysis", False, f"Error: {e}")
            return False
    
    def test_proposal_analysis(self):
        """Test proposal analysis"""
        self.print_header("Testing Proposal Analysis")
        
        proposal_data = {
            "dao_address": self.dao_address,
            "proposal_id": "test_prop_001",
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
                json=proposal_data,
                timeout=30
            )
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Proposal Analysis", True, f"Prediction: {data['prediction']:.1%}")
                
                # Test individual analysis components
                if 'summary' in data and data['summary']:
                    self.log_test("AI Summary", True, "Summary generated")
                else:
                    self.log_test("AI Summary", False, "No summary generated")
                
                if 'risk_assessment' in data:
                    self.log_test("Risk Assessment", True, f"Risk Level: {data['risk_assessment']}")
                else:
                    self.log_test("Risk Assessment", False, "No risk assessment")
                
                if 'key_points' in data and isinstance(data['key_points'], list):
                    self.log_test("Key Points", True, f"{len(data['key_points'])} key points")
                else:
                    self.log_test("Key Points", False, "No key points")
                
                if 'recommendations' in data and isinstance(data['recommendations'], list):
                    self.log_test("Recommendations", True, f"{len(data['recommendations'])} recommendations")
                else:
                    self.log_test("Recommendations", False, "No recommendations")
            else:
                self.log_test("Proposal Analysis", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Proposal Analysis", False, f"Error: {e}")
            return False
    
    def test_treasury_analysis(self):
        """Test treasury analysis"""
        self.print_header("Testing Treasury Analysis")
        
        try:
            response = requests.get(f"{self.base_url}/api/treasury/{self.dao_address}/analysis", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Treasury Analysis", True, f"Total Value: ${data['total_value_usd']:,.0f}")
                
                # Test individual metrics
                if 'asset_diversification_score' in data and 0 <= data['asset_diversification_score'] <= 1:
                    self.log_test("Diversification Score", True, f"{data['asset_diversification_score']:.1%}")
                else:
                    self.log_test("Diversification Score", False, "Invalid score")
                
                if 'risk_score' in data and 0 <= data['risk_score'] <= 1:
                    self.log_test("Risk Score", True, f"{data['risk_score']:.1%}")
                else:
                    self.log_test("Risk Score", False, "Invalid score")
                
                if 'liquidity_score' in data and 0 <= data['liquidity_score'] <= 1:
                    self.log_test("Liquidity Score", True, f"{data['liquidity_score']:.1%}")
                else:
                    self.log_test("Liquidity Score", False, "Invalid score")
                
                if 'recommendations' in data and isinstance(data['recommendations'], list):
                    self.log_test("Treasury Recommendations", True, f"{len(data['recommendations'])} recommendations")
                else:
                    self.log_test("Treasury Recommendations", False, "No recommendations")
            else:
                self.log_test("Treasury Analysis", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Treasury Analysis", False, f"Error: {e}")
            return False
    
    def test_governance_metrics(self):
        """Test governance metrics"""
        self.print_header("Testing Governance Metrics")
        
        try:
            response = requests.get(f"{self.base_url}/api/governance/{self.dao_address}/metrics", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Governance Metrics", True, f"Total Proposals: {data['total_proposals']}")
                
                # Test individual metrics
                if 'active_proposals' in data and isinstance(data['active_proposals'], int):
                    self.log_test("Active Proposals", True, f"{data['active_proposals']} active")
                else:
                    self.log_test("Active Proposals", False, "Invalid count")
                
                if 'proposal_success_rate' in data and 0 <= data['proposal_success_rate'] <= 1:
                    self.log_test("Success Rate", True, f"{data['proposal_success_rate']:.1%}")
                else:
                    self.log_test("Success Rate", False, "Invalid rate")
                
                if 'average_voter_participation' in data and 0 <= data['average_voter_participation'] <= 1:
                    self.log_test("Voter Participation", True, f"{data['average_voter_participation']:.1%}")
                else:
                    self.log_test("Voter Participation", False, "Invalid participation")
            else:
                self.log_test("Governance Metrics", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Governance Metrics", False, f"Error: {e}")
            return False
    
    def test_cross_chain_assets(self):
        """Test cross-chain assets"""
        self.print_header("Testing Cross-Chain Assets")
        
        try:
            response = requests.get(f"{self.base_url}/api/cross-chain/{self.dao_address}/assets", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Cross-Chain Assets", True, f"Total Value: ${data['total_cross_chain_value']:,.0f}")
                
                if 'assets_by_chain' in data and isinstance(data['assets_by_chain'], dict):
                    chains = list(data['assets_by_chain'].keys())
                    self.log_test("Chain Integration", True, f"Chains: {', '.join(chains)}")
                else:
                    self.log_test("Chain Integration", False, "No chain data")
                
                if 'recommendations' in data and isinstance(data['recommendations'], list):
                    self.log_test("Cross-Chain Recommendations", True, f"{len(data['recommendations'])} recommendations")
                else:
                    self.log_test("Cross-Chain Recommendations", False, "No recommendations")
            else:
                self.log_test("Cross-Chain Assets", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Cross-Chain Assets", False, f"Error: {e}")
            return False
    
    def test_action_execution(self):
        """Test action execution"""
        self.print_header("Testing Action Execution")
        
        action_data = {
            "action_type": "proposal_execution",
            "dao_address": self.dao_address,
            "proposal_id": "test_prop_001",
            "parameters": {
                "target_address": "0x1234567890123456789012345678901234567890",
                "amount": "1000000000000000000"
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/actions/execute",
                json=action_data,
                timeout=30
            )
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Action Execution", True, f"Status: {data['status']}")
                
                if 'transaction_hash' in data and data['transaction_hash']:
                    self.log_test("Transaction Hash", True, f"Hash: {data['transaction_hash'][:10]}...")
                else:
                    self.log_test("Transaction Hash", False, "No transaction hash")
            else:
                self.log_test("Action Execution", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Action Execution", False, f"Error: {e}")
            return False
    
    def test_proposal_predictions(self):
        """Test proposal predictions"""
        self.print_header("Testing Proposal Predictions")
        
        try:
            response = requests.get(f"{self.base_url}/api/predictions/{self.dao_address}/proposals?limit=5", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Proposal Predictions", True, f"Predictions: {len(data)}")
                
                if data and isinstance(data, list):
                    for i, prediction in enumerate(data[:3]):
                        if 'prediction' in prediction and 'confidence' in prediction:
                            self.log_test(f"Prediction {i+1}", True, f"Pred: {prediction['prediction']:.1%}, Conf: {prediction['confidence']:.1%}")
                        else:
                            self.log_test(f"Prediction {i+1}", False, "Missing prediction data")
                else:
                    self.log_test("Prediction Data", False, "No prediction data")
            else:
                self.log_test("Proposal Predictions", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Proposal Predictions", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("AIDA Comprehensive Test Suite")
        print(f"Testing against: {self.base_url}")
        print(f"DAO Address: {self.dao_address}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tests = [
            self.test_health_check,
            self.test_dao_health_analysis,
            self.test_proposal_analysis,
            self.test_treasury_analysis,
            self.test_governance_metrics,
            self.test_cross_chain_assets,
            self.test_action_execution,
            self.test_proposal_predictions
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        # Print summary
        self.print_header("Test Summary")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! AIDA is ready for hackathon submission!")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please check the implementation.")
        
        return passed == total

def main():
    """Main function"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    demo = AIDATestDemo(base_url)
    success = demo.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 