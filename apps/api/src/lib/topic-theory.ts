export type TopicDiagramId =
  | 'two-pointers'
  | 'fast-slow'
  | 'stack-queue'
  | 'tree-traversal'
  | 'bfs-grid'
  | 'dp-table'
  | 'hash-lookup'
  | 'binary-search';

export interface TopicTheoryContent {
  overview: string[];
  keyConcepts: string[];
  whenToUse: string[];
  commonPatterns: string[];
  complexityNotes: string;
  diagramId: TopicDiagramId;
  diagramCaption: string;
}

const THEORY_BY_SLUG: Record<string, TopicTheoryContent> = {
  'arrays-strings': {
    overview: [
      'Arrays store elements in contiguous memory with O(1) random access by index. Strings are often treated as character arrays; many interview problems reduce to scanning, comparing, or transforming sequences.',
      'Two pointers move from one or both ends toward the middle (or in the same direction at different speeds) to avoid nested loops. Sliding window maintains a contiguous subrange [left, right] that grows or shrinks while preserving an invariant (sum, unique count, etc.).',
      'Prefix sums let you answer range-sum queries in O(1) after O(n) preprocessing—essential for subarray problems with fixed or target sums.',
    ],
    keyConcepts: [
      'Contiguous storage → cache-friendly iteration',
      'Two pointers on sorted data → pair finding, palindromes, merging',
      'Sliding window → longest/shortest subarray with a constraint',
      'Prefix sum + hash map → count subarrays with sum k',
    ],
    whenToUse: [
      'Sorted array + pair/triplet sum → two pointers',
      'Contiguous subarray/substring with a limit → sliding window',
      'Range queries on static array → prefix sums',
      'Need O(1) complement lookup while scanning → hash map with one pass',
    ],
    commonPatterns: [
      'Two Sum (hash map)',
      'Valid Palindrome / Container With Most Water (two pointers)',
      'Maximum Subarray (Kadane)',
      'Longest Substring Without Repeating (sliding window)',
    ],
    complexityNotes:
      'Most array scans are O(n) time and O(1)–O(n) space. Sliding window and two pointers avoid O(n²) brute force when the array is sorted or the window property is monotonic.',
    diagramId: 'two-pointers',
    diagramCaption: 'Two pointers squeeze inward on a sorted array to find a target pair.',
  },
  'linked-lists': {
    overview: [
      'A linked list chains nodes where each node stores a value and a reference to the next node (singly linked) or both next and prev (doubly linked). Unlike arrays, you cannot jump to index i in O(1); you walk from the head.',
      'Pointer manipulation is the core skill: reversing links, merging sorted lists, and detecting cycles without extra arrays. A dummy head node before the real head simplifies insert/delete at the front.',
      'Fast and slow pointers (Floyd) detect cycles and find the middle in one pass—slow moves 1 step, fast moves 2. When fast reaches the end, slow is at the midpoint.',
    ],
    keyConcepts: [
      'Head pointer defines the list; always check for null',
      'In-place reversal rewires next pointers in O(n) time, O(1) space',
      'Dummy node → uniform handling of head edge cases',
      'Fast/slow → cycle detection, middle node, nth from end',
    ],
    whenToUse: [
      'Problem explicitly gives a linked list or requires O(1) extra space reordering',
      'Need to detect a cycle or find middle without counting length first',
      'Merge or reorder lists by changing links, not copying values',
    ],
    commonPatterns: [
      'Reverse Linked List (iterative three-pointer)',
      'Linked List Cycle (Floyd)',
      'Merge Two Sorted Lists',
      'Remove Nth Node From End (fast/slow gap)',
    ],
    complexityNotes:
      'Single pass algorithms are typically O(n) time and O(1) extra space. Recursive DFS uses O(h) stack space where h is list length.',
    diagramId: 'fast-slow',
    diagramCaption: 'Fast and slow pointers meet inside a cycle, proving a loop exists.',
  },
  'stacks-queues': {
    overview: [
      'A stack is Last-In-First-Out (LIFO): push and pop at the top. A queue is First-In-First-Out (FIFO): enqueue at the back, dequeue from the front. Both are abstract interfaces often built from arrays or linked lists.',
      'Stacks model nesting and “undo” behavior—valid parentheses, expression parsing, and monotonic stacks that keep increasing or decreasing elements to answer “next greater” style questions in linear time.',
      'Queues support BFS level-order processing. Two stacks can implement a queue with amortized O(1) operations by using an inbox and outbox stack.',
    ],
    keyConcepts: [
      'Stack → matching brackets, DFS iterative, monotonic decreasing/increasing',
      'Queue → BFS frontier, scheduling in order',
      'Monotonic stack → each element pushed/popped once → O(n) total',
      'Min stack → auxiliary structure tracking running minimum',
    ],
    whenToUse: [
      'Nested or paired symbols → stack',
      'Shortest path in unweighted graph or level order → queue (BFS)',
      'Next greater/smaller element to the right → monotonic stack',
      'Histogram / span problems → stack of indices',
    ],
    commonPatterns: [
      'Valid Parentheses',
      'Daily Temperatures (monotonic stack)',
      'Implement Queue using Stacks',
      'Largest Rectangle in Histogram',
    ],
    complexityNotes:
      'Each element enters and leaves a stack at most once in monotonic stack problems → O(n). Standard push/pop are O(1).',
    diagramId: 'stack-queue',
    diagramCaption: 'Stack (LIFO) pushes on top; queue (FIFO) serves from the front.',
  },
  trees: {
    overview: [
      'A binary tree has nodes with at most left and right children. A Binary Search Tree (BST) orders keys so left subtree < node < right subtree—enabling O(h) search when balanced.',
      'Depth-First Search (DFS) goes deep first: preorder (node-left-right), inorder (left-node-right, sorted for BST), postorder (left-right-node). Breadth-First Search (BFS) visits level by level using a queue.',
      'Many tree answers combine recursion with a return value (height, gain) and a side effect (global max path sum). Always define base case: null node.',
    ],
    keyConcepts: [
      'DFS → paths, depth, validation, subtree problems',
      'BFS → level order, shortest path in tree (unweighted)',
      'BST invariant → bounds or inorder strictly increasing',
      'Recursion depth ≈ tree height h; skewed tree h = n',
    ],
    whenToUse: [
      'Hierarchical data, paths root-to-leaf, or subtree aggregation',
      'BST problems → exploit ordering (LCA, insert, delete)',
      'Need level-by-level output → BFS',
    ],
    commonPatterns: [
      'Invert / max depth (DFS)',
      'Validate BST (min/max bounds)',
      'LCA in BST (walk from root)',
      'Max path sum (post-order with global best)',
    ],
    complexityNotes:
      'Visit each node once → O(n) time. Space is O(h) for recursion stack; balanced tree h = log n, skewed h = n.',
    diagramId: 'tree-traversal',
    diagramCaption: 'BFS visits the tree level by level; DFS goes deep before backtracking.',
  },
  graphs: {
    overview: [
      'A graph G = (V, E) has vertices and edges (directed or undirected, weighted or not). Adjacency list is the usual sparse representation; adjacency matrix suits dense graphs or O(1) edge lookup.',
      'BFS explores in layers—shortest path in unweighted graphs. DFS explores deeply—connectivity, cycles, topological sort. Directed acyclic graphs (DAGs) admit topological ordering for prerequisites.',
      'Weighted shortest paths use Dijkstra (non-negative weights) or Bellman-Ford. Union-Find helps with connected components and Kruskal-style merging.',
    ],
    keyConcepts: [
      'Visited set prevents infinite loops',
      'BFS → shortest steps in unweighted graph',
      'DFS / 3-color → cycle detection in directed graph',
      'Topological sort → course schedule, build order',
      'Dijkstra → min distance with priority queue',
    ],
    whenToUse: [
      'Grid as graph (4/8 neighbors) → flood fill, islands',
      'Dependencies between tasks → topological sort',
      'Shortest path with non-negative weights → Dijkstra',
      'Implicit graph (words one edit apart) → BFS on states',
    ],
    commonPatterns: [
      'Number of Islands (DFS/BFS flood fill)',
      'Course Schedule (topological sort)',
      'Clone Graph (DFS + hash map)',
      'Word Ladder (BFS on words)',
    ],
    complexityNotes:
      'BFS/DFS are O(V + E). Dijkstra with binary heap is O((V + E) log V). Space is O(V) for queues, visited, and distance arrays.',
    diagramId: 'bfs-grid',
    diagramCaption: 'BFS expands in waves from a source, marking cells layer by layer.',
  },
  'dynamic-programming': {
    overview: [
      'Dynamic Programming (DP) applies when a problem has overlapping subproblems and optimal substructure: the best answer for a state is built from best answers of smaller states.',
      'Define a state (often index i, or pair i,j) and a recurrence relating dp[i] to previous values. Bottom-up tabulation fills a table iteratively; top-down memoization caches recursive results.',
      'Classic families: linear DP (stairs, rob houses), knapsack/unbounded coin change, LIS, and 2D DP on two strings (edit distance, LCS).',
    ],
    keyConcepts: [
      'State definition comes before code',
      'Recurrence + base cases = complete solution',
      'Space optimization: keep only last row or rolling variables',
      'Prove why greedy fails before choosing DP',
    ],
    whenToUse: [
      'Counting ways or min/max over choices with constraints',
      'Optimal substructure visible in small examples',
      'Brute force recursion repeats same subcalls',
    ],
    commonPatterns: [
      'Climbing Stairs (Fibonacci DP)',
      'House Robber (take/skip linear)',
      'Coin Change (unbounded knapsack)',
      'Edit Distance (2D DP)',
    ],
    complexityNotes:
      'Complexity is usually O(states × transitions). 2D string DP is O(m·n) time and can often be optimized to O(min(m,n)) space.',
    diagramId: 'dp-table',
    diagramCaption: 'DP fills a table so each cell reuses optimal answers from smaller subproblems.',
  },
  hashing: {
    overview: [
      'A hash map stores key → value with average O(1) insert and lookup. Hash sets track membership without duplicates. Collisions are handled by chaining or open addressing in implementations.',
      'Frequency maps count occurrences; they power anagram grouping and top-k problems. Prefix sum combined with a map counts subarrays with a target sum by storing how often each prefix appeared.',
      'For consecutive sequences in unsorted data, store all numbers in a set and only start counting when num-1 is absent—each element is visited O(1) times overall.',
    ],
    keyConcepts: [
      'Complement lookup: target - x in map',
      'Frequency counting and bucket by frequency',
      'Canonical key for anagrams (sorted string or char count)',
      'Prefix sum + map → subarray sum equals k',
    ],
    whenToUse: [
      'Need fast lookup or deduplication while scanning',
      'Count pairs or subarrays defined by sums or differences',
      'Group items by a normalized signature (anagrams)',
    ],
    commonPatterns: [
      'Contains Duplicate (set)',
      'Group Anagrams (hash by signature)',
      'Subarray Sum Equals K (prefix + map)',
      'Top K Frequent (freq map + bucket/heap)',
    ],
    complexityNotes:
      'Average O(n) time and O(n) space for single-pass hash solutions. Worst-case hash collisions can degrade but rarely affect interview analysis.',
    diagramId: 'hash-lookup',
    diagramCaption: 'A hash map maps each value to an index for O(1) complement checks.',
  },
  'sorting-searching': {
    overview: [
      'Sorting arranges data in order—comparison sorts like merge and quicksort run in O(n log n). Knowing sort stability and when to use counting/radix sort for integers helps choose tools.',
      'Binary search works on sorted arrays or on the answer space when a predicate is monotonic (“can we achieve X?”). Maintain inclusive or exclusive bounds and always shrink the range.',
      'Variations: find first/last position of target, search rotated sorted array, and kth largest via quickselect or heap.',
    ],
    keyConcepts: [
      'Sorted array → binary search O(log n)',
      'Monotonic predicate → binary search on answer',
      'Merge sort stable O(n log n); quicksort in-place average O(n log n)',
      'Heap for top-k without full sort',
    ],
    whenToUse: [
      'Data is sorted or can be sorted once upfront',
      'Minimize/maximize value with yes/no feasibility check',
      'Find boundary between false and true predicates',
    ],
    commonPatterns: [
      'Binary Search (classic)',
      'Search Insert Position',
      'Find First and Last Position',
      'Kth Largest (heap or quickselect)',
    ],
    complexityNotes:
      'Binary search is O(log n) per query on a sorted array of size n. Sorting costs O(n log n) once; reuse sorted order for multiple queries.',
    diagramId: 'binary-search',
    diagramCaption: 'Binary search halves the search range by comparing the middle element to the target.',
  },
};

export function getTopicTheory(slug: string): TopicTheoryContent | null {
  return THEORY_BY_SLUG[slug] ?? null;
}

export function getDefaultTheory(
  description: string | null,
  category: string | null,
  difficulty: string,
): TopicTheoryContent {
  return {
    overview: [description ?? 'Study core patterns and practice problems for this topic.'],
    keyConcepts: ['Read the problem constraints carefully', 'Identify the matching pattern'],
    whenToUse: getFallbackWhenToUse(category),
    commonPatterns: [],
    complexityNotes: `Focus on efficient solutions appropriate for ${difficulty} level problems.`,
    diagramId: 'two-pointers',
    diagramCaption: 'Visual intuition for this topic.',
  };
}

function getFallbackWhenToUse(category: string | null): string[] {
  const map: Record<string, string[]> = {
    Arrays: ['Two pointers on sorted data', 'Sliding window for subarrays'],
    'Linked Lists': ['Pointer rewriting in-place', 'Fast/slow for cycles'],
    Stacks: ['LIFO matching and monotonic stack'],
    Trees: ['DFS for paths; BFS for levels'],
    Graphs: ['BFS for unweighted shortest path', 'DFS for connectivity'],
    'Dynamic Programming': ['Overlapping subproblems with optimal substructure'],
    Hashing: ['O(1) lookups and frequency counts'],
    Sorting: ['Sorted order enables binary search'],
  };
  return map[category ?? ''] ?? ['Practice pattern recognition before coding'];
}
