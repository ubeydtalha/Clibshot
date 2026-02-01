# 🖥️ FRONTEND ARCHITECTURE — CLIPSHOT

> Tauri + Vite + React tabanlı, plugin-driven, modern desktop UI mimarisi.

---

## 🎯 TASARIM PRENSİPLERİ

1. **Plugin-Driven UI** — Tüm UI parçaları plugin'lerden gelir
2. **Security First** — Tauri security model, Rust backend
3. **Performance** — Vite HMR, lazy loading, memoization
4. **Modular** — Pluginlenebilir ve genişletilebilir frontend
5. **Accessibility** — WCAG 2.1 AA uyumlu
6. **Localization** — ICU format, RTL desteği

---

## 📁 DOSYA YAPISI

```
apps/desktop/
├── src-tauri/                   # Tauri Rust Backend
│   ├── src/
│   │   ├── main.rs
│   │   ├── commands/            # Tauri commands (IPC)
│   │   ├── plugins/             # Plugin manager
│   │   ├── bridge/              # Python bridge
│   │   ├── utils/
│   │   └── state/
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   └── build.rs
│
├── src/                         # Vite + React Frontend
│   ├── app/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── stores/
│   ├── lib/                     # Tauri API wrappers
│   ├── i18n/
│   ├── styles/
│   ├── utils/
│   └── main.tsx
│
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

---

## 🦀 TAURI BACKEND (RUST)

### Main Entry Point

```rust
// src-tauri/src/main.rs

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Manager, Window};

mod commands;
mod plugins;
mod bridge;
mod utils;
mod state;

use commands::*;
use state::AppState;

fn main() {
    tauri::Builder::default()
        .manage(AppState::new())
        .setup(|app| {
            // Initialize plugin manager
            let plugin_manager = plugins::PluginManager::new();
            app.manage(plugin_manager);
            
            // Initialize Python bridge
            let python_bridge = bridge::PythonBridge::new()?;
            app.manage(python_bridge);
            
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
```

### Tauri Commands

```rust
// src-tauri/src/commands/plugins.rs

use tauri::State;
use crate::plugins::PluginManager;

#[tauri::command]
pub async fn load_plugin(
    plugin_path: String,
    plugin_manager: State<'_, PluginManager>,
) -> Result<String, String> {
    plugin_manager
        .load(&plugin_path)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn list_plugins(
    plugin_manager: State<'_, PluginManager>,
) -> Result<Vec<PluginInfo>, String> {
    Ok(plugin_manager.list().await)
}

#[tauri::command]
pub async fn unload_plugin(
    plugin_id: String,
    plugin_manager: State<'_, PluginManager>,
) -> Result<(), String> {
    plugin_manager
        .unload(&plugin_id)
        .await
        .map_err(|e| e.to_string())
}
```

### Python Bridge (PyO3)

```rust
// src-tauri/src/bridge/python.rs

use pyo3::prelude::*;
use pyo3::types::PyModule;
use std::sync::Mutex;

pub struct PythonBridge {
    runtime: Mutex<Option<Python<'static>>>,
}

impl PythonBridge {
    pub fn new() -> PyResult<Self> {
        pyo3::prepare_freethreaded_python();
        Ok(Self {
            runtime: Mutex::new(None),
        })
    }
    
    pub async fn call_fastapi(
        &self,
        endpoint: &str,
        payload: serde_json::Value,
    ) -> PyResult<serde_json::Value> {
        Python::with_gil(|py| {
            let requests = PyModule::import(py, "requests")?;
            let response = requests
                .getattr("post")?
                .call1((
                    format!("http://localhost:8000{}", endpoint),
                    payload.to_string(),
                ))?;
            
            let json_str: String = response.getattr("text")?.extract()?;
            Ok(serde_json::from_str(&json_str).unwrap())
        })
    }
}
```

---

## ⚡ VITE CONFIGURATION

```typescript
// vite.config.ts

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [
    react({
      // React Refresh
      fastRefresh: true,
      // Babel plugins
      babel: {
        plugins: ['babel-plugin-macros']
      }
    })
  ],
  
  // Tauri expects files in `src-tauri/target`
  clearScreen: false,
  
  server: {
    port: 5173,
    strictPort: true,
    // Tauri compatibility
    watch: {
      ignored: ['**/src-tauri/**']
    }
  },
  
  // Environment variables
  envPrefix: ['VITE_', 'TAURI_'],
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/components': path.resolve(__dirname, './src/components'),
      '@/pages': path.resolve(__dirname, './src/pages'),
      '@/hooks': path.resolve(__dirname, './src/hooks'),
      '@/lib': path.resolve(__dirname, './src/lib'),
      '@/stores': path.resolve(__dirname, './src/stores'),
      '@/utils': path.resolve(__dirname, './src/utils'),
    }
  },
  
  build: {
    // Tauri uses Chromium on Windows
    target: process.env.TAURI_PLATFORM === 'windows' 
      ? 'chrome105' 
      : 'safari13',
    minify: !process.env.TAURI_DEBUG ? 'esbuild' : false,
    sourcemap: !!process.env.TAURI_DEBUG,
  },
})
```

---

## 🔌 TAURI API WRAPPERS

### Command Wrappers

```typescript
// src/lib/tauri.ts

import { invoke } from '@tauri-apps/api/tauri'
import { listen, emit } from '@tauri-apps/api/event'

export interface PluginInfo {
  id: string
  name: string
  version: string
  enabled: boolean
}

// Plugin commands
export const tauriAPI = {
  plugins: {
    load: (path: string) => 
      invoke<string>('load_plugin', { pluginPath: path }),
    
    unload: (id: string) => 
      invoke<void>('unload_plugin', { pluginId: id }),
    
    list: () => 
      invoke<PluginInfo[]>('list_plugins'),
    
    getInfo: (id: string) => 
      invoke<PluginInfo>('get_plugin_info', { pluginId: id }),
  },
  
  capture: {
    start: (sourceId: string) => 
      invoke<void>('start_capture', { sourceId }),
    
    stop: () => 
      invoke<void>('stop_capture'),
    
    getSources: () => 
      invoke<CaptureSource[]>('get_capture_sources'),
  },
  
  clips: {
    list: () => 
      invoke<Clip[]>('list_clips'),
    
    get: (id: string) => 
      invoke<Clip>('get_clip', { clipId: id }),
    
    delete: (id: string) => 
      invoke<void>('delete_clip', { clipId: id }),
    
    export: (id: string, path: string) => 
      invoke<void>('export_clip', { clipId: id, exportPath: path }),
  },
  
  ai: {
    listModels: () => 
      invoke<AIModel[]>('list_ai_models'),
    
    runInference: (modelId: string, input: any) => 
      invoke<InferenceResult>('run_inference', { modelId, input }),
    
    generateMetadata: (clipId: string) => 
      invoke<Metadata>('generate_metadata', { clipId }),
  },
  
  system: {
    getInfo: () => 
      invoke<SystemInfo>('get_system_info'),
    
    getMetrics: () => 
      invoke<Metrics>('get_metrics'),
  },
}

// Event listeners
export const tauriEvents = {
  onClipCaptured: (callback: (clip: Clip) => void) =>
    listen<Clip>('clip-captured', (event) => callback(event.payload)),
  
  onPluginLoaded: (callback: (plugin: PluginInfo) => void) =>
    listen<PluginInfo>('plugin-loaded', (event) => callback(event.payload)),
  
  onAIProgress: (callback: (progress: number) => void) =>
    listen<number>('ai-progress', (event) => callback(event.payload)),
}
```

---

## 🔒 TAURI SECURITY

### tauri.conf.json

```json
{
  "build": {
    "distDir": "../dist",
    "devPath": "http://localhost:5173",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "package": {
    "productName": "ClipShot",
    "version": "0.1.0"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "shell": {
        "all": false,
        "open": true
      },
      "path": {
        "all": true
      },
      "fs": {
        "all": false,
        "readFile": true,
        "writeFile": true,
        "readDir": true,
        "copyFile": true,
        "createDir": true,
        "removeDir": true,
        "removeFile": true,
        "renameFile": true,
        "exists": true,
        "scope": ["$APPDATA", "$APPDATA/**"]
      },
      "dialog": {
        "all": false,
        "open": true,
        "save": true
      },
      "http": {
        "all": false,
        "request": true,
        "scope": ["http://localhost:8000/**"]
      }
    },
    "bundle": {
      "active": true,
      "identifier": "io.clipshot.app",
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ],
      "targets": "all"
    },
    "security": {
      "csp": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:"
    },
    "windows": [
      {
        "title": "ClipShot",
        "width": 1400,
        "height": 900,
        "minWidth": 1024,
        "minHeight": 768,
        "resizable": true,
        "fullscreen": false,
        "decorations": false,
        "transparent": true
      }
    ]
  }
}
```

---

## ⚛️ REACT COMPONENTS

### Main App

```tsx
// src/main.tsx

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './app/App'
import './styles/globals.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

```tsx
// src/app/App.tsx

import { RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { router } from './Router'
import { ThemeProvider } from '@/components/providers/ThemeProvider'
import { I18nProvider } from '@/components/providers/I18nProvider'
import { Toaster } from '@/components/ui/Toast'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <I18nProvider>
          <RouterProvider router={router} />
          <Toaster />
        </I18nProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}
```

### Using Tauri API

```tsx
// src/pages/Plugins.tsx

import { useQuery, useMutation } from '@tanstack/react-query'
import { tauriAPI } from '@/lib/tauri'
import { PluginCard } from '@/components/plugins/PluginCard'

export function PluginsPage() {
  // Fetch plugins
  const { data: plugins, isLoading } = useQuery({
    queryKey: ['plugins'],
    queryFn: () => tauriAPI.plugins.list(),
  })
  
  // Load plugin mutation
  const loadPlugin = useMutation({
    mutationFn: (path: string) => tauriAPI.plugins.load(path),
    onSuccess: () => {
      queryClient.invalidateQueries(['plugins'])
    }
  })
  
  if (isLoading) return <div>Loading...</div>
  
  return (
    <div className="grid grid-cols-3 gap-4">
      {plugins?.map(plugin => (
        <PluginCard 
          key={plugin.id} 
          plugin={plugin}
          onUnload={() => tauriAPI.plugins.unload(plugin.id)}
        />
      ))}
    </div>
  )
}
```

---

## 🎨 PLUGIN UI INTEGRATION

### Plugin Host Component

```tsx
// src/components/plugins/PluginHost.tsx

import { useEffect, useRef } from 'react'
import { tauriEvents } from '@/lib/tauri'

interface PluginHostProps {
  pluginId: string
}

export function PluginHost({ pluginId }: PluginHostProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    // Plugin UI will be injected here
    const unlisten = tauriEvents.onPluginLoaded((plugin) => {
      if (plugin.id === pluginId && containerRef.current) {
        // Load plugin UI bundle
        loadPluginUI(plugin, containerRef.current)
      }
    })
    
    return () => {
      unlisten.then(fn => fn())
    }
  }, [pluginId])
  
  return (
    <div 
      ref={containerRef}
      className="plugin-container"
      data-plugin-id={pluginId}
    />
  )
}

async function loadPluginUI(plugin: PluginInfo, container: HTMLElement) {
  // Dynamic import plugin UI module
  const module = await import(`/plugins/${plugin.id}/ui/index.js`)
  module.render(container)
}
```

---

## 📦 MODULAR & PLUGINLENEBILIR FRONTEND

### Plugin Manifest UI Extension

```json
{
  "ui": {
    "entry": "ui/index.tsx",
    "routes": [
      {
        "path": "/plugin/my-plugin",
        "component": "PluginPage"
      }
    ],
    "widgets": [
      {
        "id": "my-widget",
        "component": "MyWidget",
        "placement": "sidebar"
      }
    ],
    "menu": [
      {
        "label": "My Plugin",
        "action": "open_plugin"
      }
    ]
  }
}
```

### Dynamic Route Registration

```tsx
// src/lib/plugin-router.ts

import { RouteObject } from 'react-router-dom'

class PluginRouter {
  private routes: RouteObject[] = []
  
  registerRoute(pluginId: string, route: RouteObject) {
    this.routes.push({
      ...route,
      path: `/plugins/${pluginId}${route.path}`,
    })
  }
  
  getRoutes(): RouteObject[] {
    return this.routes
  }
}

export const pluginRouter = new PluginRouter()
```

---

## 🔄 STATE MANAGEMENT

### Zustand Store

```typescript
// src/stores/pluginStore.ts

import { create } from 'zustand'
import { tauriAPI } from '@/lib/tauri'

interface PluginStore {
  plugins: PluginInfo[]
  loading: boolean
  loadPlugins: () => Promise<void>
  loadPlugin: (path: string) => Promise<void>
  unloadPlugin: (id: string) => Promise<void>
}

export const usePluginStore = create<PluginStore>((set, get) => ({
  plugins: [],
  loading: false,
  
  loadPlugins: async () => {
    set({ loading: true })
    try {
      const plugins = await tauriAPI.plugins.list()
      set({ plugins, loading: false })
    } catch (error) {
      set({ loading: false })
      throw error
    }
  },
  
  loadPlugin: async (path: string) => {
    await tauriAPI.plugins.load(path)
    await get().loadPlugins()
  },
  
  unloadPlugin: async (id: string) => {
    await tauriAPI.plugins.unload(id)
    await get().loadPlugins()
  },
}))
```

---

## ⚡ PERFORMANCE OPTIMIZATIONS

### Code Splitting

```tsx
// Lazy loading routes
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('@/pages/Dashboard'))
const Capture = lazy(() => import('@/pages/Capture'))
const Clips = lazy(() => import('@/pages/Clips'))
const Plugins = lazy(() => import('@/pages/Plugins'))

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: (
          <Suspense fallback={<LoadingSpinner />}>
            <Dashboard />
          </Suspense>
        )
      },
      // ...
    ]
  }
])
```

### Memoization

```tsx
import { memo, useMemo } from 'react'

export const ClipCard = memo(({ clip }: { clip: Clip }) => {
  const thumbnail = useMemo(() => 
    generateThumbnail(clip), 
    [clip.id]
  )
  
  return (
    <div className="clip-card">
      <img src={thumbnail} alt={clip.title} />
      {/* ... */}
    </div>
  )
})
```

---

## 🌐 LOCALIZATION

### i18n Setup

```typescript
// src/i18n/index.ts

import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

import en from './locales/en.json'
import tr from './locales/tr.json'

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      tr: { translation: tr },
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  })

export default i18n
```

---

## 🎯 TAURI VS ELECTRON KARŞILAŞTIRMA

| Özellik | Tauri | Electron |
|---------|-------|----------|
| **Bundle Size** | ~3-5MB | ~150MB |
| **Memory Usage** | ~50MB | ~150-300MB |
| **Startup Time** | <1s | ~2-3s |
| **Backend** | Rust | Node.js |
| **Webview** | Native | Chromium |
| **Security** | Rust + allowlist | Node access control |
| **HMR** | Vite (<100ms) | Webpack (~1s) |
| **Build Tool** | Vite | Webpack/Vite |
| **Plugin System** | Native Rust | JavaScript |

**ClipShot'un Tauri'yi seçme nedenleri:**
- ✅ 30-40x daha küçük bundle
- ✅ Daha az memory kullanımı
- ✅ Rust native plugin sistemi ile doğal entegrasyon
- ✅ Modern build tooling (Vite)
- ✅ Daha güvenli (Rust + allowlist model)
    if (!url.startsWith('http://localhost') && !url.startsWith('file://')) {
      event.preventDefault();
    }
  });

  // Block new window creation
  mainWindow.webContents.setWindowOpenHandler(() => {
    return { action: 'deny' };
  });

  return mainWindow;
}
```

### Preload Script

```typescript
// src/preload/index.ts

import { contextBridge, ipcRenderer } from 'electron';
import type { ClipShotAPI } from './types';

/**
 * Exposed API to renderer process.
 * This is the ONLY way renderer can communicate with main process.
 */
const clipShotAPI: ClipShotAPI = {
  // System
  getVersion: () => ipcRenderer.invoke('system:version'),
  getPlatform: () => ipcRenderer.invoke('system:platform'),
  
  // Window controls
  window: {
    minimize: () => ipcRenderer.send('window:minimize'),
    maximize: () => ipcRenderer.send('window:maximize'),
    close: () => ipcRenderer.send('window:close'),
    isMaximized: () => ipcRenderer.invoke('window:is-maximized'),
  },
  
  // Backend API
  api: {
    get: (endpoint: string) => ipcRenderer.invoke('api:get', endpoint),
    post: (endpoint: string, data?: unknown) => ipcRenderer.invoke('api:post', endpoint, data),
    put: (endpoint: string, data?: unknown) => ipcRenderer.invoke('api:put', endpoint, data),
    delete: (endpoint: string) => ipcRenderer.invoke('api:delete', endpoint),
  },
  
  // Plugins
  plugins: {
    list: () => ipcRenderer.invoke('plugins:list'),
    get: (id: string) => ipcRenderer.invoke('plugins:get', id),
    install: (source: string) => ipcRenderer.invoke('plugins:install', source),
    uninstall: (id: string) => ipcRenderer.invoke('plugins:uninstall', id),
    enable: (id: string) => ipcRenderer.invoke('plugins:enable', id),
    disable: (id: string) => ipcRenderer.invoke('plugins:disable', id),
    getConfig: (id: string) => ipcRenderer.invoke('plugins:get-config', id),
    setConfig: (id: string, config: Record<string, unknown>) => 
      ipcRenderer.invoke('plugins:set-config', id, config),
  },
  
  // Capture
  capture: {
    start: (options?: CaptureOptions) => ipcRenderer.invoke('capture:start', options),
    stop: () => ipcRenderer.invoke('capture:stop'),
    saveReplay: (duration: number) => ipcRenderer.invoke('capture:save-replay', duration),
    getSources: () => ipcRenderer.invoke('capture:sources'),
    getStatus: () => ipcRenderer.invoke('capture:status'),
  },
  
  // AI
  ai: {
    listModels: () => ipcRenderer.invoke('ai:list-models'),
    loadModel: (id: string) => ipcRenderer.invoke('ai:load-model', id),
    infer: (request: InferenceRequest) => ipcRenderer.invoke('ai:infer', request),
  },
  
  // Config
  config: {
    get: (key?: string) => ipcRenderer.invoke('config:get', key),
    set: (key: string, value: unknown) => ipcRenderer.invoke('config:set', key, value),
  },
  
  // Events
  on: (channel: string, callback: (...args: unknown[]) => void) => {
    const subscription = (_event: Electron.IpcRendererEvent, ...args: unknown[]) => {
      callback(...args);
    };
    ipcRenderer.on(channel, subscription);
    return () => ipcRenderer.removeListener(channel, subscription);
  },
  
  // Localization
  i18n: {
    getLocale: () => ipcRenderer.invoke('i18n:locale'),
    setLocale: (locale: string) => ipcRenderer.invoke('i18n:set-locale', locale),
    getTranslations: (namespace: string) => ipcRenderer.invoke('i18n:translations', namespace),
  },
};

// Expose to renderer
contextBridge.exposeInMainWorld('clipshot', clipShotAPI);
```

### Type Definitions

```typescript
// src/preload/types.ts

export interface ClipShotAPI {
  getVersion(): Promise<string>;
  getPlatform(): Promise<NodeJS.Platform>;
  
  window: WindowAPI;
  api: BackendAPI;
  plugins: PluginsAPI;
  capture: CaptureAPI;
  ai: AIAPI;
  config: ConfigAPI;
  i18n: I18nAPI;
  
  on(channel: string, callback: (...args: unknown[]) => void): () => void;
}

export interface WindowAPI {
  minimize(): void;
  maximize(): void;
  close(): void;
  isMaximized(): Promise<boolean>;
}

export interface BackendAPI {
  get<T = unknown>(endpoint: string): Promise<T>;
  post<T = unknown>(endpoint: string, data?: unknown): Promise<T>;
  put<T = unknown>(endpoint: string, data?: unknown): Promise<T>;
  delete<T = unknown>(endpoint: string): Promise<T>;
}

export interface PluginsAPI {
  list(): Promise<Plugin[]>;
  get(id: string): Promise<Plugin>;
  install(source: string): Promise<Plugin>;
  uninstall(id: string): Promise<void>;
  enable(id: string): Promise<Plugin>;
  disable(id: string): Promise<Plugin>;
  getConfig(id: string): Promise<Record<string, unknown>>;
  setConfig(id: string, config: Record<string, unknown>): Promise<void>;
}

// Global declaration
declare global {
  interface Window {
    clipshot: ClipShotAPI;
  }
}
```

---

## ⚛️ REACT ARCHITECTURE

### App Entry

```tsx
// src/renderer/app/App.tsx

import React, { Suspense } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider } from 'react-router-dom';

import { ThemeProvider } from '@/components/providers/ThemeProvider';
import { I18nProvider } from '@/components/providers/I18nProvider';
import { PluginProvider } from '@/components/providers/PluginProvider';
import { ToastProvider } from '@/components/providers/ToastProvider';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { LoadingScreen } from '@/components/LoadingScreen';
import { router } from './Router';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 2,
    },
  },
});

export const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <I18nProvider>
            <PluginProvider>
              <ToastProvider>
                <Suspense fallback={<LoadingScreen />}>
                  <RouterProvider router={router} />
                </Suspense>
              </ToastProvider>
            </PluginProvider>
          </I18nProvider>
        </ThemeProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
};
```

### Router

```tsx
// src/renderer/app/Router.tsx

import { createHashRouter } from 'react-router-dom';
import { lazy } from 'react';

import { MainLayout } from '@/components/layout/MainLayout';

// Lazy load pages
const Dashboard = lazy(() => import('@/pages/Dashboard'));
const Capture = lazy(() => import('@/pages/Capture'));
const Clips = lazy(() => import('@/pages/Clips'));
const Editor = lazy(() => import('@/pages/Editor'));
const AIModels = lazy(() => import('@/pages/AIModels'));
const Plugins = lazy(() => import('@/pages/Plugins'));
const Marketplace = lazy(() => import('@/pages/Marketplace'));
const Settings = lazy(() => import('@/pages/Settings'));
const DevPanel = lazy(() => import('@/pages/DevPanel'));

export const router = createHashRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'capture', element: <Capture /> },
      { path: 'clips', element: <Clips /> },
      { path: 'clips/:id/edit', element: <Editor /> },
      { path: 'ai', element: <AIModels /> },
      { path: 'plugins', element: <Plugins /> },
      { path: 'marketplace', element: <Marketplace /> },
      { path: 'settings', element: <Settings /> },
      { path: 'dev', element: <DevPanel /> },
    ],
  },
]);
```

---

## 🧩 PLUGIN UI SYSTEM

### Plugin Host Component

```tsx
// src/renderer/components/plugins/PluginHost.tsx

import React, { useEffect, useState, useRef } from 'react';
import { usePlugin } from '@/hooks/usePlugins';

interface PluginHostProps {
  pluginId: string;
  slot: UISlot;
  props?: Record<string, unknown>;
}

type UISlot = 
  | 'toolbar'
  | 'sidebar'
  | 'settings-tab'
  | 'clip-editor'
  | 'overlay'
  | 'context-menu'
  | 'status-bar'
  | 'dashboard-widget';

export const PluginHost: React.FC<PluginHostProps> = ({ 
  pluginId, 
  slot,
  props = {} 
}) => {
  const { plugin, isLoading, error } = usePlugin(pluginId);
  const containerRef = useRef<HTMLDivElement>(null);
  const [Component, setComponent] = useState<React.ComponentType | null>(null);

  useEffect(() => {
    if (!plugin?.ui?.[slot]) return;

    // Dynamically load plugin component
    const loadComponent = async () => {
      try {
        const module = await plugin.loadUIComponent(slot);
        setComponent(() => module.default || module);
      } catch (err) {
        console.error(`Failed to load plugin UI: ${pluginId}/${slot}`, err);
      }
    };

    loadComponent();
  }, [plugin, pluginId, slot]);

  if (isLoading) {
    return <PluginLoadingSkeleton />;
  }

  if (error || !Component) {
    return null;
  }

  return (
    <div 
      ref={containerRef}
      className="plugin-host"
      data-plugin-id={pluginId}
      data-slot={slot}
    >
      <PluginErrorBoundary pluginId={pluginId}>
        <Component {...props} pluginId={pluginId} />
      </PluginErrorBoundary>
    </div>
  );
};

// Render all plugins for a specific slot
export const PluginSlot: React.FC<{ slot: UISlot }> = ({ slot }) => {
  const { plugins } = usePlugins({ hasUI: true, slot });
  
  // Sort by priority
  const sortedPlugins = [...plugins].sort(
    (a, b) => (a.ui?.[slot]?.priority ?? 0) - (b.ui?.[slot]?.priority ?? 0)
  );

  return (
    <>
      {sortedPlugins.map((plugin) => (
        <PluginHost
          key={`${plugin.id}-${slot}`}
          pluginId={plugin.id}
          slot={slot}
        />
      ))}
    </>
  );
};
```

### Plugin Error Boundary

```tsx
// src/renderer/components/plugins/PluginErrorBoundary.tsx

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
  pluginId: string;
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class PluginErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error(`Plugin error [${this.props.pluginId}]:`, error, errorInfo);
    
    // Report to plugin system
    window.clipshot.plugins.reportError?.(this.props.pluginId, {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
    });
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="plugin-error">
          <AlertTriangle className="w-4 h-4 text-yellow-500" />
          <span>Plugin error: {this.props.pluginId}</span>
        </div>
      );
    }

    return this.props.children;
  }
}
```

---

## 🎨 DEV PANEL

### DevPanel Page

```tsx
// src/renderer/pages/DevPanel.tsx

import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { useTranslation } from '@/hooks/useTranslation';

import { APIExplorer } from '@/components/dev/APIExplorer';
import { EventInspector } from '@/components/dev/EventInspector';
import { PluginManager } from '@/components/dev/PluginManager';
import { PermissionManager } from '@/components/dev/PermissionManager';
import { PerformanceMonitor } from '@/components/dev/PerformanceMonitor';
import { AIDebugger } from '@/components/dev/AIDebugger';

const DevPanel: React.FC = () => {
  const { t } = useTranslation('dev');
  const [activeTab, setActiveTab] = useState('api');

  return (
    <div className="dev-panel h-full flex flex-col">
      <header className="dev-panel-header px-6 py-4 border-b">
        <h1 className="text-2xl font-bold">{t('title')}</h1>
        <p className="text-muted-foreground">{t('description')}</p>
      </header>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1">
        <TabsList className="px-6 py-2 border-b">
          <TabsTrigger value="api">
            {t('tabs.api')}
          </TabsTrigger>
          <TabsTrigger value="events">
            {t('tabs.events')}
          </TabsTrigger>
          <TabsTrigger value="plugins">
            {t('tabs.plugins')}
          </TabsTrigger>
          <TabsTrigger value="permissions">
            {t('tabs.permissions')}
          </TabsTrigger>
          <TabsTrigger value="performance">
            {t('tabs.performance')}
          </TabsTrigger>
          <TabsTrigger value="ai">
            {t('tabs.ai')}
          </TabsTrigger>
        </TabsList>

        <div className="flex-1 overflow-auto p-6">
          <TabsContent value="api">
            <APIExplorer />
          </TabsContent>
          
          <TabsContent value="events">
            <EventInspector />
          </TabsContent>
          
          <TabsContent value="plugins">
            <PluginManager />
          </TabsContent>
          
          <TabsContent value="permissions">
            <PermissionManager />
          </TabsContent>
          
          <TabsContent value="performance">
            <PerformanceMonitor />
          </TabsContent>
          
          <TabsContent value="ai">
            <AIDebugger />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
};

export default DevPanel;
```

### API Explorer Component

```tsx
// src/renderer/components/dev/APIExplorer.tsx

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Play, Copy, ChevronDown, ChevronRight } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';

interface Endpoint {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  summary: string;
  description: string;
  parameters: Parameter[];
  requestBody?: RequestBody;
  responses: Record<string, Response>;
  tags: string[];
}

export const APIExplorer: React.FC = () => {
  const [selectedEndpoint, setSelectedEndpoint] = useState<Endpoint | null>(null);
  const [requestBody, setRequestBody] = useState('{}');
  const [response, setResponse] = useState<unknown>(null);

  // Fetch OpenAPI spec
  const { data: openApiSpec, isLoading } = useQuery({
    queryKey: ['openapi-spec'],
    queryFn: async () => {
      return await window.clipshot.api.get('/openapi.json');
    },
  });

  // Parse endpoints from OpenAPI spec
  const endpoints = React.useMemo(() => {
    if (!openApiSpec?.paths) return [];
    
    const result: Endpoint[] = [];
    for (const [path, methods] of Object.entries(openApiSpec.paths)) {
      for (const [method, spec] of Object.entries(methods as object)) {
        if (['get', 'post', 'put', 'delete'].includes(method)) {
          result.push({
            path,
            method: method.toUpperCase() as Endpoint['method'],
            summary: spec.summary || '',
            description: spec.description || '',
            parameters: spec.parameters || [],
            requestBody: spec.requestBody,
            responses: spec.responses || {},
            tags: spec.tags || [],
          });
        }
      }
    }
    return result;
  }, [openApiSpec]);

  // Group endpoints by tag
  const groupedEndpoints = React.useMemo(() => {
    const groups: Record<string, Endpoint[]> = {};
    for (const endpoint of endpoints) {
      const tag = endpoint.tags[0] || 'Other';
      if (!groups[tag]) groups[tag] = [];
      groups[tag].push(endpoint);
    }
    return groups;
  }, [endpoints]);

  // Execute request
  const executeMutation = useMutation({
    mutationFn: async ({ endpoint, body }: { endpoint: Endpoint; body?: unknown }) => {
      const method = endpoint.method.toLowerCase();
      switch (method) {
        case 'get':
          return await window.clipshot.api.get(endpoint.path);
        case 'post':
          return await window.clipshot.api.post(endpoint.path, body);
        case 'put':
          return await window.clipshot.api.put(endpoint.path, body);
        case 'delete':
          return await window.clipshot.api.delete(endpoint.path);
      }
    },
    onSuccess: (data) => {
      setResponse(data);
    },
  });

  const handleExecute = () => {
    if (!selectedEndpoint) return;
    
    let body;
    if (requestBody && ['POST', 'PUT'].includes(selectedEndpoint.method)) {
      try {
        body = JSON.parse(requestBody);
      } catch {
        // Invalid JSON, use as-is
      }
    }
    
    executeMutation.mutate({ endpoint: selectedEndpoint, body });
  };

  return (
    <div className="api-explorer grid grid-cols-12 gap-4 h-full">
      {/* Endpoint List */}
      <div className="col-span-4 overflow-auto border rounded-lg">
        <div className="p-4 border-b sticky top-0 bg-background">
          <Input 
            placeholder="Search endpoints..." 
            className="w-full"
          />
        </div>
        
        <div className="p-2">
          {Object.entries(groupedEndpoints).map(([tag, tagEndpoints]) => (
            <EndpointGroup 
              key={tag}
              tag={tag}
              endpoints={tagEndpoints}
              selectedEndpoint={selectedEndpoint}
              onSelect={setSelectedEndpoint}
            />
          ))}
        </div>
      </div>

      {/* Request/Response Panel */}
      <div className="col-span-8 flex flex-col gap-4">
        {selectedEndpoint ? (
          <>
            {/* Endpoint Header */}
            <Card>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <MethodBadge method={selectedEndpoint.method} />
                  <code className="text-lg">{selectedEndpoint.path}</code>
                </div>
                <p className="text-muted-foreground">
                  {selectedEndpoint.summary}
                </p>
              </CardHeader>
            </Card>

            {/* Request Body */}
            {['POST', 'PUT'].includes(selectedEndpoint.method) && (
              <Card>
                <CardHeader>
                  <h3 className="font-semibold">Request Body</h3>
                </CardHeader>
                <CardContent>
                  <textarea
                    className="w-full h-32 font-mono text-sm bg-muted p-3 rounded"
                    value={requestBody}
                    onChange={(e) => setRequestBody(e.target.value)}
                    placeholder='{"key": "value"}'
                  />
                </CardContent>
              </Card>
            )}

            {/* Execute Button */}
            <Button 
              onClick={handleExecute}
              disabled={executeMutation.isPending}
              className="self-start"
            >
              <Play className="w-4 h-4 mr-2" />
              {executeMutation.isPending ? 'Executing...' : 'Execute'}
            </Button>

            {/* Response */}
            {response && (
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <h3 className="font-semibold">Response</h3>
                  <Button variant="ghost" size="sm" onClick={() => {
                    navigator.clipboard.writeText(JSON.stringify(response, null, 2));
                  }}>
                    <Copy className="w-4 h-4" />
                  </Button>
                </CardHeader>
                <CardContent>
                  <SyntaxHighlighter 
                    language="json" 
                    style={vscDarkPlus}
                    customStyle={{ margin: 0, borderRadius: '0.375rem' }}
                  >
                    {JSON.stringify(response, null, 2)}
                  </SyntaxHighlighter>
                </CardContent>
              </Card>
            )}
          </>
        ) : (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            Select an endpoint to get started
          </div>
        )}
      </div>
    </div>
  );
};

// Helper components
const EndpointGroup: React.FC<{
  tag: string;
  endpoints: Endpoint[];
  selectedEndpoint: Endpoint | null;
  onSelect: (endpoint: Endpoint) => void;
}> = ({ tag, endpoints, selectedEndpoint, onSelect }) => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="mb-2">
      <button
        className="flex items-center gap-2 w-full p-2 hover:bg-muted rounded"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        <span className="font-medium">{tag}</span>
        <span className="text-muted-foreground text-sm">({endpoints.length})</span>
      </button>
      
      {isOpen && (
        <div className="ml-6">
          {endpoints.map((endpoint) => (
            <button
              key={`${endpoint.method}-${endpoint.path}`}
              className={`flex items-center gap-2 w-full p-2 rounded text-left text-sm ${
                selectedEndpoint?.path === endpoint.path && 
                selectedEndpoint?.method === endpoint.method
                  ? 'bg-primary/10'
                  : 'hover:bg-muted'
              }`}
              onClick={() => onSelect(endpoint)}
            >
              <MethodBadge method={endpoint.method} size="sm" />
              <span className="truncate">{endpoint.path}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

const MethodBadge: React.FC<{ method: string; size?: 'sm' | 'md' }> = ({ 
  method, 
  size = 'md' 
}) => {
  const colors: Record<string, string> = {
    GET: 'bg-green-500',
    POST: 'bg-blue-500',
    PUT: 'bg-yellow-500',
    DELETE: 'bg-red-500',
  };

  return (
    <span className={`
      ${colors[method]} text-white font-mono font-bold rounded
      ${size === 'sm' ? 'px-1.5 py-0.5 text-xs' : 'px-2 py-1 text-sm'}
    `}>
      {method}
    </span>
  );
};
```

---

## 🪝 CUSTOM HOOKS

### usePlugins Hook

```tsx
// src/renderer/hooks/usePlugins.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { Plugin, PluginPermissions } from '@/types';

interface UsePluginsOptions {
  type?: string;
  category?: string;
  enabled?: boolean;
  hasUI?: boolean;
  slot?: string;
}

export function usePlugins(options: UsePluginsOptions = {}) {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ['plugins', options],
    queryFn: async () => {
      const plugins = await window.clipshot.plugins.list();
      
      return plugins.filter((p: Plugin) => {
        if (options.type && p.type !== options.type) return false;
        if (options.category && p.category !== options.category) return false;
        if (options.enabled !== undefined && p.enabled !== options.enabled) return false;
        if (options.hasUI && !p.ui) return false;
        if (options.slot && !p.ui?.[options.slot]) return false;
        return true;
      });
    },
  });

  const installMutation = useMutation({
    mutationFn: (source: string) => window.clipshot.plugins.install(source),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plugins'] });
    },
  });

  const uninstallMutation = useMutation({
    mutationFn: (id: string) => window.clipshot.plugins.uninstall(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plugins'] });
    },
  });

  const enableMutation = useMutation({
    mutationFn: (id: string) => window.clipshot.plugins.enable(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plugins'] });
    },
  });

  const disableMutation = useMutation({
    mutationFn: (id: string) => window.clipshot.plugins.disable(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plugins'] });
    },
  });

  return {
    plugins: query.data ?? [],
    isLoading: query.isLoading,
    error: query.error,
    
    install: installMutation.mutateAsync,
    uninstall: uninstallMutation.mutateAsync,
    enable: enableMutation.mutateAsync,
    disable: disableMutation.mutateAsync,
    
    isInstalling: installMutation.isPending,
    isUninstalling: uninstallMutation.isPending,
  };
}

export function usePlugin(id: string) {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ['plugin', id],
    queryFn: () => window.clipshot.plugins.get(id),
  });

  const configQuery = useQuery({
    queryKey: ['plugin', id, 'config'],
    queryFn: () => window.clipshot.plugins.getConfig(id),
    enabled: !!query.data,
  });

  const updateConfigMutation = useMutation({
    mutationFn: (config: Record<string, unknown>) => 
      window.clipshot.plugins.setConfig(id, config),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plugin', id, 'config'] });
    },
  });

  return {
    plugin: query.data,
    config: configQuery.data,
    isLoading: query.isLoading,
    error: query.error,
    updateConfig: updateConfigMutation.mutateAsync,
  };
}
```

### useCapture Hook

```tsx
// src/renderer/hooks/useCapture.ts

import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';

type CaptureStatus = 'idle' | 'recording' | 'paused' | 'processing';

interface CaptureState {
  status: CaptureStatus;
  duration: number;
  fps: number;
  bitrate: number;
}

export function useCapture() {
  const [state, setState] = useState<CaptureState>({
    status: 'idle',
    duration: 0,
    fps: 0,
    bitrate: 0,
  });

  // Subscribe to capture events
  useEffect(() => {
    const unsubscribe = window.clipshot.on('capture:status', (data: CaptureState) => {
      setState(data);
    });
    
    return unsubscribe;
  }, []);

  // Get capture sources
  const { data: sources = [] } = useQuery({
    queryKey: ['capture-sources'],
    queryFn: () => window.clipshot.capture.getSources(),
  });

  // Start capture
  const startMutation = useMutation({
    mutationFn: (options?: CaptureOptions) => window.clipshot.capture.start(options),
  });

  // Stop capture
  const stopMutation = useMutation({
    mutationFn: () => window.clipshot.capture.stop(),
  });

  // Save replay
  const saveReplayMutation = useMutation({
    mutationFn: (duration: number) => window.clipshot.capture.saveReplay(duration),
  });

  return {
    ...state,
    sources,
    
    start: startMutation.mutateAsync,
    stop: stopMutation.mutateAsync,
    saveReplay: saveReplayMutation.mutateAsync,
    
    isStarting: startMutation.isPending,
    isStopping: stopMutation.isPending,
    isSaving: saveReplayMutation.isPending,
  };
}
```

---

## 🌍 I18N SETUP

```tsx
// src/renderer/i18n/index.ts

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import ICU from 'i18next-icu';

import en from './locales/en.json';
import tr from './locales/tr.json';

i18n
  .use(ICU)
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      tr: { translation: tr },
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;

// Hook for plugin translations
export function useTranslation(namespace?: string) {
  const { t, i18n } = useTranslation();
  
  const tPlugin = useCallback((key: string, options?: object) => {
    if (namespace) {
      return t(`plugins.${namespace}.${key}`, options);
    }
    return t(key, options);
  }, [namespace, t]);
  
  return { t: tPlugin, i18n };
}
```

---

## 🎯 Bu Mimarinin Avantajları

1. **Security** — Context isolation ile güvenli IPC
2. **Modularity** — Plugin-based UI genişletilebilirlik
3. **Performance** — Lazy loading, code splitting
4. **Developer Experience** — Hot reload, type safety
5. **Accessibility** — WCAG uyumlu komponentler
6. **Internationalization** — ICU format, RTL desteği
