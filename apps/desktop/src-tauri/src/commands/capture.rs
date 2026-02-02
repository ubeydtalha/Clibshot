use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CaptureSource {
    pub id: String,
    pub name: String,
    pub source_type: String,
}

#[tauri::command]
pub async fn start_capture(source_id: String) -> Result<(), String> {
    // Placeholder for capture start logic
    tracing::info!("Starting capture for source: {}", source_id);
    Ok(())
}

#[tauri::command]
pub async fn stop_capture() -> Result<(), String> {
    // Placeholder for capture stop logic
    tracing::info!("Stopping capture");
    Ok(())
}

#[tauri::command]
pub async fn pause_capture() -> Result<(), String> {
    // Placeholder for capture pause logic
    tracing::info!("Pausing capture");
    Ok(())
}

#[tauri::command]
pub async fn get_capture_sources() -> Result<Vec<CaptureSource>, String> {
    // Placeholder - return mock sources
    Ok(vec![
        CaptureSource {
            id: "screen_1".to_string(),
            name: "Primary Display".to_string(),
            source_type: "screen".to_string(),
        },
        CaptureSource {
            id: "window_1".to_string(),
            name: "Game Window".to_string(),
            source_type: "window".to_string(),
        },
    ])
}
