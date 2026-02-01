# ClipShot Desktop Application

Modern Tauri + Vite + React desktop application for gaming clip management.

## Prerequisites

- **Node.js** 20+ and npm (or pnpm for faster installs)
- **Rust** (latest stable) - Install from https://rustup.rs
- **Python** 3.11+ (for PyO3 bridge)
- **System dependencies**:
  - Windows: WebView2 (usually pre-installed on Windows 10/11)
  - macOS: Xcode Command Line Tools
  - Linux: webkit2gtk, libgtk-3, libayatana-appindicator

## Installation

1. Install dependencies:
```bash
npm install
```

2. Install Rust dependencies (automatic on first build):
```bash
cd src-tauri
cargo fetch
```

## Development

Run the development server with hot-reload:
```bash
npm run tauri:dev
```

This will:
- Start Vite development server on http://localhost:5173
- Launch the Tauri application
- Enable hot-reload for both frontend and Rust backend

## Building

Build for production:
```bash
npm run tauri:build
```

The compiled application will be in `src-tauri/target/release/bundle/`.

## Project Structure

```
apps/desktop/
├── src/                    # React frontend (Vite)
│   ├── app/               # App setup (Router, providers)
│   ├── components/        # React components
│   ├── pages/            # Page components
│   ├── stores/           # Zustand state management
│   ├── lib/              # Tauri API wrappers
│   ├── hooks/            # Custom React hooks
│   ├── styles/           # Global styles
│   └── utils/            # Utility functions
│
├── src-tauri/             # Rust backend (Tauri)
│   ├── src/
│   │   ├── main.rs       # Entry point
│   │   ├── commands/     # Tauri commands (IPC)
│   │   ├── plugins/      # Plugin manager
│   │   ├── bridge/       # Python bridge (PyO3)
│   │   ├── state/        # App state
│   │   └── utils/        # Utility modules
│   ├── Cargo.toml        # Rust dependencies
│   └── tauri.conf.json   # Tauri configuration
│
├── index.html            # HTML template
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # npm dependencies

## Features

- ✅ Tauri v2 with Rust backend
- ✅ Vite + React 18 with TypeScript
- ✅ Tailwind CSS for styling
- ✅ Zustand for state management
- ✅ React Router v6 for navigation
- ✅ Radix UI components
- ✅ Plugin system with dynamic UI loading
- ✅ PyO3 bridge for Python integration
- ✅ Dark mode support

## Architecture

### Frontend (React + TypeScript)
- **State Management**: Zustand stores for plugins, capture, clips, AI, and config
- **Routing**: React Router with layout and page components
- **UI Components**: Radix UI primitives with Tailwind CSS
- **API Integration**: Type-safe Tauri command wrappers

### Backend (Rust + Tauri)
- **Commands**: Plugin, capture, clips, AI, and system commands
- **Plugin Manager**: Load/unload plugins with metadata
- **Python Bridge**: PyO3 for FastAPI communication
- **State Management**: Thread-safe app state

### Security
- Minimal Tauri allowlist (principle of least privilege)
- Scoped file system access
- HTTP requests limited to localhost:8000
- No shell access except `open` command

## Available Scripts

- `npm run dev` - Start Vite dev server
- `npm run build` - Build React app
- `npm run tauri:dev` - Run Tauri in development mode
- `npm run tauri:build` - Build production app
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Troubleshooting

### Rust Build Errors
- Ensure Rust is up to date: `rustup update`
- Clean build: `cd src-tauri && cargo clean`

### Python Bridge Issues
- Ensure Python 3.11+ is installed
- Install PyO3: `pip install maturin`

### WebView Issues
- Windows: Update WebView2 Runtime
- Linux: Install webkit2gtk-4.0
- macOS: Update Xcode Command Line Tools

## Next Steps

1. Install dependencies and run development server
2. Configure backend FastAPI integration
3. Implement plugin loading system
4. Add AI model integration
5. Create capture system integration

## Documentation

See the `../../docs/` directory for:
- `04_FRONTEND_ARCHITECTURE.md` - Frontend architecture details
- `01_PROJECT_STRUCTURE.md` - Full project structure
- `02_PLUGIN_DEVELOPER_GUIDE.md` - Plugin development guide

## License

MIT
