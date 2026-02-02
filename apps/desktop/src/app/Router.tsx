import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { Dashboard } from '@/pages/Dashboard';
import { Plugins } from '@/pages/Plugins';
import { Capture } from '@/pages/Capture';
import { AIModels } from '@/pages/AIModels';
import { Settings } from '@/pages/Settings';
import { DevPanel } from '@/pages/DevPanel';

export function Router() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/plugins" element={<Plugins />} />
          <Route path="/capture" element={<Capture />} />
          <Route path="/ai-models" element={<AIModels />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/dev" element={<DevPanel />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}
