import { create } from 'zustand';
import { tauriAPI, type CaptureSource } from '@/lib/tauri';

interface CaptureStore {
  isCapturing: boolean;
  isPaused: boolean;
  sources: CaptureSource[];
  selectedSource: string | null;
  loading: boolean;
  error: string | null;

  getSources: () => Promise<void>;
  startCapture: (sourceId: string) => Promise<void>;
  stopCapture: () => Promise<void>;
  pauseCapture: () => Promise<void>;
  setSelectedSource: (sourceId: string | null) => void;
}

export const useCaptureStore = create<CaptureStore>((set, get) => ({
  isCapturing: false,
  isPaused: false,
  sources: [],
  selectedSource: null,
  loading: false,
  error: null,

  getSources: async () => {
    set({ loading: true, error: null });
    try {
      const sources = await tauriAPI.capture.getSources();
      set({ sources, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  startCapture: async (sourceId: string) => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.capture.start(sourceId);
      set({ isCapturing: true, isPaused: false, selectedSource: sourceId, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  stopCapture: async () => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.capture.stop();
      set({ isCapturing: false, isPaused: false, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  pauseCapture: async () => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.capture.pause();
      set({ isPaused: true, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  setSelectedSource: (sourceId: string | null) => {
    set({ selectedSource: sourceId });
  },
}));
