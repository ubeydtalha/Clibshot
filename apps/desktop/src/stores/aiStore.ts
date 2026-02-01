import { create } from 'zustand';
import { tauriAPI, type AIModel } from '@/lib/tauri';

interface AIStore {
  models: AIModel[];
  loading: boolean;
  error: string | null;
  inferenceProgress: number;

  loadModels: () => Promise<void>;
  runInference: (modelId: string, input: unknown) => Promise<void>;
  generateMetadata: (clipId: string) => Promise<void>;
}

export const useAIStore = create<AIStore>((set) => ({
  models: [],
  loading: false,
  error: null,
  inferenceProgress: 0,

  loadModels: async () => {
    set({ loading: true, error: null });
    try {
      const models = await tauriAPI.ai.listModels();
      set({ models, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  runInference: async (modelId: string, input: unknown) => {
    set({ loading: true, error: null, inferenceProgress: 0 });
    try {
      await tauriAPI.ai.runInference(modelId, input);
      set({ loading: false, inferenceProgress: 100 });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  generateMetadata: async (clipId: string) => {
    set({ loading: true, error: null });
    try {
      await tauriAPI.ai.generateMetadata(clipId);
      set({ loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },
}));
