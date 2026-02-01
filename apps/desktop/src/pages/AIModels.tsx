import { useEffect } from 'react';
import { useAIStore } from '@/stores';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, Button } from '@/components/ui';
import { Cpu, Download } from 'lucide-react';
import { formatFileSize } from '@/utils/format';

export function AIModels() {
  const { models, loading, loadModels } = useAIStore();

  useEffect(() => {
    loadModels();
  }, [loadModels]);

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">AI Models</h1>
          <p className="text-muted-foreground">Manage AI models for clip analysis</p>
        </div>
        <Button>
          <Download className="mr-2 h-4 w-4" />
          Download Model
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <p className="text-muted-foreground">Loading models...</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {models.length === 0 ? (
            <Card className="col-span-full">
              <CardContent className="py-8 text-center">
                <Cpu className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                <p className="text-muted-foreground">No AI models available</p>
              </CardContent>
            </Card>
          ) : (
            models.map((model) => (
              <Card key={model.id}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    {model.name}
                    <span
                      className={`text-xs ${model.loaded ? 'text-green-500' : 'text-gray-400'}`}
                    >
                      {model.loaded ? 'Loaded' : 'Not Loaded'}
                    </span>
                  </CardTitle>
                  <CardDescription>{model.model_type}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">
                      Size: {formatFileSize(model.size)}
                    </p>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm" disabled={model.loaded}>
                        Load
                      </Button>
                      <Button variant="outline" size="sm" disabled={!model.loaded}>
                        Unload
                      </Button>
                    </div>
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
