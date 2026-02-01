import { expect, afterEach, vi } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

// Extend vitest matchers
expect.extend(matchers)

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock Tauri API
global.window = global.window || ({} as any)
global.window.__TAURI__ = {
  invoke: vi.fn(),
  convertFileSrc: vi.fn((src) => src),
}

// Mock @tauri-apps/api
vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}))
