import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FileJson, FileSpreadsheet, History, Link2, PenLine, Plus, Sparkles, Trash2 } from 'lucide-react';
import { toast, Toaster } from 'sonner';
import { AuthDialog } from '@/components/auth/AuthDialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { apiClient } from '@/lib/api-client';
import { difficultyVariant } from '@/lib/difficulty';
import { useAuthStore } from '@/store/authStore';
import type { Difficulty, ImportHistoryItemDto } from '@dsa-studio/shared';

const DIFFICULTIES: Difficulty[] = ['basic', 'intermediate', 'advanced'];

const DEFAULT_TOPICS = [
  'arrays-strings',
  'linked-lists',
  'stacks-queues',
  'trees',
  'graphs',
  'dynamic-programming',
  'hashing',
  'sorting-searching',
];

interface TestCaseRow {
  input: string;
  expectedOutput: string;
  isSample: boolean;
}

const emptyTestCase = (): TestCaseRow => ({
  input: '',
  expectedOutput: '',
  isSample: true,
});

export function ImportPage() {
  const token = useAuthStore((s) => s.token);
  const [authOpen, setAuthOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('manual');

  if (!token) {
    return (
      <div className="space-y-6">
        <Toaster richColors position="top-center" />
        <AuthDialog open={authOpen} onOpenChange={setAuthOpen} />
        <h1 className="text-3xl font-bold tracking-tight">Import questions</h1>
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-12">
            <PenLine className="h-12 w-12 text-muted-foreground" />
            <p className="text-muted-foreground">Sign in to add custom questions to your bank.</p>
            <Button onClick={() => setAuthOpen(true)}>Sign in</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <Toaster richColors position="top-center" />
      <section className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Import questions</h1>
        <p className="max-w-2xl text-muted-foreground">
          Add your own problems manually, via CSV/JSON bulk import, or URL-assisted entry (you
          review and fill in details — no automated scraping).
        </p>
      </section>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="flex h-auto flex-wrap gap-1">
          <TabsTrigger value="manual">
            <PenLine className="mr-2 h-4 w-4 inline" />
            Manual
          </TabsTrigger>
          <TabsTrigger value="csv">
            <FileSpreadsheet className="mr-2 h-4 w-4 inline" />
            CSV
          </TabsTrigger>
          <TabsTrigger value="json">
            <FileJson className="mr-2 h-4 w-4 inline" />
            JSON
          </TabsTrigger>
          <TabsTrigger value="url">
            <Link2 className="mr-2 h-4 w-4 inline" />
            URL
          </TabsTrigger>
          <TabsTrigger value="ai">
            <Sparkles className="mr-2 h-4 w-4 inline" />
            AI Paste
          </TabsTrigger>
          <TabsTrigger value="history">
            <History className="mr-2 h-4 w-4 inline" />
            History
          </TabsTrigger>
        </TabsList>

        <TabsContent value="manual" className="mt-6">
          <ManualImportForm />
        </TabsContent>
        <TabsContent value="csv" className="mt-6">
          <CsvImportForm />
        </TabsContent>
        <TabsContent value="json" className="mt-6">
          <JsonImportForm />
        </TabsContent>
        <TabsContent value="url" className="mt-6">
          <UrlImportForm />
        </TabsContent>
        <TabsContent value="ai" className="mt-6">
          <AiImportForm />
        </TabsContent>
        <TabsContent value="history" className="mt-6">
          <ImportHistoryPanel />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function ManualImportForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [difficulty, setDifficulty] = useState<Difficulty>('intermediate');
  const [topicSlug, setTopicSlug] = useState('arrays-strings');
  const [tags, setTags] = useState('');
  const [constraints, setConstraints] = useState('');
  const [testCases, setTestCases] = useState<TestCaseRow[]>([emptyTestCase()]);
  const [submitting, setSubmitting] = useState(false);

  const addTestCase = () => setTestCases((tc) => [...tc, { ...emptyTestCase(), isSample: false }]);
  const removeTestCase = (index: number) =>
    setTestCases((tc) => (tc.length > 1 ? tc.filter((_, i) => i !== index) : tc));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const result = await apiClient.importManual({
        title,
        description,
        difficulty,
        topicSlug,
        tags: tags
          .split(',')
          .map((t) => t.trim())
          .filter(Boolean),
        constraints: constraints || undefined,
        testCases: testCases.map((tc) => ({
          input: tc.input,
          expectedOutput: tc.expectedOutput,
          isSample: tc.isSample,
          isHidden: !tc.isSample,
        })),
      });
      toast.success(`Imported "${result.question.title}"`);
      setTitle('');
      setDescription('');
      setTestCases([emptyTestCase()]);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Import failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Manual entry</CardTitle>
        <CardDescription>Create a custom question with test cases.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Field label="Title">
            <Input value={title} onChange={(e) => setTitle(e.target.value)} required />
          </Field>
          <Field label="Description">
            <textarea
              className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </Field>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Difficulty">
              <Select value={difficulty} onChange={(e) => setDifficulty(e.target.value as Difficulty)}>
                {DIFFICULTIES.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </Select>
            </Field>
            <Field label="Topic slug">
              <Select value={topicSlug} onChange={(e) => setTopicSlug(e.target.value)}>
                {DEFAULT_TOPICS.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </Select>
            </Field>
          </div>
          <Field label="Tags (comma-separated)">
            <Input value={tags} onChange={(e) => setTags(e.target.value)} placeholder="array, hash-table" />
          </Field>
          <Field label="Constraints">
            <Input value={constraints} onChange={(e) => setConstraints(e.target.value)} />
          </Field>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Test cases</span>
              <Button type="button" variant="outline" size="sm" onClick={addTestCase}>
                <Plus className="mr-1 h-4 w-4" />
                Add
              </Button>
            </div>
            {testCases.map((tc, i) => (
              <div key={i} className="rounded-lg border p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Case {i + 1}</span>
                  <div className="flex items-center gap-2">
                    <label className="flex items-center gap-1 text-xs">
                      <input
                        type="checkbox"
                        checked={tc.isSample}
                        onChange={(e) => {
                          const next = [...testCases];
                          next[i] = { ...tc, isSample: e.target.checked };
                          setTestCases(next);
                        }}
                      />
                      Sample (visible)
                    </label>
                    <Button type="button" variant="ghost" size="sm" onClick={() => removeTestCase(i)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <Input
                  placeholder="Input"
                  value={tc.input}
                  onChange={(e) => {
                    const next = [...testCases];
                    next[i] = { ...tc, input: e.target.value };
                    setTestCases(next);
                  }}
                  required
                />
                <Input
                  placeholder="Expected output"
                  value={tc.expectedOutput}
                  onChange={(e) => {
                    const next = [...testCases];
                    next[i] = { ...tc, expectedOutput: e.target.value };
                    setTestCases(next);
                  }}
                  required
                />
              </div>
            ))}
          </div>

          <Button type="submit" disabled={submitting}>
            {submitting ? 'Saving…' : 'Create question'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

function CsvImportForm() {
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const sample = `title,description,difficulty,topic,tags,sample_input,sample_output,hints
"My Custom Two Sum","Find two indices...",basic,arrays-strings,"[array]","4\\n2 7 11 15\\n9","0 1","[Use a hash map]"`;

  const handleFile = (file: File) => {
    const reader = new FileReader();
    reader.onload = () => setContent(String(reader.result ?? ''));
    reader.readAsText(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const result = await apiClient.importCsv(content);
      toast.success(`Imported ${result.imported} question(s)`);
      setContent('');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'CSV import failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>CSV bulk import</CardTitle>
        <CardDescription>
          Required columns: title, description, difficulty, topic. Optional: tags, sample_input,
          sample_output, hints, solution_code.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Input
          type="file"
          accept=".csv,text/csv"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFile(file);
          }}
        />
        <textarea
          className="flex min-h-[200px] w-full rounded-md border border-input bg-background px-3 py-2 font-mono text-xs"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder={sample}
        />
        <Button type="button" variant="outline" size="sm" onClick={() => setContent(sample)}>
          Load sample
        </Button>
        <Button onClick={handleSubmit} disabled={submitting || !content.trim()}>
          {submitting ? 'Importing…' : 'Import CSV'}
        </Button>
      </CardContent>
    </Card>
  );
}

function JsonImportForm() {
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const sample = JSON.stringify(
    {
      questions: [
        {
          title: 'Valid Parentheses (Custom)',
          description: 'Given a string s containing parentheses, determine if valid.',
          difficulty: 'basic',
          topic: 'stacks-queues',
          tags: ['string', 'stack'],
          testCases: [{ input: '()', output: 'true', isSample: true }],
        },
      ],
    },
    null,
    2,
  );

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const parsed = JSON.parse(content) as { questions: Record<string, unknown>[] };
      const result = await apiClient.importJson(parsed);
      toast.success(`Imported ${result.imported} question(s)`);
      setContent('');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'JSON import failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>JSON bulk import</CardTitle>
        <CardDescription>Upload a file with a top-level &quot;questions&quot; array.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Input
          type="file"
          accept=".json,application/json"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = () => setContent(String(reader.result ?? ''));
            reader.readAsText(file);
          }}
        />
        <textarea
          className="flex min-h-[240px] w-full rounded-md border border-input bg-background px-3 py-2 font-mono text-xs"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <Button type="button" variant="outline" size="sm" onClick={() => setContent(sample)}>
          Load sample
        </Button>
        <Button onClick={handleSubmit} disabled={submitting || !content.trim()}>
          {submitting ? 'Importing…' : 'Import JSON'}
        </Button>
      </CardContent>
    </Card>
  );
}

function UrlImportForm() {
  const [url, setUrl] = useState('');
  const [step, setStep] = useState<'url' | 'review'>('url');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [difficulty, setDifficulty] = useState<Difficulty>('intermediate');
  const [topicSlug, setTopicSlug] = useState('arrays-strings');
  const [testCases, setTestCases] = useState<TestCaseRow[]>([emptyTestCase()]);
  const [platform, setPlatform] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handlePreview = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await apiClient.importUrlPreview(url);
      setTitle(String(data.template.title ?? data.preview.suggestedTitle));
      setDescription('');
      setDifficulty((data.template.difficulty as Difficulty) ?? 'intermediate');
      setTopicSlug(String(data.template.topicSlug ?? 'arrays-strings'));
      setPlatform(data.preview.platform);
      setStep('review');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not parse URL');
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const result = await apiClient.importUrlConfirm({
        url,
        title,
        description,
        difficulty,
        topicSlug,
        testCases: testCases.map((tc) => ({
          input: tc.input,
          expectedOutput: tc.expectedOutput,
          isSample: tc.isSample,
          isHidden: !tc.isSample,
        })),
      });
      toast.success(`Imported "${result.question.title}"`);
      setStep('url');
      setUrl('');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Import failed');
    } finally {
      setSubmitting(false);
    }
  };

  if (step === 'review') {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Review import — {platform}</CardTitle>
          <CardDescription>
            Fill in the problem details from the external source, then confirm.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleConfirm} className="space-y-4">
            <Field label="Title">
              <Input value={title} onChange={(e) => setTitle(e.target.value)} required />
            </Field>
            <Field label="Description">
              <textarea
                className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </Field>
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="Difficulty">
                <Select value={difficulty} onChange={(e) => setDifficulty(e.target.value as Difficulty)}>
                  {DIFFICULTIES.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </Select>
              </Field>
              <Field label="Topic slug">
                <Select value={topicSlug} onChange={(e) => setTopicSlug(e.target.value)}>
                  {DEFAULT_TOPICS.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </Select>
              </Field>
            </div>
            {testCases.map((tc, i) => (
              <div key={i} className="space-y-2 rounded-lg border p-3">
                <Input
                  placeholder="Input"
                  value={tc.input}
                  onChange={(e) => {
                    const next = [...testCases];
                    next[i] = { ...tc, input: e.target.value };
                    setTestCases(next);
                  }}
                  required
                />
                <Input
                  placeholder="Expected output"
                  value={tc.expectedOutput}
                  onChange={(e) => {
                    const next = [...testCases];
                    next[i] = { ...tc, expectedOutput: e.target.value };
                    setTestCases(next);
                  }}
                  required
                />
              </div>
            ))}
            <div className="flex gap-2">
              <Button type="button" variant="outline" onClick={() => setStep('url')}>
                Back
              </Button>
              <Button type="submit" disabled={submitting}>
                {submitting ? 'Saving…' : 'Confirm import'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>URL-assisted import</CardTitle>
        <CardDescription>
          Paste a LeetCode, HackerRank, or Codeforces URL. We suggest a title — you add description
          and test cases (no automated scraping).
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handlePreview} className="flex flex-col gap-4 sm:flex-row">
          <Input
            type="url"
            placeholder="https://leetcode.com/problems/two-sum/"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
          <Button type="submit" disabled={loading}>
            {loading ? 'Parsing…' : 'Continue'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

function AiImportForm() {
  const [rawText, setRawText] = useState('');
  const [classifying, setClassifying] = useState(false);
  const [classification, setClassification] = useState<
    import('@dsa-studio/shared').ImportClassifyResponse['classification'] | null
  >(null);
  const [saving, setSaving] = useState(false);

  async function handleClassify() {
    if (!rawText.trim()) {
      toast.error('Paste problem text first');
      return;
    }
    setClassifying(true);
    setClassification(null);
    try {
      const result = await apiClient.classifyImport(rawText);
      setClassification(result.classification);
      toast.success('AI classification ready — review before saving');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Classification failed');
    } finally {
      setClassifying(false);
    }
  }

  async function handleSave() {
    if (!classification) return;
    setSaving(true);
    try {
      await apiClient.importManual({
        title: classification.title,
        description: classification.description,
        difficulty: classification.difficulty,
        topicSlug: classification.topicSlug,
        tags: classification.tags,
        constraints: classification.constraints ?? undefined,
        inputFormat: classification.inputFormat ?? undefined,
        outputFormat: classification.outputFormat ?? undefined,
        hints: classification.suggestedHints,
        testCases: [{ input: 'TBD', expectedOutput: 'TBD', isSample: true }],
        source: 'custom',
        sourceName: 'AI-assisted import',
      });
      toast.success('Question saved!');
      setRawText('');
      setClassification(null);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Save failed');
    } finally {
      setSaving(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>AI-assisted import</CardTitle>
        <CardDescription>
          Paste raw problem text. AI suggests title, difficulty, topic, and tags — you review and
          confirm before saving.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Field label="Problem text">
          <textarea
            className="min-h-[200px] w-full rounded-md border bg-background px-3 py-2 text-sm"
            value={rawText}
            onChange={(e) => setRawText(e.target.value)}
            placeholder="Paste the full problem statement from any source…"
          />
        </Field>
        <Button onClick={handleClassify} disabled={classifying || !rawText.trim()}>
          {classifying ? 'Classifying…' : 'Classify with AI'}
        </Button>

        {classification && (
          <div className="space-y-4 rounded-lg border bg-muted/30 p-4">
            <div className="flex items-center gap-2">
              <Badge variant="outline">Confidence: {classification.confidence}</Badge>
            </div>
            <Field label="Title">
              <Input
                value={classification.title}
                onChange={(e) =>
                  setClassification({ ...classification, title: e.target.value })
                }
              />
            </Field>
            <Field label="Description">
              <textarea
                className="min-h-[120px] w-full rounded-md border bg-background px-3 py-2 text-sm"
                value={classification.description}
                onChange={(e) =>
                  setClassification({ ...classification, description: e.target.value })
                }
              />
            </Field>
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="Difficulty">
                <Select
                  value={classification.difficulty}
                  onChange={(e) =>
                    setClassification({
                      ...classification,
                      difficulty: e.target.value as Difficulty,
                    })
                  }
                >
                  {DIFFICULTIES.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </Select>
              </Field>
              <Field label="Topic">
                <Select
                  value={classification.topicSlug}
                  onChange={(e) =>
                    setClassification({ ...classification, topicSlug: e.target.value })
                  }
                >
                  {DEFAULT_TOPICS.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </Select>
              </Field>
            </div>
            <Field label="Tags">
              <Input
                value={classification.tags.join(', ')}
                onChange={(e) =>
                  setClassification({
                    ...classification,
                    tags: e.target.value.split(',').map((t) => t.trim()).filter(Boolean),
                  })
                }
              />
            </Field>
            {classification.suggestedHints.length > 0 && (
              <div>
                <p className="mb-2 text-sm font-medium">Suggested hints</p>
                <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
                  {classification.suggestedHints.map((h) => (
                    <li key={h}>{h}</li>
                  ))}
                </ul>
              </div>
            )}
            <p className="text-xs text-muted-foreground">
              Add at least one test case on the Manual tab after saving, or edit this question later.
            </p>
            <Button onClick={handleSave} disabled={saving}>
              {saving ? 'Saving…' : 'Confirm & save question'}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function ImportHistoryPanel() {
  const [items, setItems] = useState<ImportHistoryItemDto[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await apiClient.getImportHistory();
      setItems(data.items);
    } catch {
      toast.error('Failed to load import history');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) {
    return (
      <div className="space-y-3">
        <Skeleton className="h-16" />
        <Skeleton className="h-16" />
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <Card>
        <CardContent className="py-10 text-center text-muted-foreground">
          No imports yet. Use manual, CSV, JSON, or URL import to add questions.
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item) => (
        <Card key={item.id}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div>
              <CardTitle className="text-base">
                <Link to={`/practice/${item.question.slug}`} className="hover:underline">
                  {item.question.title}
                </Link>
              </CardTitle>
              <CardDescription>
                {item.question.topicName} · {new Date(item.createdAt).toLocaleDateString()}
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Badge variant="outline">{item.importMethod}</Badge>
              <Badge variant={difficultyVariant(item.question.difficulty)}>
                {item.question.difficulty}
              </Badge>
            </div>
          </CardHeader>
          {item.sourceUrl && (
            <CardContent className="pt-0 text-xs text-muted-foreground truncate">{item.sourceUrl}</CardContent>
          )}
        </Card>
      ))}
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm font-medium">{label}</span>
      {children}
    </label>
  );
}
