"""
Simplified tests for Plugin API Endpoints - using only API calls
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.database import Base, get_db


# Setup test database with StaticPool to handle threading
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables once
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client"""
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Clear data between tests
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()
    
    test_client = TestClient(app)
    yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()


class TestPluginEndpoints:
    """Test Plugin CRUD operations"""
    
    def test_list_empty_plugins(self, client):
        """Test listing plugins when database is empty"""
        response = client.get("/api/v1/plugins/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_and_list_plugin(self, client):
        """Test creating and listing a plugin"""
        # Create plugin
        plugin_data = {
            "name": "test_plugin",
            "display_name": "Test Plugin",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        assert create_response.status_code == 201
        created = create_response.json()
        assert created["name"] == "test_plugin"
        
        # List plugins
        list_response = client.get("/api/v1/plugins/")
        assert list_response.status_code == 200
        plugins = list_response.json()
        assert len(plugins) == 1
        assert plugins[0]["name"] == "test_plugin"
    
    def test_get_plugin(self, client):
        """Test getting a specific plugin"""
        # Create plugin
        plugin_data = {
            "name": "get_test",
            "display_name": "Get Test",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        plugin_id = create_response.json()["id"]
        
        # Get plugin
        get_response = client.get(f"/api/v1/plugins/{plugin_id}")
        assert get_response.status_code == 200
        plugin = get_response.json()
        assert plugin["name"] == "get_test"
    
    def test_get_plugin_not_found(self, client):
        """Test getting non-existent plugin"""
        response = client.get("/api/v1/plugins/999")
        assert response.status_code == 404
    
    def test_create_plugin_duplicate_name(self, client):
        """Test creating plugin with duplicate name"""
        plugin_data = {
            "name": "duplicate",
            "display_name": "Duplicate Test",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        # First create
        client.post("/api/v1/plugins/", json=plugin_data)
        # Second create should fail
        response = client.post("/api/v1/plugins/", json=plugin_data)
        assert response.status_code == 409
    
    def test_update_plugin(self, client):
        """Test updating a plugin"""
        # Create plugin
        plugin_data = {
            "name": "update_test",
            "display_name": "Original Name",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        plugin_id = create_response.json()["id"]
        
        # Update plugin
        update_data = {
            "display_name": "Updated Name",
            "version": "2.0.0"
        }
        update_response = client.patch(f"/api/v1/plugins/{plugin_id}", json=update_data)
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["display_name"] == "Updated Name"
        assert updated["version"] == "2.0.0"
    
    def test_delete_plugin(self, client):
        """Test deleting a plugin"""
        # Create plugin
        plugin_data = {
            "name": "delete_test",
            "display_name": "Delete Test",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        plugin_id = create_response.json()["id"]
        
        # Delete plugin
        delete_response = client.delete(f"/api/v1/plugins/{plugin_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/plugins/{plugin_id}")
        assert get_response.status_code == 404
    
    def test_enable_disable_plugin(self, client):
        """Test enabling and disabling a plugin"""
        # Create plugin (disabled by default)
        plugin_data = {
            "name": "toggle_test",
            "display_name": "Toggle Test",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        plugin_id = create_response.json()["id"]
        
        # Enable plugin
        enable_response = client.post(f"/api/v1/plugins/{plugin_id}/enable")
        assert enable_response.status_code == 200
        assert enable_response.json()["enabled"] is True
        
        # Disable plugin
        disable_response = client.post(f"/api/v1/plugins/{plugin_id}/disable")
        assert disable_response.status_code == 200
        assert disable_response.json()["enabled"] is False


class TestPluginConfigurationEndpoints:
    """Test Plugin Configuration operations"""
    
    def test_create_and_get_configuration(self, client):
        """Test creating and getting plugin configuration"""
        # Create plugin first
        plugin_data = {
            "name": "config_test",
            "display_name": "Config Test",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        plugin_id = create_response.json()["id"]
        
        # Create configuration
        config_data = {
            "key": "test_key",
            "value": {"setting": "value"}
        }
        config_response = client.post(f"/api/v1/plugins/{plugin_id}/config", json=config_data)
        assert config_response.status_code == 201
        config = config_response.json()
        assert config["key"] == "test_key"
        assert config["value"] == {"setting": "value"}
        
        # Get configurations
        list_response = client.get(f"/api/v1/plugins/{plugin_id}/config")
        assert list_response.status_code == 200
        configs = list_response.json()
        assert len(configs) == 1
        assert configs[0]["key"] == "test_key"
    
    def test_update_configuration(self, client):
        """Test updating plugin configuration"""
        # Create plugin
        plugin_data = {
            "name": "config_update",
            "display_name": "Config Update",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        plugin_id = create_response.json()["id"]
        
        # Create configuration
        config_data = {
            "key": "update_key",
            "value": {"original": "value"}
        }
        config_response = client.post(f"/api/v1/plugins/{plugin_id}/config", json=config_data)
        config_id = config_response.json()["id"]
        
        # Update configuration
        update_data = {
            "value": {"updated": "value"}
        }
        update_response = client.patch(f"/api/v1/plugins/{plugin_id}/config/{config_id}", json=update_data)
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["value"] == {"updated": "value"}
    
    def test_delete_configuration(self, client):
        """Test deleting plugin configuration"""
        # Create plugin
        plugin_data = {
            "name": "config_delete",
            "display_name": "Config Delete",
            "version": "1.0.0",
            "plugin_type": "python",
            "entry_point": "test.py"
        }
        create_response = client.post("/api/v1/plugins/", json=plugin_data)
        plugin_id = create_response.json()["id"]
        
        # Create configuration
        config_data = {
            "key": "delete_key",
            "value": {"test": "value"}
        }
        config_response = client.post(f"/api/v1/plugins/{plugin_id}/config", json=config_data)
        config_id = config_response.json()["id"]
        
        # Delete configuration
        delete_response = client.delete(f"/api/v1/plugins/{plugin_id}/config/{config_id}")
        assert delete_response.status_code == 204
