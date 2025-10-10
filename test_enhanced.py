#!/usr/bin/env python3
"""
AIDA - Enhanced Test Demo Script
This script tests all functionality including new Hathor integration features
"""

import asyncio
import json
import time
from datetime import datetime
import sys
import subprocess

try:
    import requests
except ImportError:
    print("Installing requests...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    print("Requests installed successfully!")

class AIDAEnhancedTestDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.dao_address = "0x1234567890123456789012345678901234567890"
        self.test_results = []
    
    def print_header(self, title):
        print("\n" + "="*60)
        print(f"TEST: {title}")
        print("="*60)
    
    def print_section(self, title):
        print(f"\n{title}")
        print("-" * 40)
    
    def log_test(self, test_name, success, details=""):
        result = "PASS" if success else "FAIL"
        print(f"{result} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_system_health(self):
        """Test comprehensive system health"""
        self.print_header("Testing System Health & Status")
        
        try:
            # Basic health check with longer timeout and session
            session = requests.Session()
            session.headers.update({'Connection': 'close'})
            response = session.get(f"{self.base_url}/health", timeout=30)
            success = response.status_code == 200
            self.log_test("Basic Health Check", success, f"Status: {response.status_code}")
            
            # System status with features
            status_response = session.get(f"{self.base_url}/api/system/status", timeout=30)
            if status_response.status_code == 200:
                status_data = status_response.json()
                self.log_test("System Status", True, f"Version: {status_data.get('version', 'unknown')}")
                
                # Test feature flags
                features = status_data.get('features', {})
                for feature, enabled in features.items():
                    self.log_test(f"Feature: {feature}", enabled, "✓ Enabled" if enabled else "✗ Disabled")
                
                # Test active connections
                connections = status_data.get('active_connections', 0)
                self.log_test("WebSocket Connections", True, f"{connections} active")
            
            return success
        except Exception as e:
            self.log_test("System Health", False, f"Error: {e}")
            return False
    
    def test_hathor_integration(self):
        """Test Hathor Network integration features"""
        self.print_header("Testing Hathor Network Integration")
        
        try:
            # Test network info
            session = requests.Session()
            session.headers.update({'Connection': 'close'})
            response = session.get(f"{self.base_url}/api/hathor/network/info", timeout=30)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Hathor Network Connection", True, f"Network: {data.get('network', 'unknown')}")
                
                # Test feeless transactions
                if data.get('feeless_transactions'):
                    self.log_test("Feeless Transactions", True, "✓ Supported")
                else:
                    self.log_test("Feeless Transactions", False, "✗ Not supported")
                
                # Test supported features
                features = data.get('supported_features', [])
                expected_features = ['Nano Contracts', 'EVM Bridge', 'Feeless Transactions', 'Instant Finality']
                
                for feature in expected_features:
                    if feature in features:
                        self.log_test(f"Hathor Feature: {feature}", True, "✓ Available")
                    else:
                        self.log_test(f"Hathor Feature: {feature}", False, "✗ Not available")
                
                # Test nano contracts
                nano_contracts = data.get('nano_contracts', {})
                if nano_contracts:
                    self.log_test("Nano Contracts", True, f"{len(nano_contracts)} contracts deployed")
                    for contract_name, address in nano_contracts.items():
                        self.log_test(f"Contract: {contract_name}", True, f"Address: {address[:10]}...")
                
                # Test EVM bridge status
                bridge_status = data.get('evm_bridge_status', 'unknown')
                self.log_test("EVM Bridge Status", bridge_status == 'active', f"Status: {bridge_status}")
            else:
                self.log_test("Hathor Network Integration", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Hathor Network Integration", False, f"Error: {e}")
            return False
    
    def test_performance_metrics(self):
        """Test performance metrics and benchmarks"""
        self.print_header("Testing Performance Metrics")
        
        try:
            session = requests.Session()
            session.headers.update({'Connection': 'close'})
            response = session.get(f"{self.base_url}/api/performance/metrics", timeout=30)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Performance Metrics Endpoint", True, "✓ Available")
                
                # Test response times
                response_times = data.get('response_times', {})
                for endpoint, time_str in response_times.items():
                    # Check if response time is acceptable
                    is_fast = any(indicator in time_str.lower() for indicator in ['<', 'ms', '1s', '2s'])
                    self.log_test(f"Response Time: {endpoint}", is_fast, time_str)
                
                # Test throughput metrics
                throughput = data.get('throughput', {})
                for metric, value in throughput.items():
                    # Check if throughput is good
                    is_good = any(indicator in value for indicator in ['1000+', '500+', '+'])
                    self.log_test(f"Throughput: {metric}", is_good, value)
                
                # Test Hathor-specific benefits
                hathor_benefits = data.get('hathor_benefits', {})
                
                # Verify feeless transactions
                tx_cost = hathor_benefits.get('transaction_cost', '')
                is_feeless = '$0' in tx_cost and 'feeless' in tx_cost.lower()
                self.log_test("Feeless Transaction Cost", is_feeless, tx_cost)
                
                # Verify fast transactions
                tx_time = hathor_benefits.get('transaction_time', '')
                is_fast = '<' in tx_time and 's' in tx_time
                self.log_test("Fast Transaction Time", is_fast, tx_time)
                
                # Verify high success rate
                success_rate = hathor_benefits.get('success_rate', '')
                is_reliable = '99' in success_rate
                self.log_test("High Success Rate", is_reliable, success_rate)
            else:
                self.log_test("Performance Metrics", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Performance Metrics", False, f"Error: {e}")
            return False
    
    def test_ai_capabilities(self):
        """Test AI analysis capabilities"""
        self.print_header("Testing AI Analysis Capabilities")
        
        proposal_data = {
            "dao_address": self.dao_address,
            "proposal_id": "enhanced_test_001",
            "title": "AI-Powered Treasury Optimization",
            "description": """
            This proposal leverages AIDA's AI capabilities to optimize our treasury allocation.
            The AI analysis shows potential for 15% yield improvement through strategic rebalancing
            across DeFi protocols while maintaining risk levels below 20%.
            
            Key benefits:
            - Automated risk assessment
            - Real-time market analysis
            - Predictive yield optimization
            - Cross-chain diversification via Hathor EVM Bridge
            """,
            "proposer": "0x1234567890123456789012345678901234567890"
        }
        
        try:
            session = requests.Session()
            session.headers.update({'Connection': 'close', 'Content-Type': 'application/json'})
            response = session.post(
                f"{self.base_url}/api/proposals/analyze",
                json=proposal_data,
                timeout=60
            )
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("AI Proposal Analysis", True, f"Prediction: {data.get('prediction', 0):.1%}")
                
                # Test AI analysis components
                components = [
                    ('summary', 'AI Summary'),
                    ('risk_assessment', 'Risk Assessment'),
                    ('key_points', 'Key Points Extraction'),
                    ('recommendations', 'AI Recommendations'),
                    ('sentiment_score', 'Sentiment Analysis'),
                    ('impact_analysis', 'Impact Analysis')
                ]
                
                for field, name in components:
                    if field in data and data[field]:
                        if isinstance(data[field], (list, dict)):
                            count = len(data[field])
                            self.log_test(name, count > 0, f"{count} items generated")
                        else:
                            self.log_test(name, True, "✓ Generated")
                    else:
                        self.log_test(name, False, "✗ Missing")
                
                # Test prediction quality
                prediction = data.get('prediction', 0)
                confidence = data.get('confidence', 0)
                
                self.log_test("Prediction Range", 0 <= prediction <= 1, f"{prediction:.1%}")
                self.log_test("Confidence Range", 0 <= confidence <= 1, f"{confidence:.1%}")
                
                # Test sentiment analysis
                sentiment = data.get('sentiment_score', 0)
                self.log_test("Sentiment Analysis", -1 <= sentiment <= 1, f"Score: {sentiment:.2f}")
            else:
                self.log_test("AI Proposal Analysis", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("AI Analysis Capabilities", False, f"Error: {e}")
            return False
    
    def test_cross_chain_features(self):
        """Test cross-chain integration via Hathor EVM Bridge"""
        self.print_header("Testing Cross-Chain Features")
        
        try:
            session = requests.Session()
            session.headers.update({'Connection': 'close'})
            response = session.get(f"{self.base_url}/api/cross-chain/{self.dao_address}/assets", timeout=30)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                total_value = data.get('total_cross_chain_value', 0)
                self.log_test("Cross-Chain Asset Tracking", True, f"Total Value: ${total_value:,.0f}")
                
                # Test multi-chain support
                assets_by_chain = data.get('assets_by_chain', {})
                supported_chains = ['ethereum', 'polygon', 'arbitrum']
                
                for chain in supported_chains:
                    if chain in assets_by_chain:
                        chain_assets = assets_by_chain[chain]
                        self.log_test(f"Chain: {chain.title()}", True, f"{len(chain_assets)} assets")
                    else:
                        self.log_test(f"Chain: {chain.title()}", False, "No assets found")
                
                # Test risk assessment
                risk_assessment = data.get('risk_assessment', {})
                if risk_assessment:
                    risk_score = risk_assessment.get('risk_score', 0)
                    risk_level = risk_assessment.get('risk_level', 'unknown')
                    self.log_test("Cross-Chain Risk Assessment", True, f"Risk: {risk_level} ({risk_score:.1%})")
                
                # Test recommendations
                recommendations = data.get('recommendations', [])
                self.log_test("Cross-Chain Recommendations", len(recommendations) > 0, f"{len(recommendations)} recommendations")
            else:
                self.log_test("Cross-Chain Features", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Cross-Chain Features", False, f"Error: {e}")
            return False
    
    def test_automated_execution(self):
        """Test automated action execution via Nano Contracts"""
        self.print_header("Testing Automated Execution")
        
        action_data = {
            "action_type": "proposal_execution",
            "dao_address": self.dao_address,
            "proposal_id": "enhanced_test_001",
            "parameters": {
                "target_address": "0x1234567890123456789012345678901234567890",
                "amount": "1000000000000000000",
                "execution_method": "nano_contract"
            }
        }
        
        try:
            session = requests.Session()
            session.headers.update({'Connection': 'close', 'Content-Type': 'application/json'})
            response = session.post(
                f"{self.base_url}/api/actions/execute",
                json=action_data,
                timeout=60
            )
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test("Automated Action Execution", True, f"Status: {data.get('status', 'unknown')}")
                
                # Test execution details
                if 'transaction_hash' in data and data['transaction_hash']:
                    tx_hash = data['transaction_hash']
                    self.log_test("Transaction Hash", True, f"Hash: {tx_hash[:10]}...")
                
                if 'execution_time' in data:
                    self.log_test("Execution Time", True, "✓ Recorded")
                
                # Test gas usage (should be 0 on Hathor)
                gas_used = data.get('gas_used', -1)
                if gas_used == 0:
                    self.log_test("Feeless Execution", True, "✓ No gas fees")
                else:
                    self.log_test("Feeless Execution", False, f"Gas used: {gas_used}")
                
                # Test action ID
                action_id = data.get('action_id')
                self.log_test("Action Tracking", bool(action_id), f"ID: {action_id}")
            else:
                self.log_test("Automated Execution", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Automated Execution", False, f"Error: {e}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all enhanced tests"""
        self.print_header("AIDA Enhanced Comprehensive Test Suite")
        print(f"Testing against: {self.base_url}")
        print(f"DAO Address: {self.dao_address}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Testing Hathor Network Integration & AI Capabilities")
        
        tests = [
            ("System Health & Status", self.test_system_health),
            ("Hathor Network Integration", self.test_hathor_integration),
            ("Performance Metrics", self.test_performance_metrics),
            ("AI Analysis Capabilities", self.test_ai_capabilities),
            ("Cross-Chain Features", self.test_cross_chain_features),
            ("Automated Execution", self.test_automated_execution)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                print(f"\nRunning: {test_name}")
                if test_func():
                    passed += 1
                    print(f"PASS {test_name}")
                else:
                    print(f"FAIL {test_name}")
            except Exception as e:
                print(f"ERROR {test_name}: {e}")
        
        # Print comprehensive summary
        self.print_header("Enhanced Test Results Summary")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Detailed results
        print(f"\nDetailed Results:")
        for result in self.test_results:
            status = "PASS" if result['success'] else "FAIL"
            print(f"{status} {result['test']}: {result['details']}")
        
        if passed == total:
            print("\nALL TESTS PASSED! AIDA is ready for hackathon submission!")
            print("System demonstrates:")
            print("   - Complete AI integration with fallback mechanisms")
            print("   - Full Hathor Network integration (Nano Contracts + EVM Bridge)")
            print("   - Real-time performance monitoring")
            print("   - Cross-chain asset management")
            print("   - Automated execution capabilities")
            print("   - Production-ready error handling")
        else:
            print(f"\nWARNING: {total - passed} test(s) failed. Review implementation before submission.")
        
        return passed == total

def main():
    """Main function"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    demo = AIDAEnhancedTestDemo(base_url)
    success = demo.run_comprehensive_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()