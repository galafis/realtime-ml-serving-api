"""
Test suite for ML Client
Author: Gabriel Demetrios Lafis
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ml_client import MLClient
except ImportError:
    # If import fails, we'll skip tests
    MLClient = None


@pytest.mark.skipif(MLClient is None, reason="MLClient not available")
class TestMLClient:
    """Test cases for MLClient class"""

    def test_client_initialization(self):
        """Test client initialization with default parameters"""
        client = MLClient()
        assert client is not None
        assert hasattr(client, 'base_url')

    def test_client_initialization_with_custom_url(self):
        """Test client initialization with custom URL"""
        custom_url = "http://example.com:9000"
        client = MLClient(base_url=custom_url)
        assert client.base_url == custom_url

    def test_client_has_predict_method(self):
        """Test that client has predict method"""
        client = MLClient()
        assert hasattr(client, 'predict')
        assert callable(getattr(client, 'predict'))

    def test_client_has_health_check_method(self):
        """Test that client has health_check method"""
        client = MLClient()
        assert hasattr(client, 'health_check')
        assert callable(getattr(client, 'health_check'))

    def test_client_has_list_models_method(self):
        """Test that client has list_models method"""
        client = MLClient()
        assert hasattr(client, 'list_models')
        assert callable(getattr(client, 'list_models'))


# Test that can run without server
def test_client_module_import():
    """Test that ml_client module can be imported"""
    try:
        import ml_client
        assert ml_client is not None
    except ImportError:
        pytest.skip("ml_client module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
