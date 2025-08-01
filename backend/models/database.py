from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aida.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DAO(Base):
    __tablename__ = "daos"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(Text)
    treasury_address = Column(String)
    governance_token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    proposals = relationship("Proposal", back_populates="dao")
    treasury_analyses = relationship("TreasuryAnalysis", back_populates="dao")
    health_reports = relationship("DAOHealthReport", back_populates="dao")

class Proposal(Base):
    __tablename__ = "proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(String, unique=True, index=True)
    dao_id = Column(Integer, ForeignKey("daos.id"))
    title = Column(String)
    description = Column(Text)
    proposer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    voting_start = Column(DateTime)
    voting_end = Column(DateTime)
    status = Column(String)  # active, passed, failed, executed
    
    # AI Analysis fields
    ai_prediction = Column(Float)  # 0-1 probability of passing
    ai_confidence = Column(Float)  # 0-1 confidence in prediction
    ai_summary = Column(Text)
    ai_risk_assessment = Column(String)  # low, medium, high
    ai_recommendations = Column(Text)
    
    # Relationships
    dao = relationship("DAO", back_populates="proposals")
    analysis = relationship("ProposalAnalysis", back_populates="proposal", uselist=False)

class ProposalAnalysis(Base):
    __tablename__ = "proposal_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"))
    analysis_type = Column(String)  # sentiment, risk, impact, etc.
    analysis_data = Column(Text)  # JSON string of analysis results
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    proposal = relationship("Proposal", back_populates="analysis")

class TreasuryAnalysis(Base):
    __tablename__ = "treasury_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    dao_id = Column(Integer, ForeignKey("daos.id"))
    total_value_usd = Column(Float)
    asset_diversification_score = Column(Float)  # 0-1
    risk_score = Column(Float)  # 0-1
    liquidity_score = Column(Float)  # 0-1
    ai_recommendations = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dao = relationship("DAO", back_populates="treasury_analyses")

class DAOHealthReport(Base):
    __tablename__ = "dao_health_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    dao_id = Column(Integer, ForeignKey("daos.id"))
    overall_health_score = Column(Float)  # 0-1
    governance_score = Column(Float)  # 0-1
    financial_score = Column(Float)  # 0-1
    community_score = Column(Float)  # 0-1
    risk_factors = Column(Text)  # JSON array of risk factors
    recommendations = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dao = relationship("DAO", back_populates="health_reports")

class ActionExecution(Base):
    __tablename__ = "action_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String)  # proposal_execution, treasury_rebalance, etc.
    dao_address = Column(String)
    proposal_id = Column(String, nullable=True)
    transaction_hash = Column(String, nullable=True)
    status = Column(String)  # pending, executed, failed
    execution_data = Column(Text)  # JSON string of execution details
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)

class CrossChainAsset(Base):
    __tablename__ = "cross_chain_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    dao_address = Column(String)
    chain_name = Column(String)  # ethereum, polygon, etc.
    asset_address = Column(String)
    asset_symbol = Column(String)
    balance = Column(Float)
    value_usd = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 