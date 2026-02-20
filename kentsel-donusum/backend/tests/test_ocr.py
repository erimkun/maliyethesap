import pytest
from unittest.mock import AsyncMock, patch
from app.services.llm_service import LLMService

@pytest.mark.asyncio
async def test_kaks_taks_extract_mock():
    llm = LLMService()
    llm.api_key = "mock_dummy_key"
    llm.client = AsyncMock()
    
    # Mocking Claude API response
    mock_response = AsyncMock()
    mock_message_text = AsyncMock()
    mock_message_text.text = '{"taks": "0.35", "kaks": "1.75", "yapi_nizam": "ayrik", "max_yukseklik_m": 12.5}'
    mock_response.content = [mock_message_text]
    
    llm.client.messages.create.return_value = mock_response
    
    res = await llm.imar_notu_parse("Belediye planına göre emsal 1.75 ve Taks 0.35'tir.", "101", "2")
    
    assert res['taks'] == "0.35"
    assert res['kaks'] == "1.75"
    assert res['yapi_nizam'] == "ayrik"
