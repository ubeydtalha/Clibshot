"""
Tests for Plugin Manager Core
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from src.plugin_manager import (
    PluginManager, PluginBase, PluginMetadata, PluginStatus,
    get_plugin_manager
)


@pytest.fixture
def temp_plugin_dir():
    """Create a temporary directory for test plugins"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def plugin_manager(temp_plugin_dir):
    """Create a PluginManager instance for testing"""
    return PluginManager(plugin_dirs=[str(temp_plugin_dir)])


@pytest.fixture
def sample_plugin_code():
    """Sample plugin code for testing"""
    return '''
from src.plugin_manager import PluginBase, PluginMetadata

class TestPlugin(PluginBase):
    @property
    def metadata(self):
        return PluginMetadata(
            name="test_plugin",
            display_name="Test Plugin",
            version="1.0.0",
            author="Test Author",
            description="A test plugin",
            plugin_type="python"
        )
    
    def on_clip_captured(self, clip_data):
        clip_data["test_plugin_processed"] = True
        return clip_data
'''


class TestPluginMetadata:
    """Test PluginMetadata dataclass"""
    
    def test_metadata_creation(self):
        """Test creating plugin metadata"""
        metadata = PluginMetadata(
            name="test",
            display_name="Test Plugin",
            version="1.0.0"
        )
        
        assert metadata.name == "test"
        assert metadata.display_name == "Test Plugin"
        assert metadata.version == "1.0.0"
        assert metadata.plugin_type == "python"
        assert metadata.dependencies == []
    
    def test_metadata_with_dependencies(self):
        """Test metadata with dependencies"""
        metadata = PluginMetadata(
            name="test",
            display_name="Test",
            version="1.0.0",
            dependencies=["numpy", "opencv-python"]
        )
        
        assert len(metadata.dependencies) == 2
        assert "numpy" in metadata.dependencies


class TestPluginBase:
    """Test PluginBase class"""
    
    def test_plugin_base_initialization(self):
        """Test PluginBase initialization"""
        
        class SimplePlugin(PluginBase):
            @property
            def metadata(self):
                return PluginMetadata(
                    name="simple",
                    display_name="Simple",
                    version="1.0.0"
                )
        
        plugin = SimplePlugin()
        assert plugin.config == {}
        assert plugin.enabled is True
    
    def test_plugin_base_initialize(self):
        """Test plugin initialization with config"""
        
        class ConfigPlugin(PluginBase):
            @property
            def metadata(self):
                return PluginMetadata(
                    name="config",
                    display_name="Config",
                    version="1.0.0"
                )
        
        plugin = ConfigPlugin()
        plugin.initialize({"key": "value"})
        
        assert plugin.config == {"key": "value"}
    
    def test_plugin_base_not_implemented(self):
        """Test that metadata must be implemented"""
        plugin = PluginBase()
        
        with pytest.raises(NotImplementedError):
            _ = plugin.metadata


class TestPluginManager:
    """Test PluginManager class"""
    
    def test_manager_initialization(self, temp_plugin_dir):
        """Test PluginManager initialization"""
        manager = PluginManager(plugin_dirs=[str(temp_plugin_dir)])
        
        assert len(manager.plugins) == 0
        assert len(manager.plugin_status) == 0
        assert temp_plugin_dir in manager.plugin_dirs
    
    def test_discover_plugins_empty(self, plugin_manager):
        """Test discovering plugins in empty directory"""
        plugins = plugin_manager.discover_plugins()
        assert plugins == []
    
    def test_discover_plugins_with_file(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test discovering a plugin file"""
        # Create a plugin file
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        plugins = plugin_manager.discover_plugins()
        assert "test_plugin" in plugins
    
    def test_discover_plugins_with_package(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test discovering a plugin package"""
        # Create a plugin package
        plugin_package = temp_plugin_dir / "test_package"
        plugin_package.mkdir()
        init_file = plugin_package / "__init__.py"
        init_file.write_text(sample_plugin_code)
        
        plugins = plugin_manager.discover_plugins()
        assert "test_package" in plugins
    
    def test_load_plugin_success(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test successfully loading a plugin"""
        # Create plugin file
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        # Load plugin
        success = plugin_manager.load_plugin("test_plugin")
        
        assert success is True
        assert "test_plugin" in plugin_manager.plugins
        assert plugin_manager.plugin_status["test_plugin"] == PluginStatus.LOADED
    
    def test_load_plugin_not_found(self, plugin_manager):
        """Test loading non-existent plugin"""
        success = plugin_manager.load_plugin("nonexistent")
        
        assert success is False
        assert plugin_manager.plugin_status.get("nonexistent") == PluginStatus.ERROR
        assert "nonexistent" in plugin_manager.plugin_errors
    
    def test_load_plugin_with_config(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test loading plugin with configuration"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        config = {"setting": "value"}
        success = plugin_manager.load_plugin("test_plugin", config)
        
        assert success is True
        plugin = plugin_manager.get_plugin("test_plugin")
        assert plugin.config == config
    
    def test_unload_plugin_success(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test unloading a plugin"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        # Load then unload
        plugin_manager.load_plugin("test_plugin")
        success = plugin_manager.unload_plugin("test_plugin")
        
        assert success is True
        assert "test_plugin" not in plugin_manager.plugins
        assert plugin_manager.plugin_status["test_plugin"] == PluginStatus.UNLOADED
    
    def test_unload_plugin_not_loaded(self, plugin_manager):
        """Test unloading plugin that's not loaded"""
        success = plugin_manager.unload_plugin("notloaded")
        assert success is False
    
    def test_reload_plugin(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test reloading a plugin"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        # Load and reload
        plugin_manager.load_plugin("test_plugin")
        success = plugin_manager.reload_plugin("test_plugin", {"new": "config"})
        
        assert success is True
        plugin = plugin_manager.get_plugin("test_plugin")
        assert plugin.config == {"new": "config"}
    
    def test_get_plugin(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test getting a loaded plugin"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        plugin_manager.load_plugin("test_plugin")
        plugin = plugin_manager.get_plugin("test_plugin")
        
        assert plugin is not None
        assert plugin.metadata.name == "test_plugin"
    
    def test_get_all_plugins(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test getting all loaded plugins"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        plugin_manager.load_plugin("test_plugin")
        plugins = plugin_manager.get_all_plugins()
        
        assert len(plugins) == 1
        assert "test_plugin" in plugins
    
    def test_get_plugin_status(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test getting plugin status"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        plugin_manager.load_plugin("test_plugin")
        status = plugin_manager.get_plugin_status("test_plugin")
        
        assert status == PluginStatus.LOADED
    
    def test_trigger_event(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test triggering events on plugins"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        plugin_manager.load_plugin("test_plugin")
        
        clip_data = {"title": "Test Clip"}
        result = plugin_manager.trigger_event("on_clip_captured", clip_data)
        
        assert result["test_plugin_processed"] is True
        assert result["title"] == "Test Clip"
    
    def test_trigger_event_disabled_plugin(self, plugin_manager, temp_plugin_dir, sample_plugin_code):
        """Test that disabled plugins don't receive events"""
        plugin_file = temp_plugin_dir / "test_plugin.py"
        plugin_file.write_text(sample_plugin_code)
        
        plugin_manager.load_plugin("test_plugin")
        plugin = plugin_manager.get_plugin("test_plugin")
        plugin.enabled = False
        
        clip_data = {"title": "Test Clip"}
        result = plugin_manager.trigger_event("on_clip_captured", clip_data)
        
        assert "test_plugin_processed" not in result


class TestGlobalPluginManager:
    """Test global plugin manager singleton"""
    
    def test_get_plugin_manager_singleton(self):
        """Test that get_plugin_manager returns singleton"""
        manager1 = get_plugin_manager()
        manager2 = get_plugin_manager()
        
        assert manager1 is manager2
    
    def test_get_plugin_manager_creates_instance(self):
        """Test that get_plugin_manager creates instance"""
        manager = get_plugin_manager()
        
        assert manager is not None
        assert isinstance(manager, PluginManager)
