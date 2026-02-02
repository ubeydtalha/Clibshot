use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Clip {
    pub id: String,
    pub title: String,
    pub game: Option<String>,
    pub duration: u64,
    pub file_path: String,
    pub thumbnail: Option<String>,
    pub created_at: String,
}

#[tauri::command]
pub async fn list_clips() -> Result<Vec<Clip>, String> {
    // Placeholder - return mock clips
    Ok(vec![
        Clip {
            id: "clip_1".to_string(),
            title: "Epic Victory".to_string(),
            game: Some("Valorant".to_string()),
            duration: 30,
            file_path: "/clips/clip_1.mp4".to_string(),
            thumbnail: Some("/clips/clip_1_thumb.jpg".to_string()),
            created_at: "2024-01-01T00:00:00Z".to_string(),
        },
    ])
}

#[tauri::command]
pub async fn get_clip(clip_id: String) -> Result<Clip, String> {
    // Placeholder
    Ok(Clip {
        id: clip_id,
        title: "Epic Victory".to_string(),
        game: Some("Valorant".to_string()),
        duration: 30,
        file_path: "/clips/clip_1.mp4".to_string(),
        thumbnail: Some("/clips/clip_1_thumb.jpg".to_string()),
        created_at: "2024-01-01T00:00:00Z".to_string(),
    })
}

#[tauri::command]
pub async fn delete_clip(clip_id: String) -> Result<(), String> {
    tracing::info!("Deleting clip: {}", clip_id);
    Ok(())
}

#[tauri::command]
pub async fn export_clip(clip_id: String, export_path: String) -> Result<(), String> {
    tracing::info!("Exporting clip {} to {}", clip_id, export_path);
    Ok(())
}
