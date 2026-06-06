"""
seeds/questions_python_loops.py
----------------------------------
Python Learning Studio — Module 05: Loops & Iteration
18 exercises: 6 basic, 6 intermediate, 6 advanced

Usage:
    python -m seeds.questions_python_loops
"""

import asyncio

from seeds.loader import seed_questions_for_topic

TOPIC_SLUG = "loops"

QUESTIONS = [
    # ── BASIC ────────────────────────────────────────────────────────────────
    {
        "title": "Count to Five",
        "slug": "py-loop-count-five",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Count to Five\n\nUse a `for` loop with `range()` to print 1 through 5, each on its own line.\n\n**Expected output:**\n```\n1\n2\n3\n4\n5\n```\n",
        "starter_code": "# for loop printing 1 to 5\n",
        "expected_output": "1\n2\n3\n4\n5",
        "tags": ["loops", "for", "range"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "for i in range(1, 6):\n    print(i)", "explanation": "range(1, 6) produces 1, 2, 3, 4, 5.", "is_optimal": True}],
    },
    {
        "title": "While Loop Countdown",
        "slug": "py-loop-while-countdown",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## While Loop Countdown\n\nUse a `while` loop to count down from 3 to 1.\n\n**Expected output:**\n```\n3\n2\n1\n```\n",
        "starter_code": "n = 3\n# while loop countdown\n",
        "expected_output": "3\n2\n1",
        "tags": ["loops", "while"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "n = 3\nwhile n > 0:\n    print(n)\n    n -= 1", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Sum with a Loop",
        "slug": "py-loop-sum",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Sum with a Loop\n\nSum integers 1 through 10 with a `for` loop and print the result.\n\n**Expected output:**\n```\n55\n```\n",
        "starter_code": "total = 0\n# sum 1 to 10\nprint(total)\n",
        "expected_output": "55",
        "tags": ["loops", "for", "range"],
        "xp_reward": 8,
        "solutions": [{"title": "Solution", "code": "total = 0\nfor i in range(1, 11):\n    total += i\nprint(total)", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "break Statement",
        "slug": "py-loop-break",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## break Statement\n\nLoop through `range(10)` and break when `i == 3`. Print `i` at that point.\n\n**Expected output:**\n```\n3\n```\n",
        "starter_code": "for i in range(10):\n    # break when i == 3\n    pass\n",
        "expected_output": "3",
        "tags": ["loops", "break"],
        "xp_reward": 8,
        "solutions": [{"title": "Solution", "code": "for i in range(10):\n    if i == 3:\n        print(i)\n        break", "explanation": "break exits the loop immediately.", "is_optimal": True}],
    },
    {
        "title": "continue Statement",
        "slug": "py-loop-continue",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## continue Statement\n\nPrint only even numbers from 1 to 10 using `continue`.\n\n**Expected output:**\n```\n2\n4\n6\n8\n10\n```\n",
        "starter_code": "for i in range(1, 11):\n    # skip odd numbers\n    pass\n",
        "expected_output": "2\n4\n6\n8\n10",
        "tags": ["loops", "continue"],
        "xp_reward": 8,
        "solutions": [{"title": "Solution", "code": "for i in range(1, 11):\n    if i % 2 != 0:\n        continue\n    print(i)", "explanation": "continue skips the rest of the loop body for that iteration.", "is_optimal": True}],
    },
    {
        "title": "Iterate over a List",
        "slug": "py-loop-list",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Iterate over a List\n\nPrint each item in `['apple', 'banana', 'cherry']`.\n\n**Expected output:**\n```\napple\nbanana\ncherry\n```\n",
        "starter_code": "fruits = ['apple', 'banana', 'cherry']\n# print each fruit\n",
        "expected_output": "apple\nbanana\ncherry",
        "tags": ["loops", "for", "list"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "fruits = ['apple', 'banana', 'cherry']\nfor fruit in fruits:\n    print(fruit)", "explanation": "", "is_optimal": True}],
    },
    # ── INTERMEDIATE ─────────────────────────────────────────────────────────
    {
        "title": "enumerate()",
        "slug": "py-loop-enumerate",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## enumerate()\n\nPrint each item with its 1-based index from `['a', 'b', 'c']`.\n\n**Expected output:**\n```\n1 a\n2 b\n3 c\n```\n",
        "starter_code": "items = ['a', 'b', 'c']\n# use enumerate with start=1\n",
        "expected_output": "1 a\n2 b\n3 c",
        "tags": ["loops", "enumerate"],
        "xp_reward": 15,
        "solutions": [{"title": "Solution", "code": "items = ['a', 'b', 'c']\nfor i, v in enumerate(items, start=1):\n    print(i, v)", "explanation": "enumerate(start=1) gives 1-based indexing.", "is_optimal": True}],
    },
    {
        "title": "zip() Two Lists",
        "slug": "py-loop-zip",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## zip() Two Lists\n\nPair `names = ['Alice', 'Bob']` with `scores = [90, 85]` and print each pair.\n\n**Expected output:**\n```\nAlice 90\nBob 85\n```\n",
        "starter_code": "names = ['Alice', 'Bob']\nscores = [90, 85]\n# zip and print\n",
        "expected_output": "Alice 90\nBob 85",
        "tags": ["loops", "zip"],
        "xp_reward": 15,
        "solutions": [{"title": "Solution", "code": "names = ['Alice', 'Bob']\nscores = [90, 85]\nfor name, score in zip(names, scores):\n    print(name, score)", "explanation": "zip() creates pairs from two iterables.", "is_optimal": True}],
    },
    {
        "title": "loop-else Clause",
        "slug": "py-loop-else",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## loop-else Clause\n\nSearch for `7` in `[1, 2, 3, 4, 5]`. Print `'not found'` if not present (use for-else).\n\n**Expected output:**\n```\nnot found\n```\n",
        "starter_code": "nums = [1, 2, 3, 4, 5]\n# for-else to search for 7\n",
        "expected_output": "not found",
        "tags": ["loops", "for-else"],
        "xp_reward": 20,
        "solutions": [
            {
                "title": "Solution",
                "code": "nums = [1, 2, 3, 4, 5]\nfor n in nums:\n    if n == 7:\n        print('found')\n        break\nelse:\n    print('not found')",
                "explanation": "The else clause of a for loop runs only if no break was triggered.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Nested Loops — Multiplication Table",
        "slug": "py-loop-nested",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Nested Loops\n\nPrint the 2×2 multiplication table (rows 1-2, cols 1-2).\n\n**Expected output:**\n```\n1 2\n2 4\n```\n",
        "starter_code": "# nested loop multiplication table\n",
        "expected_output": "1 2\n2 4",
        "tags": ["loops", "nested"],
        "xp_reward": 15,
        "solutions": [
            {
                "title": "Solution",
                "code": "for i in range(1, 3):\n    print(' '.join(str(i * j) for j in range(1, 3)))",
                "explanation": "Nested loops iterate over row and column indices.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "range() Step Parameter",
        "slug": "py-loop-range-step",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## range() with Step\n\nPrint every 3rd number from 0 to 12 (inclusive).\n\n**Expected output:**\n```\n0\n3\n6\n9\n12\n```\n",
        "starter_code": "# use range with step=3\n",
        "expected_output": "0\n3\n6\n9\n12",
        "tags": ["loops", "range"],
        "xp_reward": 10,
        "solutions": [{"title": "Solution", "code": "for i in range(0, 13, 3):\n    print(i)", "explanation": "range(start, stop, step) generates values with the given step.", "is_optimal": True}],
    },
    {
        "title": "Flatten Nested List",
        "slug": "py-loop-flatten",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Flatten Nested List\n\nFlatten `[[1, 2], [3, 4], [5]]` into a single list and print it.\n\n**Expected output:**\n```\n[1, 2, 3, 4, 5]\n```\n",
        "starter_code": "nested = [[1, 2], [3, 4], [5]]\n# flatten into one list\n",
        "expected_output": "[1, 2, 3, 4, 5]",
        "tags": ["loops", "nested", "list"],
        "xp_reward": 20,
        "solutions": [
            {
                "title": "Solution",
                "code": "nested = [[1, 2], [3, 4], [5]]\nflat = [x for sub in nested for x in sub]\nprint(flat)",
                "explanation": "A nested list comprehension with two for clauses flattens one level.",
                "is_optimal": True,
            }
        ],
    },
    # ── ADVANCED ─────────────────────────────────────────────────────────────
    {
        "title": "Custom __iter__ and __next__",
        "slug": "py-loop-custom-iter",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": "## Custom Iterator\n\nImplement a `Countdown` class that counts from 3 to 1 using `__iter__` and `__next__`. Print each value.\n\n**Expected output:**\n```\n3\n2\n1\n```\n",
        "starter_code": "class Countdown:\n    def __init__(self, start):\n        self.current = start\n\n    def __iter__(self):\n        pass  # return self\n\n    def __next__(self):\n        pass  # implement countdown\n\nfor n in Countdown(3):\n    print(n)\n",
        "expected_output": "3\n2\n1",
        "tags": ["advanced", "iteration-protocol", "dunder"],
        "xp_reward": 30,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "class Countdown:\n"
                    "    def __init__(self, start):\n"
                    "        self.current = start\n\n"
                    "    def __iter__(self):\n"
                    "        return self\n\n"
                    "    def __next__(self):\n"
                    "        if self.current <= 0:\n"
                    "            raise StopIteration\n"
                    "        val = self.current\n"
                    "        self.current -= 1\n"
                    "        return val\n\n"
                    "for n in Countdown(3):\n"
                    "    print(n)\n"
                ),
                "explanation": "__iter__ returns self; __next__ raises StopIteration when exhausted.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Infinite Generator with yield",
        "slug": "py-loop-infinite-gen",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Infinite Generator\n\nCreate a generator `naturals()` that yields 1, 2, 3, … indefinitely. Print the first 4 values.\n\n**Expected output:**\n```\n1\n2\n3\n4\n```\n",
        "starter_code": "def naturals():\n    # infinite generator\n    pass\n\n# print first 4\n",
        "expected_output": "1\n2\n3\n4",
        "tags": ["advanced", "generators", "yield"],
        "xp_reward": 30,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "def naturals():\n"
                    "    n = 1\n"
                    "    while True:\n"
                    "        yield n\n"
                    "        n += 1\n\n"
                    "gen = naturals()\n"
                    "for _ in range(4):\n"
                    "    print(next(gen))\n"
                ),
                "explanation": "A generator function with yield creates a lazy infinite sequence.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "itertools.chain",
        "slug": "py-loop-itertools-chain",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## itertools.chain\n\nChain `[1, 2]` and `[3, 4]` with `itertools.chain` and print each element.\n\n**Expected output:**\n```\n1\n2\n3\n4\n```\n",
        "starter_code": "import itertools\n# chain the two lists\n",
        "expected_output": "1\n2\n3\n4",
        "tags": ["advanced", "itertools"],
        "xp_reward": 25,
        "solutions": [{"title": "Solution", "code": "import itertools\nfor x in itertools.chain([1, 2], [3, 4]):\n    print(x)", "explanation": "itertools.chain() lazily joins iterables end-to-end.", "is_optimal": True}],
    },
    {
        "title": "itertools.takewhile",
        "slug": "py-loop-takewhile",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## itertools.takewhile\n\nUse `itertools.takewhile` to take elements from `[1, 3, 5, 2, 4]` while they are odd. Print each.\n\n**Expected output:**\n```\n1\n3\n5\n```\n",
        "starter_code": "import itertools\nnums = [1, 3, 5, 2, 4]\n# use takewhile with odd predicate\n",
        "expected_output": "1\n3\n5",
        "tags": ["advanced", "itertools", "generators"],
        "xp_reward": 30,
        "solutions": [{"title": "Solution", "code": "import itertools\nnums = [1, 3, 5, 2, 4]\nfor n in itertools.takewhile(lambda x: x % 2 != 0, nums):\n    print(n)", "explanation": "takewhile stops as soon as the predicate returns False.", "is_optimal": True}],
    },
    {
        "title": "Loop Unrolling with zip",
        "slug": "py-loop-unroll-zip",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Loop Unrolling — Pairwise Sum\n\nCompute the pairwise sum of `[1, 2, 3]` and `[4, 5, 6]` using `zip` and list comprehension.\n\n**Expected output:**\n```\n[5, 7, 9]\n```\n",
        "starter_code": "a = [1, 2, 3]\nb = [4, 5, 6]\n# pairwise sum with zip\n",
        "expected_output": "[5, 7, 9]",
        "tags": ["advanced", "zip", "comprehension"],
        "xp_reward": 25,
        "solutions": [{"title": "Solution", "code": "a = [1, 2, 3]\nb = [4, 5, 6]\nprint([x + y for x, y in zip(a, b)])", "explanation": "zip() pairs elements; the comprehension sums each pair.", "is_optimal": True}],
    },
    {
        "title": "Generator Pipeline",
        "slug": "py-loop-gen-pipeline",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": "## Generator Pipeline\n\nBuild a two-stage generator pipeline: `double(nums)` yields each value×2, then `take(gen, n)` yields first n items. Print the first 3 doubled values of `range(10)`.\n\n**Expected output:**\n```\n0\n2\n4\n```\n",
        "starter_code": "def double(nums):\n    pass  # yield each * 2\n\ndef take(gen, n):\n    pass  # yield first n items\n\nfor v in take(double(range(10)), 3):\n    print(v)\n",
        "expected_output": "0\n2\n4",
        "tags": ["advanced", "generators", "pipeline"],
        "xp_reward": 35,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "def double(nums):\n"
                    "    for n in nums:\n"
                    "        yield n * 2\n\n"
                    "def take(gen, n):\n"
                    "    for _ in range(n):\n"
                    "        yield next(gen)\n\n"
                    "for v in take(double(range(10)), 3):\n"
                    "    print(v)\n"
                ),
                "explanation": "Generator pipelines process data lazily, one element at a time.",
                "is_optimal": True,
            }
        ],
    },
]


async def main() -> None:
    n = await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 05 — Loops & Iteration")
    print(f"Seeded {n} questions for {TOPIC_SLUG}")


if __name__ == "__main__":
    asyncio.run(main())
