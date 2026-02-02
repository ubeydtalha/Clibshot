use pyo3::prelude::*;
use pyo3::types::PyModule;
use std::sync::Mutex;

pub struct PythonBridge {
    initialized: Mutex<bool>,
}

impl PythonBridge {
    pub fn new() -> PyResult<Self> {
        // Initialize Python interpreter
        pyo3::prepare_freethreaded_python();
        
        Ok(Self {
            initialized: Mutex::new(true),
        })
    }
    
    pub async fn call_fastapi(
        &self,
        endpoint: &str,
        payload: serde_json::Value,
    ) -> PyResult<serde_json::Value> {
        Python::with_gil(|py| {
            // Import requests module
            let requests = PyModule::import(py, "requests")
                .map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        format!("Failed to import requests: {}", e)
                    )
                })?;
            
            let url = format!("http://localhost:8000{}", endpoint);
            let json_str = payload.to_string();
            
            // Make POST request
            let response = requests
                .getattr("post")?
                .call1((url, json_str))?;
            
            // Get response text
            let text: String = response.getattr("text")?.extract()?;
            
            // Parse JSON
            serde_json::from_str(&text)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("Failed to parse JSON: {}", e)
                ))
        })
    }
    
    pub fn is_initialized(&self) -> bool {
        *self.initialized.lock().unwrap()
    }
}

impl Default for PythonBridge {
    fn default() -> Self {
        Self::new().expect("Failed to initialize Python bridge")
    }
}
