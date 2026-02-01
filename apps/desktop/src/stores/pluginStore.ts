import { create } from 'zustand';
import { tauriAPI, type PluginInfo } from '@/lib/tauri';

interface PluginStore {
  plugins: PluginInfo[];
  loading: boolean;
  error: string | null;

  loadPlugins: () => Promise<void>;
  loadPlugin: (path: string) => Promise<void>;
  unloadPlugin: (id: string) => Promise<void>;
  refreshPluginInfo: (id: string) => Promise<void>;
}

export const usePluginStore = create<PluginStore>((set, get) => ({
  plugins: [],
  loading: false,
  error: null,

  loadPlugins: async () => {
    set({ loading: true, error: null });
    try {
      const plugins = await tauriAPI.plugins.list();
      set({ plugins, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  loadPlugin: async (path: string) => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.plugins.load(path);
      await get().loadPlugins();
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  unloadPlugin: async (id: string) => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.plugins.unload(id);
      await get().loadPlugins();
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  refreshPluginInfo: async (id: string) => {
    set({ loading: true, error: null });
    try {
      const plugin = await tauriAPI.plugins.getInfo(id);
      const plugins = get().plugins.map((p) => (p.id === id ? plugin : p));
      set({ plugins, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },
}));
