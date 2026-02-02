/// <reference types="vite/client" />

interface ImportMetaEnv {
<<<<<<< HEAD
  readonly VITE_API_URL?: string
  readonly DEV: boolean
  readonly MODE: string
  readonly PROD: boolean
  readonly SSR: boolean
=======
  readonly VITE_API_URL: string
  readonly TAURI_PLATFORM: string
  readonly TAURI_DEBUG: string
>>>>>>> a22cb8785c6ca7fb2e44d970ba98842c9099163d
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
