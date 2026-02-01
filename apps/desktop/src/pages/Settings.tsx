import { useConfigStore } from '@/stores';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@/components/ui';

export function Settings() {
  const { theme, setTheme, captureSettings, updateCaptureSettings } = useConfigStore();

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-muted-foreground">Configure your ClipShot experience</p>
      </div>

      <div className="max-w-2xl space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Appearance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <label className="mb-2 block text-sm font-medium">Theme</label>
                <div className="flex gap-2">
                  <Button
                    variant={theme === 'light' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setTheme('light')}
                  >
                    Light
                  </Button>
                  <Button
                    variant={theme === 'dark' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setTheme('dark')}
                  >
                    Dark
                  </Button>
                  <Button
                    variant={theme === 'system' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setTheme('system')}
                  >
                    System
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Capture Settings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <label className="mb-2 block text-sm font-medium">Quality</label>
                <div className="flex gap-2">
                  {(['low', 'medium', 'high', 'ultra'] as const).map((quality) => (
                    <Button
                      key={quality}
                      variant={captureSettings.quality === quality ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => updateCaptureSettings({ quality })}
                    >
                      {quality.charAt(0).toUpperCase() + quality.slice(1)}
                    </Button>
                  ))}
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium">
                  Frame Rate: {captureSettings.fps} FPS
                </label>
                <input
                  type="range"
                  min="30"
                  max="120"
                  step="30"
                  value={captureSettings.fps}
                  onChange={(e) => updateCaptureSettings({ fps: parseInt(e.target.value) })}
                  className="w-full"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium">Codec</label>
                <select
                  value={captureSettings.codec}
                  onChange={(e) => updateCaptureSettings({ codec: e.target.value })}
                  className="w-full rounded-md border border-input bg-background px-3 py-2"
                >
                  <option value="h264">H.264</option>
                  <option value="h265">H.265</option>
                  <option value="vp9">VP9</option>
                  <option value="av1">AV1</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
