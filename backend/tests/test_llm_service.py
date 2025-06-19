import pytest
from app.llm_service import LLMService
import os

class TestLLMService:
    """Test cases for the LLM service."""
    
    def setup_method(self):
        """Set up test environment."""
        self.llm_service = LLMService()
    
    def test_fallback_analysis(self):
        """Test fallback analysis when LLM is not available."""
        # Test with programming request
        result = self.llm_service._fallback_analysis("I want programming jokes")
        assert result["category"] == "Programming"
        assert "programming" in result["keywords"]
        assert result["reasoning"] is not None
        
        # Test with dark humor request
        result = self.llm_service._fallback_analysis("Give me some dark jokes")
        assert result["category"] == "Dark"
        assert "dark" in result["keywords"]
        
        # Test with vague request
        result = self.llm_service._fallback_analysis("Tell me a joke")
        assert result["category"] == "Any"
    
    @pytest.mark.asyncio
    async def test_analyze_request_fallback(self):
        """Test analyze_request with fallback behavior."""
        # This test will use fallback if no API key is set
        result = await self.llm_service.analyze_request("I need programming jokes")
        
        assert "category" in result
        assert "keywords" in result
        assert "reasoning" in result
        assert "user_mood" in result
        assert "suggested_amount" in result
        
        # Should be Programming category for this request
        assert result["category"] in ["Programming", "Any"]
    
    @pytest.mark.asyncio
    async def test_generate_response_context_fallback(self):
        """Test response context generation with fallback."""
        jokes_data = [
            {
                "setup": "Why do programmers prefer dark mode?",
                "delivery": "Because light attracts bugs!",
                "category": "Programming"
            }
        ]
        
        result = await self.llm_service.generate_response_context(
            "I want programming jokes", 
            jokes_data
        )
        
        assert isinstance(result, str)
        assert len(result) > 0 