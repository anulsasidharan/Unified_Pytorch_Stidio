import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BookMarked, CheckCircle2, Clock, RefreshCw } from 'lucide-react';
import { toast } from 'sonner';
import { AuthDialog } from '@/components/auth/AuthDialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient } from '@/lib/api-client';
import { DIFFICULTY_LABELS, difficultyVariant } from '@/lib/difficulty';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/store/authStore';
import type { RevisionQueueItemDto, RevisionStatsDto } from '@dsa-studio/shared';

function priorityLabel(priority: number) {
  if (priority >= 5) return { label: 'High', className: 'bg-red-500/15 text-red-700 dark:text-red-400' };
  if (priority >= 3) return { label: 'Medium', className: 'bg-amber-500/15 text-amber-700 dark:text-amber-400' };
  return { label: 'Low', className: 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-400' };
}

export function RevisionPage() {
  const token = useAuthStore((s) => s.token);
  const [authOpen, setAuthOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<RevisionQueueItemDto[]>([]);
  const [stats, setStats] = useState<RevisionStatsDto | null>(null);
  const [completingId, setCompletingId] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    try {
      const data = await apiClient.getRevisionDue();
      setItems(data.items);
      setStats(data.stats);
    } catch {
      toast.error('Failed to load revision queue');
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    load();
  }, [token, load]);

  const handleComplete = async (id: string) => {
    setCompletingId(id);
    try {
      await apiClient.completeRevision(id);
      toast.success('Revision marked complete');
      await load();
    } catch {
      toast.error('Could not complete revision');
    } finally {
      setCompletingId(null);
    }
  };

  if (!token) {
    return (
      <div className="space-y-6">
        <AuthDialog open={authOpen} onOpenChange={setAuthOpen} />
        <h1 className="text-3xl font-bold tracking-tight">Revision</h1>
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-12">
            <BookMarked className="h-12 w-12 text-muted-foreground" />
            <p className="text-muted-foreground">Sign in to view your spaced repetition queue.</p>
            <Button onClick={() => setAuthOpen(true)}>Sign in</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const grouped = {
    high: items.filter((i) => i.priority >= 5),
    medium: items.filter((i) => i.priority >= 3 && i.priority < 5),
    low: items.filter((i) => i.priority < 3),
  };

  return (
    <div className="space-y-8">
      <section className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Revision</h1>
        <p className="max-w-2xl text-muted-foreground">
          Spaced repetition reviews scheduled at 1, 3, 7, 14, and 30 day intervals after you solve a
          question.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-3">
        {loading ? (
          <>
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
          </>
        ) : (
          <>
            <StatCard icon={Clock} label="Due today" value={String(stats?.dueToday ?? items.length)} />
            <StatCard icon={RefreshCw} label="Upcoming this week" value={String(stats?.upcomingWeek ?? 0)} />
            <StatCard icon={CheckCircle2} label="Reviewed this week" value={String(stats?.reviewedThisWeek ?? 0)} />
          </>
        )}
      </section>

      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Due for revision</h2>
          <Button variant="outline" size="sm" onClick={load} disabled={loading}>
            <RefreshCw className={cn('mr-2 h-4 w-4', loading && 'animate-spin')} />
            Refresh
          </Button>
        </div>

        {loading ? (
          <div className="space-y-3">
            <Skeleton className="h-20" />
            <Skeleton className="h-20" />
          </div>
        ) : items.length === 0 ? (
          <Card>
            <CardContent className="py-10 text-center text-muted-foreground">
              No questions due today. Solve problems to build your revision queue.
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {(['high', 'medium', 'low'] as const).map((tier) => {
              const list = grouped[tier];
              if (list.length === 0) return null;
              return (
                <div key={tier} className="space-y-3">
                  <h3 className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
                    {tier === 'high' ? 'High priority' : tier === 'medium' ? 'Medium priority' : 'Low priority'}
                  </h3>
                  {list.map((item) => (
                    <RevisionRow
                      key={item.id}
                      item={item}
                      completing={completingId === item.id}
                      onComplete={() => handleComplete(item.id)}
                    />
                  ))}
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: string;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{label}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
      </CardContent>
    </Card>
  );
}

function RevisionRow({
  item,
  completing,
  onComplete,
}: {
  item: RevisionQueueItemDto;
  completing: boolean;
  onComplete: () => void;
}) {
  const prio = priorityLabel(item.priority);

  return (
    <Card>
      <CardHeader className="flex flex-row items-start justify-between gap-4 space-y-0 pb-2">
        <div className="space-y-1">
          <CardTitle className="text-base">
            <Link
              to={`/practice/${item.question.slug}`}
              className="hover:text-primary hover:underline"
            >
              {item.question.title}
            </Link>
          </CardTitle>
          <CardDescription>
            {item.question.topicName ?? 'Topic'} · Scheduled {item.scheduledDate}
          </CardDescription>
        </div>
        <div className="flex shrink-0 flex-wrap items-center gap-2">
          <span className={cn('rounded-full px-2 py-0.5 text-xs font-medium', prio.className)}>
            {prio.label} ({item.priority})
          </span>
          <Badge variant={difficultyVariant(item.question.difficulty)}>
            {DIFFICULTY_LABELS[item.question.difficulty as keyof typeof DIFFICULTY_LABELS] ??
              item.question.difficulty}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="flex flex-wrap items-center gap-2 pt-0">
        <Button size="sm" asChild>
          <Link to={`/practice/${item.question.slug}`}>Practice</Link>
        </Button>
        <Button size="sm" variant="secondary" onClick={onComplete} disabled={completing}>
          <CheckCircle2 className="mr-2 h-4 w-4" />
          {completing ? 'Saving…' : 'Mark reviewed'}
        </Button>
      </CardContent>
    </Card>
  );
}
