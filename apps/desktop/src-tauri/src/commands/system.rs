use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemInfo {
    pub platform: String,
    pub version: String,
    pub arch: String,
    pub memory_total: u64,
    pub cpu_cores: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Metrics {
    pub memory_used: u64,
    pub cpu_usage: f32,
    pub disk_usage: u64,
    pub active_plugins: u32,
}

#[tauri::command]
pub async fn get_system_info() -> Result<SystemInfo, String> {
    // Get actual system info
    Ok(SystemInfo {
        platform: std::env::consts::OS.to_string(),
        version: "0.1.0".to_string(),
        arch: std::env::consts::ARCH.to_string(),
        memory_total: 16 * 1024 * 1024 * 1024, // 16GB placeholder
        cpu_cores: num_cpus::get() as u32,
    })
}

#[tauri::command]
pub async fn get_metrics() -> Result<Metrics, String> {
    // Placeholder metrics
    Ok(Metrics {
        memory_used: 500 * 1024 * 1024, // 500MB
        cpu_usage: 25.5,
        disk_usage: 10 * 1024 * 1024 * 1024, // 10GB
        active_plugins: 3,
    })
}
