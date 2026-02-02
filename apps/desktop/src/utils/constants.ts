// Application constants

export const APP_NAME = 'ClipShot';
export const APP_VERSION = '0.1.0';

// Capture settings
export const CAPTURE_QUALITY = {
  LOW: { label: 'Low', fps: 30, bitrate: 2000 },
  MEDIUM: { label: 'Medium', fps: 60, bitrate: 5000 },
  HIGH: { label: 'High', fps: 60, bitrate: 10000 },
  ULTRA: { label: 'Ultra', fps: 120, bitrate: 20000 },
} as const;

// Supported video codecs
export const VIDEO_CODECS = ['h264', 'h265', 'vp9', 'av1'] as const;

// Clip duration limits (in seconds)
export const MIN_CLIP_DURATION = 1;
export const MAX_CLIP_DURATION = 300; // 5 minutes
export const DEFAULT_CLIP_DURATION = 30;

// File size limits
export const MAX_CLIP_SIZE = 1024 * 1024 * 1024; // 1GB

// Routes
export const ROUTES = {
  DASHBOARD: '/',
  PLUGINS: '/plugins',
  CAPTURE: '/capture',
  CLIPS: '/clips',
  AI_MODELS: '/ai-models',
  SETTINGS: '/settings',
  DEV_PANEL: '/dev',
} as const;
