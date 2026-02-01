use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct SystemInfo {
    pub os: String,
    pub arch: String,
    pub version: String,
}

#[tauri::command]
pub fn greet(name: &str) -> String {
    format!("Hello, {}! Welcome to ClipShot!", name)
}

#[tauri::command]
pub fn get_system_info() -> SystemInfo {
    SystemInfo {
        os: std::env::consts::OS.to_string(),
        arch: std::env::consts::ARCH.to_string(),
        version: "0.1.0".to_string(),
    }
}

#[tauri::command]
pub async fn call_backend_api(endpoint: String) -> Result<String, String> {
    let url = format!("http://localhost:8000/api/v1/{}", endpoint);
    
    match reqwest::get(&url).await {
        Ok(response) => {
            match response.text().await {
                Ok(text) => Ok(text),
                Err(e) => Err(format!("Failed to read response: {}", e)),
            }
        },
        Err(e) => Err(format!("Failed to call API: {}", e)),
    }
}
