/**
 * Logging utility for ClipShot Frontend
 * Provides console and Tauri logging integration
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  data?: any;
  source?: string;
}

class Logger {
  private logs: LogEntry[] = [];
  private maxLogs = 1000;
  private isDev = import.meta.env.DEV;

  private formatMessage(level: LogLevel, message: string, data?: any): LogEntry {
    return {
      timestamp: new Date().toISOString(),
      level,
      message,
      data,
      source: 'frontend'
    };
  }

  private writeLog(entry: LogEntry) {
    // Store in memory
    this.logs.push(entry);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }

    // Console output with styling
    const timestamp = new Date(entry.timestamp).toLocaleTimeString();
    const prefix = `[${timestamp}] [${entry.level.toUpperCase()}]`;
    
    switch (entry.level) {
      case 'debug':
        if (this.isDev) {
          console.debug(prefix, entry.message, entry.data || '');
        }
        break;
      case 'info':
        console.info(prefix, entry.message, entry.data || '');
        break;
      case 'warn':
        console.warn(prefix, entry.message, entry.data || '');
        break;
      case 'error':
        console.error(prefix, entry.message, entry.data || '');
        if (entry.data instanceof Error) {
          console.error(entry.data.stack);
        }
        break;
    }

    // TODO: Send to Tauri backend for file logging
    // if (window.__TAURI__) {
    //   invoke('log_message', { entry });
    // }
  }

  debug(message: string, data?: any) {
    this.writeLog(this.formatMessage('debug', message, data));
  }

  info(message: string, data?: any) {
    this.writeLog(this.formatMessage('info', message, data));
  }

  warn(message: string, data?: any) {
    this.writeLog(this.formatMessage('warn', message, data));
  }

  error(message: string, data?: any) {
    this.writeLog(this.formatMessage('error', message, data));
  }

  getLogs(): LogEntry[] {
    return [...this.logs];
  }

  clearLogs() {
    this.logs = [];
  }

  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }
}

// Singleton instance
export const logger = new Logger();

// Global error handler
window.addEventListener('error', (event) => {
  logger.error('Uncaught error', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error
  });
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
  logger.error('Unhandled promise rejection', {
    reason: event.reason,
    promise: event.promise
  });
});

// Log app startup
logger.info('ClipShot Frontend initialized', {
  isDev: import.meta.env.DEV,
  mode: import.meta.env.MODE
});
