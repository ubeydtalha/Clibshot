use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PluginInfo {
    pub id: String,
    pub name: String,
    pub version: String,
    pub enabled: bool,
    pub path: String,
}

pub struct PluginManager {
    plugins: Mutex<HashMap<String, PluginInfo>>,
}

impl PluginManager {
    pub fn new() -> Self {
        Self {
            plugins: Mutex::new(HashMap::new()),
        }
    }

    pub async fn load(&self, plugin_path: &str) -> Result<String, String> {
        let mut plugins = self.plugins.lock().unwrap();
        
        // Placeholder for actual plugin loading logic
        let plugin_id = format!("plugin_{}", plugins.len());
        let plugin_info = PluginInfo {
            id: plugin_id.clone(),
            name: "Example Plugin".to_string(),
            version: "1.0.0".to_string(),
            enabled: true,
            path: plugin_path.to_string(),
        };
        
        plugins.insert(plugin_id.clone(), plugin_info);
        Ok(plugin_id)
    }

    pub async fn unload(&self, plugin_id: &str) -> Result<(), String> {
        let mut plugins = self.plugins.lock().unwrap();
        plugins.remove(plugin_id)
            .ok_or_else(|| format!("Plugin {} not found", plugin_id))?;
        Ok(())
    }

    pub async fn list(&self) -> Vec<PluginInfo> {
        let plugins = self.plugins.lock().unwrap();
        plugins.values().cloned().collect()
    }

    pub async fn get_info(&self, plugin_id: &str) -> Result<PluginInfo, String> {
        let plugins = self.plugins.lock().unwrap();
        plugins.get(plugin_id)
            .cloned()
            .ok_or_else(|| format!("Plugin {} not found", plugin_id))
    }
}

impl Default for PluginManager {
    fn default() -> Self {
        Self::new()
    }
}
