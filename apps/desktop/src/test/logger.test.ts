import { describe, it, expect, beforeEach, vi } from 'vitest'
import { logger } from '../utils/logger'

describe('Logger', () => {
  beforeEach(() => {
    logger.clearLogs()
    vi.clearAllMocks()
  })

  it('logs debug messages in development mode', () => {
    void vi.spyOn(console, 'debug')
    logger.debug('Test debug message', { test: true })
    
    const logs = logger.getLogs()
    expect(logs).toHaveLength(1)
    expect(logs[0].level).toBe('debug')
    expect(logs[0].message).toBe('Test debug message')
  })

  it('logs info messages', () => {
    void vi.spyOn(console, 'info')
    logger.info('Test info message')
    
    const logs = logger.getLogs()
    expect(logs).toHaveLength(1)
    expect(logs[0].level).toBe('info')
    expect(logs[0].message).toBe('Test info message')
  })

  it('logs warning messages', () => {
    void vi.spyOn(console, 'warn')
    logger.warn('Test warning')
    
    const logs = logger.getLogs()
    expect(logs[0].level).toBe('warn')
  })

  it('logs error messages', () => {
    void vi.spyOn(console, 'error')
    const error = new Error('Test error')
    logger.error('Error occurred', error)
    
    const logs = logger.getLogs()
    expect(logs[0].level).toBe('error')
    expect(logs[0].data).toBe(error)
  })

  it('includes timestamp in log entries', () => {
    logger.info('Test message')
    const logs = logger.getLogs()
    
    expect(logs[0].timestamp).toBeDefined()
    expect(new Date(logs[0].timestamp)).toBeInstanceOf(Date)
  })

  it('limits log storage to maxLogs', () => {
    // Log more than maxLogs (1000)
    for (let i = 0; i < 1100; i++) {
      logger.debug(`Message ${i}`)
    }
    
    const logs = logger.getLogs()
    expect(logs.length).toBeLessThanOrEqual(1000)
  })

  it('clears logs', () => {
    logger.info('Message 1')
    logger.info('Message 2')
    expect(logger.getLogs()).toHaveLength(2)
    
    logger.clearLogs()
    expect(logger.getLogs()).toHaveLength(0)
  })

  it('exports logs as JSON', () => {
    logger.info('Test message')
    const exported = logger.exportLogs()
    
    expect(() => JSON.parse(exported)).not.toThrow()
    const parsed = JSON.parse(exported)
    expect(Array.isArray(parsed)).toBe(true)
  })

  it('includes data in log entries', () => {
    const testData = { userId: 123, action: 'click' }
    logger.info('User action', testData)
    
    const logs = logger.getLogs()
    expect(logs[0].data).toEqual(testData)
  })
})
