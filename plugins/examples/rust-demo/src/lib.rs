//! Rust Demo Plugin for ClipShot
//! 
//! This plugin demonstrates high-performance native plugin development using Rust and PyO3.

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyString};
use serde::{Deserialize, Serialize};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

/// Plugin metadata information
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct PluginInfo {
    #[pyo3(get)]
    pub id: String,
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub version: String,
}

#[pymethods]
impl PluginInfo {
    #[new]
    fn new(id: String, name: String, version: String) -> Self {
        Self { id, name, version }
    }
}

/// Clip data structure
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct Clip {
    #[pyo3(get)]
    pub id: String,
    #[pyo3(get)]
    pub title: String,
    #[pyo3(get)]
    pub width: u32,
    #[pyo3(get)]
    pub height: u32,
}

#[pymethods]
impl Clip {
    #[new]
    fn new(id: String, title: String, width: u32, height: u32) -> Self {
        Self {
            id,
            title,
            width,
            height,
        }
    }
}

/// Main plugin class
#[pyclass]
pub struct RustDemoPlugin {
    info: PluginInfo,
    config: Option<String>,
    clip_count: Arc<AtomicUsize>,
    use_simd: bool,
}

#[pymethods]
impl RustDemoPlugin {
    /// Create a new instance of the plugin
    #[new]
    fn new() -> Self {
        Self {
            info: PluginInfo {
                id: "com.clipshot.rust-demo".to_string(),
                name: "Rust Demo Plugin".to_string(),
                version: "1.0.0".to_string(),
            },
            config: None,
            clip_count: Arc::new(AtomicUsize::new(0)),
            use_simd: true,
        }
    }

    /// Initialize the plugin
    fn init(&mut self, config: &str) -> PyResult<()> {
        self.config = Some(config.to_string());
        
        // Parse config to check for SIMD setting
        if let Ok(config_data) = serde_json::from_str::<serde_json::Value>(config) {
            if let Some(use_simd) = config_data.get("useSIMD").and_then(|v| v.as_bool()) {
                self.use_simd = use_simd;
            }
        }
        
        println!("🦀 Rust Demo Plugin initialized!");
        println!("   ID: {}", self.info.id);
        println!("   Version: {}", self.info.version);
        println!("   SIMD: {}", if self.use_simd { "enabled" } else { "disabled" });
        
        Ok(())
    }

    /// Shutdown the plugin
    fn shutdown(&self) -> PyResult<()> {
        let count = self.clip_count.load(Ordering::Relaxed);
        println!("👋 Rust Demo Plugin shutting down");
        println!("   Total clips processed: {}", count);
        Ok(())
    }

    /// Handle clip captured event
    fn on_clip_captured(&self, clip: &Clip) -> PyResult<()> {
        self.clip_count.fetch_add(1, Ordering::Relaxed);
        let count = self.clip_count.load(Ordering::Relaxed);
        
        println!("🎬 Clip captured (Rust): {}", clip.title);
        println!("   ID: {}", clip.id);
        println!("   Resolution: {}x{}", clip.width, clip.height);
        println!("   Total processed: {}", count);
        
        Ok(())
    }

    /// Get plugin status (custom API endpoint)
    fn get_status(&self, py: Python) -> PyResult<PyObject> {
        let status = PyDict::new(py);
        status.set_item("status", "healthy")?;
        status.set_item("version", &self.info.version)?;
        status.set_item("clip_count", self.clip_count.load(Ordering::Relaxed))?;
        status.set_item("use_simd", self.use_simd)?;
        status.set_item("language", "rust")?;
        Ok(status.into())
    }

    /// Process image data (demonstrates high-performance operation)
    /// 
    /// This is a simplified example. In a real plugin, this would use SIMD
    /// instructions for parallel processing.
    fn process_image(&self, width: u32, height: u32, data: Vec<u8>) -> PyResult<Vec<u8>> {
        println!("🖼️  Processing image: {}x{} ({} bytes)", width, height, data.len());
        
        let mut output = data.clone();
        
        if self.use_simd {
            // Simulate SIMD processing (in real code, use SIMD intrinsics)
            // For example, applying a simple brightness filter
            for pixel in output.iter_mut() {
                *pixel = pixel.saturating_add(10);
            }
            println!("   ✅ Processed with SIMD optimizations");
        } else {
            // Standard processing
            for pixel in output.iter_mut() {
                *pixel = pixel.saturating_add(10);
            }
            println!("   ✅ Processed without SIMD");
        }
        
        Ok(output)
    }

    /// Get statistics
    fn get_stats(&self, py: Python) -> PyResult<PyObject> {
        let stats = PyDict::new(py);
        stats.set_item("clips_processed", self.clip_count.load(Ordering::Relaxed))?;
        stats.set_item("simd_enabled", self.use_simd)?;
        Ok(stats.into())
    }

    /// Reset counters
    fn reset_counters(&self) -> PyResult<usize> {
        let old_count = self.clip_count.swap(0, Ordering::Relaxed);
        println!("🔄 Counters reset! (was: {})", old_count);
        Ok(old_count)
    }
}

/// Python module definition
#[pymodule]
fn rust_demo_plugin(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<RustDemoPlugin>()?;
    m.add_class::<PluginInfo>()?;
    m.add_class::<Clip>()?;
    Ok(())
}
