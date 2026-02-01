"""
Tests for Clip API Endpoints
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.database import Base, get_db
from src.models import Clip


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


@pytest.fixture
def test_db():
    """Create a test database with proper threading support"""
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Clear data between tests instead of dropping/creating tables
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    
    yield db  # Return the db session for tests to use
    
    db.close()
    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """Create a test client"""
    return TestClient(app)


class TestClipListEndpoint:
    """Test GET /api/v1/clips"""
    
    def test_list_empty_clips(self, client, test_db):
        """Test listing clips when none exist"""
        response = client.get("/api/v1/clips/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_clips(self, client, test_db):
        """Test listing clips"""
        clip1 = Clip(
            title="Clip 1",
            file_path="/clips/clip1.mp4",
            game_name="CS2"
        )
        clip2 = Clip(
            title="Clip 2",
            file_path="/clips/clip2.mp4",
            game_name="Valorant"
        )
        
        test_db.add_all([clip1, clip2])
        test_db.commit()
        
        response = client.get("/api/v1/clips/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_list_clips_filter_by_game(self, client, test_db):
        """Test filtering clips by game name"""
        clip1 = Clip(title="CS Clip", file_path="/clips/cs.mp4", game_name="CS2")
        clip2 = Clip(title="Val Clip", file_path="/clips/val.mp4", game_name="Valorant")
        clip3 = Clip(title="CS Clip 2", file_path="/clips/cs2.mp4", game_name="CS2")
        
        test_db.add_all([clip1, clip2, clip3])
        test_db.commit()
        
        response = client.get("/api/v1/clips/?game_name=CS2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(clip["game_name"] == "CS2" for clip in data)
    
    def test_list_clips_filter_by_processed(self, client, test_db):
        """Test filtering clips by processed status"""
        clip1 = Clip(title="Processed", file_path="/clips/p.mp4", processed=True)
        clip2 = Clip(title="Unprocessed 1", file_path="/clips/u1.mp4", processed=False)
        clip3 = Clip(title="Unprocessed 2", file_path="/clips/u2.mp4", processed=False)
        
        test_db.add_all([clip1, clip2, clip3])
        test_db.commit()
        
        response = client.get("/api/v1/clips/?processed=false")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(not clip["processed"] for clip in data)
    
    def test_list_clips_pagination(self, client, test_db):
        """Test clip list pagination"""
        for i in range(5):
            clip = Clip(
                title=f"Clip {i}",
                file_path=f"/clips/clip{i}.mp4"
            )
            test_db.add(clip)
        test_db.commit()
        
        response = client.get("/api/v1/clips/?skip=2&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_list_clips_ordered_by_created(self, client, test_db):
        """Test clips are ordered by created_at descending"""
        clip1 = Clip(title="First", file_path="/clips/1.mp4")
        clip2 = Clip(title="Second", file_path="/clips/2.mp4")
        clip3 = Clip(title="Third", file_path="/clips/3.mp4")
        
        test_db.add_all([clip1, clip2, clip3])
        test_db.commit()
        
        response = client.get("/api/v1/clips/")
        
        assert response.status_code == 200
        data = response.json()
        # Should be ordered newest first
        assert data[0]["title"] == "Third"
        assert data[2]["title"] == "First"


class TestClipGetEndpoint:
    """Test GET /api/v1/clips/{id}"""
    
    def test_get_clip_success(self, client, test_db):
        """Test getting a specific clip"""
        clip = Clip(
            title="Test Clip",
            file_path="/clips/test.mp4",
            game_name="CS2",
            duration=45,
            resolution="1920x1080",
            fps=60
        )
        
        test_db.add(clip)
        test_db.commit()
        test_db.refresh(clip)
        
        response = client.get(f"/api/v1/clips/{clip.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Clip"
        assert data["game_name"] == "CS2"
        assert data["duration"] == 45
    
    def test_get_clip_not_found(self, client, test_db):
        """Test getting non-existent clip"""
        response = client.get("/api/v1/clips/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestClipCreateEndpoint:
    """Test POST /api/v1/clips"""
    
    def test_create_clip_success(self, client, test_db):
        """Test creating a new clip"""
        clip_data = {
            "title": "Epic Victory",
            "file_path": "/clips/epic.mp4",
            "description": "Amazing clutch",
            "game_name": "CS2",
            "duration": 45,
            "resolution": "1920x1080",
            "fps": 60,
            "codec": "h264",
            "tags": ["epic", "clutch"]
        }
        
        response = client.post("/api/v1/clips/", json=clip_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Epic Victory"
        assert data["id"] is not None
        assert len(data["tags"]) == 2
        assert data["processed"] is False
    
    def test_create_clip_minimal_data(self, client, test_db):
        """Test creating clip with minimal required fields"""
        clip_data = {
            "title": "Minimal Clip",
            "file_path": "/clips/minimal.mp4"
        }
        
        response = client.post("/api/v1/clips/", json=clip_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Clip"
        assert data["description"] is None
        assert data["game_name"] is None
    
    def test_create_clip_with_metadata(self, client, test_db):
        """Test creating clip with metadata"""
        clip_data = {
            "title": "Meta Clip",
            "file_path": "/clips/meta.mp4",
            "metadata": {
                "highlights": [{"timestamp": 10, "score": 0.9}],
                "custom_field": "value"
            }
        }
        
        response = client.post("/api/v1/clips/", json=clip_data)
        
        assert response.status_code == 201
        # Note: metadata field is clip_metadata in DB but metadata in API
        # The plugin event handler might modify it
    
    def test_create_clip_with_recorded_at(self, client, test_db):
        """Test creating clip with recorded timestamp"""
        clip_data = {
            "title": "Timestamped Clip",
            "file_path": "/clips/time.mp4",
            "recorded_at": "2026-01-15T14:30:00"
        }
        
        response = client.post("/api/v1/clips/", json=clip_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["recorded_at"] is not None


class TestClipUpdateEndpoint:
    """Test PUT /api/v1/clips/{id}"""
    
    def test_update_clip_success(self, client, test_db):
        """Test updating a clip"""
        clip = Clip(
            title="Original Title",
            file_path="/clips/original.mp4",
            game_name="CS2"
        )
        test_db.add(clip)
        test_db.commit()
        test_db.refresh(clip)
        
        update_data = {
            "title": "Updated Title",
            "description": "New description",
            "tags": ["updated", "new"]
        }
        
        response = client.put(f"/api/v1/clips/{clip.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "New description"
        assert len(data["tags"]) == 2
    
    def test_update_clip_processing_status(self, client, test_db):
        """Test updating clip processing status"""
        clip = Clip(
            title="Processing Test",
            file_path="/clips/process.mp4",
            processed=False,
            processing_status="pending"
        )
        test_db.add(clip)
        test_db.commit()
        test_db.refresh(clip)
        
        update_data = {
            "processed": True,
            "processing_status": "completed"
        }
        
        response = client.put(f"/api/v1/clips/{clip.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["processed"] is True
        assert data["processing_status"] == "completed"
    
    def test_update_clip_not_found(self, client, test_db):
        """Test updating non-existent clip"""
        update_data = {"title": "Updated"}
        
        response = client.put("/api/v1/clips/999", json=update_data)
        
        assert response.status_code == 404


class TestClipDeleteEndpoint:
    """Test DELETE /api/v1/clips/{id}"""
    
    def test_delete_clip_success(self, client, test_db):
        """Test deleting a clip"""
        clip = Clip(
            title="Delete Me",
            file_path="/clips/delete.mp4"
        )
        test_db.add(clip)
        test_db.commit()
        test_db.refresh(clip)
        
        response = client.delete(f"/api/v1/clips/{clip.id}")
        
        assert response.status_code == 204
        
        # Verify clip was deleted
        deleted = test_db.query(Clip).filter_by(id=clip.id).first()
        assert deleted is None
    
    def test_delete_clip_not_found(self, client, test_db):
        """Test deleting non-existent clip"""
        response = client.delete("/api/v1/clips/999")
        
        assert response.status_code == 404


class TestClipStatsEndpoint:
    """Test GET /api/v1/clips/stats"""
    
    def test_clip_stats_empty(self, client, test_db):
        """Test stats with no clips"""
        response = client.get("/api/v1/clips/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_clips"] == 0
        assert data["processed_clips"] == 0
        assert data["unprocessed_clips"] == 0
    
    def test_clip_stats_with_data(self, client, test_db):
        """Test stats with clips"""
        clip1 = Clip(title="C1", file_path="/c1.mp4", processed=True, game_name="CS2")
        clip2 = Clip(title="C2", file_path="/c2.mp4", processed=False, game_name="CS2")
        clip3 = Clip(title="C3", file_path="/c3.mp4", processed=False, game_name="Valorant")
        
        test_db.add_all([clip1, clip2, clip3])
        test_db.commit()
        
        response = client.get("/api/v1/clips/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_clips"] == 3
        assert data["processed_clips"] == 1
        assert data["unprocessed_clips"] == 2
        assert data["total_games"] == 2
        assert "CS2" in data["games"]
        assert "Valorant" in data["games"]


class TestClipValidation:
    """Test clip data validation"""
    
    def test_create_clip_missing_title(self, client, test_db):
        """Test creating clip without title"""
        clip_data = {
            "file_path": "/clips/no_title.mp4"
        }
        
        response = client.post("/api/v1/clips/", json=clip_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_clip_missing_file_path(self, client, test_db):
        """Test creating clip without file_path"""
        clip_data = {
            "title": "No File Path"
        }
        
        response = client.post("/api/v1/clips/", json=clip_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_clip_invalid_pagination(self, client, test_db):
        """Test list with invalid pagination parameters"""
        response = client.get("/api/v1/clips/?skip=-1")
        
        assert response.status_code == 422  # Validation error
        
        response = client.get("/api/v1/clips/?limit=0")
        
        assert response.status_code == 422  # Validation error
