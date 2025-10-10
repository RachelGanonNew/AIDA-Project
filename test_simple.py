#!/usr/bin/env python3

import requests
import json

def test_endpoints():
    base_url = "http://localhost:8000"
    
    print("Testing AIDA endpoints...")
    
    # Test basic health
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health: {response.status_code}")
    except Exception as e:
        print(f"Health: ERROR - {e}")
    
    # Test Hathor network info
    try:
        response = requests.get(f"{base_url}/api/hathor/network/info", timeout=10)
        print(f"Hathor Network: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Network: {data.get('network', 'unknown')}")
            print(f"  Feeless: {data.get('feeless_transactions', False)}")
    except Exception as e:
        print(f"Hathor Network: ERROR - {e}")
    
    # Test performance metrics
    try:
        response = requests.get(f"{base_url}/api/performance/metrics", timeout=10)
        print(f"Performance: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Transaction Cost: {data.get('hathor_benefits', {}).get('transaction_cost', 'unknown')}")
    except Exception as e:
        print(f"Performance: ERROR - {e}")
    
    # Test action execution
    try:
        action_data = {
            "action_type": "proposal_execution",
            "dao_address": "0x1234567890123456789012345678901234567890",
            "proposal_id": "test_001",
            "parameters": {
                "target_address": "0x1234567890123456789012345678901234567890",
                "amount": "1000000000000000000"
            }
        }
        response = requests.post(f"{base_url}/api/actions/execute", json=action_data, timeout=30)
        print(f"Action Execution: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: {data.get('status', 'unknown')}")
            print(f"  Gas Used: {data.get('gas_used', 'unknown')}")
    except Exception as e:
        print(f"Action Execution: ERROR - {e}")

if __name__ == "__main__":
    test_endpoints()