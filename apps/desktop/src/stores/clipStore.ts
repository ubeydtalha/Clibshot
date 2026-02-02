import { create } from 'zustand';
import { tauriAPI, type Clip } from '@/lib/tauri';

interface ClipStore {
  clips: Clip[];
  selectedClip: Clip | null;
  loading: boolean;
  error: string | null;

  loadClips: () => Promise<void>;
  getClip: (id: string) => Promise<void>;
  deleteClip: (id: string) => Promise<void>;
  exportClip: (id: string, path: string) => Promise<void>;
  setSelectedClip: (clip: Clip | null) => void;
}

export const useClipStore = create<ClipStore>((set, get) => ({
  clips: [],
  selectedClip: null,
  loading: false,
  error: null,

  loadClips: async () => {
    set({ loading: true, error: null });
    try {
      const clips = await tauriAPI.clips.list();
      set({ clips, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  getClip: async (id: string) => {
    set({ loading: true, error: null });
    try {
      const clip = await tauriAPI.clips.get(id);
      set({ selectedClip: clip, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  deleteClip: async (id: string) => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.clips.delete(id);
      const clips = get().clips.filter((c) => c.id !== id);
      set({ clips, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  exportClip: async (id: string, path: string) => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.clips.export(id, path);
      set({ loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  setSelectedClip: (clip: Clip | null) => {
    set({ selectedClip: clip });
  },
}));
