"""One-off generator for backend/data/snippets.json (100 starter snippets)."""

from __future__ import annotations

import json
import os

TOPICS: list[tuple[str, str, list[tuple[str, str, str, str]]]] = [
    (
        "python-basics",
        "Python Basics",
        [
            ("hello-print", "Hello Print", "Minimal print greeting", 'print("Hello, Python!")'),
            (
                "main-guard",
                "Main Guard",
                "Standard script entry pattern",
                'def main():\n    print("running")\n\nif __name__ == "__main__":\n    main()',
            ),
            (
                "comment-style",
                "Comment Style",
                "Inline and block comments",
                '# single-line comment\n"""Docstring-style block"""\nprint("ok")',
            ),
            ("repl-expr", "REPL Expression", "Evaluate and display expression", "result = 2 + 3\nprint(result)"),
        ],
    ),
    (
        "variables-types",
        "Variables & Types",
        [
            ("type-check", "Type Check", "Inspect object type", "value = 42\nprint(type(value).__name__)"),
            ("truthy-falsy", "Truthy Falsy", "Check truthiness of values", 'print(bool(0), bool(""), bool([1]))'),
            ("none-check", "None Check", "Compare with None safely", "x = None\nprint(x is None)"),
            ("swap-vars", "Swap Variables", "Tuple unpacking swap", "a, b = 1, 2\na, b = b, a\nprint(a, b)"),
        ],
    ),
    (
        "strings",
        "Strings",
        [
            ("fstring", "F-String Format", "Embed variables in strings", 'name = "Ada"\nprint(f"Hello, {name}!")'),
            ("split-join", "Split and Join", "Tokenize and rejoin", 'parts = "a,b,c".split(",")\nprint("-".join(parts))'),
            ("strip-text", "Strip Whitespace", "Clean user input", 'text = "  hello  "\nprint(text.strip())'),
            ("slice-string", "String Slice", "Extract substring", 'word = "Python"\nprint(word[0:3])'),
        ],
    ),
    (
        "control-flow",
        "Control Flow",
        [
            (
                "if-elif-else",
                "If Elif Else",
                "Branch on score",
                'score = 85\nif score >= 90:\n    grade = "A"\nelif score >= 80:\n    grade = "B"\nelse:\n    grade = "C"\nprint(grade)',
            ),
            ("ternary", "Ternary Expression", "Compact conditional", 'n = 4\nlabel = "even" if n % 2 == 0 else "odd"\nprint(label)'),
            (
                "match-case",
                "Match Case",
                "Pattern matching status",
                'status = 404\nmatch status:\n    case 200:\n        print("ok")\n    case 404:\n        print("not found")\n    case _:\n        print("other")',
            ),
            (
                "guard-clause",
                "Guard Clause",
                "Early return pattern",
                'def parse(value):\n    if value is None:\n        return "missing"\n    return value.upper()\nprint(parse(None))',
            ),
        ],
    ),
    (
        "loops",
        "Loops",
        [
            ("for-range", "For Range", "Iterate with range", "total = 0\nfor i in range(1, 4):\n    total += i\nprint(total)"),
            ("while-break", "While Break", "Exit loop early", "n = 0\nwhile True:\n    n += 1\n    if n == 3:\n        break\nprint(n)"),
            (
                "enumerate-zip",
                "Enumerate Zip",
                "Parallel iteration",
                'names = ["a", "b"]\nscores = [10, 20]\nfor i, (n, s) in enumerate(zip(names, scores)):\n    print(i, n, s)',
            ),
            ("comprehension-sum", "Comprehension Sum", "Sum squares", "nums = [1, 2, 3, 4]\nprint(sum(x * x for x in nums))"),
        ],
    ),
    (
        "lists-tuples",
        "Lists & Tuples",
        [
            ('list-append', "List Append", "Grow a list", 'items = []\nitems.append("task")\nprint(items)'),
            ("list-slice", "List Slice", "Copy sublist", "data = [0, 1, 2, 3, 4]\nprint(data[1:4])"),
            ("tuple-unpack", "Tuple Unpack", "Unpack coordinates", "point = (3, 4)\nx, y = point\nprint(x + y)"),
            ("sorted-key", "Sorted Key", "Sort by length", 'words = ["pear", "fig", "apple"]\nprint(sorted(words, key=len))'),
        ],
    ),
    (
        "dicts-sets",
        "Dicts & Sets",
        [
            ("dict-get", "Dict Get Default", "Safe lookup", 'user = {"name": "Ana"}\nprint(user.get("role", "guest"))'),
            ("dict-comp", "Dict Comprehension", "Square mapping", "print({x: x * x for x in range(4)})"),
            ("set-ops", "Set Operations", "Union and intersection", "a, b = {1, 2}, {2, 3}\nprint(sorted(a | b), sorted(a & b))"),
            (
                "counter-pattern",
                "Counter Pattern",
                "Count occurrences",
                'from collections import Counter\nc = Counter("banana")\nprint(dict(c))',
            ),
        ],
    ),
    (
        "functions",
        "Functions",
        [
            ("default-arg", "Default Argument", "Function with default", 'def greet(name="world"):\n    return f"hi {name}"\nprint(greet())'),
            ("args-kwargs", "Args Kwargs", "Variadic function", "def total(*nums):\n    return sum(nums)\nprint(total(1, 2, 3))"),
            (
                "lambda-sort",
                "Lambda Sort",
                "Sort pairs by second item",
                'pairs = [("b", 2), ("a", 1)]\nprint(sorted(pairs, key=lambda p: p[1]))',
            ),
            (
                "partial-fn",
                "Partial Function",
                "Pre-fill arguments",
                "from functools import partial\nadd5 = partial(lambda a, b: a + b, 5)\nprint(add5(3))",
            ),
        ],
    ),
    (
        "oop",
        "OOP",
        [
            (
                "basic-class",
                "Basic Class",
                "Simple data class",
                'class User:\n    def __init__(self, name):\n        self.name = name\nprint(User("Ada").name)',
            ),
            (
                "classmethod",
                "Class Method",
                "Alternative constructor",
                "class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n    @classmethod\n    def origin(cls):\n        return cls(0, 0)\nprint(Point.origin().x)",
            ),
            (
                "property-getter",
                "Property Getter",
                "Computed attribute",
                "class Circle:\n    def __init__(self, r):\n        self.r = r\n    @property\n    def area(self):\n        return 3.14 * self.r ** 2\nprint(Circle(2).area)",
            ),
            (
                "inherit-super",
                "Inheritance Super",
                "Extend parent class",
                'class Animal:\n    def speak(self):\n        return "..."\nclass Dog(Animal):\n    def speak(self):\n        return super().speak() + " woof"\nprint(Dog().speak())',
            ),
        ],
    ),
    (
        "dunder-methods",
        "Dunder Methods",
        [
            (
                "repr-str",
                "Repr and Str",
                "Object string forms",
                'class Item:\n    def __init__(self, name):\n        self.name = name\n    def __repr__(self):\n        return f"Item({self.name!r})"\nprint(repr(Item("book")))',
            ),
            (
                "len-eq",
                "Len and Eq",
                "Rich comparison basics",
                "class Box:\n    def __init__(self, n):\n        self.n = n\n    def __len__(self):\n        return self.n\n    def __eq__(self, other):\n        return isinstance(other, Box) and self.n == other.n\nprint(len(Box(3)), Box(2) == Box(2))",
            ),
            (
                "getitem",
                "Get Item",
                "Indexable object",
                'class Tags:\n    def __init__(self, items):\n        self.items = items\n    def __getitem__(self, i):\n        return self.items[i]\nprint(Tags(["a", "b"])[1])',
            ),
            (
                "context-manager",
                "Context Manager",
                "Resource cleanup",
                'class Managed:\n    def __enter__(self):\n        print("open")\n        return self\n    def __exit__(self, *args):\n        print("close")\nwith Managed():\n    pass',
            ),
        ],
    ),
    (
        "modules-packages",
        "Modules & Packages",
        [
            ("import-alias", "Import Alias", "Short module alias", 'import json as js\nprint(js.dumps({"ok": True}))'),
            ("from-import", "From Import", "Import specific name", "from math import sqrt\nprint(round(sqrt(9), 2))"),
            ('dunder-all', "Dunder All", "Public API list", '__all__ = ["add"]\ndef add(a, b):\n    return a + b\nprint(__all__)'),
            ("importlib-reload", "Importlib Reload", "Reload module in REPL", 'import importlib\nprint(hasattr(importlib, "reload"))'),
        ],
    ),
    (
        "file-io",
        "File I/O",
        [
            (
                "write-read-text",
                "Write Read Text",
                "Basic text file I/O",
                'from io import StringIO\nbuf = StringIO()\nbuf.write("line\\n")\nbuf.seek(0)\nprint(buf.read().strip())',
            ),
            ("pathlib-join", "Pathlib Join", "Build paths safely", 'from pathlib import Path\np = Path("data") / "app.json"\nprint(p.as_posix())'),
            ('json-loads', "JSON Loads", "Parse JSON string", 'import json\nprint(json.loads(\'{"x": 1}\')["x"])'),
            ("csv-row", "CSV Row", "Parse CSV line", 'import csv\nfrom io import StringIO\nrow = next(csv.reader(StringIO("a,1\\n")))\nprint(row)'),
        ],
    ),
    (
        "exceptions",
        "Exceptions",
        [
            ("try-except", "Try Except", "Handle ValueError", 'try:\n    int("x")\nexcept ValueError:\n    print("bad number")'),
            (
                "raise-custom",
                "Raise Custom",
                "Custom exception",
                'class AppError(Exception):\n    pass\ntry:\n    raise AppError("fail")\nexcept AppError as e:\n    print(type(e).__name__)',
            ),
            (
                "else-finally",
                "Else Finally",
                "Complete try structure",
                'try:\n    ok = True\nexcept Exception:\n    ok = False\nelse:\n    print("success" if ok else "fail")\nfinally:\n    print("done")',
            ),
            (
                "logging-basic",
                "Logging Basic",
                "Log info message",
                'import logging\nlogging.basicConfig(level=logging.INFO)\nlogging.info("started")',
            ),
        ],
    ),
    (
        "iterators-generators",
        "Iterators & Generators",
        [
            ("iter-next", "Iter Next", "Manual iteration", "it = iter([1, 2])\nprint(next(it), next(it))"),
            (
                "yield-gen",
                "Yield Generator",
                "Simple generator",
                "def count_to(n):\n    for i in range(1, n + 1):\n        yield i\nprint(list(count_to(3)))",
            ),
            ("gen-expression", "Generator Expression", "Lazy filtering", "nums = (x * x for x in range(4) if x % 2)\nprint(list(nums))"),
            ("itertools-chain", "Itertools Chain", "Flatten iterables", "from itertools import chain\nprint(list(chain([1, 2], [3])))"),
        ],
    ),
    (
        "decorators",
        "Decorators",
        [
            (
                "simple-decorator",
                "Simple Decorator",
                "Wrap function call",
                'def logged(fn):\n    def wrapper(*a, **k):\n        print("call")\n        return fn(*a, **k)\n    return wrapper\n@logged\ndef add(a, b):\n    return a + b\nprint(add(1, 2))',
            ),
            (
                "wraps-decorator",
                "Wraps Decorator",
                "Preserve metadata",
                'from functools import wraps\ndef tag(name):\n    def deco(fn):\n        @wraps(fn)\n        def wrapper(*a, **k):\n            return fn(*a, **k)\n        return wrapper\n    return deco\n@tag("demo")\ndef work():\n    """docs"""\n    return 1\nprint(work.__name__)',
            ),
            ("lru-cache", "LRU Cache", "Memoize calls", "from functools import lru_cache\n@lru_cache\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\nprint(fib(10))"),
            (
                "decorator-args",
                "Decorator Args",
                "Parameterized decorator",
                "def repeat(n):\n    def deco(fn):\n        def wrapper(*a, **k):\n            return [fn(*a, **k) for _ in range(n)]\n        return wrapper\n    return deco\n@repeat(2)\ndef hi():\n    return \"hi\"\nprint(hi())",
            ),
        ],
    ),
    (
        "functional",
        "Functional",
        [
            (
                "map-filter",
                "Map Filter",
                "Transform and filter",
                "nums = [1, 2, 3, 4]\nprint(list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, nums))))",
            ),
            ("reduce-sum", "Reduce Sum", "Fold with reduce", "from functools import reduce\nprint(reduce(lambda a, b: a + b, [1, 2, 3, 4]))"),
            (
                "operator-itemgetter",
                "Itemgetter Sort",
                "Sort records by key",
                "from operator import itemgetter\nrows = [(\"b\", 2), (\"a\", 1)]\nprint(sorted(rows, key=itemgetter(1)))",
            ),
            ("pure-function", "Pure Function", "No side effects", "def add_tax(price, rate=0.1):\n    return round(price * (1 + rate), 2)\nprint(add_tax(10))"),
        ],
    ),
    (
        "comprehensions",
        "Comprehensions",
        [
            ("list-comp", "List Comprehension", "Filter and map", "print([x for x in range(6) if x % 2 == 0])"),
            ("dict-comp", "Dict Comprehension", "Build lookup table", 'print({c: ord(c) for c in "ab"})'),
            ("set-comp", "Set Comprehension", "Unique transformed values", 'print({len(w) for w in ["a", "bb", "a"]})'),
            ("walrus-comp", "Walrus in Loop", "Assign inside condition", "data = [1, 2, 3, 4]\nif (n := len(data)) > 2:\n    print(n)"),
        ],
    ),
    (
        "type-hints",
        "Type Hints",
        [
            ("basic-hints", "Basic Hints", "Annotate args and return", "def add(a: int, b: int) -> int:\n    return a + b\nprint(add(2, 3))"),
            (
                "optional-hint",
                "Optional Hint",
                "Optional parameter",
                'from typing import Optional\ndef greet(name: Optional[str] = None) -> str:\n    return f"hi {name or \'guest\'}"\nprint(greet())',
            ),
            (
                "list-dict-hints",
                "List Dict Hints",
                "Container annotations",
                "from typing import List, Dict\ndef total(scores: List[int]) -> int:\n    return sum(scores)\nprint(total([1, 2, 3]))",
            ),
            (
                "typeddict-note",
                "TypedDict Note",
                "Structured dict typing",
                'from typing import TypedDict\nclass User(TypedDict):\n    name: str\nu: User = {"name": "Ada"}\nprint(u["name"])',
            ),
        ],
    ),
    (
        "testing",
        "Testing",
        [
            ("assert-test", "Assert Test", "Simple assertion", "def double(x):\n    return x * 2\nassert double(2) == 4\nprint(\"pass\")"),
            ("pytest-style", "Pytest Style", "Test function naming", 'def test_sum():\n    assert 1 + 1 == 2\n\ntest_sum()\nprint("ok")'),
            (
                "mock-patch",
                "Mock Patch",
                "Stub dependency",
                'from unittest.mock import patch\nwith patch("builtins.len", return_value=5):\n    print(len([1, 2, 3]))',
            ),
            (
                "parametrize-pattern",
                "Parametrize Pattern",
                "Table-driven tests",
                "cases = [(1, 2, 3), (2, 3, 5)]\nfor a, b, expected in cases:\n    assert a + b == expected\nprint(len(cases))",
            ),
        ],
    ),
    (
        "stdlib",
        "Standard Library",
        [
            (
                "datetime-now",
                "Datetime Now",
                "Current UTC date",
                "from datetime import datetime, timezone\nprint(datetime.now(timezone.utc).year > 2000)",
            ),
            ("collections-deque", "Deque Rotate", "Efficient queue ops", "from collections import deque\nd = deque([1, 2, 3])\nd.rotate(1)\nprint(list(d))"),
            ("itertools-permutations", "Permutations", "Generate permutations", 'from itertools import permutations\nprint(len(list(permutations("ab"))))'),
            (
                "dataclass-user",
                "Dataclass User",
                "Auto-generated methods",
                'from dataclasses import dataclass\n@dataclass\nclass User:\n    name: str\nprint(User("Ada").name)',
            ),
        ],
    ),
    (
        "concurrency",
        "Concurrency",
        [
            (
                "thread-start",
                "Thread Start",
                "Run worker thread",
                'import threading\ndef work():\n    print("thread")\nt = threading.Thread(target=work)\nt.start()\nt.join()',
            ),
            ("queue-worker", "Queue Worker", "Producer consumer queue", "import queue\nq = queue.Queue()\nq.put(1)\nprint(q.get())"),
            ("lock-counter", "Lock Counter", "Protect shared state", "import threading\ncount = 0\nlock = threading.Lock()\nwith lock:\n    count += 1\nprint(count)"),
            (
                "executor-map",
                "Executor Map",
                "Thread pool map",
                "from concurrent.futures import ThreadPoolExecutor\nwith ThreadPoolExecutor(max_workers=2) as ex:\n    print(list(ex.map(lambda x: x * 2, [1, 2, 3])))",
            ),
        ],
    ),
    (
        "async",
        "Async",
        [
            ("async-def", "Async Def", "Define coroutine", "import asyncio\nasync def main():\n    return 42\nprint(asyncio.run(main()))"),
            (
                "gather-tasks",
                "Gather Tasks",
                "Run coroutines concurrently",
                "import asyncio\nasync def one():\n    return 1\nasync def main():\n    return sum(await asyncio.gather(one(), one()))\nprint(asyncio.run(main()))",
            ),
            (
                "async-for",
                "Async For",
                "Iterate async generator",
                "import asyncio\nasync def gen():\n    for x in range(2):\n        yield x\nasync def main():\n    return [x async for x in gen()]\nprint(asyncio.run(main()))",
            ),
            (
                "asyncio-sleep",
                "Asyncio Sleep",
                "Non-blocking delay",
                'import asyncio\nasync def main():\n    await asyncio.sleep(0)\n    return "done"\nprint(asyncio.run(main()))',
            ),
        ],
    ),
    (
        "performance",
        "Performance",
        [
            ("timeit-once", "Timeit Once", "Measure tiny snippet", 'import timeit\nprint(timeit.timeit("1 + 1", number=1000) > 0)'),
            (
                "slots-memory",
                "Slots Memory",
                "Reduce instance dict overhead",
                "class Point:\n    __slots__ = (\"x\", \"y\")\n    def __init__(self, x, y):\n        self.x, self.y = x, y\nprint(Point(1, 2).x)",
            ),
            ("local-ref", "Local Reference", "Avoid repeated lookups", "import math\nsqrt = math.sqrt\nprint(round(sqrt(16), 2))"),
            ("join-strings", "Join Strings", "Efficient concatenation", 'parts = ["a", "b", "c"]\nprint("".join(parts))'),
        ],
    ),
    (
        "design-patterns",
        "Design Patterns",
        [
            (
                "singleton-meta",
                "Singleton Pattern",
                "Single shared instance",
                "class Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\nprint(Singleton() is Singleton())",
            ),
            (
                "factory-fn",
                "Factory Function",
                "Create by type key",
                'def make(kind):\n    return {"a": list, "b": set}[kind]()\nprint(type(make("a")).__name__)',
            ),
            (
                "strategy-fn",
                "Strategy Function",
                "Pluggable algorithm",
                'def add(a, b):\n    return a + b\ndef mul(a, b):\n    return a * b\nops = {"+": add, "*": mul}\nprint(ops["+"](2, 3))',
            ),
            (
                "observer-callbacks",
                "Observer Callbacks",
                "Notify subscribers",
                'class Subject:\n    def __init__(self):\n        self.listeners = []\n    def subscribe(self, fn):\n        self.listeners.append(fn)\n    def emit(self, value):\n        for fn in self.listeners:\n            fn(value)\ns = Subject()\ns.subscribe(lambda v: print(v))\ns.emit(1)',
            ),
        ],
    ),
    (
        "data-scripting",
        "Data & Scripting",
        [
            (
                "argparse-basic",
                "Argparse Basic",
                "CLI flag parsing",
                'import argparse\np = argparse.ArgumentParser()\np.add_argument("--name", default="world")\nargs = p.parse_args([])\nprint(args.name)',
            ),
            (
                "csv-dictreader",
                "CSV DictReader",
                "Read CSV as dict rows",
                'import csv\nfrom io import StringIO\nr = csv.DictReader(StringIO("name,score\\nAda,10\\n"))\nprint(list(r)[0]["name"])',
            ),
            ("requests-mock", "HTTP Pattern", "HTTP GET pattern (no network)", 'url = "https://example.com/api"\nprint(url.endswith("/api"))'),
            (
                "pydantic-model",
                "Pydantic Model",
                "Validate data shape",
                'try:\n    from pydantic import BaseModel\n    class Item(BaseModel):\n        name: str\n    print(Item(name="book").name)\nexcept ImportError:\n    print("book")',
            ),
        ],
    ),
]

FEATURED_SUFFIXES = {"hello-print", "fstring", "list-comp", "async-def", "dataclass-user"}


def main() -> None:
    snippets: list[dict] = []
    for topic_slug, module_name, items in TOPICS:
        for i, (slug_suffix, title, desc, code) in enumerate(items):
            slug = f"snip-{topic_slug}-{slug_suffix}"
            snippets.append(
                {
                    "title": title,
                    "slug": slug,
                    "description": f"{module_name}: {desc}",
                    "code": code,
                    "topic_slug": topic_slug,
                    "tags": [topic_slug.split("-")[0], "starter", "pattern"],
                    "difficulty": "basic" if i < 2 else ("intermediate" if i == 2 else "advanced"),
                    "is_featured": slug_suffix in FEATURED_SUFFIXES,
                }
            )

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "snippets.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(snippets, fh, indent=2)
    print(f"Wrote {len(snippets)} snippets to {path}")


if __name__ == "__main__":
    main()
