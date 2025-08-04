from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional
import os
from dotenv import load_dotenv

from models.database import engine, Base
from models.schemas import (
    DAOHealthResponse, 
    ProposalAnalysisRequest, 
    ProposalAnalysisResponse,
    ProposalSummaryResponse,
    ActionExecutionRequest,
    ActionExecutionResponse,
    TreasuryAnalysisResponse,
    GovernanceMetricsResponse
)
from services.ai_service import AIService
from services.dao_service import DAOService
from services.hathor_service import HathorService
from services.proposal_service import ProposalService
from services.treasury_service import TreasuryService

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting AIDA - AI-Driven DAO Analyst")
    yield
    # Shutdown
    print("🛑 Shutting down AIDA")

app = FastAPI(
    title="AIDA - AI-Driven DAO Analyst",
    description="Intelligent financial and governance analyst for DAOs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return response

# Initialize services
ai_service = AIService()
dao_service = DAOService()
hathor_service = HathorService()
proposal_service = ProposalService()
treasury_service = TreasuryService()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to AIDA - AI-Driven DAO Analyst",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AIDA"}

@app.get("/api/dao/{dao_address}/health", response_model=DAOHealthResponse)
async def get_dao_health(dao_address: str):
    """
    Get comprehensive health analysis of a DAO
    """
    try:
        health_data = await dao_service.analyze_dao_health(dao_address)
        
        return health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing DAO health: {str(e)}")

@app.post("/api/proposals/analyze", response_model=ProposalAnalysisResponse)
async def analyze_proposal(
    request: ProposalAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze a governance proposal using AI
    """
    try:
        # Add to background tasks for async processing
        background_tasks.add_task(proposal_service.store_analysis, request)
        
        # Analyze proposal
        analysis_result = await ai_service.analyze_proposal(request.dict())
        
        return ProposalAnalysisResponse(
            proposal_id=request.proposal_id,
            dao_address=request.dao_address,
            **analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing proposal: {str(e)}")

@app.get("/api/proposals/{proposal_id}/summary", response_model=ProposalSummaryResponse)
async def get_proposal_summary(proposal_id: str):
    """
    Get AI-generated summary of a governance proposal
    """
    try:
        summary = await proposal_service.get_proposal_summary(proposal_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Proposal summary not found: {str(e)}")

@app.post("/api/actions/execute", response_model=ActionExecutionResponse)
async def execute_action(request: ActionExecutionRequest):
    """
    Execute automated action using Hathor Nano Contracts
    """
    try:
        result = await hathor_service.execute_action(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing action: {str(e)}")

@app.get("/api/treasury/{dao_address}/analysis", response_model=TreasuryAnalysisResponse)
async def analyze_treasury(dao_address: str):
    """
    Get AI-powered treasury analysis
    """
    try:
        analysis = await treasury_service.analyze_treasury(dao_address)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing treasury: {str(e)}")

@app.get("/api/governance/{dao_address}/metrics", response_model=GovernanceMetricsResponse)
async def get_governance_metrics(dao_address: str):
    """
    Get governance metrics and predictions
    """
    try:
        metrics = await dao_service.get_governance_metrics(dao_address)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting governance metrics: {str(e)}")

@app.get("/api/predictions/{dao_address}/proposals")
async def get_proposal_predictions(dao_address: str, limit: int = 10):
    """
    Get AI predictions for upcoming proposals
    """
    try:
        predictions = await proposal_service.get_proposal_predictions(dao_address, limit)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting predictions: {str(e)}")

@app.get("/api/cross-chain/{dao_address}/assets")
async def get_cross_chain_assets(dao_address: str):
    """
    Get cross-chain asset analysis via Hathor EVM Bridge
    """
    try:
        assets = await hathor_service.get_cross_chain_assets(dao_address)
        return assets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting cross-chain assets: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 