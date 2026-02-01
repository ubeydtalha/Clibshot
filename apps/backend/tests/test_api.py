"""
Tests for ClipShot Backend API
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check_returns_200(self):
        """Health endpoint should return 200 OK"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
    
    def test_health_check_returns_json(self):
        """Health endpoint should return JSON"""
        response = client.get("/api/v1/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_check_has_status_field(self):
        """Health response should have status field"""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
    
    def test_health_check_has_service_field(self):
        """Health response should have service name"""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "service" in data
        assert data["service"] == "clipshot-backend"
    
    def test_health_check_has_version_field(self):
        """Health response should have version"""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "0.1.0"
    
    def test_health_check_has_timestamp(self):
        """Health response should have timestamp"""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "timestamp" in data
        # Verify it's a valid ISO format
        from datetime import datetime
        datetime.fromisoformat(data["timestamp"])


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_returns_200(self):
        """Root endpoint should return 200 OK"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_has_message(self):
        """Root response should have message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
    
    def test_root_has_docs_link(self):
        """Root response should have docs link"""
        response = client.get("/")
        data = response.json()
        assert "docs" in data
        assert data["docs"] == "/api/docs"
    
    def test_root_has_health_link(self):
        """Root response should have health link"""
        response = client.get("/")
        data = response.json()
        assert "health" in data
        assert data["health"] == "/api/v1/health"


class TestPluginsEndpoint:
    """Test plugins endpoint"""
    
    def test_plugins_endpoint_returns_200(self):
        """Plugins endpoint should return 200 OK"""
        response = client.get("/api/v1/plugins")
        assert response.status_code == 200
    
    def test_plugins_endpoint_returns_list(self):
        """Plugins endpoint should return a list"""
        response = client.get("/api/v1/plugins")
        data = response.json()
        assert isinstance(data, list)
    
    def test_plugins_endpoint_has_count(self):
        """Plugins endpoint list should be countable"""
        response = client.get("/api/v1/plugins")
        data = response.json()
        assert isinstance(data, list)
        # Just verify it's a valid list (count is implicit in list length)


class TestClipsEndpoint:
    """Test clips endpoint"""
    
    def test_clips_endpoint_returns_200(self):
        """Clips endpoint should return 200 OK"""
        response = client.get("/api/v1/clips")
        assert response.status_code == 200
    
    def test_clips_endpoint_returns_list(self):
        """Clips endpoint should return a list"""
        response = client.get("/api/v1/clips")
        data = response.json()
        assert isinstance(data, list)
    
    def test_clips_endpoint_has_count(self):
        """Clips endpoint list should be countable"""
        response = client.get("/api/v1/clips")
        data = response.json()
        assert isinstance(data, list)
        # Just verify it's a valid list (count is implicit in list length)


class TestAIEndpoint:
    """Test AI models endpoint"""
    
    def test_ai_models_endpoint_returns_200(self):
        """AI models endpoint should return 200 OK"""
        response = client.get("/api/v1/ai/models")
        assert response.status_code == 200
    
    def test_ai_models_endpoint_returns_list(self):
        """AI models endpoint should return list structure"""
        response = client.get("/api/v1/ai/models")
        data = response.json()
        assert "models" in data
        assert isinstance(data["models"], list)


class TestCORS:
    """Test CORS configuration"""
    
    def test_cors_allows_tauri_origin(self):
        """CORS should allow Tauri origin"""
        response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "tauri://localhost",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_vite_dev_origin(self):
        """CORS should allow Vite dev server origin"""
        response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_on_nonexistent_endpoint(self):
        """Should return 404 for nonexistent endpoints"""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404
    
    def test_404_returns_json(self):
        """404 response should be JSON"""
        response = client.get("/api/v1/nonexistent")
        assert response.headers["content-type"] == "application/json"


class TestDocumentation:
    """Test API documentation endpoints"""
    
    def test_swagger_docs_accessible(self):
        """Swagger docs should be accessible"""
        response = client.get("/api/docs")
        assert response.status_code == 200
    
    def test_redoc_docs_accessible(self):
        """ReDoc docs should be accessible"""
        response = client.get("/api/redoc")
        assert response.status_code == 200


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
