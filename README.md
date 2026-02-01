# ClipShot 🎮✨

> AI-Powered Gaming Clips Platform

ClipShot is a modular, plugin-driven platform for capturing, editing, and sharing gaming clips with intelligent highlight detection.

## Features

- 🎥 **Screen Capture** - Record gameplay with minimal performance impact
- 🤖 **AI-Powered Highlights** - Automatically detect and create highlight reels
- 🔌 **Plugin System** - Extend functionality with custom plugins
- 🌍 **Multi-Language Support** - Available in 5+ languages
- 🛡️ **Secure Sandbox** - Isolated plugin execution with resource limits
- 📊 **Performance Monitoring** - Real-time metrics and health checks
- 🐳 **Docker Ready** - Easy deployment with Docker Compose

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- Rust 1.70+
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/ubeydtalha/Clibshot.git
cd Clibshot

# Install dependencies
npm install

# Start development environment
docker-compose up -d

# Run the desktop app
cd apps/desktop
npm install
npm run tauri dev
```

## Documentation

- [Setup Guide](docs/guides/SETUP.md)
- [Architecture Overview](docs/guides/ARCHITECTURE.md)
- [Plugin Development](docs/guides/PLUGIN_DEVELOPMENT.md)
- [API Reference](docs/api/README.md)
- [Contributing](docs/guides/CONTRIBUTING.md)
- [Deployment](docs/guides/DEPLOYMENT.md)

## Project Structure

```
clipshot/
├── apps/
│   ├── desktop/          # Tauri desktop app
│   └── backend/          # FastAPI server
├── docs/                 # Documentation
│   ├── guides/          # User & developer guides
│   └── api/             # API documentation
├── tools/
│   ├── mcp-server/      # Performance monitoring
│   └── scripts/         # Build & deployment scripts
├── .github/
│   └── workflows/       # CI/CD pipelines
└── docker/              # Docker configurations
```

## Development

### Backend

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd apps/desktop
npm install
npm run dev
```

### Running Tests

```bash
# All tests
./tools/scripts/test.sh

# Backend only
cd apps/backend && pytest

# Frontend only
cd apps/desktop && npm test
```

### Building

```bash
# Build all components
./tools/scripts/build.sh

# Create release
./tools/scripts/release.sh 1.0.0
```

## Security

ClipShot implements multiple security layers:

- **Process Isolation** - Plugins run in separate processes
- **Permission System** - Granular access control
- **Resource Limits** - CPU, memory, and I/O restrictions
- **Filesystem Jail** - Isolated plugin directories
- **Network Controls** - Restricted network access

See [Security Documentation](docs/06_SECURITY_SANDBOX.md) for details.

## Performance

Target Performance Metrics:

- UI Frame Time: <16ms (60fps)
- Clip Trigger Latency: <50ms
- AI Inference (Local): <200ms
- Memory Usage: <512MB (idle)
- CPU Usage: <2% (idle)

See [Performance Documentation](docs/09_PERFORMANCE_MCP.md) for details.

## Localization

Supported Languages:

- 🇺🇸 English
- 🇹🇷 Turkish (Türkçe)
- 🇩🇪 German (Deutsch)
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)

See [Localization Documentation](docs/08_LOCALIZATION.md) for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/guides/CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/ubeydtalha/Clibshot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ubeydtalha/Clibshot/discussions)
- **Discord**: [Join our Discord](https://discord.gg/clipshot)

## Roadmap

- [ ] Phase 1: Core Infrastructure ✅
- [ ] Phase 2: Security & Sandbox ✅
- [ ] Phase 3: Performance Monitoring ✅
- [ ] Phase 4: Localization ✅
- [ ] Phase 5: CI/CD & Deployment ✅
- [ ] Phase 6: Plugin Marketplace
- [ ] Phase 7: AI Integration
- [ ] Phase 8: Cloud Sync
- [ ] Phase 9: Mobile App
- [ ] Phase 10: Browser Extension

## Acknowledgments

- Built with [Tauri](https://tauri.app/)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- UI with [React](https://react.dev/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)

---

Made with ❤️ by the ClipShot Team
