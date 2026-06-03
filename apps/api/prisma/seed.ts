import {
  Difficulty,
  PrismaClient,
  QuestionSource,
} from '@prisma/client';

const prisma = new PrismaClient();

interface SeedQuestion {
  slug: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  constraints?: string;
  hints: string[];
  tags: string[];
  testCases: Array<{
    input: string;
    expectedOutput: string;
    explanation?: string;
    isSample: boolean;
    isHidden: boolean;
    orderIndex: number;
  }>;
  solution: {
    language: string;
    approachName: string;
    code: string;
    explanation: string;
    timeComplexity: string;
    spaceComplexity: string;
    isOptimal: boolean;
  };
}

interface SeedTopic {
  slug: string;
  name: string;
  category: string;
  description: string;
  difficultyLevel: Difficulty;
  orderIndex: number;
  iconUrl: string;
  questions: SeedQuestion[];
}

const TOPICS: SeedTopic[] = [
  {
    slug: 'arrays-strings',
    name: 'Arrays & Strings',
    category: 'Arrays',
    description: 'Fundamental array and string manipulation techniques including two pointers and sliding window.',
    difficultyLevel: Difficulty.basic,
    orderIndex: 1,
    iconUrl: '📊',
    questions: [
      {
        slug: 'two-sum',
        title: 'Two Sum',
        description:
          'Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.',
        difficulty: Difficulty.basic,
        constraints: '2 <= nums.length <= 10^4',
        hints: ['Try brute force with nested loops first', 'Can a hash map help you find complements in O(1)?'],
        tags: ['array', 'hash-table'],
        testCases: [
          { input: '4\n2 7 11 15\n9', expectedOutput: '0 1', explanation: '2 + 7 = 9', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '3\n3 2 4\n6', expectedOutput: '1 2', isSample: true, isHidden: false, orderIndex: 1 },
          { input: '2\n3 3\n6', expectedOutput: '0 1', isSample: false, isHidden: true, orderIndex: 2 },
        ],
        solution: {
          language: 'python',
          approachName: 'Hash Map',
          code: 'def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i',
          explanation: 'Store each value and index; check complement on each step.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'valid-palindrome',
        title: 'Valid Palindrome',
        description: 'Given a string `s`, return `true` if it is a palindrome, considering only alphanumeric characters and ignoring cases.',
        difficulty: Difficulty.basic,
        hints: ['Use two pointers from both ends', 'Skip non-alphanumeric characters'],
        tags: ['string', 'two-pointers'],
        testCases: [
          { input: 'A man, a plan, a canal: Panama', expectedOutput: 'true', isSample: true, isHidden: false, orderIndex: 0 },
          { input: 'race a car', expectedOutput: 'false', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Two Pointers',
          code: 'def is_palindrome(s):\n    left, right = 0, len(s) - 1\n    while left < right:\n        while left < right and not s[left].isalnum():\n            left += 1\n        while left < right and not s[right].isalnum():\n            right -= 1\n        if s[left].lower() != s[right].lower():\n            return False\n        left += 1\n        right -= 1\n    return True',
          explanation: 'Move pointers inward, skipping non-alphanumeric chars.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'container-with-most-water',
        title: 'Container With Most Water',
        description:
          'Given `height`, find two lines that together with the x-axis form a container that holds the most water.',
        difficulty: Difficulty.intermediate,
        hints: ['Start with widest container', 'Move the pointer at the shorter line'],
        tags: ['array', 'two-pointers'],
        testCases: [
          { input: '9\n1 8 6 2 5 4 8 3 7', expectedOutput: '49', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '2\n1 1', expectedOutput: '1', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Two Pointers',
          code: 'def max_area(height):\n    left, right = 0, len(height) - 1\n    best = 0\n    while left < right:\n        best = max(best, min(height[left], height[right]) * (right - left))\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return best',
          explanation: 'Greedy two-pointer sweep from both ends.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'maximum-subarray',
        title: 'Maximum Subarray',
        description: 'Given an integer array `nums`, find the contiguous subarray with the largest sum and return its sum.',
        difficulty: Difficulty.intermediate,
        hints: ["Kadane's algorithm tracks running sum", 'Reset running sum when it becomes negative'],
        tags: ['array', 'dynamic-programming'],
        testCases: [
          { input: '9\n-2 1 -3 4 -1 2 1 -5 4', expectedOutput: '6', explanation: '[4,-1,2,1]', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '1\n1', expectedOutput: '1', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: "Kadane's Algorithm",
          code: 'def max_subarray(nums):\n    best = cur = nums[0]\n    for n in nums[1:]:\n        cur = max(n, cur + n)\n        best = max(best, cur)\n    return best',
          explanation: 'Track max ending here and global max.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'longest-substring-without-repeating',
        title: 'Longest Substring Without Repeating Characters',
        description: 'Given a string `s`, find the length of the longest substring without repeating characters.',
        difficulty: Difficulty.intermediate,
        hints: ['Use a sliding window', 'Track last seen index of each character'],
        tags: ['string', 'sliding-window', 'hash-table'],
        testCases: [
          { input: 'abcabcbb', expectedOutput: '3', isSample: true, isHidden: false, orderIndex: 0 },
          { input: 'bbbbb', expectedOutput: '1', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Sliding Window',
          code: 'def length_of_longest_substring(s):\n    last = {}\n    start = best = 0\n    for i, ch in enumerate(s):\n        if ch in last and last[ch] >= start:\n            start = last[ch] + 1\n        last[ch] = i\n        best = max(best, i - start + 1)\n    return best',
          explanation: 'Expand window and shrink when duplicate found.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(min(n, alphabet))',
          isOptimal: true,
        },
      },
    ],
  },
  {
    slug: 'linked-lists',
    name: 'Linked Lists',
    category: 'Linked Lists',
    description: 'Singly and doubly linked list operations, cycle detection, and pointer manipulation.',
    difficultyLevel: Difficulty.basic,
    orderIndex: 2,
    iconUrl: '🔗',
    questions: [
      {
        slug: 'reverse-linked-list',
        title: 'Reverse Linked List',
        description: 'Given the head of a singly linked list, reverse the list and return the reversed list head.',
        difficulty: Difficulty.basic,
        hints: ['Track previous, current, and next pointers', 'Iteratively reverse links'],
        tags: ['linked-list'],
        testCases: [
          { input: '1->2->3->4->5', expectedOutput: '5->4->3->2->1', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '1->2', expectedOutput: '2->1', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Iterative',
          code: 'def reverse_list(head):\n    prev = None\n    cur = head\n    while cur:\n        nxt = cur.next\n        cur.next = prev\n        prev = cur\n        cur = nxt\n    return prev',
          explanation: 'Reverse links one node at a time.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'linked-list-cycle',
        title: 'Linked List Cycle',
        description: 'Given head, determine if the linked list has a cycle in it.',
        difficulty: Difficulty.basic,
        hints: ["Floyd's tortoise and hare", 'If fast catches slow, cycle exists'],
        tags: ['linked-list', 'two-pointers'],
        testCases: [
          { input: '3->2->0->-4 (cycle at -4)', expectedOutput: 'true', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '1->2 (no cycle)', expectedOutput: 'false', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: "Floyd's Cycle Detection",
          code: 'def has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            return True\n    return False',
          explanation: 'Two pointers move at different speeds.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'merge-two-sorted-lists',
        title: 'Merge Two Sorted Lists',
        description: 'Merge two sorted linked lists and return it as one sorted list.',
        difficulty: Difficulty.basic,
        hints: ['Use a dummy head node', 'Compare heads and attach smaller node'],
        tags: ['linked-list'],
        testCases: [
          { input: '1->2->4, 1->3->4', expectedOutput: '1->1->2->3->4->4', isSample: true, isHidden: false, orderIndex: 0 },
          { input: 'empty, empty', expectedOutput: 'empty', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Iterative Merge',
          code: 'def merge_two_lists(l1, l2):\n    dummy = cur = ListNode(0)\n    while l1 and l2:\n        if l1.val <= l2.val:\n            cur.next = l1\n            l1 = l1.next\n        else:\n            cur.next = l2\n            l2 = l2.next\n        cur = cur.next\n    cur.next = l1 or l2\n    return dummy.next',
          explanation: 'Merge like merge sort merge step.',
          timeComplexity: 'O(n + m)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'remove-nth-node-from-end',
        title: 'Remove Nth Node From End of List',
        description: 'Given the head of a linked list, remove the nth node from the end and return its head.',
        difficulty: Difficulty.intermediate,
        hints: ['Two pointers n steps apart', 'Use dummy node for edge cases'],
        tags: ['linked-list', 'two-pointers'],
        testCases: [
          { input: '1->2->3->4->5, n=2', expectedOutput: '1->2->3->5', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '1, n=1', expectedOutput: 'empty', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Two Pointers',
          code: 'def remove_nth_from_end(head, n):\n    dummy = ListNode(0, head)\n    fast = slow = dummy\n    for _ in range(n + 1):\n        fast = fast.next\n    while fast:\n        fast = fast.next\n        slow = slow.next\n    slow.next = slow.next.next\n    return dummy.next',
          explanation: 'Gap of n+1 between fast and slow.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'reorder-list',
        title: 'Reorder List',
        description:
          'Reorder the list to L0→Ln→L1→Ln-1→L2→Ln-2… without modifying node values.',
        difficulty: Difficulty.advanced,
        hints: ['Find middle with slow/fast', 'Reverse second half, then merge'],
        tags: ['linked-list'],
        testCases: [
          { input: '1->2->3->4', expectedOutput: '1->4->2->3', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '1->2->3->4->5', expectedOutput: '1->5->2->4->3', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Split-Reverse-Merge',
          code: '# Split at middle, reverse second half, merge alternately',
          explanation: 'Three-phase pointer manipulation.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
    ],
  },
  {
    slug: 'stacks-queues',
    name: 'Stacks & Queues',
    category: 'Stacks',
    description: 'Stack and queue ADTs, monotonic stacks, and classic LIFO/FIFO problems.',
    difficultyLevel: Difficulty.basic,
    orderIndex: 3,
    iconUrl: '📚',
    questions: [
      {
        slug: 'valid-parentheses',
        title: 'Valid Parentheses',
        description: 'Given a string containing `()[]{}`, determine if the input string is valid.',
        difficulty: Difficulty.basic,
        hints: ['Use a stack for opening brackets', 'Pop and match on closing brackets'],
        tags: ['string', 'stack'],
        testCases: [
          { input: '()', expectedOutput: 'true', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '()[]{}', expectedOutput: 'true', isSample: true, isHidden: false, orderIndex: 1 },
          { input: '(]', expectedOutput: 'false', isSample: false, isHidden: true, orderIndex: 2 },
        ],
        solution: {
          language: 'python',
          approachName: 'Stack',
          code: 'def is_valid(s):\n    stack = []\n    pairs = {")": "(", "]": "[", "}": "{"}\n    for ch in s:\n        if ch in pairs:\n            if not stack or stack.pop() != pairs[ch]:\n                return False\n        else:\n            stack.append(ch)\n    return not stack',
          explanation: 'Classic bracket matching with stack.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'min-stack',
        title: 'Min Stack',
        description: 'Design a stack that supports push, pop, top, and retrieving the minimum element in O(1).',
        difficulty: Difficulty.intermediate,
        hints: ['Track current minimum on each push', 'Use auxiliary stack or store pairs'],
        tags: ['stack', 'design'],
        testCases: [
          { input: 'push -2, push 0, push -3, getMin, pop, top, getMin', expectedOutput: '-3\n0\n-2', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Auxiliary Min Stack',
          code: 'class MinStack:\n    def __init__(self):\n        self.stack = []\n        self.mins = []\n    def push(self, val):\n        self.stack.append(val)\n        self.mins.append(min(val, self.mins[-1] if self.mins else val))',
          explanation: 'Parallel stack stores running minimum.',
          timeComplexity: 'O(1) per op',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'daily-temperatures',
        title: 'Daily Temperatures',
        description: 'Given daily temperatures, return an array where each element is days until a warmer temperature.',
        difficulty: Difficulty.intermediate,
        hints: ['Monotonic decreasing stack of indices', 'Pop when warmer day found'],
        tags: ['array', 'stack', 'monotonic-stack'],
        testCases: [
          { input: '73 74 75 71 69 72 76 73', expectedOutput: '1 1 4 2 1 1 0 0', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Monotonic Stack',
          code: 'def daily_temperatures(temps):\n    res = [0] * len(temps)\n    stack = []\n    for i, t in enumerate(temps):\n        while stack and temps[stack[-1]] < t:\n            j = stack.pop()\n            res[j] = i - j\n        stack.append(i)\n    return res',
          explanation: 'Stack stores indices waiting for warmer day.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'implement-queue-using-stacks',
        title: 'Implement Queue using Stacks',
        description: 'Implement a FIFO queue using only two stacks.',
        difficulty: Difficulty.basic,
        hints: ['Use inbox and outbox stacks', 'Move elements when outbox empty'],
        tags: ['stack', 'queue', 'design'],
        testCases: [
          { input: 'push 1, push 2, peek, pop, empty', expectedOutput: '1\nfalse', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Two Stack Queue',
          code: 'class MyQueue:\n    def __init__(self):\n        self.in_stack, self.out_stack = [], []',
          explanation: 'Amortized O(1) with lazy transfer.',
          timeComplexity: 'O(1) amortized',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'largest-rectangle-in-histogram',
        title: 'Largest Rectangle in Histogram',
        description: 'Given heights of bars, return the area of the largest rectangle in the histogram.',
        difficulty: Difficulty.advanced,
        hints: ['Monotonic increasing stack', 'Compute width when popping'],
        tags: ['stack', 'monotonic-stack'],
        testCases: [
          { input: '2 1 5 6 2 3', expectedOutput: '10', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Monotonic Stack',
          code: 'def largest_rectangle_area(heights):\n    stack = []\n    best = 0\n    heights.append(0)\n    for i, h in enumerate(heights):\n        while stack and heights[stack[-1]] > h:\n            j = stack.pop()\n            w = i if not stack else i - stack[-1] - 1\n            best = max(best, heights[j] * w)\n        stack.append(i)\n    return best',
          explanation: 'Pop shorter bars and compute max area.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
    ],
  },
  {
    slug: 'trees',
    name: 'Trees',
    category: 'Trees',
    description: 'Binary trees, BST operations, traversals, and tree property problems.',
    difficultyLevel: Difficulty.intermediate,
    orderIndex: 4,
    iconUrl: '🌳',
    questions: [
      {
        slug: 'invert-binary-tree',
        title: 'Invert Binary Tree',
        description: 'Given the root of a binary tree, invert the tree and return its root.',
        difficulty: Difficulty.basic,
        hints: ['Swap left and right recursively', 'BFS also works level by level'],
        tags: ['tree', 'dfs'],
        testCases: [
          { input: '[4,2,7,1,3,6,9]', expectedOutput: '[4,7,2,9,6,3,1]', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Recursive DFS',
          code: 'def invert_tree(root):\n    if not root:\n        return None\n    root.left, root.right = invert_tree(root.right), invert_tree(root.left)\n    return root',
          explanation: 'Swap children at each node.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(h)',
          isOptimal: true,
        },
      },
      {
        slug: 'maximum-depth-of-binary-tree',
        title: 'Maximum Depth of Binary Tree',
        description: 'Given the root of a binary tree, return its maximum depth.',
        difficulty: Difficulty.basic,
        hints: ['Depth = 1 + max(left, right)', 'Use BFS level count'],
        tags: ['tree', 'dfs', 'bfs'],
        testCases: [
          { input: '[3,9,20,null,null,15,7]', expectedOutput: '3', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Recursive DFS',
          code: 'def max_depth(root):\n    if not root:\n        return 0\n    return 1 + max(max_depth(root.left), max_depth(root.right))',
          explanation: 'Classic recursive depth.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(h)',
          isOptimal: true,
        },
      },
      {
        slug: 'validate-bst',
        title: 'Validate Binary Search Tree',
        description: 'Determine if a binary tree is a valid BST.',
        difficulty: Difficulty.intermediate,
        hints: ['Pass min/max bounds down the tree', 'Inorder should be strictly increasing'],
        tags: ['tree', 'bst'],
        testCases: [
          { input: '[2,1,3]', expectedOutput: 'true', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '[5,1,4,null,null,3,6]', expectedOutput: 'false', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Bounds DFS',
          code: 'def is_valid_bst(root, low=float("-inf"), high=float("inf")):\n    if not root:\n        return True\n    if not (low < root.val < high):\n        return False\n    return is_valid_bst(root.left, low, root.val) and is_valid_bst(root.right, root.val, high)',
          explanation: 'Each node must fit within valid range.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(h)',
          isOptimal: true,
        },
      },
      {
        slug: 'lowest-common-ancestor-bst',
        title: 'Lowest Common Ancestor of a BST',
        description: 'Find the lowest common ancestor of two given nodes in a BST.',
        difficulty: Difficulty.intermediate,
        hints: ['If both values smaller, go left', 'If both larger, go right'],
        tags: ['tree', 'bst'],
        testCases: [
          { input: 'root=[6,2,8,0,4,7,9], p=2, q=8', expectedOutput: '6', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'BST Property Walk',
          code: 'def lca(root, p, q):\n    while root:\n        if p.val < root.val and q.val < root.val:\n            root = root.left\n        elif p.val > root.val and q.val > root.val:\n            root = root.right\n        else:\n            return root',
          explanation: 'Walk from root using BST ordering.',
          timeComplexity: 'O(h)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'binary-tree-maximum-path-sum',
        title: 'Binary Tree Maximum Path Sum',
        description: 'Find the maximum path sum of any non-empty path in a binary tree.',
        difficulty: Difficulty.advanced,
        hints: ['At each node compute best path through it', 'Track global max separately'],
        tags: ['tree', 'dfs'],
        testCases: [
          { input: '[-10,9,20,null,null,15,7]', expectedOutput: '42', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Post-order DFS',
          code: 'def max_path_sum(root):\n    best = float("-inf")\n    def gain(node):\n        nonlocal best\n        if not node:\n            return 0\n        left = max(gain(node.left), 0)\n        right = max(gain(node.right), 0)\n        best = max(best, node.val + left + right)\n        return node.val + max(left, right)\n    gain(root)\n    return best',
          explanation: 'Return max gain upward; update global for through-path.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(h)',
          isOptimal: true,
        },
      },
    ],
  },
  {
    slug: 'graphs',
    name: 'Graphs',
    category: 'Graphs',
    description: 'Graph traversals, shortest paths, topological sort, and union-find.',
    difficultyLevel: Difficulty.intermediate,
    orderIndex: 5,
    iconUrl: '🕸️',
    questions: [
      {
        slug: 'number-of-islands',
        title: 'Number of Islands',
        description: 'Given a grid of `1`s (land) and `0`s (water), return the number of islands.',
        difficulty: Difficulty.intermediate,
        hints: ['DFS/BFS flood fill from each unvisited land cell', 'Mark visited cells'],
        tags: ['graph', 'dfs', 'bfs', 'matrix'],
        testCases: [
          { input: '4x5 grid with 1 islands', expectedOutput: '1', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'DFS Flood Fill',
          code: 'def num_islands(grid):\n    # DFS each land cell\n    pass',
          explanation: 'Count connected components of land.',
          timeComplexity: 'O(m * n)',
          spaceComplexity: 'O(m * n)',
          isOptimal: true,
        },
      },
      {
        slug: 'course-schedule',
        title: 'Course Schedule',
        description: 'Return true if you can finish all courses given prerequisites (detect cycle in directed graph).',
        difficulty: Difficulty.intermediate,
        hints: ['Topological sort with Kahn BFS', 'Or DFS cycle detection with 3-color'],
        tags: ['graph', 'topological-sort'],
        testCases: [
          { input: 'numCourses=2, prerequisites=[[1,0]]', expectedOutput: 'true', isSample: true, isHidden: false, orderIndex: 0 },
          { input: 'numCourses=2, prerequisites=[[1,0],[0,1]]', expectedOutput: 'false', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: "Kahn's Algorithm",
          code: 'def can_finish(numCourses, prerequisites):\n    # BFS topological sort\n    pass',
          explanation: 'Cycle exists iff not all nodes processed.',
          timeComplexity: 'O(V + E)',
          spaceComplexity: 'O(V + E)',
          isOptimal: true,
        },
      },
      {
        slug: 'clone-graph',
        title: 'Clone Graph',
        description: 'Return a deep copy of a connected undirected graph.',
        difficulty: Difficulty.intermediate,
        hints: ['Hash map from old node to clone', 'BFS/DFS to copy neighbors'],
        tags: ['graph', 'dfs', 'bfs'],
        testCases: [
          { input: 'adjList=[[2,4],[1,3],[2,4],[1,3]]', expectedOutput: 'deep copy', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'DFS with Hash Map',
          code: 'def clone_graph(node):\n    clones = {}\n    def dfs(n):\n        if n in clones:\n            return clones[n]\n        copy = Node(n.val)\n        clones[n] = copy\n        copy.neighbors = [dfs(nei) for nei in n.neighbors]\n        return copy\n    return dfs(node) if node else None',
          explanation: 'Memoize clones while traversing.',
          timeComplexity: 'O(V + E)',
          spaceComplexity: 'O(V)',
          isOptimal: true,
        },
      },
      {
        slug: 'network-delay-time',
        title: 'Network Delay Time',
        description: 'Given a network of nodes, return the time for all nodes to receive a signal from node k.',
        difficulty: Difficulty.advanced,
        hints: ["Dijkstra's shortest path from source k", 'Track max distance reached'],
        tags: ['graph', 'dijkstra', 'heap'],
        testCases: [
          { input: 'times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2', expectedOutput: '2', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: "Dijkstra's Algorithm",
          code: 'def network_delay_time(times, n, k):\n    # Min-heap Dijkstra\n    pass',
          explanation: 'Single-source shortest paths; answer is max dist.',
          timeComplexity: 'O(E log V)',
          spaceComplexity: 'O(V + E)',
          isOptimal: true,
        },
      },
      {
        slug: 'word-ladder',
        title: 'Word Ladder',
        description: 'Return the length of the shortest transformation sequence from beginWord to endWord.',
        difficulty: Difficulty.advanced,
        hints: ['BFS on implicit graph of one-letter edits', 'Use set for O(1) word lookup'],
        tags: ['graph', 'bfs'],
        testCases: [
          { input: 'beginWord=hit, endWord=cog, wordList=[hot,dot,dog,lot,log,cog]', expectedOutput: '5', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'BFS',
          code: 'def ladder_length(beginWord, endWord, wordList):\n    # BFS shortest path\n    pass',
          explanation: 'Each word is a node; edges differ by one letter.',
          timeComplexity: 'O(N * L^2)',
          spaceComplexity: 'O(N)',
          isOptimal: true,
        },
      },
    ],
  },
  {
    slug: 'dynamic-programming',
    name: 'Dynamic Programming',
    category: 'Dynamic Programming',
    description: 'Classic DP patterns: knapsack, LCS, LIS, and state transition problems.',
    difficultyLevel: Difficulty.intermediate,
    orderIndex: 6,
    iconUrl: '🧩',
    questions: [
      {
        slug: 'climbing-stairs',
        title: 'Climbing Stairs',
        description: 'You can climb 1 or 2 steps. In how many distinct ways can you climb to the top?',
        difficulty: Difficulty.basic,
        hints: ['ways(n) = ways(n-1) + ways(n-2)', 'Same as Fibonacci'],
        tags: ['dynamic-programming'],
        testCases: [
          { input: '2', expectedOutput: '2', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '3', expectedOutput: '3', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Bottom-up DP',
          code: 'def climb_stairs(n):\n    a, b = 1, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a',
          explanation: 'Rolling Fibonacci DP.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'house-robber',
        title: 'House Robber',
        description: 'Return the maximum amount you can rob without robbing two adjacent houses.',
        difficulty: Difficulty.intermediate,
        hints: ['At each house: rob it + i-2 or skip', 'Track prev and prevprev'],
        tags: ['dynamic-programming'],
        testCases: [
          { input: '1 2 3 1', expectedOutput: '4', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '2 7 9 3 1', expectedOutput: '12', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Linear DP',
          code: 'def rob(nums):\n    prev = curr = 0\n    for n in nums:\n        prev, curr = curr, max(curr, prev + n)\n    return curr',
          explanation: 'Cannot take adjacent houses.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'coin-change',
        title: 'Coin Change',
        description: 'Return the fewest number of coins needed to make up amount, or -1 if impossible.',
        difficulty: Difficulty.intermediate,
        hints: ['dp[a] = min coins for amount a', 'Try each coin and take min'],
        tags: ['dynamic-programming'],
        testCases: [
          { input: 'coins=[1,2,5], amount=11', expectedOutput: '3', isSample: true, isHidden: false, orderIndex: 0 },
          { input: 'coins=[2], amount=3', expectedOutput: '-1', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Unbounded Knapsack DP',
          code: 'def coin_change(coins, amount):\n    dp = [float("inf")] * (amount + 1)\n    dp[0] = 0\n    for a in range(1, amount + 1):\n        for c in coins:\n            if c <= a:\n                dp[a] = min(dp[a], dp[a - c] + 1)\n    return dp[amount] if dp[amount] != float("inf") else -1',
          explanation: 'Classic coin change DP.',
          timeComplexity: 'O(amount * coins)',
          spaceComplexity: 'O(amount)',
          isOptimal: true,
        },
      },
      {
        slug: 'longest-increasing-subsequence',
        title: 'Longest Increasing Subsequence',
        description: 'Return the length of the longest strictly increasing subsequence.',
        difficulty: Difficulty.advanced,
        hints: ['O(n log n) with patience sorting / tails array', 'Or O(n^2) DP'],
        tags: ['dynamic-programming', 'binary-search'],
        testCases: [
          { input: '10 9 2 5 3 7 101 18', expectedOutput: '4', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Patience Sorting',
          code: 'def length_of_lis(nums):\n    tails = []\n    for n in nums:\n        lo, hi = 0, len(tails)\n        while lo < hi:\n            mid = (lo + hi) // 2\n            if tails[mid] < n:\n                lo = mid + 1\n            else:\n                hi = mid\n        if lo == len(tails):\n            tails.append(n)\n        else:\n            tails[lo] = n\n    return len(tails)',
          explanation: 'Maintain smallest tail for each length.',
          timeComplexity: 'O(n log n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'edit-distance',
        title: 'Edit Distance',
        description: 'Return the minimum number of operations to convert word1 to word2.',
        difficulty: Difficulty.advanced,
        hints: ['Classic 2D DP on prefixes', 'Insert, delete, replace transitions'],
        tags: ['dynamic-programming', 'string'],
        testCases: [
          { input: 'horse, ros', expectedOutput: '3', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: '2D DP',
          code: 'def min_distance(word1, word2):\n    m, n = len(word1), len(word2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1):\n        dp[i][0] = i\n    for j in range(n + 1):\n        dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            cost = 0 if word1[i-1] == word2[j-1] else 1\n            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)\n    return dp[m][n]',
          explanation: 'Levenshtein distance DP.',
          timeComplexity: 'O(m * n)',
          spaceComplexity: 'O(m * n)',
          isOptimal: true,
        },
      },
    ],
  },
  {
    slug: 'hashing',
    name: 'Hashing',
    category: 'Hashing',
    description: 'Hash maps, frequency counting, and subarray/substring problems.',
    difficultyLevel: Difficulty.basic,
    orderIndex: 7,
    iconUrl: '#️⃣',
    questions: [
      {
        slug: 'contains-duplicate',
        title: 'Contains Duplicate',
        description: 'Return true if any value appears at least twice in the array.',
        difficulty: Difficulty.basic,
        hints: ['Use a set while iterating', 'Compare size of set vs array'],
        tags: ['array', 'hash-table'],
        testCases: [
          { input: '1 2 3 1', expectedOutput: 'true', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '1 2 3 4', expectedOutput: 'false', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Hash Set',
          code: 'def contains_duplicate(nums):\n    return len(set(nums)) != len(nums)',
          explanation: 'Set detects duplicates in one pass.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'group-anagrams',
        title: 'Group Anagrams',
        description: 'Group strings that are anagrams of each other.',
        difficulty: Difficulty.intermediate,
        hints: ['Use sorted string or char count as key', 'Hash map of key -> list'],
        tags: ['string', 'hash-table'],
        testCases: [
          { input: 'eat tea tan ate nat bat', expectedOutput: '[[eat,tea,ate],[tan,nat],[bat]]', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Hash Map by Signature',
          code: 'def group_anagrams(strs):\n    groups = {}\n    for s in strs:\n        key = tuple(sorted(s))\n        groups.setdefault(key, []).append(s)\n    return list(groups.values())',
          explanation: 'Anagrams share sorted tuple key.',
          timeComplexity: 'O(n * k log k)',
          spaceComplexity: 'O(n * k)',
          isOptimal: true,
        },
      },
      {
        slug: 'subarray-sum-equals-k',
        title: 'Subarray Sum Equals K',
        description: 'Return the total number of continuous subarrays whose sum equals k.',
        difficulty: Difficulty.intermediate,
        hints: ['Prefix sum + hash map of counts', 'Count how often prefix-k appeared'],
        tags: ['array', 'hash-table', 'prefix-sum'],
        testCases: [
          { input: '1 1 1, k=2', expectedOutput: '2', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Prefix Sum Hash Map',
          code: 'def subarray_sum(nums, k):\n    count = prefix = 0\n    freq = {0: 1}\n    for n in nums:\n        prefix += n\n        count += freq.get(prefix - k, 0)\n        freq[prefix] = freq.get(prefix, 0) + 1\n    return count',
          explanation: 'Prefix sums with complement counting.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'longest-consecutive-sequence',
        title: 'Longest Consecutive Sequence',
        description: 'Return the length of the longest consecutive elements sequence in unsorted array.',
        difficulty: Difficulty.intermediate,
        hints: ['Put all nums in a set', 'Only start sequences from sequence minimum'],
        tags: ['array', 'hash-table'],
        testCases: [
          { input: '100 4 200 1 3 2', expectedOutput: '4', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Hash Set Sequence Start',
          code: 'def longest_consecutive(nums):\n    nums_set = set(nums)\n    best = 0\n    for n in nums_set:\n        if n - 1 not in nums_set:\n            cur = n\n            length = 1\n            while cur + 1 in nums_set:\n                cur += 1\n                length += 1\n            best = max(best, length)\n    return best',
          explanation: 'Only expand from sequence starts.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
      {
        slug: 'top-k-frequent-elements',
        title: 'Top K Frequent Elements',
        description: 'Return the k most frequent elements.',
        difficulty: Difficulty.intermediate,
        hints: ['Count frequencies with hash map', 'Use bucket sort or heap for top k'],
        tags: ['array', 'hash-table', 'heap'],
        testCases: [
          { input: '1 1 1 2 2 3, k=2', expectedOutput: '1 2', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Bucket Sort by Frequency',
          code: 'def top_k_frequent(nums, k):\n    freq = {}\n    for n in nums:\n        freq[n] = freq.get(n, 0) + 1\n    buckets = [[] for _ in range(len(nums) + 1)]\n    for n, c in freq.items():\n        buckets[c].append(n)\n    res = []\n    for i in range(len(buckets) - 1, 0, -1):\n        for n in buckets[i]:\n            res.append(n)\n            if len(res) == k:\n                return res\n    return res',
          explanation: 'Bucket index = frequency.',
          timeComplexity: 'O(n)',
          spaceComplexity: 'O(n)',
          isOptimal: true,
        },
      },
    ],
  },
  {
    slug: 'sorting-searching',
    name: 'Sorting & Searching',
    category: 'Sorting',
    description: 'Classic sorting algorithms and binary search variations.',
    difficultyLevel: Difficulty.basic,
    orderIndex: 8,
    iconUrl: '🔍',
    questions: [
      {
        slug: 'binary-search',
        title: 'Binary Search',
        description: 'Given a sorted array and target, return the index of target or -1.',
        difficulty: Difficulty.basic,
        hints: ['Maintain left and right bounds', 'Compare mid and shrink range'],
        tags: ['array', 'binary-search'],
        testCases: [
          { input: '5\n-1 0 3 5 9 12\n9', expectedOutput: '4', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '2\n-1 0 3 5 9 12\n2', expectedOutput: '-1', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Classic Binary Search',
          code: 'def search(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1',
          explanation: 'Standard binary search on sorted array.',
          timeComplexity: 'O(log n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'search-insert-position',
        title: 'Search Insert Position',
        description: 'Return the index where target would be inserted in sorted array.',
        difficulty: Difficulty.basic,
        hints: ['Binary search for first index >= target', 'Return lo when loop ends'],
        tags: ['array', 'binary-search'],
        testCases: [
          { input: '4\n1 3 5 6\n5', expectedOutput: '2', isSample: true, isHidden: false, orderIndex: 0 },
          { input: '4\n1 3 5 6\n2', expectedOutput: '1', isSample: true, isHidden: false, orderIndex: 1 },
        ],
        solution: {
          language: 'python',
          approachName: 'Lower Bound Binary Search',
          code: 'def search_insert(nums, target):\n    lo, hi = 0, len(nums)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo',
          explanation: 'Find leftmost insertion point.',
          timeComplexity: 'O(log n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'find-first-and-last-position',
        title: 'Find First and Last Position of Element in Sorted Array',
        description: 'Find starting and ending position of target in sorted array.',
        difficulty: Difficulty.intermediate,
        hints: ['Run binary search for left bound', 'Run binary search for right bound'],
        tags: ['array', 'binary-search'],
        testCases: [
          { input: '6\n5 7 7 8 8 10\n8', expectedOutput: '3 4', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Two Binary Searches',
          code: 'def search_range(nums, target):\n    def bound(find_left):\n        lo, hi = 0, len(nums)\n        while lo < hi:\n            mid = (lo + hi) // 2\n            if nums[mid] < target or (find_left and nums[mid] == target and mid > 0 and nums[mid-1] == target):\n                lo = mid + 1\n            else:\n                hi = mid\n        return lo\n    left = bound(True)\n    if left == len(nums) or nums[left] != target:\n        return [-1, -1]\n    return [left, bound(False) - 1]',
          explanation: 'Separate lower/upper bound searches.',
          timeComplexity: 'O(log n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'search-in-rotated-sorted-array',
        title: 'Search in Rotated Sorted Array',
        description: 'Search target in rotated sorted array with distinct values.',
        difficulty: Difficulty.intermediate,
        hints: ['Identify which half is sorted', 'Decide which half contains target'],
        tags: ['array', 'binary-search'],
        testCases: [
          { input: '7\n4 5 6 7 0 1 2\n0', expectedOutput: '4', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Modified Binary Search',
          code: 'def search_rotated(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[lo] <= nums[mid]:\n            if nums[lo] <= target < nums[mid]:\n                hi = mid - 1\n            else:\n                lo = mid + 1\n        else:\n            if nums[mid] < target <= nums[hi]:\n                lo = mid + 1\n            else:\n                hi = mid - 1\n    return -1',
          explanation: 'Binary search with rotated invariant.',
          timeComplexity: 'O(log n)',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
      {
        slug: 'kth-largest-element',
        title: 'Kth Largest Element in an Array',
        description: 'Find the kth largest element in an unsorted array.',
        difficulty: Difficulty.intermediate,
        hints: ['Quickselect average O(n)', 'Or min-heap of size k'],
        tags: ['array', 'heap', 'quickselect'],
        testCases: [
          { input: '6\n3 2 1 5 6 4\n2', expectedOutput: '5', isSample: true, isHidden: false, orderIndex: 0 },
        ],
        solution: {
          language: 'python',
          approachName: 'Quickselect',
          code: 'def find_kth_largest(nums, k):\n    # Quickselect partition\n    pass',
          explanation: 'Partition around pivot like quicksort.',
          timeComplexity: 'O(n) average',
          spaceComplexity: 'O(1)',
          isOptimal: true,
        },
      },
    ],
  },
];

async function seedTopic(topicData: SeedTopic): Promise<void> {
  const topic = await prisma.topic.upsert({
    where: { slug: topicData.slug },
    update: {
      topicName: topicData.name,
      category: topicData.category,
      description: topicData.description,
      difficultyLevel: topicData.difficultyLevel,
      orderIndex: topicData.orderIndex,
      iconUrl: topicData.iconUrl,
      totalQuestions: topicData.questions.length,
      isActive: true,
    },
    create: {
      slug: topicData.slug,
      topicName: topicData.name,
      category: topicData.category,
      description: topicData.description,
      difficultyLevel: topicData.difficultyLevel,
      orderIndex: topicData.orderIndex,
      iconUrl: topicData.iconUrl,
      prerequisites: [],
      totalQuestions: topicData.questions.length,
    },
  });

  for (const q of topicData.questions) {
    const question = await prisma.question.upsert({
      where: { slug: q.slug },
      update: {
        title: q.title,
        description: q.description,
        difficulty: q.difficulty,
        constraints: q.constraints ?? null,
        hints: q.hints,
        tags: q.tags,
        source: QuestionSource.internal,
        isActive: true,
        topicId: topic.topicId,
      },
      create: {
        topicId: topic.topicId,
        slug: q.slug,
        title: q.title,
        description: q.description,
        difficulty: q.difficulty,
        constraints: q.constraints ?? null,
        hints: q.hints,
        tags: q.tags,
        source: QuestionSource.internal,
      },
    });

    await prisma.testCase.deleteMany({ where: { questionId: question.questionId } });
    await prisma.testCase.createMany({
      data: q.testCases.map((tc) => ({
        questionId: question.questionId,
        input: tc.input,
        expectedOutput: tc.expectedOutput,
        explanation: tc.explanation ?? null,
        isSample: tc.isSample,
        isHidden: tc.isHidden,
        orderIndex: tc.orderIndex,
      })),
    });

    await prisma.solution.deleteMany({ where: { questionId: question.questionId } });
    await prisma.solution.create({
      data: {
        questionId: question.questionId,
        language: q.solution.language,
        approachName: q.solution.approachName,
        code: q.solution.code,
        explanation: q.solution.explanation,
        timeComplexity: q.solution.timeComplexity,
        spaceComplexity: q.solution.spaceComplexity,
        isOptimal: q.solution.isOptimal,
      },
    });
  }
}

async function main(): Promise<void> {
  console.log('🌱 Seeding database...');

  for (const topic of TOPICS) {
    await seedTopic(topic);
    console.log(`  ✓ ${topic.name} (${topic.questions.length} questions)`);
  }

  const [topicCount, questionCount] = await Promise.all([
    prisma.topic.count(),
    prisma.question.count(),
  ]);

  console.log(`\n✅ Seed complete: ${topicCount} topics, ${questionCount} questions`);
}

main()
  .catch((error) => {
    console.error('Seed failed:', error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
