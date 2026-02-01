import { create } from 'zustand';

interface ConfigStore {
  theme: 'light' | 'dark' | 'system';
  language: string;
  captureSettings: {
    quality: 'low' | 'medium' | 'high' | 'ultra';
    fps: number;
    codec: string;
    autoCapture: boolean;
  };
  
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  setLanguage: (language: string) => void;
  updateCaptureSettings: (settings: Partial<ConfigStore['captureSettings']>) => void;
}

// Note: For persistence, consider using localStorage directly or a persistence library
export const useConfigStore = create<ConfigStore>((set) => ({
  theme: 'system',
  language: 'en',
  captureSettings: {
    quality: 'high',
    fps: 60,
    codec: 'h264',
    autoCapture: true,
  },

  setTheme: (theme) => {
    set({ theme });
    // Persist to localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('clipshot-theme', theme);
    }
  },
  setLanguage: (language) => {
    set({ language });
    if (typeof window !== 'undefined') {
      localStorage.setItem('clipshot-language', language);
    }
  },
  updateCaptureSettings: (settings) =>
    set((state) => ({
      captureSettings: { ...state.captureSettings, ...settings },
    })),
}));
