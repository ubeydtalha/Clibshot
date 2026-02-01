/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly TAURI_PLATFORM: string
  readonly TAURI_DEBUG: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
