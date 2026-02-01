import { useEffect } from 'react';
import { useClipStore, useCaptureStore } from '@/stores';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui';
import { Film, Clock, HardDrive } from 'lucide-react';

export function Dashboard() {
  const { clips, loadClips } = useClipStore();
  const { isCapturing } = useCaptureStore();

  useEffect(() => {
    loadClips();
  }, [loadClips]);

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Welcome to ClipShot</p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Clips</CardTitle>
            <Film className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{clips.length}</div>
            <p className="text-xs text-muted-foreground">Captured clips</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Recording</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{isCapturing ? 'Active' : 'Idle'}</div>
            <p className="text-xs text-muted-foreground">Current status</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Storage</CardTitle>
            <HardDrive className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">--</div>
            <p className="text-xs text-muted-foreground">Available space</p>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <h2 className="mb-4 text-xl font-semibold">Recent Clips</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {clips.length === 0 ? (
            <Card className="col-span-full">
              <CardContent className="py-8 text-center">
                <p className="text-muted-foreground">No clips yet. Start capturing!</p>
              </CardContent>
            </Card>
          ) : (
            clips.slice(0, 6).map((clip) => (
              <Card key={clip.id}>
                <CardHeader>
                  <CardTitle className="text-base">{clip.title}</CardTitle>
                  <CardDescription>{clip.game || 'No game detected'}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{clip.duration}s</p>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
