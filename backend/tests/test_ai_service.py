"""
Unit tests for AI Service
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from services.ai_service import AIService
from services.base_service import BaseService


class TestAIService:
    """Test cases for AIService"""
    
    @pytest.fixture
    def ai_service(self):
        """Create AI service instance for testing"""
        return AIService()
    
    @pytest.fixture
    def mock_openai_response(self):
        """Mock OpenAI API response"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "0.75"
        return mock_response
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment_with_openai(self, ai_service, mock_openai_response):
        """Test sentiment analysis with OpenAI API"""
        test_text = "This is a positive proposal that will improve the DAO."
        
        with patch.object(ai_service, 'openai_available', True):
            with patch.object(ai_service, 'openai_client') as mock_client:
                mock_client.chat.completions.create = AsyncMock(return_value=mock_openai_response)
                
                result = await ai_service._analyze_sentiment(test_text)
                
                assert isinstance(result, float)
                assert -1.0 <= result <= 1.0
                mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment_fallback(self, ai_service):
        """Test sentiment analysis fallback when OpenAI is unavailable"""
        test_text = "This proposal will improve the DAO governance."
        
        with patch.object(ai_service, 'openai_available', False):
            result = await ai_service._analyze_sentiment(test_text)
            
            assert isinstance(result, float)
            assert -1.0 <= result <= 1.0
    
    @pytest.mark.asyncio
    async def test_generate_summary_with_openai(self, ai_service):
        """Test summary generation with OpenAI API"""
        test_text = "This is a long proposal text that needs to be summarized."
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This proposal aims to improve governance."
        
        with patch.object(ai_service, 'openai_available', True):
            with patch.object(ai_service, 'openai_client') as mock_client:
                mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
                
                result = await ai_service._generate_summary(test_text)
                
                assert isinstance(result, str)
                assert len(result) > 0
                mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_summary_fallback(self, ai_service):
        """Test summary generation fallback"""
        test_text = "This is a test proposal."
        
        with patch.object(ai_service, 'openai_available', False):
            result = await ai_service._generate_summary(test_text)
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert "proposal" in result.lower()
    
    @pytest.mark.asyncio
    async def test_assess_risk_with_openai(self, ai_service):
        """Test risk assessment with OpenAI API"""
        test_text = "This proposal involves significant changes to treasury allocation."
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "medium"
        
        with patch.object(ai_service, 'openai_available', True):
            with patch.object(ai_service, 'openai_client') as mock_client:
                mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
                
                result = await ai_service._assess_risk(test_text)
                
                assert isinstance(result, str)
                assert result in ['low', 'medium', 'high']
                mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_assess_risk_fallback(self, ai_service):
        """Test risk assessment fallback"""
        test_text = "This proposal involves treasury changes."
        
        with patch.object(ai_service, 'openai_available', False):
            result = await ai_service._assess_risk(test_text)
            
            assert isinstance(result, str)
            assert result in ['low', 'medium', 'high']
    
    @pytest.mark.asyncio
    async def test_extract_key_points_with_openai(self, ai_service):
        """Test key points extraction with OpenAI API"""
        test_text = "This proposal will improve governance, increase efficiency, and reduce costs."
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Improve governance\nIncrease efficiency\nReduce costs"
        
        with patch.object(ai_service, 'openai_available', True):
            with patch.object(ai_service, 'openai_client') as mock_client:
                mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
                
                result = await ai_service._extract_key_points(test_text)
                
                assert isinstance(result, list)
                assert len(result) > 0
                assert all(isinstance(point, str) for point in result)
                mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_extract_key_points_fallback(self, ai_service):
        """Test key points extraction fallback"""
        test_text = "This proposal will improve governance."
        
        with patch.object(ai_service, 'openai_available', False):
            result = await ai_service._extract_key_points(test_text)
            
            assert isinstance(result, list)
            assert len(result) > 0
            assert all(isinstance(point, str) for point in result)
    
    @pytest.mark.asyncio
    async def test_generate_recommendations_with_openai(self, ai_service):
        """Test recommendations generation with OpenAI API"""
        test_text = "This proposal involves treasury rebalancing."
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Consider the risk-reward profile\nEvaluate market conditions"
        
        with patch.object(ai_service, 'openai_available', True):
            with patch.object(ai_service, 'openai_client') as mock_client:
                mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
                
                result = await ai_service._generate_recommendations(test_text)
                
                assert isinstance(result, list)
                assert len(result) > 0
                assert all(isinstance(rec, str) for rec in result)
                mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_recommendations_fallback(self, ai_service):
        """Test recommendations generation fallback"""
        test_text = "This proposal involves treasury changes."
        
        with patch.object(ai_service, 'openai_available', False):
            result = await ai_service._generate_recommendations(test_text)
            
            assert isinstance(result, list)
            assert len(result) > 0
            assert all(isinstance(rec, str) for rec in result)
    
    @pytest.mark.asyncio
    async def test_analyze_impact_with_openai(self, ai_service):
        """Test impact analysis with OpenAI API"""
        test_text = "This proposal will increase treasury yield by 20%."
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "high"
        
        with patch.object(ai_service, 'openai_available', True):
            with patch.object(ai_service, 'openai_client') as mock_client:
                mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
                
                result = await ai_service._analyze_impact(test_text)
                
                assert isinstance(result, str)
                assert result in ['low', 'medium', 'high']
                mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_impact_fallback(self, ai_service):
        """Test impact analysis fallback"""
        test_text = "This proposal will increase yield."
        
        with patch.object(ai_service, 'openai_available', False):
            result = await ai_service._analyze_impact(test_text)
            
            assert isinstance(result, str)
            assert result in ['low', 'medium', 'high']
    
    @pytest.mark.asyncio
    async def test_analyze_proposal_comprehensive(self, ai_service):
        """Test comprehensive proposal analysis"""
        proposal_data = {
            "dao_address": "0x1234567890abcdef",
            "proposal_id": "prop_001",
            "title": "Treasury Rebalancing Proposal",
            "description": "This proposal aims to rebalance the treasury portfolio to optimize yield and reduce risk exposure.",
            "proposer": "0xabcdef1234567890"
        }
        
        with patch.object(ai_service, 'openai_available', False):  # Use fallback for testing
            result = await ai_service.analyze_proposal(proposal_data)
            
            assert isinstance(result, dict)
            assert 'sentiment_score' in result
            assert 'summary' in result
            assert 'risk_level' in result
            assert 'key_points' in result
            assert 'recommendations' in result
            assert 'impact_level' in result
            assert 'prediction' in result
            
            assert isinstance(result['sentiment_score'], float)
            assert isinstance(result['summary'], str)
            assert isinstance(result['risk_level'], str)
            assert isinstance(result['key_points'], list)
            assert isinstance(result['recommendations'], list)
            assert isinstance(result['impact_level'], str)
            assert isinstance(result['prediction'], dict)
    
    def test_fallback_responses_loaded(self, ai_service):
        """Test that fallback responses are properly loaded"""
        assert hasattr(ai_service, 'fallback_responses')
        assert isinstance(ai_service.fallback_responses, dict)
        assert 'summaries' in ai_service.fallback_responses
        assert 'key_points' in ai_service.fallback_responses
        assert 'recommendations' in ai_service.fallback_responses
        
        assert isinstance(ai_service.fallback_responses['summaries'], list)
        assert isinstance(ai_service.fallback_responses['key_points'], list)
        assert isinstance(ai_service.fallback_responses['recommendations'], list)
    
    def test_openai_availability_check(self, ai_service):
        """Test OpenAI availability check"""
        # Test when OpenAI is available
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            ai_service_with_key = AIService()
            assert ai_service_with_key.openai_available is True
        
        # Test when OpenAI is not available
        with patch.dict('os.environ', {}, clear=True):
            ai_service_without_key = AIService()
            assert ai_service_without_key.openai_available is False
    
    @pytest.mark.asyncio
    async def test_error_handling_openai_failure(self, ai_service):
        """Test error handling when OpenAI API fails"""
        test_text = "Test proposal text."
        
        with patch.object(ai_service, 'openai_available', True):
            with patch.object(ai_service, 'openai_client') as mock_client:
                mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
                
                # Should fall back to fallback method
                result = await ai_service._analyze_sentiment(test_text)
                
                assert isinstance(result, float)
                assert -1.0 <= result <= 1.0


class TestAIServiceIntegration:
    """Integration tests for AI Service"""
    
    @pytest.fixture
    def ai_service(self):
        """Create AI service instance for integration testing"""
        return AIService()
    
    @pytest.mark.asyncio
    async def test_full_proposal_analysis_workflow(self, ai_service):
        """Test complete proposal analysis workflow"""
        proposal_data = {
            "dao_address": "0x1234567890abcdef",
            "proposal_id": "prop_002",
            "title": "Governance Structure Improvement",
            "description": "This proposal suggests implementing a new voting mechanism to improve governance efficiency and increase community participation. The changes include reducing voting complexity and enhancing transparency.",
            "proposer": "0xabcdef1234567890"
        }
        
        result = await ai_service.analyze_proposal(proposal_data)
        
        # Verify all required fields are present
        required_fields = [
            'sentiment_score', 'summary', 'risk_level', 'key_points',
            'recommendations', 'impact_level', 'prediction'
        ]
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
        
        # Verify data types and constraints
        assert -1.0 <= result['sentiment_score'] <= 1.0
        assert result['risk_level'] in ['low', 'medium', 'high']
        assert result['impact_level'] in ['low', 'medium', 'high']
        assert len(result['key_points']) > 0
        assert len(result['recommendations']) > 0
        assert isinstance(result['prediction'], dict)
        assert 'confidence' in result['prediction']
        assert 'outcome' in result['prediction']
    
    @pytest.mark.asyncio
    async def test_multiple_proposals_consistency(self, ai_service):
        """Test consistency across multiple proposal analyses"""
        proposals = [
            {
                "dao_address": "0x1234567890abcdef",
                "proposal_id": "prop_003",
                "title": "Low Risk Proposal",
                "description": "This proposal suggests minor UI improvements.",
                "proposer": "0xabcdef1234567890"
            },
            {
                "dao_address": "0x1234567890abcdef",
                "proposal_id": "prop_004",
                "title": "High Risk Proposal",
                "description": "This proposal suggests completely restructuring the treasury with high-risk investments.",
                "proposer": "0xabcdef1234567890"
            }
        ]
        
        results = []
        for proposal in proposals:
            result = await ai_service.analyze_proposal(proposal)
            results.append(result)
        
        # Verify both analyses completed successfully
        assert len(results) == 2
        for result in results:
            assert 'sentiment_score' in result
            assert 'risk_level' in result
            assert 'impact_level' in result 