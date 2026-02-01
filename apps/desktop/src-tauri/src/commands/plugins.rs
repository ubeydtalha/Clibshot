use tauri::State;
use crate::plugins::{PluginManager, PluginInfo};

#[tauri::command]
pub async fn load_plugin(
    plugin_path: String,
    plugin_manager: State<'_, PluginManager>,
) -> Result<String, String> {
    plugin_manager.load(&plugin_path).await
}

#[tauri::command]
pub async fn unload_plugin(
    plugin_id: String,
    plugin_manager: State<'_, PluginManager>,
) -> Result<(), String> {
    plugin_manager.unload(&plugin_id).await
}

#[tauri::command]
pub async fn list_plugins(
    plugin_manager: State<'_, PluginManager>,
) -> Result<Vec<PluginInfo>, String> {
    Ok(plugin_manager.list().await)
}

#[tauri::command]
pub async fn get_plugin_info(
    plugin_id: String,
    plugin_manager: State<'_, PluginManager>,
) -> Result<PluginInfo, String> {
    plugin_manager.get_info(&plugin_id).await
}
