import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { TopicDto } from '@/lib/api-client';
import { TopicDiagram, type TopicDiagramId } from '@/components/theory/diagrams/TopicDiagrams';

export function TopicTheoryPanel({ topic }: { topic: TopicDto }) {
  const theory = topic.theory;
  if (!theory) {
    return (
      <Card>
        <CardContent className="py-8 text-muted-foreground">
          {topic.description ?? 'Theory content is not available for this topic yet.'}
        </CardContent>
      </Card>
    );
  }

  const diagramId = (theory.diagramId ?? 'two-pointers') as TopicDiagramId;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>What is {topic.name}?</CardTitle>
        </CardHeader>
        <CardContent className="prose prose-sm max-w-none space-y-3 dark:prose-invert">
          {theory.overview.map((paragraph) => (
            <p key={paragraph.slice(0, 40)}>{paragraph}</p>
          ))}
        </CardContent>
      </Card>

      <TopicDiagram diagramId={diagramId} caption={theory.diagramCaption ?? ''} />

      {theory.keyConcepts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Key concepts</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc space-y-1.5 pl-5 text-sm">
              {theory.keyConcepts.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {theory.whenToUse.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">When to use this pattern</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc space-y-1.5 pl-5 text-sm">
              {theory.whenToUse.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {theory.commonPatterns.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Common problem patterns</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="grid gap-2 sm:grid-cols-2">
              {theory.commonPatterns.map((item) => (
                <li
                  key={item}
                  className="rounded-md border bg-muted/40 px-3 py-2 text-sm font-medium"
                >
                  {item}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {theory.complexityNotes && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Complexity notes</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">{theory.complexityNotes}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
