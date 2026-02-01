#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

mod commands;
mod plugins;
mod bridge;
mod state;

use commands::*;
use plugins::PluginManager;
use bridge::PythonBridge;
use state::AppState;

fn main() {
    // Initialize logging
    tracing_subscriber::fmt::init();
    
    tauri::Builder::default()
        .manage(AppState::new())
        .setup(|app| {
            tracing::info!("Initializing ClipShot application");
            
            // Initialize plugin manager
            let plugin_manager = PluginManager::new();
            app.manage(plugin_manager);
            
            // Initialize Python bridge
            match PythonBridge::new() {
                Ok(python_bridge) => {
                    tracing::info!("Python bridge initialized successfully");
                    app.manage(python_bridge);
                }
                Err(e) => {
                    tracing::warn!("Failed to initialize Python bridge: {}", e);
                    // Continue without Python bridge - it's optional
                }
            }
            
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            // Plugin commands
            load_plugin,
            unload_plugin,
            list_plugins,
            get_plugin_info,
            
            // Capture commands
            start_capture,
            stop_capture,
            pause_capture,
            get_capture_sources,
            
            // Clip commands
            list_clips,
            get_clip,
            delete_clip,
            export_clip,
            
            // AI commands
            list_ai_models,
            run_inference,
            generate_metadata,
            
            // System commands
            get_system_info,
            get_metrics,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
