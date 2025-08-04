#!/bin/bash

# 🎬 AIDA Video Demo Commands
# Run these commands during your screen recording

echo "🎬 AIDA Demo Commands Ready!"
echo "Copy and paste these during your video recording:"
echo ""

echo "# 1. DAO Health Analysis"
echo 'curl -s "http://localhost:8000/api/dao/0x1234567890123456789012345678901234567890/health" | python3 -m json.tool'
echo ""

echo "# 2. Treasury Analysis"  
echo 'curl -s "http://localhost:8000/api/treasury/0x1234567890123456789012345678901234567890/analysis" | python3 -m json.tool'
echo ""

echo "# 3. Governance Metrics"
echo 'curl -s "http://localhost:8000/api/governance/0x1234567890123456789012345678901234567890/metrics" | python3 -m json.tool'
echo ""

echo "# 4. Cross-Chain Assets"
echo 'curl -s "http://localhost:8000/api/cross-chain/0x1234567890123456789012345678901234567890/assets" | python3 -m json.tool'
echo ""

echo "# 5. AI Predictions"
echo 'curl -s "http://localhost:8000/api/predictions/0x1234567890123456789012345678901234567890/proposals" | python3 -m json.tool'
echo ""

echo "# 6. Automated Execution"
echo 'curl -s "http://localhost:8000/api/actions/execute" -X POST -H "Content-Type: application/json" -d '"'"'{"dao_address": "0x1234567890123456789012345678901234567890", "action_type": "treasury_rebalance", "parameters": {"target_allocation": {"USDC": 0.4, "ETH": 0.3, "UNI": 0.2, "AAVE": 0.1}}}'"'"' | python3 -m json.tool'
echo ""

echo "# 7. Health Check"
echo 'curl -s "http://localhost:8000/health" | python3 -m json.tool'
echo ""

echo "🎥 Ready for recording!"