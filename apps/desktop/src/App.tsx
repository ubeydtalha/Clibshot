import { useState, useEffect } from 'react'
import { invoke } from '@tauri-apps/api/core'
import { logger } from './utils/logger'
import './App.css'

interface SystemInfo {
  os: string
  arch: string
  version: string
}

function App() {
  const [greetMsg, setGreetMsg] = useState('')
  const [name, setName] = useState('')
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null)
  const [backendStatus, setBackendStatus] = useState<string>('Checking...')

  useEffect(() => {
    logger.info('App component mounted')
    
    // Get system info on mount
    invoke<SystemInfo>('get_system_info')
      .then((info) => {
        logger.info('System info retrieved', info)
        setSystemInfo(info)
      })
      .catch((error) => {
        logger.error('Failed to get system info', error)
      })
    
    // Check backend status
    logger.debug('Checking backend status...')
    invoke<string>('call_backend_api', { endpoint: 'health' })
      .then(() => {
        logger.info('Backend is online')
        setBackendStatus('✅ Backend Online')
      })
      .catch((error) => {
        logger.warn('Backend is offline', error)
        setBackendStatus('❌ Backend Offline')
      })
  }, [])

  async function greet() {
    try {
      logger.debug('Greet command called', { name })
      const msg = await invoke<string>('greet', { name })
      setGreetMsg(msg)
      logger.info('Greet successful', { message: msg })
    } catch (error) {
      logger.error('Greet command failed', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4">
            🎮 ClipShot
          </h1>
          <p className="text-xl text-gray-400">
            Modular Gaming Clip Platform
          </p>
        </header>

        {/* System Info */}
        {systemInfo && (
          <div className="bg-gray-800 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold mb-4">System Information</h2>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-gray-400">Operating System</p>
                <p className="text-lg font-medium">{systemInfo.os}</p>
              </div>
              <div>
                <p className="text-gray-400">Architecture</p>
                <p className="text-lg font-medium">{systemInfo.arch}</p>
              </div>
              <div>
                <p className="text-gray-400">Version</p>
                <p className="text-lg font-medium">{systemInfo.version}</p>
              </div>
            </div>
          </div>
        )}

        {/* Backend Status */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Backend Status</h2>
          <p className="text-lg">{backendStatus}</p>
          <p className="text-sm text-gray-400 mt-2">
            FastAPI should be running on http://localhost:8000
          </p>
        </div>

        {/* Greet Section */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Test Tauri Command</h2>
          <div className="flex gap-4">
            <input
              className="flex-1 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your name..."
              value={name}
              onChange={(e) => setName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && greet()}
            />
            <button
              className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-medium transition-colors"
              onClick={greet}
            >
              Greet
            </button>
          </div>
          {greetMsg && (
            <p className="mt-4 text-lg text-green-400">{greetMsg}</p>
          )}
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-2">📚 Documentation</h3>
            <p className="text-gray-400 mb-4">
              Read the comprehensive docs to understand the architecture.
            </p>
            <a
              href="https://github.com/yourusername/clipshot/tree/main/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300"
            >
              View Docs →
            </a>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-2">🔌 Plugin System</h3>
            <p className="text-gray-400 mb-4">
              Create plugins in Python, Rust, or C++ to extend functionality.
            </p>
            <a
              href="https://github.com/yourusername/clipshot/tree/main/plugins/examples"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300"
            >
              View Examples →
            </a>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center mt-12 text-gray-500">
          <p>Built with Tauri + Vite + React + FastAPI</p>
          <p className="mt-2">
            Stack: Rust • TypeScript • Python • Tailwind CSS
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App
