use std::sync::Mutex;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppState {
    pub initialized: bool,
}

impl AppState {
    pub fn new() -> Self {
        Self {
            initialized: false,
        }
    }
}

impl Default for AppState {
    fn default() -> Self {
        Self::new()
    }
}

pub type AppStateHandle = Mutex<AppState>;
