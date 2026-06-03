import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { TopicTheoryPanel } from '@/components/theory/TopicTheoryPanel';
import { apiClient, type QuestionSummaryDto, type TopicDto } from '@/lib/api-client';
import { DIFFICULTY_LABELS, difficultyVariant, progressIcon } from '@/lib/difficulty';
import type { Difficulty } from '@dsa-studio/shared';

const DIFFICULTY_ORDER: Difficulty[] = ['basic', 'intermediate', 'advanced'];

export function TopicDetailPage() {
  const { topicSlug } = useParams<{ topicSlug: string }>();
  const [tab, setTab] = useState('theory');
  const [topic, setTopic] = useState<TopicDto | null>(null);
  const [questions, setQuestions] = useState<QuestionSummaryDto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!topicSlug) return;
    let cancelled = false;
    (async () => {
      try {
        const topicRes = await apiClient.getTopicBySlug(topicSlug);
        const qRes = await apiClient.getTopicQuestions(topicRes.topic.id);
        if (!cancelled) {
          setTopic(topicRes.topic);
          setQuestions(qRes.items);
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Failed to load topic');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [topicSlug]);

  const grouped = useMemo(() => {
    const map = new Map<Difficulty, QuestionSummaryDto[]>();
    for (const d of DIFFICULTY_ORDER) map.set(d, []);
    for (const q of questions) {
      const key = q.difficulty as Difficulty;
      if (map.has(key)) map.get(key)!.push(q);
    }
    return map;
  }, [questions]);

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (error || !topic) {
    return <p className="text-destructive">{error ?? 'Topic not found'}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="sm" asChild>
          <Link to="/learn">
            <ArrowLeft className="mr-1 h-4 w-4" />
            Back
          </Link>
        </Button>
        <span className="text-2xl" aria-hidden>
          {topic.icon ?? '📚'}
        </span>
        <div>
          <h1 className="text-2xl font-bold">{topic.name}</h1>
          <p className="text-sm text-muted-foreground">{topic.category}</p>
        </div>
        <Badge variant={difficultyVariant(topic.difficulty)} className="ml-auto">
          {topic.difficulty}
        </Badge>
      </div>

      <Tabs value={tab} onValueChange={setTab}>
        <TabsList>
          <TabsTrigger value="theory">Theory</TabsTrigger>
          <TabsTrigger value="practice">Practice Questions</TabsTrigger>
          <TabsTrigger value="notes">Notes</TabsTrigger>
        </TabsList>

        <TabsContent value="theory">
          <TopicTheoryPanel topic={topic} />
        </TabsContent>

        <TabsContent value="practice">
          <div className="space-y-6">
            {DIFFICULTY_ORDER.map((diff) => {
              const items = grouped.get(diff) ?? [];
              if (items.length === 0) return null;
              return (
                <section key={diff}>
                  <h2 className="mb-3 text-lg font-semibold">{DIFFICULTY_LABELS[diff]}</h2>
                  <ul className="space-y-2">
                    {items.map((q) => (
                      <li key={q.id}>
                        <Link
                          to={`/practice/${q.slug}`}
                          className="flex items-center gap-3 rounded-lg border bg-card px-4 py-3 transition-colors hover:bg-accent"
                        >
                          <span aria-hidden>{progressIcon(q.progressStatus)}</span>
                          <span className="flex-1 font-medium">{q.title}</span>
                          <Badge variant={difficultyVariant(q.difficulty)}>{q.difficulty}</Badge>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </section>
              );
            })}
          </div>
        </TabsContent>

        <TabsContent value="notes">
          <Card>
            <CardContent className="py-8 text-center text-muted-foreground">
              Personal topic notes coming in a future release.
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
