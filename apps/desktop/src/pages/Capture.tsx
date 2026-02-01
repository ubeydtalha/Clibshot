import { useEffect } from 'react';
import { useCaptureStore } from '@/stores';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@/components/ui';
import { Video, Square, Pause } from 'lucide-react';

export function Capture() {
  const { isCapturing, isPaused, sources, getSources, startCapture, stopCapture, pauseCapture, selectedSource } =
    useCaptureStore();

  useEffect(() => {
    getSources();
  }, [getSources]);

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Capture</h1>
        <p className="text-muted-foreground">Record your gameplay</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Capture Sources</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {sources.map((source) => (
                <button
                  key={source.id}
                  onClick={() => !isCapturing && startCapture(source.id)}
                  disabled={isCapturing}
                  className="w-full rounded-lg border p-4 text-left transition-colors hover:bg-accent disabled:opacity-50"
                >
                  <div className="flex items-center gap-3">
                    <Video className="h-5 w-5" />
                    <div>
                      <p className="font-medium">{source.name}</p>
                      <p className="text-sm text-muted-foreground">{source.source_type}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Capture Controls</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="rounded-lg bg-muted p-6 text-center">
                <p className="mb-2 text-sm text-muted-foreground">Status</p>
                <p className="text-2xl font-bold">
                  {isCapturing ? (isPaused ? 'Paused' : 'Recording') : 'Idle'}
                </p>
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={() => stopCapture()}
                  disabled={!isCapturing}
                  variant="destructive"
                  className="flex-1"
                >
                  <Square className="mr-2 h-4 w-4" />
                  Stop
                </Button>
                <Button
                  onClick={() => pauseCapture()}
                  disabled={!isCapturing || isPaused}
                  variant="outline"
                  className="flex-1"
                >
                  <Pause className="mr-2 h-4 w-4" />
                  Pause
                </Button>
              </div>

              {selectedSource && (
                <p className="text-sm text-muted-foreground">
                  Recording from: {sources.find((s) => s.id === selectedSource)?.name}
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
