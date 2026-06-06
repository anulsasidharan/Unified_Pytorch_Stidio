import type { Lesson, LessonDifficulty, ModuleCurriculum } from "../types";
import { MODULE_LIST, type ModuleMeta } from "@/lib/module-meta";

const SAMPLE_BY_SLUG: Record<string, { title: string; code: string; explanation: string }[]> = {
  "python-basics": [
    {
      title: "Hello, Python",
      code: 'print("Hello, Python!")',
      explanation: "Every script can start with print() to verify your environment works.",
    },
    {
      title: "Main guard",
      code: 'def main():\n    print("ready")\n\nif __name__ == "__main__":\n    main()',
      explanation: "The __name__ guard keeps import side effects out of reusable modules.",
    },
  ],
  "variables-types": [
    {
      title: "Inspect types",
      code: "value = 42\nprint(type(value))",
      explanation: "type() reveals the runtime class of any object.",
    },
    {
      title: "Identity vs equality",
      code: "a = [1, 2]\nb = [1, 2]\nprint(a == b, a is b)",
      explanation: "== compares values; is compares object identity.",
    },
  ],
  strings: [
    {
      title: "f-strings",
      code: 'name = "Ada"\nprint(f"Hello, {name}!")',
      explanation: "f-strings embed expressions directly in string literals.",
    },
    {
      title: "Split and join",
      code: 'parts = "a,b,c".split(",")\nprint("-".join(parts))',
      explanation: "split() tokenizes text; join() rebuilds delimited strings efficiently.",
    },
  ],
  "control-flow": [
    {
      title: "if / elif / else",
      code: "score = 85\nif score >= 90:\n    grade = \"A\"\nelif score >= 80:\n    grade = \"B\"\nelse:\n    grade = \"C\"\nprint(grade)",
      explanation: "Branch on conditions to handle different input cases.",
    },
    {
      title: "match-case",
      code: "status = 404\nmatch status:\n    case 200:\n        print(\"ok\")\n    case 404:\n        print(\"not found\")\n    case _:\n        print(\"other\")",
      explanation: "Structural pattern matching replaces long elif chains for discrete values.",
    },
  ],
  loops: [
    {
      title: "for with range",
      code: "total = 0\nfor i in range(1, 4):\n    total += i\nprint(total)",
      explanation: "range() produces a sequence of integers for counted loops.",
    },
    {
      title: "enumerate and zip",
      code: 'names = ["Ada", "Bob"]\nscores = [90, 85]\nfor i, (n, s) in enumerate(zip(names, scores)):\n    print(i, n, s)',
      explanation: "enumerate adds indices; zip walks multiple sequences in parallel.",
    },
  ],
  "lists-tuples": [
    {
      title: "List basics",
      code: "items = [1, 2, 3]\nitems.append(4)\nprint(items[-1])",
      explanation: "Lists are mutable ordered sequences — ideal for collections that change.",
    },
    {
      title: "Tuple unpacking",
      code: "point = (3, 4)\nx, y = point\nprint(x + y)",
      explanation: "Tuples are immutable; unpacking assigns multiple names in one step.",
    },
  ],
  "dicts-sets": [
    {
      title: "Dict lookup",
      code: 'user = {"name": "Ana"}\nprint(user.get("role", "guest"))',
      explanation: "get() returns a default when a key is missing instead of raising KeyError.",
    },
    {
      title: "Set operations",
      code: "a, b = {1, 2}, {2, 3}\nprint(sorted(a & b))",
      explanation: "Sets model unique membership and support fast union/intersection.",
    },
  ],
  functions: [
    {
      title: "Define a function",
      code: 'def greet(name="world"):\n    return f"hi {name}"\nprint(greet())',
      explanation: "Functions encapsulate reusable logic with parameters and return values.",
    },
    {
      title: "*args",
      code: "def total(*nums):\n    return sum(nums)\nprint(total(1, 2, 3))",
      explanation: "*args collects extra positional arguments into a tuple.",
    },
  ],
  oop: [
    {
      title: "Simple class",
      code: 'class User:\n    def __init__(self, name):\n        self.name = name\nprint(User("Ada").name)',
      explanation: "Classes bundle data (attributes) and behavior (methods) into one type.",
    },
    {
      title: "@property",
      code: "class Circle:\n    def __init__(self, r):\n        self.r = r\n    @property\n    def area(self):\n        return 3.14 * self.r ** 2\nprint(Circle(2).area)",
      explanation: "Properties expose computed attributes with method-like logic.",
    },
  ],
  "dunder-methods": [
    {
      title: "__repr__",
      code: 'class Item:\n    def __init__(self, name):\n        self.name = name\n    def __repr__(self):\n        return f"Item({self.name!r})"\nprint(repr(Item("book")))',
      explanation: "__repr__ should be unambiguous — aimed at developers debugging objects.",
    },
    {
      title: "Context manager",
      code: 'class Managed:\n    def __enter__(self):\n        print("open")\n        return self\n    def __exit__(self, *args):\n        print("close")\nwith Managed():\n    pass',
      explanation: "__enter__/__exit__ guarantee cleanup even when errors occur.",
    },
  ],
  "modules-packages": [
    {
      title: "Import styles",
      code: "from math import sqrt\nprint(round(sqrt(9), 2))",
      explanation: "Import only what you need to keep namespaces clear.",
    },
    {
      title: "Package __all__",
      code: '__all__ = ["add"]\ndef add(a, b):\n    return a + b\nprint(__all__)',
      explanation: "__all__ documents the public API when using from package import *.",
    },
  ],
  "file-io": [
    {
      title: "Pathlib",
      code: 'from pathlib import Path\np = Path("data") / "app.json"\nprint(p.suffix)',
      explanation: "pathlib replaces os.path string juggling with object-oriented paths.",
    },
    {
      title: "JSON",
      code: 'import json\nprint(json.loads(\'{"x": 1}\')["x"])',
      explanation: "json.loads/dumps convert between Python objects and JSON text.",
    },
  ],
  exceptions: [
    {
      title: "try / except",
      code: 'try:\n    int("x")\nexcept ValueError:\n    print("bad number")',
      explanation: "Catch specific exceptions instead of bare except to avoid hiding bugs.",
    },
    {
      title: "Custom exception",
      code: 'class AppError(Exception):\n    pass\ntry:\n    raise AppError("fail")\nexcept AppError:\n    print("handled")',
      explanation: "Domain-specific exceptions make error handling self-documenting.",
    },
  ],
  "iterators-generators": [
    {
      title: "Generator",
      code: "def count_to(n):\n    for i in range(1, n + 1):\n        yield i\nprint(list(count_to(3)))",
      explanation: "yield pauses a function and produces values lazily, saving memory.",
    },
    {
      title: "iter / next",
      code: "it = iter([1, 2])\nprint(next(it))",
      explanation: "The iterator protocol powers for loops under the hood.",
    },
  ],
  decorators: [
    {
      title: "Simple decorator",
      code: 'def logged(fn):\n    def wrapper(*a, **k):\n        print("call")\n        return fn(*a, **k)\n    return wrapper\n@logged\ndef add(a, b):\n    return a + b\nprint(add(1, 2))',
      explanation: "Decorators wrap functions to add cross-cutting behavior.",
    },
    {
      title: "@lru_cache",
      code: "from functools import lru_cache\n@lru_cache\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\nprint(fib(10))",
      explanation: "Memoization caches pure function results for repeated inputs.",
    },
  ],
  functional: [
    {
      title: "map and filter",
      code: "nums = [1, 2, 3, 4]\nprint(list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, nums))))",
      explanation: "map transforms; filter selects — building blocks of functional style.",
    },
    {
      title: "reduce",
      code: "from functools import reduce\nprint(reduce(lambda a, b: a + b, [1, 2, 3, 4]))",
      explanation: "reduce folds a sequence into a single accumulated value.",
    },
  ],
  comprehensions: [
    {
      title: "List comprehension",
      code: "print([x for x in range(6) if x % 2 == 0])",
      explanation: "Comprehensions combine looping, filtering, and mapping in one expression.",
    },
    {
      title: "Dict comprehension",
      code: 'print({c: ord(c) for c in "ab"})',
      explanation: "Dict comprehensions build mappings concisely from iterables.",
    },
  ],
  "type-hints": [
    {
      title: "Basic annotations",
      code: "def add(a: int, b: int) -> int:\n    return a + b\nprint(add(2, 3))",
      explanation: "Type hints document intent and enable static analysis with mypy.",
    },
    {
      title: "Optional",
      code: 'from typing import Optional\ndef greet(name: Optional[str] = None) -> str:\n    return f"hi {name or \'guest\'}"\nprint(greet())',
      explanation: "Optional[T] means the value may be T or None.",
    },
  ],
  testing: [
    {
      title: "assert in tests",
      code: 'def double(x):\n    return x * 2\nassert double(2) == 4\nprint("pass")',
      explanation: "assert states expected behavior; pytest collects assert failures as test results.",
    },
    {
      title: "unittest.mock",
      code: 'from unittest.mock import patch\nwith patch("builtins.len", return_value=5):\n    print(len([1, 2, 3]))',
      explanation: "Mocks isolate the unit under test from external dependencies.",
    },
  ],
  stdlib: [
    {
      title: "dataclass",
      code: 'from dataclasses import dataclass\n@dataclass\nclass User:\n    name: str\nprint(User("Ada").name)',
      explanation: "dataclasses auto-generate __init__, __repr__, and comparison methods.",
    },
    {
      title: "collections.deque",
      code: "from collections import deque\nd = deque([1, 2, 3])\nd.appendleft(0)\nprint(list(d))",
      explanation: "deque offers O(1) append/pop from both ends — great for queues.",
    },
  ],
  concurrency: [
    {
      title: "Thread",
      code: 'import threading\ndef work():\n    print("thread")\nt = threading.Thread(target=work)\nt.start()\nt.join()',
      explanation: "Threads share memory — good for I/O-bound work, limited by the GIL for CPU work.",
    },
    {
      title: "ThreadPoolExecutor",
      code: "from concurrent.futures import ThreadPoolExecutor\nwith ThreadPoolExecutor(max_workers=2) as ex:\n    print(list(ex.map(lambda x: x * 2, [1, 2, 3])))",
      explanation: "Executors manage a pool of workers and simplify submitting tasks.",
    },
  ],
  async: [
    {
      title: "async / await",
      code: "import asyncio\nasync def main():\n    return 42\nprint(asyncio.run(main()))",
      explanation: "Coroutines cooperatively yield control while waiting on I/O.",
    },
    {
      title: "asyncio.gather",
      code: "import asyncio\nasync def one():\n    return 1\nasync def main():\n    return sum(await asyncio.gather(one(), one()))\nprint(asyncio.run(main()))",
      explanation: "gather runs multiple coroutines concurrently on one event loop.",
    },
  ],
  performance: [
    {
      title: "timeit",
      code: 'import timeit\nprint(timeit.timeit("1 + 1", number=1000) > 0)',
      explanation: "Measure before optimizing — timeit runs micro-benchmarks reliably.",
    },
    {
      title: "__slots__",
      code: "class Point:\n    __slots__ = (\"x\", \"y\")\n    def __init__(self, x, y):\n        self.x, self.y = x, y\nprint(Point(1, 2).x)",
      explanation: "__slots__ reduces per-instance memory by fixing attribute layout.",
    },
  ],
  "design-patterns": [
    {
      title: "Strategy",
      code: 'def add(a, b):\n    return a + b\ndef mul(a, b):\n    return a * b\nops = {"+": add, "*": mul}\nprint(ops["+"](2, 3))',
      explanation: "Strategy swaps algorithms at runtime via a shared interface.",
    },
    {
      title: "Factory",
      code: 'def make(kind):\n    return {"list": list, "set": set}[kind]()\nprint(type(make("list")).__name__)',
      explanation: "Factories centralize object creation behind a simple API.",
    },
  ],
  "data-scripting": [
    {
      title: "argparse",
      code: 'import argparse\np = argparse.ArgumentParser()\np.add_argument("--name", default="world")\nargs = p.parse_args([])\nprint(args.name)',
      explanation: "argparse builds CLI interfaces with flags, help text, and validation.",
    },
    {
      title: "csv.DictReader",
      code: 'import csv\nfrom io import StringIO\nr = csv.DictReader(StringIO("name,score\\nAda,10\\n"))\nprint(list(r)[0]["name"])',
      explanation: "DictReader maps CSV rows to dictionaries keyed by column name.",
    },
  ],
};

function lessonTitle(level: LessonDifficulty): string {
  return (
    { basic: "Core concepts", intermediate: "Applied patterns", advanced: "Deep dive" } as const
  )[level];
}

function buildMermaid(slug: string, level: LessonDifficulty): string {
  const label = slug.replace(/-/g, " ");
  return `flowchart LR
  A["${label}<br/>${level}"] --> B["Practice exercises"]
  B --> C["Mini project"]`;
}

function buildCurriculum(meta: ModuleMeta, slug: string): ModuleCurriculum {
  const samples = SAMPLE_BY_SLUG[slug] ?? [
    {
      title: "Runnable example",
      code: 'print("Hello, Python!")',
      explanation: "Run code in the editor to reinforce this module's concepts.",
    },
  ];

  const levels: LessonDifficulty[] = ["basic", "intermediate", "advanced"];

  return {
    topicSlug: slug,
    intro: {
      overview: [
        meta.description,
        `This module covers ${meta.name} across three tiers — basic foundations, intermediate patterns, and advanced internals.`,
        `Capstone: ${meta.mini_project}`,
      ],
      learningPath: [
        "Read the tier lessons for this module",
        "Run the sample code in the editor",
        "Complete practice exercises at each difficulty",
        "Build the end-of-module mini project",
      ],
      prerequisites:
        meta.module_number <= 1
          ? ["No prior Python required"]
          : [`Modules 1–${meta.module_number - 1} recommended`],
    },
    lessons: levels.map((level, idx) => ({
      slug: `${level}-concepts`,
      title: lessonTitle(level),
      order: idx + 1,
      difficulty: level,
      summary: meta.levels[level],
      explanation: [
        `**${level.charAt(0).toUpperCase() + level.slice(1)} tier:** ${meta.levels[level]}`,
        "Work through the sample code, then open the linked practice exercises to apply what you learned.",
        level === "advanced"
          ? "Advanced topics connect language internals to real-world design and performance trade-offs."
          : level === "intermediate"
            ? "Intermediate topics bridge syntax basics with patterns you will use in production code."
            : "Basic topics establish vocabulary and muscle memory for every later module.",
      ],
      mermaid: buildMermaid(slug, level),
      diagramCaption: `${meta.name} — ${level} learning path`,
      sampleCode: [samples[idx] ?? samples[0]],
      realWorldApplications: [
        meta.mini_project.split("—")[0].trim(),
        `Production Python code in ${meta.name.toLowerCase()}`,
        "Interview-style coding problems at this tier",
      ],
      keyTakeaways: [
        meta.levels[level].split(",")[0],
        "Run and modify sample code before attempting exercises",
        "Use the AI tutor when stuck on error messages or edge cases",
      ],
    })),
  };
}

export const PYTHON_CURRICULA: ModuleCurriculum[] = MODULE_LIST.map(({ slug, ...meta }) =>
  buildCurriculum(meta, slug),
);

export function getPythonCurriculum(topicSlug: string): ModuleCurriculum | undefined {
  return PYTHON_CURRICULA.find((c) => c.topicSlug === topicSlug);
}
