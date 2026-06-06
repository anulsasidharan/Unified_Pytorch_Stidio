"""
seeds/questions_python_modules_11_15.py
---------------------------------------
Python Learning Studio — Modules 11-15

Modules and counts:
- modules-packages: 22 (8 basic, 8 intermediate, 6 advanced)
- file-io: 24 (10 basic, 8 intermediate, 6 advanced)
- exceptions: 24 (10 basic, 8 intermediate, 6 advanced)
- iterators-generators: 28 (8 basic, 10 intermediate, 10 advanced)
- decorators: 26 (8 basic, 10 intermediate, 8 advanced)

Usage:
    python -m seeds.questions_python_modules_11_15
"""

import asyncio
from textwrap import dedent

from seeds.loader import seed_questions_for_topic


def _q(
    *,
    title: str,
    slug: str,
    difficulty: str,
    prompt: str,
    starter_code: str,
    solution_code: str,
    expected_output: str,
    tags: list[str],
    question_type: str = "code_completion",
) -> dict:
    xp = {"basic": 8, "intermediate": 18, "advanced": 30}[difficulty]
    mins = {"basic": 4, "intermediate": 8, "advanced": 12}[difficulty]
    return {
        "title": title,
        "slug": slug,
        "difficulty": difficulty,
        "question_type": question_type,
        "problem_statement": (
            f"## {title}\n\n"
            f"{prompt}\n\n"
            f"**Expected output:**\n```\n{expected_output}\n```\n"
        ),
        "starter_code": starter_code,
        "expected_output": expected_output,
        "tags": tags,
        "xp_reward": xp,
        "time_estimate_mins": mins,
        "solutions": [
            {
                "title": "Solution",
                "code": solution_code,
                "explanation": "Reference solution with deterministic stdout.",
                "is_optimal": True,
            }
        ],
    }


def _modules_packages_questions() -> list[dict]:
    questions: list[dict] = []
    add = questions.append

    # 8 basic
    add(
        _q(
            title="Import math and Print sqrt",
            slug="py-modpkg-basic-math-sqrt",
            difficulty="basic",
            prompt="Import `math` and print the square root of 81.",
            starter_code="# import math and print sqrt of 81\n",
            solution_code="import math\nprint(int(math.sqrt(81)))",
            expected_output="9",
            tags=["python", "modules", "imports"],
        )
    )
    add(
        _q(
            title="Use from-import with pi",
            slug="py-modpkg-basic-from-pi",
            difficulty="basic",
            prompt="Import `pi` from `math` and print `round(pi, 2)`.",
            starter_code="# from math import pi\n",
            solution_code="from math import pi\nprint(round(pi, 2))",
            expected_output="3.14",
            tags=["python", "modules", "from-import"],
        )
    )
    add(
        _q(
            title="Use import alias",
            slug="py-modpkg-basic-alias",
            difficulty="basic",
            prompt="Import `math` as `m` and print `m.factorial(5)`.",
            starter_code="# import math as m\n",
            solution_code="import math as m\nprint(m.factorial(5))",
            expected_output="120",
            tags=["python", "modules", "alias"],
        )
    )
    add(
        _q(
            title="Inspect module name",
            slug="py-modpkg-basic-module-name",
            difficulty="basic",
            prompt="Import `json` and print `json.__name__`.",
            starter_code="# import json and print __name__\n",
            solution_code="import json\nprint(json.__name__)",
            expected_output="json",
            tags=["python", "modules", "dunder"],
        )
    )
    add(
        _q(
            title="Use collections Counter",
            slug="py-modpkg-basic-counter",
            difficulty="basic",
            prompt="Use `Counter` on `'banana'` and print the count of `'a'`.",
            starter_code="# use Counter on banana\n",
            solution_code="from collections import Counter\nprint(Counter('banana')['a'])",
            expected_output="3",
            tags=["python", "modules", "collections"],
        )
    )
    add(
        _q(
            title="Use pathlib for suffix",
            slug="py-modpkg-basic-pathlib-suffix",
            difficulty="basic",
            prompt="Create `Path('notes.txt')` and print its suffix.",
            starter_code="# use pathlib.Path\n",
            solution_code="from pathlib import Path\nprint(Path('notes.txt').suffix)",
            expected_output=".txt",
            tags=["python", "modules", "pathlib"],
        )
    )
    add(
        _q(
            title="Use statistics mean",
            slug="py-modpkg-basic-statistics-mean",
            difficulty="basic",
            prompt="Import `mean` from `statistics` and print mean of `[2, 4, 6, 8]`.",
            starter_code="# from statistics import mean\n",
            solution_code="from statistics import mean\nprint(int(mean([2, 4, 6, 8])))",
            expected_output="5",
            tags=["python", "modules", "statistics"],
        )
    )
    add(
        _q(
            title="Use itertools count",
            slug="py-modpkg-basic-itertools-count",
            difficulty="basic",
            prompt="Use `itertools.count(10, 2)` and print the first three values separated by spaces.",
            starter_code="# use itertools.count\n",
            solution_code=dedent(
                """
                import itertools
                c = itertools.count(10, 2)
                print(next(c), next(c), next(c))
                """
            ).strip(),
            expected_output="10 12 14",
            tags=["python", "modules", "itertools"],
        )
    )

    # 8 intermediate
    add(
        _q(
            title="Dynamic import with importlib",
            slug="py-modpkg-int-importlib",
            difficulty="intermediate",
            prompt="Use `importlib.import_module` to import `math` and print `math.gcd(20, 30)`.",
            starter_code="# import importlib and dynamically import math\n",
            solution_code="import importlib\nmath = importlib.import_module('math')\nprint(math.gcd(20, 30))",
            expected_output="10",
            tags=["python", "modules", "importlib"],
        )
    )
    add(
        _q(
            title="Check module in sys.modules",
            slug="py-modpkg-int-sys-modules",
            difficulty="intermediate",
            prompt="Import `json` then print whether `'json'` is present in `sys.modules`.",
            starter_code="# import json and sys\n",
            solution_code="import json\nimport sys\nprint('json' in sys.modules)",
            expected_output="True",
            tags=["python", "modules", "sys"],
        )
    )
    add(
        _q(
            title="Read package name of module",
            slug="py-modpkg-int-package-name",
            difficulty="intermediate",
            prompt="Import `json.encoder` and print whether `__package__` equals `'json'`.",
            starter_code="# import json.encoder\n",
            solution_code="import json.encoder\nprint(json.encoder.__package__ == 'json')",
            expected_output="True",
            tags=["python", "packages", "module-metadata"],
        )
    )
    add(
        _q(
            title="Use pkgutil iter_modules",
            slug="py-modpkg-int-pkgutil",
            difficulty="intermediate",
            prompt="Use `pkgutil.iter_modules()` and print whether module name `'json'` exists.",
            starter_code="# use pkgutil.iter_modules\n",
            solution_code="import pkgutil\nprint(any(m.name == 'json' for m in pkgutil.iter_modules()))",
            expected_output="True",
            tags=["python", "packages", "pkgutil"],
        )
    )
    add(
        _q(
            title="Alias collision avoidance",
            slug="py-modpkg-int-alias-collision",
            difficulty="intermediate",
            prompt="Import `statistics as stats` and print `stats.median([9, 1, 5])`.",
            starter_code="# import statistics as stats\n",
            solution_code="import statistics as stats\nprint(stats.median([9, 1, 5]))",
            expected_output="5",
            tags=["python", "modules", "alias"],
        )
    )
    add(
        _q(
            title="Use __all__ style export list",
            slug="py-modpkg-int-all-list",
            difficulty="intermediate",
            prompt="Given `exports = ['a', 'b', 'c']`, assign to `__all__` and print `len(__all__)`.",
            starter_code="exports = ['a', 'b', 'c']\n# assign __all__\n",
            solution_code="exports = ['a', 'b', 'c']\n__all__ = exports\nprint(len(__all__))",
            expected_output="3",
            tags=["python", "packages", "__all__"],
        )
    )
    add(
        _q(
            title="Relative style import concept",
            slug="py-modpkg-int-relative-concept",
            difficulty="intermediate",
            prompt="Print the string that represents a relative import from sibling module `utils`.",
            starter_code="# print relative import statement text\n",
            solution_code="print('from . import utils')",
            expected_output="from . import utils",
            tags=["python", "packages", "relative-import"],
        )
    )
    add(
        _q(
            title="Safe optional import",
            slug="py-modpkg-int-optional-import",
            difficulty="intermediate",
            prompt="Attempt to import `tomllib`; print `available` if import works else `missing`.",
            starter_code="# try importing tomllib\n",
            solution_code=dedent(
                """
                try:
                    import tomllib  # noqa: F401
                    print('available')
                except ModuleNotFoundError:
                    print('missing')
                """
            ).strip(),
            expected_output="available",
            tags=["python", "modules", "optional-deps"],
        )
    )

    # 6 advanced
    add(
        _q(
            title="Inspect module spec",
            slug="py-modpkg-adv-module-spec",
            difficulty="advanced",
            prompt="Use `importlib.util.find_spec('json')` and print whether origin is not `None`.",
            starter_code="# use importlib.util.find_spec\n",
            solution_code="import importlib.util\nspec = importlib.util.find_spec('json')\nprint(spec is not None and spec.origin is not None)",
            expected_output="True",
            tags=["python", "modules", "import-system"],
        )
    )
    add(
        _q(
            title="Programmatic reload",
            slug="py-modpkg-adv-reload",
            difficulty="advanced",
            prompt="Import `math`, call `importlib.reload(math)`, then print `math.ceil(2.1)`.",
            starter_code="# import math and reload it\n",
            solution_code="import importlib\nimport math\nimportlib.reload(math)\nprint(math.ceil(2.1))",
            expected_output="3",
            tags=["python", "modules", "reload"],
        )
    )
    add(
        _q(
            title="Read module file attribute",
            slug="py-modpkg-adv-file-attr",
            difficulty="advanced",
            prompt="Import `json` and print whether `json.__file__` ends with `.py`.",
            starter_code="# print json.__file__ check\n",
            solution_code="import json\nprint(json.__file__.endswith('.py'))",
            expected_output="True",
            tags=["python", "modules", "introspection"],
        )
    )
    add(
        _q(
            title="Namespace package style path",
            slug="py-modpkg-adv-module-path",
            difficulty="advanced",
            prompt="Import `json` and print whether `json` has attribute `__path__`.",
            starter_code="# check if module has __path__\n",
            solution_code="import json\nprint(hasattr(json, '__path__'))",
            expected_output="True",
            tags=["python", "packages", "namespace"],
        )
    )
    add(
        _q(
            title="Fix invalid import statement",
            slug="py-modpkg-adv-debug-import",
            difficulty="advanced",
            question_type="debug_model",
            prompt=(
                "The code uses invalid syntax:\n\n"
                "```python\n"
                "import math.sqrt\n"
                "print(math.sqrt(16))\n"
                "```\n\n"
                "Fix it so the script prints 4."
            ),
            starter_code="import math.sqrt\nprint(math.sqrt(16))\n",
            solution_code="import math\nprint(int(math.sqrt(16)))",
            expected_output="4",
            tags=["python", "modules", "debugging"],
        )
    )
    add(
        _q(
            title="Runtime attribute loading",
            slug="py-modpkg-adv-getattr",
            difficulty="advanced",
            prompt="Import `math`, fetch `pow` via `getattr`, and print `pow(2, 5)`.",
            starter_code="# getattr from module\n",
            solution_code="import math\npow_fn = getattr(math, 'pow')\nprint(int(pow_fn(2, 5)))",
            expected_output="32",
            tags=["python", "modules", "reflection"],
        )
    )

    assert len([q for q in questions if q["difficulty"] == "basic"]) == 8
    assert len([q for q in questions if q["difficulty"] == "intermediate"]) == 8
    assert len([q for q in questions if q["difficulty"] == "advanced"]) == 6
    return questions


def _file_io_questions() -> list[dict]:
    questions: list[dict] = []
    add = questions.append

    # 10 basic
    basic_specs = [
        (
            "Write and Read with Temporary File",
            "py-fileio-basic-temp-write-read",
            "Use `tempfile.NamedTemporaryFile` to write `hello` and read it back.",
            dedent(
                """
                import tempfile
                with tempfile.NamedTemporaryFile('w+', delete=True) as f:
                    f.write('hello')
                    f.seek(0)
                    print(f.read())
                """
            ).strip(),
            "hello",
            ["python", "file-io", "tempfile"],
        ),
        (
            "Read First Line",
            "py-fileio-basic-first-line",
            "Use `io.StringIO('a\\nb\\n')` and print the first line stripped.",
            "from io import StringIO\nf = StringIO('a\\nb\\n')\nprint(f.readline().strip())",
            "a",
            ["python", "file-io", "readline"],
        ),
        (
            "Read All Lines Count",
            "py-fileio-basic-lines-count",
            "Use `io.StringIO('x\\ny\\nz')` and print number of lines.",
            "from io import StringIO\nf = StringIO('x\\ny\\nz')\nprint(len(f.readlines()))",
            "3",
            ["python", "file-io", "readlines"],
        ),
        (
            "Append Text",
            "py-fileio-basic-append",
            "Write `A`, append `B`, then print combined content using a temp file.",
            dedent(
                """
                import tempfile
                with tempfile.NamedTemporaryFile('w+', delete=True) as f:
                    f.write('A')
                    f.flush()
                    f.seek(0, 2)
                    f.write('B')
                    f.seek(0)
                    print(f.read())
                """
            ).strip(),
            "AB",
            ["python", "file-io", "append"],
        ),
        (
            "Write Multiple Lines",
            "py-fileio-basic-write-lines",
            "Use `writelines` with `['1\\n', '2\\n']` and print stripped joined result.",
            "from io import StringIO\nf = StringIO()\nf.writelines(['1\\n', '2\\n'])\nf.seek(0)\nprint(f.read().strip().replace('\\n', ','))",
            "1,2",
            ["python", "file-io", "write"],
        ),
        (
            "File Pointer Position",
            "py-fileio-basic-tell",
            "Write `python` to `StringIO` and print `tell()` position.",
            "from io import StringIO\nf = StringIO()\nf.write('python')\nprint(f.tell())",
            "6",
            ["python", "file-io", "tell"],
        ),
        (
            "Seek Back to Start",
            "py-fileio-basic-seek",
            "Read one char from `StringIO('abc')`, seek to start, print first char again.",
            "from io import StringIO\nf = StringIO('abc')\nf.read(1)\nf.seek(0)\nprint(f.read(1))",
            "a",
            ["python", "file-io", "seek"],
        ),
        (
            "CSV Reader Basic",
            "py-fileio-basic-csv-reader",
            "Parse `name,age\\nAna,20` with `csv.DictReader` and print age.",
            "import csv\nfrom io import StringIO\ndata = StringIO('name,age\\nAna,20\\n')\nrow = next(csv.DictReader(data))\nprint(row['age'])",
            "20",
            ["python", "file-io", "csv"],
        ),
        (
            "JSON Dump and Load",
            "py-fileio-basic-json",
            "Dump `{'x': 3}` to JSON string and load it back, then print `x`.",
            "import json\ns = json.dumps({'x': 3})\nobj = json.loads(s)\nprint(obj['x'])",
            "3",
            ["python", "file-io", "json"],
        ),
        (
            "Path Exists Check",
            "py-fileio-basic-path-exists",
            "Create a temporary file path and print `True` if it exists.",
            "import tempfile\nfrom pathlib import Path\nwith tempfile.NamedTemporaryFile() as f:\n    print(Path(f.name).exists())",
            "True",
            ["python", "file-io", "pathlib"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in basic_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="basic",
                prompt=prompt,
                starter_code="# complete file I/O task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 8 intermediate
    intermediate_specs = [
        (
            "Context Manager Auto Close",
            "py-fileio-int-context-close",
            "Open a temp file with `with` and print whether `f.closed` is `True` after block.",
            "import tempfile\nwith tempfile.NamedTemporaryFile('w+', delete=True) as f:\n    f.write('x')\nprint(f.closed)",
            "True",
            ["python", "file-io", "context-manager"],
        ),
        (
            "Read Chunk Sizes",
            "py-fileio-int-chunk-read",
            "Read `abcdef` in chunks of 2 from `StringIO` and print chunks joined by `|`.",
            "from io import StringIO\nf = StringIO('abcdef')\nparts = []\nwhile (chunk := f.read(2)):\n    parts.append(chunk)\nprint('|'.join(parts))",
            "ab|cd|ef",
            ["python", "file-io", "streaming"],
        ),
        (
            "CSV Writer Roundtrip",
            "py-fileio-int-csv-writer",
            "Write one CSV row `['A', 'B']` and print resulting text stripped.",
            "import csv\nfrom io import StringIO\nbuf = StringIO()\nwriter = csv.writer(buf, lineterminator='\\n')\nwriter.writerow(['A', 'B'])\nprint(buf.getvalue().strip())",
            "A,B",
            ["python", "file-io", "csv"],
        ),
        (
            "JSON Indent Length",
            "py-fileio-int-json-indent",
            "Pretty-print `{'a': 1}` with indent=2 and print number of lines.",
            "import json\ns = json.dumps({'a': 1}, indent=2)\nprint(len(s.splitlines()))",
            "3",
            ["python", "file-io", "json"],
        ),
        (
            "Pathlib Stem and Suffix",
            "py-fileio-int-path-stem",
            "For `Path('report.final.txt')`, print `stem|suffix`.",
            "from pathlib import Path\np = Path('report.final.txt')\nprint(f'{p.stem}|{p.suffix}')",
            "report.final|.txt",
            ["python", "file-io", "pathlib"],
        ),
        (
            "Temporary Directory Listing",
            "py-fileio-int-tempdir-list",
            "Create two files in a temp directory and print sorted count of entries.",
            "import tempfile\nfrom pathlib import Path\nwith tempfile.TemporaryDirectory() as d:\n    p = Path(d)\n    (p / 'a.txt').write_text('a', encoding='utf-8')\n    (p / 'b.txt').write_text('b', encoding='utf-8')\n    print(len(sorted(p.iterdir())))",
            "2",
            ["python", "file-io", "directories"],
        ),
        (
            "Encoding Roundtrip UTF-8",
            "py-fileio-int-encoding",
            "Write `'cafe'` with UTF-8 and read back, then print uppercase text.",
            "import tempfile\nfrom pathlib import Path\nwith tempfile.TemporaryDirectory() as d:\n    p = Path(d) / 'x.txt'\n    p.write_text('cafe', encoding='utf-8')\n    print(p.read_text(encoding='utf-8').upper())",
            "CAFE",
            ["python", "file-io", "encoding"],
        ),
        (
            "Filter Non Empty Lines",
            "py-fileio-int-filter-lines",
            "Given `StringIO('a\\n\\n b \\n')`, print count of non-empty stripped lines.",
            "from io import StringIO\nf = StringIO('a\\n\\n b \\n')\nprint(sum(1 for line in f if line.strip()))",
            "2",
            ["python", "file-io", "text-processing"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in intermediate_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="intermediate",
                prompt=prompt,
                starter_code="# complete intermediate file I/O task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 6 advanced
    advanced_specs = [
        (
            "Atomic Replace with Pathlib",
            "py-fileio-adv-atomic-replace",
            "Write `new` to temp file and atomically replace target file, then print final content.",
            dedent(
                """
                import tempfile
                from pathlib import Path
                with tempfile.TemporaryDirectory() as d:
                    root = Path(d)
                    target = root / 'data.txt'
                    tmp = root / 'data.tmp'
                    target.write_text('old', encoding='utf-8')
                    tmp.write_text('new', encoding='utf-8')
                    tmp.replace(target)
                    print(target.read_text(encoding='utf-8'))
                """
            ).strip(),
            "new",
            ["python", "file-io", "atomic-write"],
            "code_completion",
        ),
        (
            "Use mmap for Byte Access",
            "py-fileio-adv-mmap",
            "Create a temp binary file `ABC`, memory-map it, and print the middle byte as text.",
            dedent(
                """
                import mmap
                import tempfile
                from pathlib import Path
                with tempfile.TemporaryDirectory() as d:
                    p = Path(d) / 'bytes.bin'
                    p.write_bytes(b'ABC')
                    with p.open('r+b') as fh:
                        with mmap.mmap(fh.fileno(), 0) as mm:
                            print(mm[1:2].decode())
                """
            ).strip(),
            "B",
            ["python", "file-io", "mmap"],
            "code_completion",
        ),
        (
            "Debug Wrong File Mode",
            "py-fileio-adv-debug-mode",
            "Fix code that writes text using binary mode so it runs and prints `ok`.",
            "with open('x.txt', 'wb') as f:\n    f.write('ok')\nprint('ok')",
            "ok",
            ["python", "file-io", "debugging"],
            "debug_model",
        ),
        (
            "Safely Handle Missing File",
            "py-fileio-adv-missing-file",
            "Handle `FileNotFoundError` for `definitely_missing.txt` and print `missing`.",
            "from pathlib import Path\np = Path('definitely_missing.txt')\ntry:\n    p.read_text(encoding='utf-8')\n    print('found')\nexcept FileNotFoundError:\n    print('missing')",
            "missing",
            ["python", "file-io", "exceptions"],
            "code_completion",
        ),
        (
            "Buffered Writer Flush",
            "py-fileio-adv-buffered-flush",
            "Use `io.BufferedWriter` over `BytesIO`, flush, then print buffer length.",
            "import io\nraw = io.BytesIO()\nbuf = io.BufferedWriter(raw)\nbuf.write(b'abc')\nbuf.flush()\nprint(len(raw.getvalue()))",
            "3",
            ["python", "file-io", "buffering"],
            "code_completion",
        ),
        (
            "Read JSON Lines Stream",
            "py-fileio-adv-json-lines",
            "Parse two JSON lines and print sum of `v` fields.",
            "import json\nfrom io import StringIO\nf = StringIO('{\"v\": 2}\\n{\"v\": 5}\\n')\nprint(sum(json.loads(line)['v'] for line in f if line.strip()))",
            "7",
            ["python", "file-io", "jsonl"],
            "code_completion",
        ),
    ]
    for title, slug, prompt, solution, expected, tags, qtype in advanced_specs:
        code = solution
        if slug == "py-fileio-adv-debug-mode":
            code = (
                "import tempfile\n"
                "from pathlib import Path\n"
                "with tempfile.TemporaryDirectory() as d:\n"
                "    p = Path(d) / 'x.txt'\n"
                "    p.write_text('ok', encoding='utf-8')\n"
                "    print(p.read_text(encoding='utf-8'))"
            )
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="advanced",
                prompt=prompt,
                starter_code="# complete advanced file I/O task\n",
                solution_code=code,
                expected_output=expected,
                tags=tags,
                question_type=qtype,
            )
        )

    assert len([q for q in questions if q["difficulty"] == "basic"]) == 10
    assert len([q for q in questions if q["difficulty"] == "intermediate"]) == 8
    assert len([q for q in questions if q["difficulty"] == "advanced"]) == 6
    return questions


def _exceptions_questions() -> list[dict]:
    questions: list[dict] = []
    add = questions.append

    # 10 basic
    basic_specs = [
        (
            "Catch ZeroDivisionError",
            "py-exc-basic-zero-division",
            "Catch division by zero and print `handled`.",
            "try:\n    1 / 0\nexcept ZeroDivisionError:\n    print('handled')",
            "handled",
            ["python", "exceptions", "try-except"],
        ),
        (
            "Catch ValueError from int",
            "py-exc-basic-value-error",
            "Convert `'abc'` with `int()` and catch `ValueError` to print `bad int`.",
            "try:\n    int('abc')\nexcept ValueError:\n    print('bad int')",
            "bad int",
            ["python", "exceptions", "valueerror"],
        ),
        (
            "Catch KeyError",
            "py-exc-basic-key-error",
            "Access missing key in dict and print `missing key` in `except`.",
            "d = {'a': 1}\ntry:\n    print(d['b'])\nexcept KeyError:\n    print('missing key')",
            "missing key",
            ["python", "exceptions", "keyerror"],
        ),
        (
            "Catch IndexError",
            "py-exc-basic-index-error",
            "Access index 5 in `[1]` and catch `IndexError` to print `bad index`.",
            "items = [1]\ntry:\n    print(items[5])\nexcept IndexError:\n    print('bad index')",
            "bad index",
            ["python", "exceptions", "indexerror"],
        ),
        (
            "Raise RuntimeError",
            "py-exc-basic-raise-runtime",
            "Raise `RuntimeError('oops')`, catch it, and print its message.",
            "try:\n    raise RuntimeError('oops')\nexcept RuntimeError as e:\n    print(e)",
            "oops",
            ["python", "exceptions", "raise"],
        ),
        (
            "Use finally block",
            "py-exc-basic-finally",
            "Use `try/finally` and print `done` from `finally`.",
            "try:\n    x = 1 + 1\nfinally:\n    print('done')",
            "done",
            ["python", "exceptions", "finally"],
        ),
        (
            "Else block runs",
            "py-exc-basic-else",
            "Use `try/except/else` where no exception occurs; print `clean` from `else`.",
            "try:\n    int('7')\nexcept ValueError:\n    print('bad')\nelse:\n    print('clean')",
            "clean",
            ["python", "exceptions", "else"],
        ),
        (
            "Catch Multiple Exceptions",
            "py-exc-basic-multiple",
            "Catch `ValueError` or `TypeError` for `int(None)` and print `invalid`.",
            "try:\n    int(None)\nexcept (ValueError, TypeError):\n    print('invalid')",
            "invalid",
            ["python", "exceptions", "multiple"],
        ),
        (
            "Get exception type name",
            "py-exc-basic-type-name",
            "Trigger `ValueError` and print the exception class name.",
            "try:\n    int('x')\nexcept Exception as e:\n    print(type(e).__name__)",
            "ValueError",
            ["python", "exceptions", "introspection"],
        ),
        (
            "Re-raise pattern",
            "py-exc-basic-reraise",
            "Raise and catch `ValueError`, then print `caught once`.",
            "try:\n    raise ValueError('x')\nexcept ValueError:\n    print('caught once')",
            "caught once",
            ["python", "exceptions", "control-flow"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in basic_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="basic",
                prompt=prompt,
                starter_code="# complete exception handling task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 8 intermediate
    intermediate_specs = [
        (
            "Custom Exception Class",
            "py-exc-int-custom-class",
            "Define `class TooSmallError(Exception)` and raise/catch it to print `custom`.",
            "class TooSmallError(Exception):\n    pass\ntry:\n    raise TooSmallError('custom')\nexcept TooSmallError as e:\n    print(e)",
            "custom",
            ["python", "exceptions", "custom"],
        ),
        (
            "Exception Chaining",
            "py-exc-int-chaining",
            "Raise `RuntimeError('outer')` from `ValueError('inner')` and print cause type.",
            "try:\n    try:\n        int('bad')\n    except ValueError as e:\n        raise RuntimeError('outer') from e\nexcept RuntimeError as e:\n    print(type(e.__cause__).__name__)",
            "ValueError",
            ["python", "exceptions", "chaining"],
        ),
        (
            "Assert and Catch",
            "py-exc-int-assert",
            "Fail an assertion and catch `AssertionError` to print `asserted`.",
            "try:\n    assert 2 < 1, 'nope'\nexcept AssertionError:\n    print('asserted')",
            "asserted",
            ["python", "exceptions", "assert"],
        ),
        (
            "Convert with fallback function",
            "py-exc-int-fallback",
            "Write a function returning `-1` when `int()` fails; print result for `'z'`.",
            "def to_int_or_minus_one(s):\n    try:\n        return int(s)\n    except ValueError:\n        return -1\nprint(to_int_or_minus_one('z'))",
            "-1",
            ["python", "exceptions", "functions"],
        ),
        (
            "Suppress specific exception",
            "py-exc-int-contextlib-suppress",
            "Use `contextlib.suppress(KeyError)` and print `ok` after missing key access.",
            "from contextlib import suppress\nd = {}\nwith suppress(KeyError):\n    _ = d['x']\nprint('ok')",
            "ok",
            ["python", "exceptions", "contextlib"],
        ),
        (
            "Try Except Finally Order",
            "py-exc-int-order",
            "Show order by printing `try`, then `except`, then `finally` on new lines.",
            "try:\n    print('try')\n    1 / 0\nexcept ZeroDivisionError:\n    print('except')\nfinally:\n    print('finally')",
            "try\nexcept\nfinally",
            ["python", "exceptions", "flow"],
        ),
        (
            "Parse with custom message",
            "py-exc-int-custom-message",
            "Raise `ValueError('expected int')` when text is not digits; print message.",
            "text = 'abc'\ntry:\n    if not text.isdigit():\n        raise ValueError('expected int')\nexcept ValueError as e:\n    print(e)",
            "expected int",
            ["python", "exceptions", "validation"],
        ),
        (
            "Handle FileNotFoundError",
            "py-exc-int-file-not-found",
            "Attempt to open missing file and print `not found` when exception occurs.",
            "try:\n    open('no_such_file_123.txt', 'r', encoding='utf-8')\nexcept FileNotFoundError:\n    print('not found')",
            "not found",
            ["python", "exceptions", "file-errors"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in intermediate_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="intermediate",
                prompt=prompt,
                starter_code="# complete intermediate exceptions task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 6 advanced
    advanced_specs = [
        (
            "Create Rich Custom Exception",
            "py-exc-adv-rich-exception",
            "Create exception with `code` attribute and print it after catching.",
            "class ApiError(Exception):\n    def __init__(self, msg, code):\n        super().__init__(msg)\n        self.code = code\ntry:\n    raise ApiError('fail', 503)\nexcept ApiError as e:\n    print(e.code)",
            "503",
            ["python", "exceptions", "custom"],
            "code_completion",
        ),
        (
            "Use ExceptionGroup",
            "py-exc-adv-exception-group",
            "Raise `ExceptionGroup` with one `ValueError` and print count via `except* ValueError`.",
            "try:\n    raise ExceptionGroup('group', [ValueError('a')])\nexcept* ValueError as eg:\n    print(len(eg.exceptions))",
            "1",
            ["python", "exceptions", "exceptiongroup"],
            "code_completion",
        ),
        (
            "Traceback Formatting",
            "py-exc-adv-traceback",
            "Catch an exception and print whether formatted traceback contains `ZeroDivisionError`.",
            "import traceback\ntry:\n    1 / 0\nexcept ZeroDivisionError:\n    text = traceback.format_exc()\n    print('ZeroDivisionError' in text)",
            "True",
            ["python", "exceptions", "traceback"],
            "code_completion",
        ),
        (
            "Debug Bare Except Bug",
            "py-exc-adv-debug-bare-except",
            "Fix code that uses bare `except` to only catch `ValueError`, then print `safe`.",
            "try:\n    int('x')\nexcept:\n    print('safe')",
            "safe",
            ["python", "exceptions", "debugging"],
            "debug_model",
        ),
        (
            "Raise from None",
            "py-exc-adv-from-none",
            "Raise `RuntimeError('wrapped') from None` and print whether `__cause__` is `None`.",
            "try:\n    try:\n        int('a')\n    except ValueError:\n        raise RuntimeError('wrapped') from None\nexcept RuntimeError as e:\n    print(e.__cause__ is None)",
            "True",
            ["python", "exceptions", "chaining"],
            "code_completion",
        ),
        (
            "Validate and Aggregate Errors",
            "py-exc-adv-aggregate",
            "Collect validation errors from two checks and print total count.",
            "errors = []\nfor value in ['', 'abc']:\n    try:\n        if not value:\n            raise ValueError('empty')\n        if not value.isdigit():\n            raise TypeError('not digit')\n    except Exception:\n        errors.append('e')\nprint(len(errors))",
            "2",
            ["python", "exceptions", "validation"],
            "code_completion",
        ),
    ]
    for title, slug, prompt, solution, expected, tags, qtype in advanced_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="advanced",
                prompt=prompt,
                starter_code="# complete advanced exceptions task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
                question_type=qtype,
            )
        )

    assert len([q for q in questions if q["difficulty"] == "basic"]) == 10
    assert len([q for q in questions if q["difficulty"] == "intermediate"]) == 8
    assert len([q for q in questions if q["difficulty"] == "advanced"]) == 6
    return questions


def _iterators_generators_questions() -> list[dict]:
    questions: list[dict] = []
    add = questions.append

    # 8 basic
    basic_specs = [
        (
            "Use iter and next",
            "py-itergen-basic-next",
            "Create iterator from `[10, 20]` and print first item with `next`.",
            "it = iter([10, 20])\nprint(next(it))",
            "10",
            ["python", "iterators", "next"],
        ),
        (
            "Handle StopIteration",
            "py-itergen-basic-stop-iteration",
            "Exhaust iterator `[1]` and print `done` when `StopIteration` is raised.",
            "it = iter([1])\nnext(it)\ntry:\n    next(it)\nexcept StopIteration:\n    print('done')",
            "done",
            ["python", "iterators", "stopiteration"],
        ),
        (
            "Simple Generator Yield",
            "py-itergen-basic-yield",
            "Create generator yielding `1` then `2`, and print values space-separated.",
            "def gen():\n    yield 1\n    yield 2\nprint(*gen())",
            "1 2",
            ["python", "generators", "yield"],
        ),
        (
            "Generator Expression Sum",
            "py-itergen-basic-genexpr-sum",
            "Use generator expression to sum squares of `[1,2,3]` and print total.",
            "print(sum(x * x for x in [1, 2, 3]))",
            "14",
            ["python", "generators", "genexpr"],
        ),
        (
            "Enumerate Iterator",
            "py-itergen-basic-enumerate",
            "Use `enumerate(['a','b'], start=1)` and print first pair as `index:item`.",
            "i, v = next(iter(enumerate(['a', 'b'], start=1)))\nprint(f'{i}:{v}')",
            "1:a",
            ["python", "iterators", "enumerate"],
        ),
        (
            "Zip Iterator",
            "py-itergen-basic-zip",
            "Zip `[1,2]` and `['x','y']`, print second tuple as `2-y`.",
            "pairs = list(zip([1, 2], ['x', 'y']))\na, b = pairs[1]\nprint(f'{a}-{b}')",
            "2-y",
            ["python", "iterators", "zip"],
        ),
        (
            "Range Is Iterable",
            "py-itergen-basic-range",
            "Get iterator from `range(3)` and print first two numbers.",
            "it = iter(range(3))\nprint(next(it), next(it))",
            "0 1",
            ["python", "iterators", "range"],
        ),
        (
            "Reverse Iterator",
            "py-itergen-basic-reversed",
            "Use `reversed([1,2,3])` and print first value.",
            "it = reversed([1, 2, 3])\nprint(next(it))",
            "3",
            ["python", "iterators", "reversed"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in basic_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="basic",
                prompt=prompt,
                starter_code="# complete iterator/generator basics task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 10 intermediate
    intermediate_specs = [
        (
            "Stateful Counter Generator",
            "py-itergen-int-counter",
            "Write a generator that yields 1..3 and print values with commas.",
            "def counter():\n    for i in range(1, 4):\n        yield i\nprint(','.join(str(x) for x in counter()))",
            "1,2,3",
            ["python", "generators", "state"],
        ),
        (
            "Yield From Delegation",
            "py-itergen-int-yield-from",
            "Use `yield from [4, 5]` and print generated list length.",
            "def g():\n    yield from [4, 5]\nprint(len(list(g())))",
            "2",
            ["python", "generators", "yield-from"],
        ),
        (
            "Generator with send",
            "py-itergen-int-send",
            "Create generator receiving value via `send` and print doubled number.",
            "def g():\n    x = yield\n    yield x * 2\nit = g()\nnext(it)\nprint(it.send(6))",
            "12",
            ["python", "generators", "send"],
        ),
        (
            "Infinite Generator Take",
            "py-itergen-int-infinite",
            "Create infinite even generator and print first 4 values space-separated.",
            "def evens():\n    n = 0\n    while True:\n        yield n\n        n += 2\nit = evens()\nprint(next(it), next(it), next(it), next(it))",
            "0 2 4 6",
            ["python", "generators", "infinite"],
        ),
        (
            "Custom Iterator Class",
            "py-itergen-int-custom-iterator",
            "Build iterator class yielding 1,2,3 and print sum of it.",
            "class OneToThree:\n    def __iter__(self):\n        self.n = 1\n        return self\n    def __next__(self):\n        if self.n > 3:\n            raise StopIteration\n        v = self.n\n        self.n += 1\n        return v\nprint(sum(OneToThree()))",
            "6",
            ["python", "iterators", "classes"],
        ),
        (
            "Lazy Filtering",
            "py-itergen-int-filter",
            "Use `filter` to keep odd numbers from range(6) and print them joined.",
            "vals = filter(lambda x: x % 2 == 1, range(6))\nprint(','.join(str(v) for v in vals))",
            "1,3,5",
            ["python", "iterators", "filter"],
        ),
        (
            "Map Iterator Consumption",
            "py-itergen-int-map",
            "Use `map(str.upper, ['a','b'])` and print second item.",
            "m = map(str.upper, ['a', 'b'])\nnext(m)\nprint(next(m))",
            "B",
            ["python", "iterators", "map"],
        ),
        (
            "Tee Split Iterator",
            "py-itergen-int-tee",
            "Use `itertools.tee` on `[7,8]` and print first value from each iterator.",
            "import itertools\na, b = itertools.tee(iter([7, 8]))\nprint(next(a), next(b))",
            "7 7",
            ["python", "iterators", "itertools"],
        ),
        (
            "Takewhile Example",
            "py-itergen-int-takewhile",
            "Use `itertools.takewhile` to take values `<4` from `[1,3,4,2]` and print sum.",
            "import itertools\nvals = itertools.takewhile(lambda x: x < 4, [1, 3, 4, 2])\nprint(sum(vals))",
            "4",
            ["python", "iterators", "itertools"],
        ),
        (
            "Dropwhile Example",
            "py-itergen-int-dropwhile",
            "Use `itertools.dropwhile` to drop `<3` from `[1,2,3,4]` and print first remaining.",
            "import itertools\nvals = itertools.dropwhile(lambda x: x < 3, [1, 2, 3, 4])\nprint(next(vals))",
            "3",
            ["python", "iterators", "itertools"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in intermediate_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="intermediate",
                prompt=prompt,
                starter_code="# complete intermediate iterator/generator task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 10 advanced
    advanced_specs = [
        (
            "Generator close handling",
            "py-itergen-adv-close",
            "Create generator with `try/finally`; close it and print `closed` from finally.",
            "def g():\n    try:\n        while True:\n            yield 1\n    finally:\n        print('closed')\nit = g()\nnext(it)\nit.close()",
            "closed",
            ["python", "generators", "close"],
            "code_completion",
        ),
        (
            "Generator throw handling",
            "py-itergen-adv-throw",
            "Handle thrown `ValueError` inside generator and print `handled`.",
            "def g():\n    try:\n        yield 1\n    except ValueError:\n        print('handled')\nit = g()\nnext(it)\ntry:\n    it.throw(ValueError('x'))\nexcept StopIteration:\n    pass",
            "handled",
            ["python", "generators", "throw"],
            "code_completion",
        ),
        (
            "Coroutine style accumulator",
            "py-itergen-adv-coroutine",
            "Build accumulator generator using `send`, send 3 and 4, print total.",
            "def acc():\n    total = 0\n    while True:\n        x = yield total\n        total += x\nit = acc()\nnext(it)\nit.send(3)\nprint(it.send(4))",
            "7",
            ["python", "generators", "coroutine"],
            "code_completion",
        ),
        (
            "Iter call sentinel",
            "py-itergen-adv-iter-call",
            "Use `iter(callable, sentinel)` with values `[1,2,0]` and print sum.",
            "vals = iter([1, 2, 0].__iter__().__next__, 0)\nprint(sum(vals))",
            "3",
            ["python", "iterators", "sentinel"],
            "code_completion",
        ),
        (
            "Debug missing StopIteration",
            "py-itergen-adv-debug-stopiteration",
            "Fix iterator class that forgets to raise `StopIteration`; print `3` from sum.",
            "class Bad:\n    def __iter__(self):\n        self.i = 0\n        return self\n    def __next__(self):\n        self.i += 1\n        return self.i\nprint(sum(x for x in Bad() if x <= 2))",
            "3",
            ["python", "iterators", "debugging"],
            "debug_model",
        ),
        (
            "Memory efficient chaining",
            "py-itergen-adv-chain",
            "Use `itertools.chain` on `[1,2]` and `(3,)`, then print last element.",
            "import itertools\nvals = list(itertools.chain([1, 2], (3,)))\nprint(vals[-1])",
            "3",
            ["python", "iterators", "chain"],
            "code_completion",
        ),
        (
            "Islice window",
            "py-itergen-adv-islice",
            "Use `itertools.islice(range(10), 3, 6)` and print values comma-separated.",
            "import itertools\nprint(','.join(str(x) for x in itertools.islice(range(10), 3, 6)))",
            "3,4,5",
            ["python", "iterators", "islice"],
            "code_completion",
        ),
        (
            "Pairwise iteration",
            "py-itergen-adv-pairwise",
            "Use `itertools.pairwise([1,2,3])` and print number of produced pairs.",
            "import itertools\nprint(len(list(itertools.pairwise([1, 2, 3]))))",
            "2",
            ["python", "iterators", "pairwise"],
            "code_completion",
        ),
        (
            "Groupby requires sort",
            "py-itergen-adv-groupby",
            "Sort `[1,1,2,2,2]`, group with `itertools.groupby`, print key with longest run.",
            "import itertools\nbest_k = None\nbest_n = -1\nfor k, grp in itertools.groupby(sorted([1, 1, 2, 2, 2])):\n    n = len(list(grp))\n    if n > best_n:\n        best_n = n\n        best_k = k\nprint(best_k)",
            "2",
            ["python", "iterators", "groupby"],
            "code_completion",
        ),
        (
            "Composed generator pipeline",
            "py-itergen-adv-pipeline",
            "Create pipeline doubling numbers then filtering >5 from `range(5)`, print sum.",
            "nums = (x * 2 for x in range(5))\nfiltered = (x for x in nums if x > 5)\nprint(sum(filtered))",
            "14",
            ["python", "generators", "pipeline"],
            "code_completion",
        ),
    ]
    for title, slug, prompt, solution, expected, tags, qtype in advanced_specs:
        if slug == "py-itergen-adv-debug-stopiteration":
            solution = (
                "class Good:\n"
                "    def __iter__(self):\n"
                "        self.i = 0\n"
                "        return self\n"
                "    def __next__(self):\n"
                "        self.i += 1\n"
                "        if self.i > 2:\n"
                "            raise StopIteration\n"
                "        return self.i\n"
                "print(sum(Good()))"
            )
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="advanced",
                prompt=prompt,
                starter_code="# complete advanced iterator/generator task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
                question_type=qtype,
            )
        )

    assert len([q for q in questions if q["difficulty"] == "basic"]) == 8
    assert len([q for q in questions if q["difficulty"] == "intermediate"]) == 10
    assert len([q for q in questions if q["difficulty"] == "advanced"]) == 10
    return questions


def _decorators_questions() -> list[dict]:
    questions: list[dict] = []
    add = questions.append

    # 8 basic
    basic_specs = [
        (
            "Simple function decorator",
            "py-deco-basic-simple",
            "Create decorator that prints `start` before wrapped function output.",
            "def log_start(fn):\n    def wrapper():\n        print('start')\n        fn()\n    return wrapper\n@log_start\ndef hello():\n    print('hello')\nhello()",
            "start\nhello",
            ["python", "decorators", "basics"],
        ),
        (
            "Decorator returns value",
            "py-deco-basic-return",
            "Decorate a function returning 3 so wrapper adds 2 and print result.",
            "def plus_two(fn):\n    def wrapper():\n        return fn() + 2\n    return wrapper\n@plus_two\ndef val():\n    return 3\nprint(val())",
            "5",
            ["python", "decorators", "return-values"],
        ),
        (
            "Use @wraps metadata",
            "py-deco-basic-wraps",
            "Use `functools.wraps` and print preserved function name.",
            "from functools import wraps\ndef deco(fn):\n    @wraps(fn)\n    def wrapper():\n        return fn()\n    return wrapper\n@deco\ndef greet():\n    return 'hi'\nprint(greet.__name__)",
            "greet",
            ["python", "decorators", "wraps"],
        ),
        (
            "Decorator with *args",
            "py-deco-basic-args",
            "Decorate add function and print sum for `2, 5`.",
            "def passthrough(fn):\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper\n@passthrough\ndef add(a, b):\n    return a + b\nprint(add(2, 5))",
            "7",
            ["python", "decorators", "args"],
        ),
        (
            "Count calls decorator",
            "py-deco-basic-count-calls",
            "Decorator tracks call count; call twice and print count.",
            "def count_calls(fn):\n    def wrapper():\n        wrapper.calls += 1\n        return fn()\n    wrapper.calls = 0\n    return wrapper\n@count_calls\ndef ping():\n    return 'pong'\nping()\nping()\nprint(ping.calls)",
            "2",
            ["python", "decorators", "state"],
        ),
        (
            "Decorate function printing text",
            "py-deco-basic-before-after",
            "Decorator prints `before`, then function, then `after`.",
            "def around(fn):\n    def wrapper():\n        print('before')\n        fn()\n        print('after')\n    return wrapper\n@around\ndef run():\n    print('run')\nrun()",
            "before\nrun\nafter",
            ["python", "decorators", "execution-order"],
        ),
        (
            "Identity decorator",
            "py-deco-basic-identity",
            "Write decorator returning original function behavior; print `42`.",
            "def identity(fn):\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper\n@identity\ndef f():\n    return 42\nprint(f())",
            "42",
            ["python", "decorators", "basics"],
        ),
        (
            "Decorate with uppercase output",
            "py-deco-basic-uppercase",
            "Decorator uppercases string result; print decorated output.",
            "def upper(fn):\n    def wrapper():\n        return fn().upper()\n    return wrapper\n@upper\ndef word():\n    return 'python'\nprint(word())",
            "PYTHON",
            ["python", "decorators", "strings"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in basic_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="basic",
                prompt=prompt,
                starter_code="# complete basic decorators task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 10 intermediate
    intermediate_specs = [
        (
            "Parameterized decorator",
            "py-deco-int-parameterized",
            "Create decorator factory `repeat(n)` and print `hi` two times.",
            "def repeat(n):\n    def deco(fn):\n        def wrapper():\n            for _ in range(n):\n                fn()\n        return wrapper\n    return deco\n@repeat(2)\ndef say_hi():\n    print('hi')\nsay_hi()",
            "hi\nhi",
            ["python", "decorators", "factory"],
        ),
        (
            "Timing decorator skeleton",
            "py-deco-int-timing",
            "Decorator should run function then print `done`.",
            "def timed(fn):\n    def wrapper():\n        fn()\n        print('done')\n    return wrapper\n@timed\ndef work():\n    pass\nwork()",
            "done",
            ["python", "decorators", "timing"],
        ),
        (
            "Memoization decorator basic",
            "py-deco-int-memo",
            "Memoize square function; call twice with same input and print cache size.",
            "def memo(fn):\n    cache = {}\n    def wrapper(x):\n        if x not in cache:\n            cache[x] = fn(x)\n        return cache[x]\n    wrapper.cache = cache\n    return wrapper\n@memo\ndef sq(x):\n    return x * x\nsq(4)\nsq(4)\nprint(len(sq.cache))",
            "1",
            ["python", "decorators", "memoization"],
        ),
        (
            "Decorator with kwargs",
            "py-deco-int-kwargs",
            "Decorate function with kwargs support and print `name=Ana`.",
            "def pass_kwargs(fn):\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper\n@pass_kwargs\ndef show(name='x'):\n    print(f'name={name}')\nshow(name='Ana')",
            "name=Ana",
            ["python", "decorators", "kwargs"],
        ),
        (
            "Stack two decorators",
            "py-deco-int-stacking",
            "Stack decorators adding prefix and suffix around `core` and print result.",
            "def prefix(fn):\n    def wrapper():\n        return 'A-' + fn()\n    return wrapper\ndef suffix(fn):\n    def wrapper():\n        return fn() + '-Z'\n    return wrapper\n@prefix\n@suffix\ndef core():\n    return 'core'\nprint(core())",
            "A-core-Z",
            ["python", "decorators", "stacking"],
        ),
        (
            "Class based decorator",
            "py-deco-int-class-based",
            "Create class decorator callable that triples function result.",
            "class Triple:\n    def __init__(self, fn):\n        self.fn = fn\n    def __call__(self):\n        return self.fn() * 3\n@Triple\ndef get_two():\n    return 2\nprint(get_two())",
            "6",
            ["python", "decorators", "class-based"],
        ),
        (
            "Permission check decorator",
            "py-deco-int-permission",
            "Decorator allows call only when `is_admin=True`; print `allowed`.",
            "def require_admin(fn):\n    def wrapper(is_admin):\n        if is_admin:\n            return fn(is_admin)\n        return 'denied'\n    return wrapper\n@require_admin\ndef action(is_admin):\n    return 'allowed'\nprint(action(True))",
            "allowed",
            ["python", "decorators", "guards"],
        ),
        (
            "Retry once decorator",
            "py-deco-int-retry-once",
            "Decorator retries once on `ValueError`; function succeeds second time and prints `ok`.",
            "def retry_once(fn):\n    def wrapper():\n        try:\n            return fn()\n        except ValueError:\n            return fn()\n    return wrapper\nstate = {'n': 0}\n@retry_once\ndef flaky():\n    state['n'] += 1\n    if state['n'] == 1:\n        raise ValueError('first fail')\n    return 'ok'\nprint(flaky())",
            "ok",
            ["python", "decorators", "retry"],
        ),
        (
            "Log arguments decorator",
            "py-deco-int-log-args",
            "Decorator prints argument count before calling function with three args.",
            "def log_args(fn):\n    def wrapper(*args, **kwargs):\n        print(len(args))\n        return fn(*args, **kwargs)\n    return wrapper\n@log_args\ndef total(a, b, c):\n    return a + b + c\ntotal(1, 2, 3)",
            "3",
            ["python", "decorators", "logging"],
        ),
        (
            "Decorator preserves docstring",
            "py-deco-int-docstring",
            "Use `@wraps` and print wrapped function docstring.",
            "from functools import wraps\ndef deco(fn):\n    @wraps(fn)\n    def wrapper():\n        return fn()\n    return wrapper\n@deco\ndef sample():\n    '''demo doc'''\n    return 1\nprint(sample.__doc__)",
            "demo doc",
            ["python", "decorators", "wraps"],
        ),
    ]
    for title, slug, prompt, solution, expected, tags in intermediate_specs:
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="intermediate",
                prompt=prompt,
                starter_code="# complete intermediate decorators task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
            )
        )

    # 8 advanced
    advanced_specs = [
        (
            "Decorator with closure state",
            "py-deco-adv-closure-state",
            "Create decorator counting successful calls and print count after three calls.",
            "def count_success(fn):\n    count = 0\n    def wrapper():\n        nonlocal count\n        fn()\n        count += 1\n        return count\n    return wrapper\n@count_success\ndef op():\n    return None\nop()\nop()\nprint(op())",
            "3",
            ["python", "decorators", "closures"],
            "code_completion",
        ),
        (
            "Descriptor style method decorator",
            "py-deco-adv-method",
            "Decorate instance method to multiply return value by 10 and print result.",
            "def times_ten(fn):\n    def wrapper(self, *args, **kwargs):\n        return fn(self, *args, **kwargs) * 10\n    return wrapper\nclass A:\n    @times_ten\n    def v(self):\n        return 3\nprint(A().v())",
            "30",
            ["python", "decorators", "methods"],
            "code_completion",
        ),
        (
            "Async compatible decorator",
            "py-deco-adv-async",
            "Write async decorator that awaits wrapped coroutine and print `7`.",
            "import asyncio\ndef deco(fn):\n    async def wrapper():\n        return await fn()\n    return wrapper\n@deco\nasync def get_num():\n    return 7\nprint(asyncio.run(get_num()))",
            "7",
            ["python", "decorators", "async"],
            "code_completion",
        ),
        (
            "Rate limiter skeleton",
            "py-deco-adv-rate-limiter",
            "Implement simple limiter allowing first two calls; print third call result `blocked`.",
            "def limit_two(fn):\n    state = {'count': 0}\n    def wrapper():\n        state['count'] += 1\n        if state['count'] > 2:\n            return 'blocked'\n        return fn()\n    return wrapper\n@limit_two\ndef ping():\n    return 'ok'\nping()\nping()\nprint(ping())",
            "blocked",
            ["python", "decorators", "rate-limit"],
            "code_completion",
        ),
        (
            "Debug missing wraps metadata",
            "py-deco-adv-debug-wraps",
            "Fix decorator to preserve function name so output is `target`.",
            "def deco(fn):\n    def wrapper():\n        return fn()\n    return wrapper\n@deco\ndef target():\n    return 1\nprint(target.__name__)",
            "target",
            ["python", "decorators", "debugging"],
            "debug_model",
        ),
        (
            "Decorator factory with label",
            "py-deco-adv-factory-label",
            "Decorator factory prepends label `'INFO'` and print result for message `ok`.",
            "def label(prefix):\n    def deco(fn):\n        def wrapper(msg):\n            return f'{prefix}:{fn(msg)}'\n        return wrapper\n    return deco\n@label('INFO')\ndef emit(msg):\n    return msg\nprint(emit('ok'))",
            "INFO:ok",
            ["python", "decorators", "factory"],
            "code_completion",
        ),
        (
            "Compose decorators programmatically",
            "py-deco-adv-compose",
            "Apply two decorators manually to function returning `x`; print `A-x-B`.",
            "def add_a(fn):\n    def wrapper():\n        return 'A-' + fn()\n    return wrapper\ndef add_b(fn):\n    def wrapper():\n        return fn() + '-B'\n    return wrapper\ndef base():\n    return 'x'\nwrapped = add_b(add_a(base))\nprint(wrapped())",
            "A-x-B",
            ["python", "decorators", "composition"],
            "code_completion",
        ),
        (
            "Cache decorator with clear",
            "py-deco-adv-cache-clear",
            "Decorator caches values and provides `clear`; print cache size after clear.",
            "def cache(fn):\n    store = {}\n    def wrapper(x):\n        if x not in store:\n            store[x] = fn(x)\n        return store[x]\n    def clear():\n        store.clear()\n    wrapper.clear = clear\n    wrapper.store = store\n    return wrapper\n@cache\ndef inc(x):\n    return x + 1\ninc(1)\ninc.clear()\nprint(len(inc.store))",
            "0",
            ["python", "decorators", "cache"],
            "code_completion",
        ),
    ]
    for title, slug, prompt, solution, expected, tags, qtype in advanced_specs:
        if slug == "py-deco-adv-debug-wraps":
            solution = (
                "from functools import wraps\n"
                "def deco(fn):\n"
                "    @wraps(fn)\n"
                "    def wrapper():\n"
                "        return fn()\n"
                "    return wrapper\n"
                "@deco\n"
                "def target():\n"
                "    return 1\n"
                "print(target.__name__)"
            )
        add(
            _q(
                title=title,
                slug=slug,
                difficulty="advanced",
                prompt=prompt,
                starter_code="# complete advanced decorators task\n",
                solution_code=solution,
                expected_output=expected,
                tags=tags,
                question_type=qtype,
            )
        )

    assert len([q for q in questions if q["difficulty"] == "basic"]) == 8
    assert len([q for q in questions if q["difficulty"] == "intermediate"]) == 10
    assert len([q for q in questions if q["difficulty"] == "advanced"]) == 8
    return questions


MODULES_PACKAGES_QUESTIONS = _modules_packages_questions()
FILE_IO_QUESTIONS = _file_io_questions()
EXCEPTIONS_QUESTIONS = _exceptions_questions()
ITERATORS_GENERATORS_QUESTIONS = _iterators_generators_questions()
DECORATORS_QUESTIONS = _decorators_questions()

assert len(MODULES_PACKAGES_QUESTIONS) == 22
assert len(FILE_IO_QUESTIONS) == 24
assert len(EXCEPTIONS_QUESTIONS) == 24
assert len(ITERATORS_GENERATORS_QUESTIONS) == 28
assert len(DECORATORS_QUESTIONS) == 26

TOPIC_BATCH = [
    ("modules-packages", MODULES_PACKAGES_QUESTIONS, "Module 11 — Modules & Packages"),
    ("file-io", FILE_IO_QUESTIONS, "Module 12 — File I/O"),
    ("exceptions", EXCEPTIONS_QUESTIONS, "Module 13 — Exceptions"),
    ("iterators-generators", ITERATORS_GENERATORS_QUESTIONS, "Module 14 — Iterators & Generators"),
    ("decorators", DECORATORS_QUESTIONS, "Module 15 — Decorators"),
]


async def main() -> None:
    total = 0
    for topic_slug, questions, module_label in TOPIC_BATCH:
        seeded = await seed_questions_for_topic(topic_slug, questions, module_label)
        total += seeded
    print(f"Seeded {total} questions across modules 11-15")


if __name__ == "__main__":
    asyncio.run(main())
