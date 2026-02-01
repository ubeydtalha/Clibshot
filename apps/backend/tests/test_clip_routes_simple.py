"""
Simplified tests for Clip API Endpoints - using only API calls
"""
import pytest
from datetime import datetime
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


class TestClipEndpoints:
    """Test Clip CRUD operations"""
    
    def test_list_empty_clips(self, client):
        """Test listing clips when database is empty"""
        response = client.get("/api/v1/clips/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_and_list_clip(self, client):
        """Test creating and listing a clip"""
        # Create clip
        clip_data = {
            "title": "Test Clip",
            "file_path": "/clips/test.mp4",
            "game_name": "CS2"
        }
        create_response = client.post("/api/v1/clips/", json=clip_data)
        assert create_response.status_code == 201
        created = create_response.json()
        assert created["title"] == "Test Clip"
        assert created["file_path"] == "/clips/test.mp4"
        
        # List clips
        list_response = client.get("/api/v1/clips/")
        assert list_response.status_code == 200
        clips = list_response.json()
        assert len(clips) == 1
        assert clips[0]["title"] == "Test Clip"
    
    def test_get_clip(self, client):
        """Test getting a specific clip"""
        # Create clip
        clip_data = {
            "title": "Get Test Clip",
            "file_path": "/clips/get.mp4"
        }
        create_response = client.post("/api/v1/clips/", json=clip_data)
        clip_id = create_response.json()["id"]
        
        # Get clip
        get_response = client.get(f"/api/v1/clips/{clip_id}")
        assert get_response.status_code == 200
        clip = get_response.json()
        assert clip["title"] == "Get Test Clip"
    
    def test_get_clip_not_found(self, client):
        """Test getting non-existent clip"""
        response = client.get("/api/v1/clips/999")
        assert response.status_code == 404
    
    def test_create_clip_with_metadata(self, client):
        """Test creating clip with full metadata"""
        clip_data = {
            "title": "Full Metadata Clip",
            "file_path": "/clips/full.mp4",
            "game_name": "Valorant",
            "duration": 45,
            "resolution": "1920x1080",
            "fps": 60,
            "tags": ["highlight", "ace"],
            "clip_metadata": {"player": "test_user", "map": "Haven"}
        }
        response = client.post("/api/v1/clips/", json=clip_data)
        assert response.status_code == 201
        clip = response.json()
        assert clip["title"] == "Full Metadata Clip"
        assert clip["game_name"] == "Valorant"
        assert clip["duration"] == 45
        assert "highlight" in clip["tags"]
        # Response uses serialization alias 'metadata' not 'clip_metadata'
        assert clip["metadata"]["player"] == "test_user"
    
    def test_update_clip(self, client):
        """Test updating a clip"""
        # Create clip
        clip_data = {
            "title": "Original Title",
            "file_path": "/clips/update.mp4"
        }
        create_response = client.post("/api/v1/clips/", json=clip_data)
        clip_id = create_response.json()["id"]
        
        # Update clip
        update_data = {
            "title": "Updated Title",
            "game_name": "CS2",
            "processed": True
        }
        update_response = client.patch(f"/api/v1/clips/{clip_id}", json=update_data)
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["title"] == "Updated Title"
        assert updated["game_name"] == "CS2"
        assert updated["processed"] is True
    
    def test_delete_clip(self, client):
        """Test deleting a clip"""
        # Create clip
        clip_data = {
            "title": "Delete Me",
            "file_path": "/clips/delete.mp4"
        }
        create_response = client.post("/api/v1/clips/", json=clip_data)
        clip_id = create_response.json()["id"]
        
        # Delete clip
        delete_response = client.delete(f"/api/v1/clips/{clip_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/clips/{clip_id}")
        assert get_response.status_code == 404
    
    def test_filter_clips_by_game(self, client):
        """Test filtering clips by game name"""
        # Create clips
        client.post("/api/v1/clips/", json={"title": "CS Clip", "file_path": "/cs.mp4", "game_name": "CS2"})
        client.post("/api/v1/clips/", json={"title": "Val Clip", "file_path": "/val.mp4", "game_name": "Valorant"})
        
        # Filter by CS2
        response = client.get("/api/v1/clips/?game_name=CS2")
        assert response.status_code == 200
        clips = response.json()
        assert len(clips) == 1
        assert clips[0]["game_name"] == "CS2"
    
    def test_filter_clips_by_processed(self, client):
        """Test filtering clips by processed status"""
        # Create clips
        client.post("/api/v1/clips/", json={"title": "Processed", "file_path": "/p.mp4", "processed": True})
        client.post("/api/v1/clips/", json={"title": "Unprocessed", "file_path": "/u.mp4", "processed": False})
        
        # Filter by unprocessed (use 0 instead of False string)
        response = client.get("/api/v1/clips/?processed=0")
        assert response.status_code == 200
        clips = response.json()
        assert len(clips) == 1
        assert clips[0]["processed"] is False
    
    def test_pagination(self, client):
        """Test clip pagination"""
        # Create 5 clips
        for i in range(5):
            client.post("/api/v1/clips/", json={
                "title": f"Clip {i}",
                "file_path": f"/clip{i}.mp4"
            })
        
        # Get page 1 (2 items)
        response = client.get("/api/v1/clips/?skip=0&limit=2")
        assert response.status_code == 200
        clips = response.json()
        assert len(clips) == 2
        
        # Get page 2 (next 2 items)
        response = client.get("/api/v1/clips/?skip=2&limit=2")
        assert response.status_code == 200
        clips = response.json()
        assert len(clips) == 2
    
    def test_clip_stats(self, client):
        """Test clip statistics endpoint"""
        # Create clips with different games and statuses
        client.post("/api/v1/clips/", json={"title": "C1", "file_path": "/c1.mp4", "game_name": "CS2", "processed": True})
        client.post("/api/v1/clips/", json={"title": "C2", "file_path": "/c2.mp4", "game_name": "CS2", "processed": False})
        client.post("/api/v1/clips/", json={"title": "C3", "file_path": "/c3.mp4", "game_name": "Valorant", "processed": False})
        
        # Get stats
        response = client.get("/api/v1/clips/stats")
        assert response.status_code == 200
        stats = response.json()
        assert stats["total_clips"] == 3
        assert stats["processed_clips"] == 1
        assert stats["unprocessed_clips"] == 2
    
    def test_create_clip_missing_title(self, client):
        """Test creating clip without required title"""
        clip_data = {
            "file_path": "/clips/test.mp4"
        }
        response = client.post("/api/v1/clips/", json=clip_data)
        assert response.status_code == 422
    
    def test_create_clip_missing_file_path(self, client):
        """Test creating clip without required file_path"""
        clip_data = {
            "title": "Test Clip"
        }
        response = client.post("/api/v1/clips/", json=clip_data)
        assert response.status_code == 422
