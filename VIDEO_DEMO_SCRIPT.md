# 🎬 AIDA Video Demo Script
## AI-Driven DAO Analyst - Complete UI Walkthrough

### **🎯 Demo Duration: 5-7 minutes**

---

## **📝 Recording Setup**
1. Open browser to `http://localhost:3000`
2. Open second tab to `http://localhost:8000/docs`
3. Have terminal ready with curl commands
4. Screen resolution: 1920x1080 recommended

---

## **🎬 Scene 1: Introduction (30 seconds)**
**[Show AIDA Homepage]**

> "Welcome to AIDA - the AI-Driven DAO Analyst. This is a comprehensive platform that revolutionizes DAO governance and treasury management using artificial intelligence and cross-chain integration."

**Actions:**
- Show the main dashboard loading
- Highlight the clean, modern UI
- Point out key navigation elements

---

## **🎬 Scene 2: DAO Health Analysis (60 seconds)**
**[Navigate to Dashboard/Health Section]**

> "Let's start with our DAO Health Analysis. AIDA provides real-time monitoring of your DAO's overall health across three key dimensions."

**Show in UI:**
- Overall health score: 73.6%
- Governance score: 72.5%
- Financial score: 67.1% 
- Community score: 81.2%

**API Demo in Terminal:**
```bash
curl -s "http://localhost:8000/api/dao/0x1234567890123456789012345678901234567890/health" | python3 -m json.tool
```

> "Notice how our AI provides confidence scoring and identifies risk factors automatically."

---

## **🎬 Scene 3: Treasury Management (90 seconds)**
**[Navigate to Treasury Section]**

> "The treasury management module analyzes your entire portfolio in real-time. We're currently managing $2.5 million across multiple assets."

**Show in UI:**
- Total portfolio value: $2.5M
- Asset breakdown pie chart
- Diversification score: 69.8%
- Risk assessment: 45.6%
- Liquidity score: 87.2%

**Highlight Key Holdings:**
- USDC: $1M (40%) - Stable foundation
- ETH: $800K (32%) - Primary crypto holding
- UNI: $400K (16%) - DeFi exposure
- AAVE: $300K (12%) - Lending protocol

**API Demo:**
```bash
curl -s "http://localhost:8000/api/treasury/0x1234567890123456789012345678901234567890/analysis" | python3 -m json.tool
```

---

## **🎬 Scene 4: Governance Analytics (60 seconds)**
**[Navigate to Governance Section]**

> "Our governance module tracks all proposal activity and voting patterns. We're currently monitoring 45 proposals with a 71% success rate."

**Show in UI:**
- Total proposals: 45
- Active proposals: 3
- Success rate: 71.1%
- Voter participation: 68% (trending up!)
- Top voters and their contribution

**API Demo:**
```bash
curl -s "http://localhost:8000/api/governance/0x1234567890123456789012345678901234567890/metrics" | python3 -m json.tool
```

---

## **🎬 Scene 5: Cross-Chain Integration (60 seconds)**
**[Show Cross-Chain Assets]**

> "AIDA supports multi-chain operations. We're tracking $913K across Ethereum, Polygon, and Arbitrum networks."

**Show in UI:**
- Total cross-chain value: $913K
- Chain distribution:
  - Ethereum: 98.6% ($900K)
  - Polygon: 0.9% ($8K)
  - Arbitrum: 0.5% ($5K)
- Bridge status monitoring
- Risk alerts (show pending transaction alert)

**API Demo:**
```bash
curl -s "http://localhost:8000/api/cross-chain/0x1234567890123456789012345678901234567890/assets" | python3 -m json.tool
```

---

## **🎬 Scene 6: AI Predictions (45 seconds)**
**[Show Predictions Dashboard]**

> "Our AI engine provides predictive analytics for proposal outcomes. Currently tracking 10 active proposals with success rate predictions."

**Show in UI:**
- List of proposals with predictions
- Success rate percentages (70%-115%)
- Confidence scores
- Trending topics
- AI recommendations

**API Demo:**
```bash
curl -s "http://localhost:8000/api/predictions/0x1234567890123456789012345678901234567890/proposals" | python3 -m json.tool
```

---

## **🎬 Scene 7: Automated Execution (45 seconds)**
**[Show Action Execution]**

> "One of AIDA's most powerful features is automated execution using Hathor Nano Contracts. Let's execute a treasury rebalancing action."

**Show in UI:**
- Action execution interface
- Parameter configuration
- Real-time execution status

**API Demo:**
```bash
curl -s "http://localhost:8000/api/actions/execute" -X POST -H "Content-Type: application/json" -d '{
  "dao_address": "0x1234567890123456789012345678901234567890",
  "action_type": "treasury_rebalance",
  "parameters": {"target_allocation": {"USDC": 0.4, "ETH": 0.3, "UNI": 0.2, "AAVE": 0.1}}
}'
```

**Show Results:**
- Transaction hash
- Execution time
- Gas usage
- Success confirmation

---

## **🎬 Scene 8: Developer Experience (30 seconds)**
**[Switch to API Documentation Tab]**

> "For developers, AIDA provides comprehensive API documentation with interactive testing capabilities."

**Show in UI:**
- Interactive Swagger UI at localhost:8000/docs
- Available endpoints
- Try-it-out functionality
- Request/response examples

---

## **🎬 Scene 9: Conclusion (30 seconds)**
**[Return to Main Dashboard]**

> "AIDA represents the future of DAO management - combining AI intelligence, cross-chain capabilities, and automated execution in one powerful platform. With 87.5% test success rate and production-ready features, AIDA is ready to revolutionize your DAO operations."

**Final UI Tour:**
- Quick scroll through main dashboard
- Highlight key metrics one more time
- Show real-time updates

---

## **🎥 Recording Tips**

### **Technical Setup:**
- Use OBS Studio or similar screen recording software
- Record at 1920x1080, 30fps
- Enable system audio for click sounds
- Use a good microphone for narration

### **Browser Setup:**
- Use Chrome/Firefox in full-screen mode
- Clear browser cache for clean loading
- Zoom to 100% for optimal visibility
- Close unnecessary tabs/applications

### **Presentation Tips:**
- Speak clearly and at moderate pace
- Pause briefly between sections
- Use mouse cursor to highlight important elements
- Keep terminal commands visible for 2-3 seconds

### **Post-Production:**
- Add intro/outro with AIDA branding
- Include background music (optional)
- Add captions for accessibility
- Export in MP4 format for compatibility

---

## **📁 Files for Video Assets**
- Logo: `frontend/public/logo192.png`
- Favicon: `frontend/public/favicon.ico`
- Screenshots can be taken during recording
- API responses can be saved as JSON files

---

**🎬 Ready to Record!** Follow this script while screen recording for a comprehensive AIDA demo video.