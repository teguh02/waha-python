"""
Unit tests for WAHA Python client
"""

import pytest
from waha_python import WAHAClient, WAHAAuthenticationError

def test_client_initialization():
    """Test client initialization"""
    client = WAHAClient(
        base_url="http://localhost:3000",
        api_key="test-key"
    )
    
    assert client.base_url == "http://localhost:3000"
    assert client.api_key == "test-key"
    assert client.timeout == 30
    
    # Check that modules are initialized
    assert hasattr(client, 'sessions')
    assert hasattr(client, 'messages')
    assert hasattr(client, 'chats')
    assert hasattr(client, 'contacts')
    assert hasattr(client, 'groups')
    assert hasattr(client, 'status')
    assert hasattr(client, 'channels')

def test_client_context_manager():
    """Test client context manager"""
    with WAHAClient(base_url="http://localhost:3000") as client:
        assert client is not None
    
    # Client should be closed after context
    assert client._session.closed

def test_default_base_url():
    """Test default base URL"""
    client = WAHAClient()
    assert client.base_url == "http://localhost:3000"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

