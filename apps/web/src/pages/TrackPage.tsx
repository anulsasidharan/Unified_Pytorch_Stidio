import { useEffect, useMemo, useState } from 'react';
import {
  Bar,
  BarChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Award, Calendar, Flame, Target, TrendingUp, Trophy } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { apiClient } from '@/lib/api-client';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/store/authStore';
import type { AnalyticsResponse, DailyActivity, ProgressOverviewResponse } from '@dsa-studio/shared';

const HEATMAP_COLORS = [
  'bg-muted',
  'bg-emerald-200 dark:bg-emerald-900',
  'bg-emerald-400 dark:bg-emerald-700',
  'bg-emerald-500 dark:bg-emerald-600',
  'bg-emerald-600 dark:bg-emerald-500',
];

const PIE_COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899'];

export function TrackPage() {
  const token = useAuthStore((s) => s.token);
  const user = useAuthStore((s) => s.user);
  const setAuth = useAuthStore((s) => s.setAuth);
  const [progress, setProgress] = useState<ProgressOverviewResponse | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [activities, setActivities] = useState<DailyActivity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dailyTarget, setDailyTarget] = useState(user?.dailyTarget ?? 3);
  const [savingGoal, setSavingGoal] = useState(false);
  const [calendarMonth, setCalendarMonth] = useState(() => new Date());
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    setDailyTarget(user?.dailyTarget ?? 3);

    Promise.all([
      apiClient.getProgress(),
      apiClient.getAnalytics(30),
      apiClient.getDailyActivity({ limit: 90 }),
    ])
      .then(([prog, anal, daily]) => {
        setProgress(prog);
        setAnalytics(anal);
        setActivities(daily.items);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token, user?.dailyTarget]);

  const activityMap = useMemo(
    () => new Map(activities.map((a) => [a.activityDate, a])),
    [activities],
  );

  async function saveDailyGoal() {
    if (!token) return;
    setSavingGoal(true);
    try {
      const { user: updated } = await apiClient.updateProfile({ dailyTarget });
      if (token) setAuth(token, updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update goal');
    } finally {
      setSavingGoal(false);
    }
  }

  if (!token) {
    return (
      <div className="rounded-lg border bg-card p-8 text-center">
        <h1 className="text-2xl font-bold">Progress Tracker</h1>
        <p className="mt-2 text-muted-foreground">Sign in to view your analytics, streaks, and goals.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid gap-4 sm:grid-cols-3">
          <Skeleton className="h-28" />
          <Skeleton className="h-28" />
          <Skeleton className="h-28" />
        </div>
        <Skeleton className="h-80" />
      </div>
    );
  }

  if (error || !progress || !analytics) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/5 p-6">
        <p className="text-destructive">{error ?? 'Failed to load progress data'}</p>
      </div>
    );
  }

  const { overall, streak } = progress;
  const allBadges = analytics.badges ?? [];

  return (
    <div className="space-y-8">
      <section className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Your Progress</h1>
        <p className="text-muted-foreground">
          Track daily activity, streaks, topic mastery, and achievements.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={Flame}
          label="Current streak"
          value={`${streak.currentStreak} days`}
          hint={`Longest: ${streak.longestStreak} days`}
        />
        <StatCard
          icon={Trophy}
          label="Questions solved"
          value={String(overall.totalSolved)}
          hint={`${overall.overallPercentage}% of ${overall.totalQuestions}`}
        />
        <StatCard
          icon={Target}
          label="Today's goal"
          value={`${streak.todaySolved} / ${streak.dailyTarget}`}
          hint={streak.todayGoalMet ? 'Goal met!' : 'Keep going'}
          highlight={streak.todayGoalMet}
        />
        <StatCard
          icon={TrendingUp}
          label="Topics mastered"
          value={`${overall.topicsMastered} / ${overall.totalTopics}`}
          hint={`${streak.totalActiveDays} active days`}
        />
      </section>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="topics">Topics</TabsTrigger>
          <TabsTrigger value="streaks">Streaks & Goals</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Daily summary</CardTitle>
                <CardDescription>
                  {new Date().toLocaleDateString(undefined, {
                    weekday: 'long',
                    month: 'long',
                    day: 'numeric',
                  })}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <SummaryRow
                  label="Questions solved"
                  value={`${streak.todaySolved} / ${streak.dailyTarget}`}
                  badge={streak.todayGoalMet ? 'Goal met!' : undefined}
                />
                <SummaryRow
                  label="Time spent"
                  value={formatMinutes(
                    activityMap.get(new Date().toISOString().slice(0, 10))?.timeSpentMinutes ?? 0,
                  )}
                />
                <SummaryRow
                  label="Topics today"
                  value={
                    activityMap.get(new Date().toISOString().slice(0, 10))?.topicsCovered.join(', ') ||
                    'None yet'
                  }
                />
                <SummaryRow label="Current streak" value={`${streak.currentStreak} days`} />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Overall progress</CardTitle>
                <CardDescription>
                  {overall.totalSolved} of {overall.totalQuestions} questions
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ProgressBar percentage={overall.overallPercentage} />
                <div className="space-y-2">
                  {overall.byDifficulty.map((d) => (
                    <div key={d.difficulty} className="space-y-1">
                      <div className="flex justify-between text-xs capitalize">
                        <span>{d.difficulty}</span>
                        <span>
                          {d.solved}/{d.total} ({d.percentage}%)
                        </span>
                      </div>
                      <ProgressBar percentage={d.percentage} size="sm" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>30-day activity heatmap</CardTitle>
              <CardDescription>
                Peak: {analytics.summary.peakDay?.questionsSolved ?? 0} questions on{' '}
                {analytics.summary.peakDay?.date ?? '—'} · Avg: {analytics.summary.averagePerDay}/day
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ActivityHeatmap heatmap={analytics.heatmap} />
            </CardContent>
          </Card>

          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Weekly activity</CardTitle>
                <CardDescription>Questions solved per day (last 7 days)</CardDescription>
              </CardHeader>
              <CardContent className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={analytics.weeklyBar}>
                    <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                    <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="solved" fill="#10b981" radius={[4, 4, 0, 0]} name="Solved" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Topic distribution</CardTitle>
                <CardDescription>Solved questions by topic</CardDescription>
              </CardHeader>
              <CardContent className="h-64">
                {analytics.topicPie.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={analytics.topicPie}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        label={({ name, percent }) =>
                          `${name} ${((percent ?? 0) * 100).toFixed(0)}%`
                        }
                      >
                        {analytics.topicPie.map((_, index) => (
                          <Cell key={index} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="flex h-full items-center justify-center text-sm text-muted-foreground">
                    Solve questions to see topic breakdown
                  </p>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="topics" className="space-y-4">
          {overall.topicBreakdown.length === 0 ? (
            <Card>
              <CardContent className="py-8 text-center text-muted-foreground">
                No topic progress yet. Start practicing to track mastery.
              </CardContent>
            </Card>
          ) : (
            overall.topicBreakdown
              .sort((a, b) => b.percentage - a.percentage)
              .map((topic) => (
                <Card key={topic.topicId}>
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between gap-2">
                      <CardTitle className="text-base">{topic.name}</CardTitle>
                      <span className="text-sm text-muted-foreground">
                        {topic.solved}/{topic.total}
                      </span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <ProgressBar percentage={topic.percentage} />
                  </CardContent>
                </Card>
              ))
          )}
        </TabsContent>

        <TabsContent value="streaks" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  Activity calendar
                </CardTitle>
                <CardDescription>Color intensity reflects questions solved</CardDescription>
              </CardHeader>
              <CardContent>
                <ActivityCalendar
                  month={calendarMonth}
                  activityMap={activityMap}
                  onPrev={() =>
                    setCalendarMonth(
                      (m) => new Date(m.getFullYear(), m.getMonth() - 1, 1),
                    )
                  }
                  onNext={() =>
                    setCalendarMonth(
                      (m) => new Date(m.getFullYear(), m.getMonth() + 1, 1),
                    )
                  }
                />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  Daily goal
                </CardTitle>
                <CardDescription>Set how many questions you want to solve each day</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3">
                  <Input
                    type="number"
                    min={1}
                    max={50}
                    value={dailyTarget}
                    onChange={(e) => setDailyTarget(Number(e.target.value))}
                    className="w-24"
                  />
                  <span className="text-sm text-muted-foreground">questions / day</span>
                </div>
                <Button onClick={saveDailyGoal} disabled={savingGoal}>
                  {savingGoal ? 'Saving…' : 'Save goal'}
                </Button>
                <p className="text-xs text-muted-foreground">
                  Streaks count consecutive days when you meet this goal.
                </p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5" />
                Achievements
              </CardTitle>
              <CardDescription>
                {allBadges.filter((b) => b.earned).length} of {allBadges.length} badges earned
              </CardDescription>
            </CardHeader>
            <CardContent>
              <BadgeGrid badges={allBadges} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Streak stats</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 sm:grid-cols-3">
              <div>
                <p className="text-2xl font-bold">{streak.currentStreak}</p>
                <p className="text-sm text-muted-foreground">Current streak</p>
              </div>
              <div>
                <p className="text-2xl font-bold">{streak.longestStreak}</p>
                <p className="text-sm text-muted-foreground">Longest streak</p>
              </div>
              <div>
                <p className="text-2xl font-bold">{streak.totalActiveDays}</p>
                <p className="text-sm text-muted-foreground">Total active days</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
  hint,
  highlight,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: string;
  hint: string;
  highlight?: boolean;
}) {
  return (
    <article
      className={cn(
        'rounded-lg border bg-card p-4 shadow-sm',
        highlight && 'border-emerald-500/50',
      )}
    >
      <div className="mb-3 flex items-center gap-2 text-muted-foreground">
        <Icon className="h-4 w-4" />
        <span className="text-sm font-medium">{label}</span>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      <p className="mt-1 text-xs text-muted-foreground">{hint}</p>
    </article>
  );
}

function SummaryRow({
  label,
  value,
  badge,
}: {
  label: string;
  value: string;
  badge?: string;
}) {
  return (
    <div className="flex items-center justify-between gap-2">
      <span className="text-muted-foreground">{label}</span>
      <span className="flex items-center gap-2 font-medium">
        {value}
        {badge && (
          <Badge variant="secondary" className="bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-100">
            {badge}
          </Badge>
        )}
      </span>
    </div>
  );
}

function ProgressBar({ percentage, size = 'md' }: { percentage: number; size?: 'sm' | 'md' }) {
  return (
    <div
      className={cn('w-full overflow-hidden rounded-full bg-muted', size === 'sm' ? 'h-1.5' : 'h-2.5')}
    >
      <div
        className="h-full rounded-full bg-emerald-500 transition-all"
        style={{ width: `${Math.min(100, percentage)}%` }}
      />
    </div>
  );
}

function ActivityHeatmap({
  heatmap,
}: {
  heatmap: AnalyticsResponse['heatmap'];
}) {
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-1">
        {heatmap.map((day) => (
          <div
            key={day.date}
            title={`${day.date}: ${day.questionsSolved} solved`}
            className={cn('h-3 w-3 rounded-sm', HEATMAP_COLORS[day.level])}
          />
        ))}
      </div>
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        <span>Less</span>
        {HEATMAP_COLORS.map((color, i) => (
          <div key={i} className={cn('h-3 w-3 rounded-sm', color)} />
        ))}
        <span>More</span>
      </div>
    </div>
  );
}

function ActivityCalendar({
  month,
  activityMap,
  onPrev,
  onNext,
}: {
  month: Date;
  activityMap: Map<string, DailyActivity>;
  onPrev: () => void;
  onNext: () => void;
}) {
  const year = month.getFullYear();
  const monthIndex = month.getMonth();
  const firstDay = new Date(year, monthIndex, 1).getDay();
  const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();
  const monthLabel = month.toLocaleDateString(undefined, { month: 'long', year: 'numeric' });

  const cells: Array<{ day: number | null; dateKey?: string; level?: number; goalMet?: boolean }> =
    [];
  for (let i = 0; i < firstDay; i++) cells.push({ day: null });
  for (let day = 1; day <= daysInMonth; day++) {
    const dateKey = `${year}-${String(monthIndex + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const activity = activityMap.get(dateKey);
    cells.push({
      day,
      dateKey,
      level: activity ? Math.min(4, activity.questionsSolved) : 0,
      goalMet: activity?.dailyGoalMet,
    });
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Button variant="outline" size="sm" onClick={onPrev}>
          Prev
        </Button>
        <span className="font-medium">{monthLabel}</span>
        <Button variant="outline" size="sm" onClick={onNext}>
          Next
        </Button>
      </div>
      <div className="grid grid-cols-7 gap-1 text-center text-xs text-muted-foreground">
        {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map((d) => (
          <div key={d} className="py-1 font-medium">
            {d}
          </div>
        ))}
        {cells.map((cell, i) =>
          cell.day === null ? (
            <div key={`empty-${i}`} />
          ) : (
            <div
              key={cell.dateKey}
              title={cell.dateKey}
              className={cn(
                'relative flex aspect-square items-center justify-center rounded-md text-xs',
                HEATMAP_COLORS[cell.level ?? 0],
                cell.goalMet && 'ring-2 ring-emerald-500 ring-offset-1',
              )}
            >
              {cell.day}
            </div>
          ),
        )}
      </div>
    </div>
  );
}

function BadgeGrid({ badges }: { badges: AnalyticsResponse['badges'] }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {badges.map((badge) => (
        <div
          key={badge.id}
          className={cn(
            'flex items-start gap-3 rounded-lg border p-3',
            badge.earned ? 'bg-card' : 'opacity-50 grayscale',
          )}
        >
          <span className="text-2xl" aria-hidden>
            {badge.icon}
          </span>
          <div>
            <p className="font-medium">{badge.name}</p>
            <p className="text-xs text-muted-foreground">{badge.description}</p>
            {badge.earned && badge.earnedAt && (
              <p className="mt-1 text-xs text-muted-foreground">
                Earned {new Date(badge.earnedAt).toLocaleDateString()}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

function formatMinutes(minutes: number): string {
  if (minutes < 60) return `${minutes}m`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}
