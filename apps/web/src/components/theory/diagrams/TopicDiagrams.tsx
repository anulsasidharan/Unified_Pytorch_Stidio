import { cn } from '@/lib/utils';
import { useStepAnimation } from '@/hooks/useStepAnimation';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, Pause, Play } from 'lucide-react';

export type TopicDiagramId =
  | 'two-pointers'
  | 'fast-slow'
  | 'stack-queue'
  | 'tree-traversal'
  | 'bfs-grid'
  | 'dp-table'
  | 'hash-lookup'
  | 'binary-search';

interface DiagramProps {
  step: number;
}

function DiagramShell({
  title,
  steps,
  caption,
  render,
}: {
  title: string;
  steps: string[];
  caption: string;
  render: (props: DiagramProps) => React.ReactNode;
}) {
  const { step, playing, setPlaying, next, prev } = useStepAnimation(steps.length);

  return (
    <div className="rounded-lg border bg-muted/30 p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-sm font-semibold">{title}</h3>
        <div className="flex items-center gap-1">
          <Button type="button" variant="outline" size="icon" className="h-8 w-8" onClick={prev} aria-label="Previous step">
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            type="button"
            variant="outline"
            size="icon"
            className="h-8 w-8"
            onClick={() => setPlaying((p) => !p)}
            aria-label={playing ? 'Pause' : 'Play'}
          >
            {playing ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </Button>
          <Button type="button" variant="outline" size="icon" className="h-8 w-8" onClick={next} aria-label="Next step">
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <div className="flex min-h-[140px] items-center justify-center">{render({ step })}</div>
      <p className="mt-3 text-center text-sm text-muted-foreground">{steps[step]}</p>
      <p className="mt-1 text-center text-xs text-muted-foreground/80">{caption}</p>
      <div className="mt-3 flex justify-center gap-1.5">
        {steps.map((_, i) => (
          <span
            key={i}
            className={cn('h-1.5 w-1.5 rounded-full transition-colors', i === step ? 'bg-primary' : 'bg-muted-foreground/30')}
          />
        ))}
      </div>
    </div>
  );
}

function TwoPointersDiagram({ step }: DiagramProps) {
  const values = [1, 3, 5, 7, 9, 11];
  const left = step < 2 ? 0 : step < 4 ? 1 : 2;
  const right = step < 2 ? 5 : step < 4 ? 4 : 3;
  const target = 12;

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex items-end gap-2">
        {values.map((v, i) => (
          <div key={i} className="flex flex-col items-center gap-1">
            <div
              className={cn(
                'flex h-10 w-10 items-center justify-center rounded-md border-2 text-sm font-mono font-semibold transition-all duration-500',
                i === left && 'border-blue-500 bg-blue-500/15 scale-110',
                i === right && 'border-emerald-500 bg-emerald-500/15 scale-110',
                i !== left && i !== right && 'border-border bg-card',
              )}
            >
              {v}
            </div>
            <span className="text-[10px] text-muted-foreground">
              {i === left ? 'L' : i === right ? 'R' : ''}
            </span>
          </div>
        ))}
      </div>
      <p className="text-xs font-medium">
        sum = {values[left] + values[right]} {values[left] + values[right] === target ? '✓ target' : ''}
      </p>
    </div>
  );
}

function FastSlowDiagram({ step }: DiagramProps) {
  const nodes = ['A', 'B', 'C', 'D', 'E'];
  const slow = Math.min(step, 4);
  const fast = Math.min(step * 2, 4);

  return (
    <div className="flex items-center gap-1">
      {nodes.map((label, i) => (
        <div key={i} className="flex items-center">
          <div
            className={cn(
              'flex h-10 w-10 items-center justify-center rounded-full border-2 text-xs font-bold transition-all duration-500',
              i === slow && 'border-blue-500 bg-blue-500/20',
              i === fast && 'border-amber-500 bg-amber-500/20',
              i !== slow && i !== fast && 'border-border bg-card',
            )}
          >
            {label}
          </div>
          {i < nodes.length - 1 && (
            <span className={cn('mx-0.5 text-muted-foreground', i === 4 && step >= 3 && 'text-primary')}>
              {i === 4 && step >= 3 ? '↩' : '→'}
            </span>
          )}
        </div>
      ))}
      <div className="ml-2 text-xs text-muted-foreground">
        <div className="text-blue-600 dark:text-blue-400">slow</div>
        <div className="text-amber-600 dark:text-amber-400">fast</div>
      </div>
    </div>
  );
}

function StackQueueDiagram({ step }: DiagramProps) {
  const stackItems = step >= 1 ? (step >= 2 ? ['(', '['] : ['(']) : [];
  const queueItems =
    step === 0 ? [] : step === 1 ? [1] : step === 2 ? [1, 2] : step === 3 ? [2, 3] : [3, 4];

  const showStack = step < 3;

  return (
    <div className="flex gap-8">
      <div className={cn('flex flex-col items-center transition-opacity', showStack ? 'opacity-100' : 'opacity-40')}>
        <span className="mb-2 text-xs font-semibold uppercase tracking-wide">Stack (LIFO)</span>
        <div className="flex h-28 w-16 flex-col-reverse items-center justify-start gap-1 rounded-md border-2 border-dashed border-blue-500/50 bg-blue-500/5 p-1">
          {stackItems.map((ch, i) => (
            <div key={i} className="flex h-8 w-12 animate-in fade-in slide-in-from-bottom-2 items-center justify-center rounded bg-blue-500/20 text-sm font-mono">
              {ch}
            </div>
          ))}
          {stackItems.length === 0 && <span className="text-[10px] text-muted-foreground">empty</span>}
        </div>
      </div>
      <div className={cn('flex flex-col items-center transition-opacity', !showStack ? 'opacity-100' : 'opacity-40')}>
        <span className="mb-2 text-xs font-semibold uppercase tracking-wide">Queue (FIFO)</span>
        <div className="flex h-16 w-40 items-center gap-1 rounded-md border-2 border-dashed border-emerald-500/50 bg-emerald-500/5 p-2">
          {queueItems.map((n, i) => (
            <div
              key={i}
              className={cn(
                'flex h-10 w-10 items-center justify-center rounded bg-emerald-500/20 text-sm font-mono transition-all',
                i === 0 && step >= 3 && 'ring-2 ring-emerald-500',
              )}
            >
              {n}
            </div>
          ))}
          {queueItems.length === 0 && <span className="text-[10px] text-muted-foreground">empty</span>}
        </div>
        {step >= 3 && <span className="mt-1 text-[10px] text-emerald-600">dequeue front</span>}
      </div>
    </div>
  );
}

function TreeTraversalDiagram({ step }: DiagramProps) {
  const levels = [['1'], ['2', '3'], ['4', '5', '6', '7']];
  const bfsOrder = ['1', '2', '3', '4', '5', '6', '7'];
  const dfsOrder = ['1', '2', '4', '5', '3', '6', '7'];
  const useBfs = step < 4;
  const highlighted = new Set((useBfs ? bfsOrder : dfsOrder).slice(0, (step % 4) + 1));

  return (
    <div className="flex flex-col items-center gap-3">
      <span className="text-xs font-medium text-primary">{useBfs ? 'BFS — level order' : 'DFS — depth first'}</span>
      {levels.map((row, ri) => (
        <div key={ri} className="flex gap-4">
          {row.map((n) => (
            <div
              key={n}
              className={cn(
                'flex h-9 w-9 items-center justify-center rounded-full border-2 text-sm font-semibold transition-all duration-400',
                highlighted.has(n) ? 'border-primary bg-primary/20 scale-110' : 'border-border bg-card opacity-50',
              )}
            >
              {n}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

function BfsGridDiagram({ step }: DiagramProps) {
  const grid = [
    ['S', '.', '.', '#'],
    ['.', '.', '#', '.'],
    ['.', '.', '.', 'E'],
  ];
  const visited = new Set<string>();
  const layers = [
    ['0,0'],
    ['0,1', '1,0'],
    ['1,1', '2,0'],
    ['2,1', '2,2'],
  ];
  for (let i = 0; i <= Math.min(step, layers.length - 1); i++) {
    layers[i].forEach((c) => visited.add(c));
  }

  return (
    <div className="grid grid-cols-4 gap-1">
      {grid.map((row, r) =>
        row.map((cell, c) => {
          const key = `${r},${c}`;
          const isVisited = visited.has(key);
          return (
            <div
              key={key}
              className={cn(
                'flex h-10 w-10 items-center justify-center rounded text-xs font-bold transition-all duration-500',
                cell === '#' && 'bg-muted text-muted-foreground',
                cell === 'S' && 'bg-blue-500/30 text-blue-700 dark:text-blue-300',
                cell === 'E' && 'bg-emerald-500/30 text-emerald-700 dark:text-emerald-300',
                cell === '.' && isVisited && 'bg-primary/25 ring-2 ring-primary',
                cell === '.' && !isVisited && 'bg-card border',
              )}
            >
              {cell}
            </div>
          );
        }),
      )}
    </div>
  );
}

function DpTableDiagram({ step }: DiagramProps) {
  const coins = [1, 2, 5];
  const amount = 5;
  const dpSteps = [
    [0, 1, 1, 2, 2, 3],
    [0, 1, 1, 2, 2, 3],
    [0, 1, 1, 2, 2, 3],
    [0, 1, 1, 2, 2, 3],
    [0, 1, 1, 2, 2, 3],
    [0, 1, 1, 2, 2, 3],
  ];
  const activeCol = Math.min(step, amount);
  const row = dpSteps[Math.min(step, dpSteps.length - 1)];

  return (
    <div className="flex flex-col items-center gap-2">
      <p className="text-xs text-muted-foreground">coin change: coins = [{coins.join(', ')}], amount = {amount}</p>
      <div className="flex gap-1">
        {row.map((val, i) => (
          <div key={i} className="flex flex-col items-center gap-1">
            <div
              className={cn(
                'flex h-9 w-9 items-center justify-center rounded border text-sm font-mono transition-all duration-500',
                i === activeCol ? 'border-primary bg-primary/20 scale-110' : 'border-border bg-card',
              )}
            >
              {val === Infinity ? '∞' : val}
            </div>
            <span className="text-[10px] text-muted-foreground">{i}</span>
          </div>
        ))}
      </div>
      {step >= 3 && <p className="text-xs font-medium text-primary">dp[5] = 3 coins (5, or 2+2+1, …)</p>}
    </div>
  );
}

function HashLookupDiagram({ step }: DiagramProps) {
  const nums = [2, 7, 11, 15];
  const target = 9;
  const seenUpTo = Math.min(step, 3);

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex gap-2">
        {nums.map((n, i) => (
          <div
            key={i}
            className={cn(
              'flex h-10 w-10 items-center justify-center rounded-md border-2 font-mono text-sm transition-all duration-500',
              i <= seenUpTo ? 'border-primary bg-primary/15' : 'border-border bg-card opacity-50',
            )}
          >
            {n}
          </div>
        ))}
      </div>
      <div className="rounded-md border bg-card p-2 text-xs">
        <span className="font-semibold">map: </span>
        {nums.slice(0, seenUpTo + 1).map((n, i) => (
          <span key={i} className="mr-2 font-mono">
            {n}→{i}
          </span>
        ))}
        {seenUpTo < 0 && <span className="text-muted-foreground">empty</span>}
      </div>
      {step >= 2 && (
        <p className="text-xs text-emerald-600 dark:text-emerald-400">
          target − {nums[1]} = {target - nums[1]} found in map → indices [0, 1]
        </p>
      )}
    </div>
  );
}

function BinarySearchDiagram({ step }: DiagramProps) {
  const arr = [1, 3, 5, 7, 9, 11, 13];
  const target = 7;
  const ranges = [
    { lo: 0, hi: 6, mid: 3 },
    { lo: 4, hi: 6, mid: 5 },
    { lo: 4, hi: 4, mid: 4 },
  ];
  const { lo, hi, mid } = ranges[Math.min(step, ranges.length - 1)];

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="flex gap-2">
        {arr.map((v, i) => (
          <div key={i} className="flex flex-col items-center gap-1">
            <div
              className={cn(
                'flex h-10 w-10 items-center justify-center rounded-md border-2 font-mono text-sm transition-all duration-500',
                i === mid && 'border-primary bg-primary/25 scale-110',
                i >= lo && i <= hi && i !== mid && 'border-amber-500/50 bg-amber-500/10',
                (i < lo || i > hi) && 'opacity-30 border-border',
              )}
            >
              {v}
            </div>
            <span className="text-[9px] text-muted-foreground">
              {i === lo ? 'lo' : i === hi ? 'hi' : i === mid ? 'mid' : ''}
            </span>
          </div>
        ))}
      </div>
      <p className="text-xs">
        arr[mid] = {arr[mid]} {arr[mid] === target ? '— found!' : arr[mid] < target ? '→ search right' : '→ search left'}
      </p>
    </div>
  );
}

const DIAGRAM_CONFIG: Record<
  TopicDiagramId,
  { title: string; steps: string[]; render: (props: DiagramProps) => React.ReactNode }
> = {
  'two-pointers': {
    title: 'Two pointers on a sorted array',
    steps: [
      'Start with left at index 0 and right at the last index.',
      'Compute sum = arr[left] + arr[right]. If sum is too small, move left forward.',
      'If sum is too large, move right backward.',
      'When sum equals the target, you found the pair.',
    ],
    render: (p) => <TwoPointersDiagram {...p} />,
  },
  'fast-slow': {
    title: 'Fast & slow pointers',
    steps: [
      'Both pointers start at the head.',
      'Each step: slow moves 1 node, fast moves 2 nodes.',
      'If there is a cycle, fast eventually laps slow.',
      'They meet inside the loop — cycle detected.',
    ],
    render: (p) => <FastSlowDiagram {...p} />,
  },
  'stack-queue': {
    title: 'Stack vs queue',
    steps: [
      'Stack starts empty — push adds to the top.',
      'Push another opener; the top is always removed first (LIFO).',
      'Switch to queue: enqueue 1, then 2 at the back.',
      'Dequeue removes from the front (FIFO), not the back.',
    ],
    render: (p) => <StackQueueDiagram {...p} />,
  },
  'tree-traversal': {
    title: 'Tree traversals',
    steps: [
      'BFS visits the root first.',
      'Then all nodes at depth 1, left to right.',
      'Then depth 2 — level by level.',
      'DFS goes deep (left subtree) before visiting siblings.',
    ],
    render: (p) => <TreeTraversalDiagram {...p} />,
  },
  'bfs-grid': {
    title: 'BFS on a grid',
    steps: [
      'Begin at source cell S; mark it visited.',
      'Expand to all unblocked neighbors in the first layer.',
      'Continue layer by layer — shortest path in unweighted grids.',
      'Reach E when the wavefront hits the target.',
    ],
    render: (p) => <BfsGridDiagram {...p} />,
  },
  'dp-table': {
    title: 'DP table fill',
    steps: [
      'Base case: dp[0] = 0 ways to make amount 0.',
      'For amount 1, try each coin and take the minimum count.',
      'Fill cells left to right using prior optimal answers.',
      'dp[amount] stores the best answer for that subproblem.',
    ],
    render: (p) => <DpTableDiagram {...p} />,
  },
  'hash-lookup': {
    title: 'Hash map complement',
    steps: [
      'Scan the array left to right.',
      'Store each value and its index in the map.',
      'For 7, check if 9 − 7 = 2 is already in the map.',
      'Complement found — return both indices.',
    ],
    render: (p) => <HashLookupDiagram {...p} />,
  },
  'binary-search': {
    title: 'Binary search',
    steps: [
      'Set lo and hi to the full array range; pick mid.',
      'If arr[mid] < target, discard the left half.',
      'If arr[mid] > target, discard the right half.',
      'When lo == hi, mid is the target index (if present).',
    ],
    render: (p) => <BinarySearchDiagram {...p} />,
  },
};

export function TopicDiagram({ diagramId, caption }: { diagramId: TopicDiagramId; caption: string }) {
  const config = DIAGRAM_CONFIG[diagramId];
  if (!config) return null;

  return (
    <DiagramShell title={config.title} steps={config.steps} caption={caption} render={config.render} />
  );
}
