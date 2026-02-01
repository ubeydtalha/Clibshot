import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { invoke } from '@tauri-apps/api/core'
import App from '../App'

vi.mock('@tauri-apps/api/core')

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the main heading', () => {
    vi.mocked(invoke).mockResolvedValue({ os: 'Windows', arch: 'x64', version: '10' })
    render(<App />)
    expect(screen.getByText(/ClipShot/i)).toBeInTheDocument()
  })

  it('calls get_system_info on mount', async () => {
    const mockSystemInfo = {
      os: 'Windows',
      arch: 'x86_64',
      version: '11'
    }
    
    vi.mocked(invoke).mockResolvedValue(mockSystemInfo)
    render(<App />)

    await waitFor(() => {
      expect(invoke).toHaveBeenCalledWith('get_system_info')
    })
  })

  it('displays system information when loaded', async () => {
    const mockSystemInfo = {
      os: 'Windows',
      arch: 'x86_64',
      version: '11'
    }
    
    vi.mocked(invoke).mockResolvedValue(mockSystemInfo)
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/Windows/i)).toBeInTheDocument()
      expect(screen.getByText(/x86_64/i)).toBeInTheDocument()
    })
  })

  it('checks backend health on mount', async () => {
    vi.mocked(invoke).mockImplementation((cmd: string) => {
      if (cmd === 'get_system_info') {
        return Promise.resolve({ os: 'Windows', arch: 'x64', version: '10' })
      }
      if (cmd === 'call_backend_api') {
        return Promise.resolve('OK')
      }
      return Promise.resolve('')
    })

    render(<App />)

    await waitFor(() => {
      expect(invoke).toHaveBeenCalledWith('call_backend_api', { endpoint: 'health' })
    })
  })

  it('shows backend online status when health check succeeds', async () => {
    vi.mocked(invoke).mockImplementation((cmd: string) => {
      if (cmd === 'get_system_info') {
        return Promise.resolve({ os: 'Windows', arch: 'x64', version: '10' })
      }
      if (cmd === 'call_backend_api') {
        return Promise.resolve('OK')
      }
      return Promise.resolve('')
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/Backend Online/i)).toBeInTheDocument()
    })
  })

  it('shows backend offline status when health check fails', async () => {
    vi.mocked(invoke).mockImplementation((cmd: string) => {
      if (cmd === 'get_system_info') {
        return Promise.resolve({ os: 'Windows', arch: 'x64', version: '10' })
      }
      if (cmd === 'call_backend_api') {
        return Promise.reject(new Error('Connection failed'))
      }
      return Promise.resolve('')
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/Backend Offline/i)).toBeInTheDocument()
    })
  })
})
