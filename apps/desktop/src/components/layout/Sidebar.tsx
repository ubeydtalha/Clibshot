import { NavLink } from 'react-router-dom';
import { Home, Film, Cpu, Package, Settings, Code } from 'lucide-react';
import { cn } from '@/utils/format';

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Capture', href: '/capture', icon: Film },
  { name: 'Plugins', href: '/plugins', icon: Package },
  { name: 'AI Models', href: '/ai-models', icon: Cpu },
  { name: 'Settings', href: '/settings', icon: Settings },
  { name: 'Dev Panel', href: '/dev', icon: Code },
];

export function Sidebar() {
  return (
    <div className="flex h-full w-64 flex-col border-r bg-card">
      <div className="flex h-16 items-center border-b px-6">
        <h1 className="text-xl font-bold">ClipShot</h1>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              )
            }
          >
            <item.icon className="h-5 w-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
      <div className="border-t p-4">
        <p className="text-xs text-muted-foreground">Version 0.1.0</p>
      </div>
    </div>
  );
}
