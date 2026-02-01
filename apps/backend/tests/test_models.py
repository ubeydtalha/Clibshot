"""
Tests for Database Models
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.models import Plugin, PluginConfiguration, Clip


@pytest.fixture
def db_engine():
    """Create a test database engine"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    """Create a test database session"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


class TestPluginModel:
    """Test Plugin model"""
    
    def test_create_plugin(self, db_session):
        """Test creating a plugin"""
        plugin = Plugin(
            name="test_plugin",
            display_name="Test Plugin",
            version="1.0.0",
            plugin_type="python",
            entry_point="plugins/test_plugin.py",
            enabled=True
        )
        
        db_session.add(plugin)
        db_session.commit()
        
        assert plugin.id is not None
        assert plugin.name == "test_plugin"
        assert plugin.enabled is True
        assert plugin.created_at is not None
        assert plugin.updated_at is not None
    
    def test_plugin_with_metadata(self, db_session):
        """Test plugin with metadata"""
        plugin = Plugin(
            name="meta_plugin",
            display_name="Meta Plugin",
            version="1.0.0",
            plugin_type="python",
            entry_point="plugins/meta.py",
            plugin_metadata={"config": {"key": "value"}, "dependencies": ["numpy"]}
        )
        
        db_session.add(plugin)
        db_session.commit()
        
        assert plugin.plugin_metadata is not None
        assert plugin.plugin_metadata["config"]["key"] == "value"
        assert "numpy" in plugin.plugin_metadata["dependencies"]
    
    def test_plugin_unique_name(self, db_session):
        """Test that plugin names must be unique"""
        plugin1 = Plugin(
            name="unique",
            display_name="First",
            version="1.0.0",
            plugin_type="python",
            entry_point="plugins/first.py"
        )
        plugin2 = Plugin(
            name="unique",
            display_name="Second",
            version="2.0.0",
            plugin_type="python",
            entry_point="plugins/second.py"
        )
        
        db_session.add(plugin1)
        db_session.commit()
        
        db_session.add(plugin2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_plugin_relationship_with_configurations(self, db_session):
        """Test plugin relationship with configurations"""
        plugin = Plugin(
            name="config_plugin",
            display_name="Config Plugin",
            version="1.0.0",
            plugin_type="python",
            entry_point="plugins/config.py"
        )
        
        db_session.add(plugin)
        db_session.commit()
        
        config1 = PluginConfiguration(
            plugin_id=plugin.id,
            key="setting1",
            value={"enabled": True}
        )
        config2 = PluginConfiguration(
            plugin_id=plugin.id,
            key="setting2",
            value={"threshold": 0.7}
        )
        
        db_session.add_all([config1, config2])
        db_session.commit()
        
        assert len(plugin.configurations) == 2
        assert plugin.configurations[0].key in ["setting1", "setting2"]
    
    def test_plugin_cascade_delete_configurations(self, db_session):
        """Test that deleting plugin deletes its configurations"""
        plugin = Plugin(
            name="cascade_plugin",
            display_name="Cascade Plugin",
            version="1.0.0",
            plugin_type="python",
            entry_point="plugins/cascade.py"
        )
        
        db_session.add(plugin)
        db_session.commit()
        
        config = PluginConfiguration(
            plugin_id=plugin.id,
            key="test_key",
            value={"test": "value"}
        )
        
        db_session.add(config)
        db_session.commit()
        
        config_id = config.id
        
        # Delete plugin
        db_session.delete(plugin)
        db_session.commit()
        
        # Check config was deleted
        deleted_config = db_session.query(PluginConfiguration).filter_by(id=config_id).first()
        assert deleted_config is None


class TestPluginConfigurationModel:
    """Test PluginConfiguration model"""
    
    def test_create_configuration(self, db_session):
        """Test creating a plugin configuration"""
        plugin = Plugin(
            name="test",
            display_name="Test",
            version="1.0.0",
            plugin_type="python",
            entry_point="test.py"
        )
        db_session.add(plugin)
        db_session.commit()
        
        config = PluginConfiguration(
            plugin_id=plugin.id,
            key="test_setting",
            value={"enabled": True, "threshold": 0.5}
        )
        
        db_session.add(config)
        db_session.commit()
        
        assert config.id is not None
        assert config.key == "test_setting"
        assert config.value["enabled"] is True
        assert config.created_at is not None
    
    def test_configuration_json_value(self, db_session):
        """Test JSON value storage"""
        plugin = Plugin(
            name="json_test",
            display_name="JSON Test",
            version="1.0.0",
            plugin_type="python",
            entry_point="json.py"
        )
        db_session.add(plugin)
        db_session.commit()
        
        complex_value = {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "bool": True,
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }
        
        config = PluginConfiguration(
            plugin_id=plugin.id,
            key="complex",
            value=complex_value
        )
        
        db_session.add(config)
        db_session.commit()
        
        # Retrieve and verify
        retrieved = db_session.query(PluginConfiguration).filter_by(id=config.id).first()
        assert retrieved.value == complex_value


class TestClipModel:
    """Test Clip model"""
    
    def test_create_clip(self, db_session):
        """Test creating a clip"""
        clip = Clip(
            title="Epic Victory",
            file_path="/clips/epic_victory.mp4",
            game_name="Counter-Strike 2",
            duration=45,
            resolution="1920x1080",
            fps=60
        )
        
        db_session.add(clip)
        db_session.commit()
        
        assert clip.id is not None
        assert clip.title == "Epic Victory"
        assert clip.processed is False
        assert clip.created_at is not None
    
    def test_clip_with_metadata(self, db_session):
        """Test clip with metadata"""
        clip = Clip(
            title="Test Clip",
            file_path="/clips/test.mp4",
            clip_metadata={
                "highlights": [
                    {"timestamp": 10.5, "duration": 5.2, "score": 0.85}
                ],
                "analyzed_by": "highlight_detector"
            }
        )
        
        db_session.add(clip)
        db_session.commit()
        
        assert clip.clip_metadata is not None
        assert len(clip.clip_metadata["highlights"]) == 1
        assert clip.clip_metadata["analyzed_by"] == "highlight_detector"
    
    def test_clip_with_tags(self, db_session):
        """Test clip with tags"""
        clip = Clip(
            title="Tagged Clip",
            file_path="/clips/tagged.mp4",
            tags=["epic", "clutch", "victory"]
        )
        
        db_session.add(clip)
        db_session.commit()
        
        assert len(clip.tags) == 3
        assert "clutch" in clip.tags
    
    def test_clip_processing_status(self, db_session):
        """Test clip processing status"""
        clip = Clip(
            title="Processing Test",
            file_path="/clips/processing.mp4",
            processed=False,
            processing_status="pending"
        )
        
        db_session.add(clip)
        db_session.commit()
        
        # Update processing status
        clip.processed = True
        clip.processing_status = "completed"
        db_session.commit()
        
        assert clip.processed is True
        assert clip.processing_status == "completed"
    
    def test_clip_recorded_at(self, db_session):
        """Test clip recorded timestamp"""
        recorded_time = datetime(2026, 1, 15, 14, 30, 0)
        
        clip = Clip(
            title="Timestamped Clip",
            file_path="/clips/timestamped.mp4",
            recorded_at=recorded_time
        )
        
        db_session.add(clip)
        db_session.commit()
        
        assert clip.recorded_at == recorded_time
    
    def test_query_clips_by_game(self, db_session):
        """Test querying clips by game"""
        clip1 = Clip(title="CS2 Clip 1", file_path="/clips/cs2_1.mp4", game_name="Counter-Strike 2")
        clip2 = Clip(title="CS2 Clip 2", file_path="/clips/cs2_2.mp4", game_name="Counter-Strike 2")
        clip3 = Clip(title="Valorant Clip", file_path="/clips/val.mp4", game_name="Valorant")
        
        db_session.add_all([clip1, clip2, clip3])
        db_session.commit()
        
        cs2_clips = db_session.query(Clip).filter_by(game_name="Counter-Strike 2").all()
        
        assert len(cs2_clips) == 2
    
    def test_query_clips_by_processed_status(self, db_session):
        """Test querying clips by processed status"""
        clip1 = Clip(title="Processed", file_path="/clips/p1.mp4", processed=True)
        clip2 = Clip(title="Unprocessed", file_path="/clips/u1.mp4", processed=False)
        clip3 = Clip(title="Also Unprocessed", file_path="/clips/u2.mp4", processed=False)
        
        db_session.add_all([clip1, clip2, clip3])
        db_session.commit()
        
        unprocessed = db_session.query(Clip).filter_by(processed=False).all()
        
        assert len(unprocessed) == 2


class TestModelTimestamps:
    """Test timestamp functionality on models"""
    
    def test_plugin_timestamps(self, db_session):
        """Test plugin created_at and updated_at"""
        plugin = Plugin(
            name="timestamp_test",
            display_name="Timestamp Test",
            version="1.0.0",
            plugin_type="python",
            entry_point="test.py"
        )
        
        db_session.add(plugin)
        db_session.commit()
        
        created_at = plugin.created_at
        updated_at = plugin.updated_at
        
        assert created_at is not None
        assert updated_at is not None
        
        # Update plugin
        plugin.display_name = "Updated Name"
        db_session.commit()
        
        assert plugin.created_at == created_at  # created_at shouldn't change
        assert plugin.updated_at >= updated_at  # updated_at should be newer or same
    
    def test_clip_timestamps(self, db_session):
        """Test clip created_at and updated_at"""
        clip = Clip(
            title="Timestamp Test",
            file_path="/clips/test.mp4"
        )
        
        db_session.add(clip)
        db_session.commit()
        
        created_at = clip.created_at
        
        # Update clip
        clip.processed = True
        db_session.commit()
        
        assert clip.created_at == created_at
        assert clip.updated_at >= created_at
