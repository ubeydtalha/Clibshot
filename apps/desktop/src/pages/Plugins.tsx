import { useEffect } from 'react';
import { usePluginStore } from '@/stores';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, Button } from '@/components/ui';
import { Package, Play, Square } from 'lucide-react';

export function Plugins() {
  const { plugins, loading, loadPlugins, unloadPlugin } = usePluginStore();

  useEffect(() => {
    loadPlugins();
  }, [loadPlugins]);

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Plugins</h1>
          <p className="text-muted-foreground">Manage your installed plugins</p>
        </div>
        <Button>
          <Package className="mr-2 h-4 w-4" />
          Install Plugin
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <p className="text-muted-foreground">Loading plugins...</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {plugins.length === 0 ? (
            <Card className="col-span-full">
              <CardContent className="py-8 text-center">
                <Package className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                <p className="text-muted-foreground">No plugins installed</p>
              </CardContent>
            </Card>
          ) : (
            plugins.map((plugin) => (
              <Card key={plugin.id}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    {plugin.name}
                    {plugin.enabled ? (
                      <Play className="h-4 w-4 text-green-500" />
                    ) : (
                      <Square className="h-4 w-4 text-gray-400" />
                    )}
                  </CardTitle>
                  <CardDescription>v{plugin.version}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => unloadPlugin(plugin.id)}
                      disabled={!plugin.enabled}
                    >
                      Unload
                    </Button>
                    <Button variant="outline" size="sm" disabled>
                      Configure
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  );
}
