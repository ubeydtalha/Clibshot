import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui';
import { Code } from 'lucide-react';

export function DevPanel() {
  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Developer Panel</h1>
        <p className="text-muted-foreground">Development tools and debugging</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Code className="h-5 w-5" />
            API Explorer
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Developer tools will be available here. This includes API testing, event monitoring, and
            performance metrics.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
