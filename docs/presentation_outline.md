## AIDA: AI-Driven DAO Analyst — Hackathon Pitch Deck

Reference template: `https://apse1-uc.hackerearth.com/he-public-ap-south-1/Prototype%20submission%20Template43c7cf4.pptx`

---

### 1. Title / Cover
- **Project**: AIDA — AI-Driven DAO Analyst
- **Tagline**: Smarter governance. Automated execution. Cross-chain clarity.
- **Team**: AIDA Team
- **Links**: Repo, Demo video (see `demo.mp4`), Live demo (if applicable)

---

### 2. Problem Statement
- **Governance apathy**: Proposals are complex; participants lack time/context to vote well
- **Manual execution**: Even passed proposals are executed slowly and manually
- **Treasury fragmentation**: Assets spread across chains, poor unified visibility and risk analysis

---

### 3. Opportunity / Why Now
- **DAOs are growing** but lack decision support tools
- **AI summarization and predictions** can compress complexity into actionable insight
- **Hathor Nano Contracts + EVM Bridge** enable lightweight, automated, and cross-chain aware execution

---

### 4. Solution Overview
- **AIDA**: AI insights + automated execution + cross‑chain treasury view
- **Three components**:
  - AI Backend (Python): summarize proposals, predict vote outcomes, assess treasury risks
  - Hathor Integration: Nano Contract to auto-execute approved proposals; EVM Bridge for cross-chain asset data
  - Front-End Dashboard: simple UI to surface insights and trigger automated actions
- **Hackathon scope**: Functional demo over production polish

---

### 5. Architecture
- **Backend** (`backend/`): FastAPI/Flask-style service exposing AI endpoints
- **Services**: `ai_service.py`, `hathor_service.py`, `treasury_service.py`, `proposal_service.py`
- **Contracts** (`contracts/`): `ProposalExecutor.sol`, `TreasuryManager.sol`
- **Frontend** (`frontend/`): React + TypeScript dashboard
- **Orchestration**: Docker Compose for end-to-end demo

---

### 6. AI Backend (Methods & Model Tasks)
- **Proposal summarization**: condense text to key points and pros/cons
- **Outcome prediction**: estimate likely vote results (e.g., approve/reject probability)
- **Risk analysis**: flag treasury concentrations, volatility exposure, runway projections
- **APIs**: REST endpoints consumed by frontend

---

### 7. Hathor Integration
- **Nano Contract**: Encodes the execution path for approved proposals
- **Automation**: Triggers on-chain actions after on-chain/DAO approval
- **EVM Bridge**: Pulls balances/activity from Ethereum and other chains for a unified view

---

### 8. Front-End Dashboard
- **Proposal Insights**: summaries, sentiment, predicted outcome, confidence
- **Treasury View**: cross-chain balances, risk flags, historical trends (MVP subset for demo)
- **Actions**: trigger automated execution via Nano Contract when approved

---

### 9. Demo Flow (What We’ll Show)
1) Load a real/representative proposal
2) AIDA generates summary, pros/cons, and predicted outcome
3) Treasury assessment view highlights risk hotspots
4) Proposal passes (simulated) → automation triggers via Nano Contract
5) Show success state and audit trail

---

### 10. Key Features (MVP)
- Proposal summarization and explainability
- Outcome prediction with confidence scoring
- Treasury risk detection (e.g., concentration, volatility)
- One-click automated execution for approved proposals

---

### 11. Impact & Metrics
- **Reduce decision time**: faster comprehension of proposals
- **Increase participation**: clearer insights → more informed voting
- **Operational efficiency**: automated execution reduces manual ops and errors
- **KPIs**: time-to-decision, participation rate, % automated executions, incident reduction

---

### 12. Differentiation
- **AI-native governance** vs. static dashboards
- **Hathor Nano Contracts** for lightweight, deterministic automation
- **Cross-chain view** via EVM Bridge baked into the workflow

---

### 13. Security & Risks
- Guardrails on automated execution (role-based triggers, dry-run)
- Clear audit trails and transparency
- Model limitations acknowledged; human-in-the-loop controls present

---

### 14. Roadmap
- Post-hackathon: refine models, expand chain coverage, richer risk analytics
- Governance plugins for major DAO frameworks
- Advanced simulation (e.g., proposal impact on runway/TVL)

---

### 15. Team & Ask
- Team introduces domain + ML + blockchain experience
- Ask: feedback, pilot DAOs, grants/partnerships

---

### 16. Appendix
- Links to repo, docs, and demo video (`demo.mp4`)
- Contract references and endpoints



