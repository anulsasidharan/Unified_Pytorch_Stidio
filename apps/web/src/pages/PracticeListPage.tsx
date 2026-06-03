import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient, type QuestionSummaryDto } from '@/lib/api-client';
import { difficultyVariant } from '@/lib/difficulty';

export function PracticeListPage() {
  const [questions, setQuestions] = useState<QuestionSummaryDto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await apiClient.getTopics({ limit: 1 });
        const firstTopic = data.items[0];
        if (!firstTopic) {
          setQuestions([]);
          return;
        }
        const q = await apiClient.getTopicQuestions(firstTopic.id);
        if (!cancelled) setQuestions(q.items);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Failed to load');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Practice</h1>
        <p className="mt-1 text-muted-foreground">
          Jump into coding problems. Browse all topics from the{' '}
          <Link to="/learn" className="text-primary underline">
            Learn
          </Link>{' '}
          page.
        </p>
      </div>

      {loading && <Skeleton className="h-48 w-full" />}
      {error && <p className="text-destructive">{error}</p>}

      {!loading && !error && (
        <ul className="space-y-2">
          {questions.map((q) => (
            <li key={q.id}>
              <Link
                to={`/practice/${q.slug}`}
                className="flex items-center gap-3 rounded-lg border px-4 py-3 hover:bg-accent"
              >
                <span className="flex-1 font-medium">{q.title}</span>
                <Badge variant={difficultyVariant(q.difficulty)}>{q.difficulty}</Badge>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
