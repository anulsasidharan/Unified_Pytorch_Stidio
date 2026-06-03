import { useCallback, useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, Bookmark, Lightbulb, Play, Send } from 'lucide-react';
import { toast, Toaster } from 'sonner';
import type { CodeLanguage } from '@dsa-studio/shared';
import { ChatPanel } from '@/components/chat/ChatPanel';
import { AuthDialog } from '@/components/auth/AuthDialog';
import { CodeEditor } from '@/components/editor/CodeEditor';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog } from '@/components/ui/dialog';
import { Select } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { apiClient, type QuestionDetailDto, type RunResultDto, type SolutionDto } from '@/lib/api-client';
import { difficultyVariant } from '@/lib/difficulty';
import { useAuthStore } from '@/store/authStore';

export function PracticePage() {
  const { questionSlug } = useParams<{ questionSlug: string }>();
  const token = useAuthStore((s) => s.token);
  const user = useAuthStore((s) => s.user);

  const [question, setQuestion] = useState<QuestionDetailDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState('description');
  const [language, setLanguage] = useState<CodeLanguage>('python');
  const [code, setCode] = useState('');
  const [runResult, setRunResult] = useState<RunResultDto | null>(null);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [authOpen, setAuthOpen] = useState(false);
  const [hintsOpen, setHintsOpen] = useState(false);
  const [hints, setHints] = useState<string[]>([]);
  const [hintTier, setHintTier] = useState(0);
  const [solutions, setSolutions] = useState<SolutionDto[]>([]);
  const [solutionsLoading, setSolutionsLoading] = useState(false);

  const loadStarter = useCallback(
    async (qId: string, lang: CodeLanguage) => {
      const starter = await apiClient.getStarterCode(qId, lang);
      setCode(starter.code);
    },
    [],
  );

  useEffect(() => {
    if (!questionSlug) return;
    let cancelled = false;
    (async () => {
      try {
        const { question: q } = await apiClient.getQuestionBySlug(questionSlug);
        if (cancelled) return;
        setQuestion(q);
        await loadStarter(q.id, 'python');
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Failed to load question');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [questionSlug, loadStarter]);

  useEffect(() => {
    if (!question) return;
    loadStarter(question.id, language).catch(() => {});
  }, [language, question, loadStarter]);

  async function requireAuth(): Promise<boolean> {
    if (token) return true;
    setAuthOpen(true);
    return false;
  }

  async function handleRun() {
    if (!question || !(await requireAuth())) return;
    setRunning(true);
    setRunResult(null);
    try {
      const result = await apiClient.runCode({
        questionId: question.id,
        language,
        code,
      });
      setRunResult(result);
      if (result.status === 'accepted') {
        toast.success('All sample tests passed!');
      } else {
        toast.error(`Sample tests: ${result.testCasesPassed}/${result.totalTestCases} passed`);
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Run failed');
    } finally {
      setRunning(false);
    }
  }

  async function handleSubmit() {
    if (!question || !(await requireAuth())) return;
    setSubmitting(true);
    try {
      const result = await apiClient.submitCode({
        questionId: question.id,
        language,
        code,
      });
      if (result.status === 'accepted') {
        toast.success('Accepted! Progress updated.');
        setQuestion((q) => (q ? { ...q, progressStatus: 'solved' } : q));
      } else {
        toast.error(`Result: ${result.status} (${result.testCasesPassed}/${result.totalTestCases})`);
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Submit failed');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleShowHint() {
    if (!question || !(await requireAuth())) return;
    const nextTier = Math.min(hintTier + 1, 10);
    try {
      const data = await apiClient.getHints(question.id, nextTier);
      setHints(data.hints);
      setHintTier(nextTier);
      setHintsOpen(true);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load hints');
    }
  }

  async function loadSolutions() {
    if (!question || !token) {
      setAuthOpen(true);
      return;
    }
    setSolutionsLoading(true);
    try {
      const data = await apiClient.getSolutions(question.id);
      setSolutions(data.items);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Solutions unavailable');
    } finally {
      setSolutionsLoading(false);
    }
  }

  useEffect(() => {
    if (tab === 'solutions' && solutions.length === 0 && !solutionsLoading) {
      loadSolutions();
    }
  }, [tab]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  if (error || !question) {
    return <p className="text-destructive">{error ?? 'Question not found'}</p>;
  }

  return (
    <div className="space-y-4">
      <Toaster richColors position="top-right" />
      <AuthDialog open={authOpen} onOpenChange={setAuthOpen} />

      <div className="flex flex-wrap items-center gap-3">
        <Button variant="ghost" size="sm" asChild>
          <Link to={question.topicSlug ? `/learn/${question.topicSlug}` : '/learn'}>
            <ArrowLeft className="mr-1 h-4 w-4" />
            Back
          </Link>
        </Button>
        <h1 className="flex-1 text-xl font-bold sm:text-2xl">{question.title}</h1>
        <Badge variant={difficultyVariant(question.difficulty)}>{question.difficulty}</Badge>
        {question.tags.slice(0, 3).map((tag) => (
          <Badge key={tag} variant="outline">
            {tag}
          </Badge>
        ))}
        <Button variant="ghost" size="icon" aria-label="Bookmark">
          <Bookmark className="h-4 w-4" />
        </Button>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="space-y-4">
          <Tabs value={tab} onValueChange={setTab}>
            <TabsList>
              <TabsTrigger value="description">Description</TabsTrigger>
              <TabsTrigger value="solutions">Solutions</TabsTrigger>
              <TabsTrigger value="submissions">Submissions</TabsTrigger>
            </TabsList>

            <TabsContent value="description">
              <Card>
                <CardContent className="prose prose-sm max-w-none space-y-4 pt-6 dark:prose-invert">
                  <div className="whitespace-pre-wrap">{question.description}</div>
                  {question.constraints && (
                    <div>
                      <h3 className="font-semibold">Constraints</h3>
                      <p className="whitespace-pre-wrap text-muted-foreground">{question.constraints}</p>
                    </div>
                  )}
                  {question.testCases.length > 0 && (
                    <div>
                      <h3 className="font-semibold">Examples</h3>
                      {question.testCases.map((tc, i) => (
                        <div key={tc.id} className="mt-2 rounded-md bg-muted p-3 text-sm">
                          <p>
                            <strong>Example {i + 1}</strong>
                          </p>
                          <pre className="mt-1 overflow-x-auto">Input: {tc.input}</pre>
                          <pre className="overflow-x-auto">Output: {tc.expectedOutput}</pre>
                          {tc.explanation && (
                            <p className="mt-1 text-muted-foreground">{tc.explanation}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="solutions">
              <Card>
                <CardContent className="space-y-4 pt-6">
                  {solutionsLoading && <p className="text-sm text-muted-foreground">Loading…</p>}
                  {!solutionsLoading && solutions.length === 0 && (
                    <p className="text-sm text-muted-foreground">
                      Attempt this question first to unlock solutions, or click Solutions again after
                      signing in.
                    </p>
                  )}
                  {solutions.map((sol) => (
                    <div key={sol.id} className="rounded-md border p-4">
                      <div className="mb-2 flex items-center gap-2">
                        <Badge>{sol.language}</Badge>
                        <span className="font-medium">{sol.approach}</span>
                        {sol.isOptimal && <Badge variant="basic">Optimal</Badge>}
                      </div>
                      <p className="mb-2 text-xs text-muted-foreground">
                        {sol.timeComplexity} time · {sol.spaceComplexity} space
                      </p>
                      {sol.explanation && (
                        <p className="mb-2 text-sm text-muted-foreground">{sol.explanation}</p>
                      )}
                      <pre className="overflow-x-auto rounded bg-muted p-3 text-xs">{sol.code}</pre>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="submissions">
              <Card>
                <CardContent className="py-8 text-center text-sm text-muted-foreground">
                  Submission history will appear here after you submit solutions.
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          <div className="flex flex-wrap gap-2">
            <Select
              value={language}
              onChange={(e) => setLanguage(e.target.value as CodeLanguage)}
              className="w-36"
              aria-label="Programming language"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="typescript">TypeScript</option>
            </Select>
            <Button variant="outline" onClick={handleShowHint}>
              <Lightbulb className="mr-1 h-4 w-4" />
              Hints ({hintTier}/{question.hints.length || '?'})
            </Button>
            <Button variant="outline" onClick={handleRun} disabled={running}>
              <Play className="mr-1 h-4 w-4" />
              {running ? 'Running…' : 'Run'}
            </Button>
            <Button onClick={handleSubmit} disabled={submitting}>
              <Send className="mr-1 h-4 w-4" />
              {submitting ? 'Submitting…' : 'Submit'}
            </Button>
          </div>

          {!token && (
            <p className="text-sm text-muted-foreground">
              <button type="button" className="text-primary underline" onClick={() => setAuthOpen(true)}>
                Sign in
              </button>{' '}
              to run code, submit, and view hints.
            </p>
          )}
          {user && (
            <p className="text-xs text-muted-foreground">
              Signed in as {user.username} · Status: {question.progressStatus ?? 'not_attempted'}
            </p>
          )}
        </div>

        <div className="space-y-4">
          <CodeEditor language={language} value={code} onChange={setCode} height="480px" />

          <Card aria-live="polite">
            <CardHeader className="py-3">
              <CardTitle className="text-sm font-medium">Test results (sample)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 pb-4 text-sm">
              {!runResult && (
                <p className="text-muted-foreground">Run your code against sample test cases.</p>
              )}
              {runResult?.results.map((r, i) => (
                <div
                  key={r.testCaseId ?? i}
                  className={`rounded-md border p-2 ${r.passed ? 'border-emerald-200 bg-emerald-50 dark:border-emerald-900 dark:bg-emerald-950/30' : 'border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/30'}`}
                >
                  <p className="font-medium">
                    Test {i + 1}: {r.passed ? 'Passed' : 'Failed'}
                    {r.executionTimeMs != null && ` (${r.executionTimeMs}ms)`}
                  </p>
                  {!r.passed && r.expectedOutput != null && (
                    <>
                      <p className="mt-1 text-xs">Expected: {r.expectedOutput}</p>
                      <p className="text-xs">Got: {r.actualOutput ?? '(empty)'}</p>
                      {r.error && <p className="text-xs text-destructive">{r.error}</p>}
                    </>
                  )}
                </div>
              ))}
              {runResult && (
                <p className="text-xs text-muted-foreground">
                  Total: {runResult.executionTimeMs}ms · {runResult.testCasesPassed}/
                  {runResult.totalTestCases} passed
                </p>
              )}
            </CardContent>
          </Card>

          {token && (
            <ChatPanel
              questionId={question.id}
              code={code}
              language={language}
              compact
            />
          )}
        </div>
      </div>

      <Dialog open={hintsOpen} onOpenChange={setHintsOpen} title="Progressive hints">
        <ol className="list-decimal space-y-2 pl-5 text-sm">
          {hints.map((h) => (
            <li key={h}>{h}</li>
          ))}
        </ol>
        {hintTier < (question.hints.length || 0) && (
          <Button className="mt-4" variant="outline" onClick={handleShowHint}>
            Reveal next hint
          </Button>
        )}
      </Dialog>
    </div>
  );
}
