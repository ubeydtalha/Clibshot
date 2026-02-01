import { create } from 'zustand';
import { persist } from 'zustand/middleware';

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

export const useConfigStore = create<ConfigStore>()(
  persist(
    (set) => ({
      theme: 'system',
      language: 'en',
      captureSettings: {
        quality: 'high',
        fps: 60,
        codec: 'h264',
        autoCapture: true,
      },

      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
      updateCaptureSettings: (settings) =>
        set((state) => ({
          captureSettings: { ...state.captureSettings, ...settings },
        })),
    }),
    {
      name: 'clipshot-config',
    }
  )
);
