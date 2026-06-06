# Unified Python Learning Studio — CLAUDE.md

> **Architecture Origin**: Forked and adapted from Unified PyTorch Studio (which itself was adapted from Unified DSA Studio).
> All backend infrastructure, spaced repetition engine, daily tracker, auth, and DB patterns are reused.
> Domain content, topic taxonomy, question schema extensions, live code execution, and AI tutor persona are Python-specific.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Reuse Map](#2-architecture-reuse-map)
3. [Tech Stack](#3-tech-stack)
4. [Python Learning Curriculum](#4-python-learning-curriculum)
5. [Database Schema](#5-database-schema)
6. [API Endpoints](#6-api-endpoints)
7. [Frontend Pages & Components](#7-frontend-pages--components)
8. [AI Tutor Configuration](#8-ai-tutor-configuration)
9. [Live Code Execution Engine](#9-live-code-execution-engine)
10. [Spaced Repetition & Tracker](#10-spaced-repetition--tracker)
11. [Question Format Specification](#11-question-format-specification)
12. [Seed Data Summary](#12-seed-data-summary)
13. [Implementation Roadmap](#13-implementation-roadmap)
14. [Environment Variables](#14-environment-variables)
15. [Project Folder Structure](#15-project-folder-structure)

---

## 1. Project Overview

**Unified Python Learning Studio** is an interactive, AI-powered platform for learning Python from absolute beginner to professional level. It covers 25 structured modules ranging from syntax basics to advanced topics like async programming, design patterns, performance optimization, and data engineering.

### Core Value Proposition

| Feature | Description |
|---|---|
| **Structured Curriculum** | 25 modules × 3 levels (Basic / Intermediate / Advanced) |
| **Live Code Execution** | Monaco Editor + Pyodide (Python in browser, zero server cost) |
| **AI Python Tutor** | GPT-4o tutor specialized in Python debugging, PEP 8, Pythonic code |
| **Spaced Repetition** | SM-2 algorithm for question scheduling and long-term retention |
| **Daily Tracker** | Streak system, heatmap, time-spent analytics |
| **Auto-Grader** | Checks output, handles edge cases, gives line-level feedback |
| **Project Challenges** | End-of-module real-world mini projects |
| **Snippet Library** | 500+ reusable Pythonic patterns |

### Target Audience
- Beginners learning Python from scratch
- Developers from other languages transitioning to Python
- Data practitioners wanting stronger Python fundamentals
- Developers preparing for Python interviews

---

## 2. Architecture Reuse Map

All infrastructure is reused from Unified PyTorch Studio. Only domain content changes.

| Component | Reuse | Action Required |
|---|---|---|
| FastAPI backend structure | ✅ Full reuse | Change domain models only |
| PostgreSQL DB schema | ✅ Full reuse | Add `starter_code`, `expected_output`, `run_in_browser` columns |
| JWT Auth / user management | ✅ Full reuse | No change |
| Spaced repetition engine (SM-2) | ✅ Full reuse | No change |
| Daily tracker / streak logic | ✅ Full reuse | No change |
| Analytics dashboard | ✅ Full reuse | Retheme labels only |
| External question import | ✅ Full reuse | Add `.py` file import |
| Next.js frontend layout | ✅ Full reuse | Retheme (Python blue/yellow) + new sidebar |
| Docker Compose config | ✅ Full reuse | No change |
| CI/CD pipeline | ✅ Full reuse | No change |
| AI chatbot service | ✅ Adapt | Swap system prompt → Python tutor |
| Colab integration | ✅ Adapt | Point to Python notebooks |
| Topic seeder | 🔄 Replace | 25 Python modules replace PyTorch modules |
| Question DB content | 🔄 Replace | Python-specific questions/solutions |
| Code execution | 🆕 New | Add Pyodide WASM + Monaco Editor |
| Output assertion engine | 🆕 New | Auto-grader for Python output |
| PEP 8 linter | 🆕 New | Real-time style feedback |

---

## 3. Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Cache**: Redis (session, leaderboard, rate limiting)
- **Task Queue**: Celery + Redis (background grading, email digests)
- **Auth**: JWT (access + refresh tokens), bcrypt password hashing
- **Code Sandbox**: Pyodide (browser-side) + Docker-isolated subprocess (server-side fallback)
- **AI**: OpenAI GPT-4o via LangChain

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: Tailwind CSS + shadcn/ui
- **Code Editor**: Monaco Editor (VS Code engine)
- **Python Runtime**: Pyodide (Python 3.11 WASM)
- **Charts**: Recharts
- **State**: Zustand

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Cloud**: AWS (ECS Fargate / EC2, RDS, ElastiCache, S3)
- **CDN**: CloudFront
- **CI/CD**: GitHub Actions

---

## 4. Python Learning Curriculum

### Module Overview (25 Modules)

Each module has:
- **3 difficulty tiers**: Basic / Intermediate / Advanced
- **8–12 practice questions** per tier
- **1 mini project** at end of module
- **Concept cards** with visual explanations
- **Runnable code examples** in Monaco Editor

---

### Module 1 — Python Basics & Setup
**Slug**: `python-basics`

| Level | Topics |
|---|---|
| Basic | Python installation, REPL, print(), comments, indentation rules |
| Intermediate | Script execution, `__name__ == "__main__"`, shebang lines, virtual environments |
| Advanced | Python versions (2 vs 3), CPython vs PyPy vs Jython, bytecode, .pyc files |

**Mini Project**: "Hello World+" — CLI tool that greets the user by name with timestamp

---

### Module 2 — Variables, Data Types & Operators
**Slug**: `variables-types`

| Level | Topics |
|---|---|
| Basic | int, float, str, bool, None; variable assignment; type() |
| Intermediate | Type coercion, implicit vs explicit conversion, int overflow (Python has none), id() and is |
| Advanced | Memory model (stack vs heap), object identity, mutable vs immutable deep dive, sys.getsizeof() |

---

### Module 3 — Strings & String Operations
**Slug**: `strings`

| Level | Topics |
|---|---|
| Basic | String literals, concatenation, indexing, slicing, len() |
| Intermediate | String methods (split, join, strip, replace, find), f-strings, format() |
| Advanced | Unicode handling, encode/decode, regex basics with `re`, str interning, multiline strings |

---

### Module 4 — Control Flow
**Slug**: `control-flow`

| Level | Topics |
|---|---|
| Basic | if/elif/else, comparison operators, logical operators (and/or/not) |
| Intermediate | Nested conditions, ternary expressions, short-circuit evaluation, match-case (Python 3.10+) |
| Advanced | State machines with match-case, guard clauses, early return patterns, truthy/falsy deep dive |

---

### Module 5 — Loops & Iteration
**Slug**: `loops`

| Level | Topics |
|---|---|
| Basic | for loops, while loops, range(), break, continue, pass |
| Intermediate | enumerate(), zip(), nested loops, loop-else clause |
| Advanced | Iteration protocol (`__iter__`, `__next__`), infinite generators, loop unrolling, performance patterns |

---

### Module 6 — Data Structures — Lists & Tuples
**Slug**: `lists-tuples`

| Level | Topics |
|---|---|
| Basic | List creation, indexing, append, remove, pop, slicing |
| Intermediate | List comprehensions, sorted(), key functions, list as stack/queue, tuple unpacking |
| Advanced | Memory layout, list internals, amortized O(1) append, `array` module vs list, namedtuple |

---

### Module 7 — Data Structures — Dictionaries & Sets
**Slug**: `dicts-sets`

| Level | Topics |
|---|---|
| Basic | Dict creation, get/set/delete, .keys()/.values()/.items(), set operations |
| Intermediate | Dict comprehensions, set comprehensions, defaultdict, Counter, OrderedDict |
| Advanced | Hash table internals, hash collisions, frozenset, dict merge operators (Python 3.9+), dict ordering guarantee |

---

### Module 8 — Functions & Scope
**Slug**: `functions`

| Level | Topics |
|---|---|
| Basic | def, return, positional args, default args, calling functions |
| Intermediate | *args, **kwargs, keyword-only args, docstrings, type hints, LEGB scope rule |
| Advanced | Closures, nonlocal, functools (partial, lru_cache, reduce), higher-order functions, function annotations |

---

### Module 9 — Object-Oriented Programming
**Slug**: `oop`

| Level | Topics |
|---|---|
| Basic | class, __init__, self, instance vs class attributes, methods |
| Intermediate | Inheritance, super(), method overriding, @classmethod, @staticmethod, @property |
| Advanced | Multiple inheritance, MRO (C3 linearization), __slots__, abstract classes (ABC), metaclasses, __init_subclass__ |

---

### Module 10 — Dunder Methods & Operator Overloading
**Slug**: `dunder-methods`

| Level | Topics |
|---|---|
| Basic | __str__, __repr__, __len__, __eq__ |
| Intermediate | __lt__/__gt__ (total_ordering), __add__, __getitem__, __contains__, __call__ |
| Advanced | __enter__/__exit__ (context managers), __get__/__set__ (descriptors), __missing__, __class_getitem__ |

---

### Module 11 — Modules, Packages & Imports
**Slug**: `modules-packages`

| Level | Topics |
|---|---|
| Basic | import, from/import, aliases, standard library overview |
| Intermediate | Creating packages (__init__.py), relative imports, __all__, importlib |
| Advanced | sys.path manipulation, custom importers, namespace packages (PEP 420), lazy imports, circular import resolution |

---

### Module 12 — File I/O & Serialization
**Slug**: `file-io`

| Level | Topics |
|---|---|
| Basic | open(), read/write modes, with statement, readlines(), writelines() |
| Intermediate | pathlib, os.path, shutil, csv module, JSON read/write |
| Advanced | Binary files, struct module, pickle, shelve, mmap, memory-mapped files |

---

### Module 13 — Exception Handling & Debugging
**Slug**: `exceptions`

| Level | Topics |
|---|---|
| Basic | try/except/finally, common exceptions, raise |
| Intermediate | Custom exceptions, exception chaining (__cause__, __context__), else clause, logging basics |
| Advanced | Exception groups (Python 3.11+), traceback module, pdb debugger, sys.exc_info(), context managers for errors |

---

### Module 14 — Iterators & Generators
**Slug**: `iterators-generators`

| Level | Topics |
|---|---|
| Basic | iter(), next(), for loop under the hood |
| Intermediate | yield, generator functions, generator expressions, send() |
| Advanced | yield from, coroutine basics, infinite generators, itertools (chain, islice, product, combinations), generator pipelines |

---

### Module 15 — Decorators
**Slug**: `decorators`

| Level | Topics |
|---|---|
| Basic | What decorators are, @functools.wraps, simple decorator pattern |
| Intermediate | Decorators with arguments, class decorators, stacking decorators |
| Advanced | Descriptor-based decorators, decorator factories, memoization, rate limiters, retry decorators |

---

### Module 16 — Functional Programming
**Slug**: `functional`

| Level | Topics |
|---|---|
| Basic | map(), filter(), lambda, sorted() with key |
| Intermediate | functools.reduce(), partial(), operator module, zip_longest |
| Advanced | Immutability patterns, pure functions, function composition, toolz library patterns, monadic patterns in Python |

---

### Module 17 — Comprehensions & Expressions
**Slug**: `comprehensions`

| Level | Topics |
|---|---|
| Basic | List comprehensions, conditional comprehensions |
| Intermediate | Dict comprehensions, set comprehensions, nested comprehensions |
| Advanced | Generator expressions vs list comprehensions (memory), walrus operator (:=), expression trees |

---

### Module 18 — Type Hints & Static Typing
**Slug**: `type-hints`

| Level | Topics |
|---|---|
| Basic | Basic annotations (int, str, list), -> return type, Optional |
| Intermediate | Union, List[T], Dict[K,V], Tuple, TypeVar, Generic classes |
| Advanced | Protocol, TypedDict, Literal, Final, overload, mypy configuration, runtime type checking with beartype |

---

### Module 19 — Testing with pytest
**Slug**: `testing`

| Level | Topics |
|---|---|
| Basic | assert statements, writing test functions, running pytest, test discovery |
| Intermediate | fixtures, parametrize, conftest.py, mocking with unittest.mock |
| Advanced | pytest plugins, coverage.py, property-based testing with Hypothesis, TDD workflow, integration vs unit tests |

---

### Module 20 — Standard Library Deep Dive
**Slug**: `stdlib`

| Level | Topics |
|---|---|
| Basic | os, sys, math, random, datetime, time |
| Intermediate | collections, itertools, functools, pathlib, re, json, csv |
| Advanced | dataclasses, enum, contextlib, weakref, gc, inspect, ast, dis |

---

### Module 21 — Concurrency — Threading & Multiprocessing
**Slug**: `concurrency`

| Level | Topics |
|---|---|
| Basic | GIL explanation, threading.Thread, multiprocessing.Process |
| Intermediate | Thread pools (ThreadPoolExecutor), process pools, Queue, Lock, Event |
| Advanced | Race conditions, deadlocks, semaphores, shared memory (Python 3.8+), concurrent.futures patterns |

---

### Module 22 — Async Programming & asyncio
**Slug**: `async`

| Level | Topics |
|---|---|
| Basic | async/await syntax, coroutines, asyncio.run() |
| Intermediate | asyncio.gather(), asyncio.create_task(), aiohttp, async generators |
| Advanced | Event loop internals, asyncio.Queue, backpressure, structured concurrency (TaskGroup Python 3.11+), trio patterns |

---

### Module 23 — Performance & Optimization
**Slug**: `performance`

| Level | Topics |
|---|---|
| Basic | timeit, profiling with cProfile, understanding Big O in Python context |
| Intermediate | Memory profiling (memory_profiler), slots optimization, avoiding common Python bottlenecks |
| Advanced | Cython basics, Numba JIT, ctypes/cffi for C extensions, NumPy vectorization over loops, PyPy tradeoffs |

---

### Module 24 — Design Patterns in Python
**Slug**: `design-patterns`

| Level | Topics |
|---|---|
| Basic | Singleton, Factory, Observer patterns |
| Intermediate | Strategy, Decorator (design pattern vs Python decorator), Command, Builder |
| Advanced | Pythonic alternatives to GoF patterns, SOLID principles in Python, dataclasses-based patterns, Protocol-based polymorphism |

---

### Module 25 — Python for Data & Scripting
**Slug**: `data-scripting`

| Level | Topics |
|---|---|
| Basic | Reading/writing CSV, JSON, XML; argparse for CLI tools |
| Intermediate | pandas basics, API calls with requests/httpx, environment variables with dotenv |
| Advanced | SQLAlchemy ORM basics, Pydantic for data validation, building CLI tools with Typer/Click, scripting with subprocess |

---

## 5. Database Schema

### New Columns vs PyTorch Studio

Add these columns to `questions` table:

```sql
ALTER TABLE questions
  ADD COLUMN starter_code       TEXT,           -- Pre-filled code for the editor
  ADD COLUMN expected_output    TEXT,           -- Expected stdout for auto-grading
  ADD COLUMN expected_output_type VARCHAR(20)  -- 'exact', 'contains', 'regex', 'custom'
    DEFAULT 'exact',
  ADD COLUMN run_in_browser     BOOLEAN DEFAULT TRUE,  -- Pyodide eligible
  ADD COLUMN time_limit_ms      INTEGER DEFAULT 5000,  -- Execution time limit
  ADD COLUMN test_cases         JSONB,          -- Array of {input, expected_output}
  ADD COLUMN pep8_required      BOOLEAN DEFAULT FALSE; -- Fail if PEP 8 violations
```

### New Table: `code_submissions`

```sql
CREATE TABLE code_submissions (
  id              SERIAL PRIMARY KEY,
  user_id         INTEGER NOT NULL REFERENCES users(id),
  question_id     INTEGER NOT NULL REFERENCES questions(id),
  submitted_code  TEXT NOT NULL,
  actual_output   TEXT,
  is_correct      BOOLEAN,
  pep8_score      INTEGER,           -- 0-100
  execution_time_ms INTEGER,
  error_message   TEXT,
  submitted_at    TIMESTAMP DEFAULT NOW()
);
```

### New Table: `snippets`

```sql
CREATE TABLE snippets (
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(200) NOT NULL,
  slug        VARCHAR(200) UNIQUE,
  description TEXT,
  code        TEXT NOT NULL,
  module_id   INTEGER REFERENCES topics(id),
  tags        TEXT[],
  difficulty  VARCHAR(20),           -- 'beginner', 'intermediate', 'advanced'
  is_featured BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMP DEFAULT NOW()
);
```

### Existing Tables (Unchanged from PyTorch Studio)

- `users` — auth, profile, preferences
- `topics` — module definitions (now 25 rows)
- `questions` — practice questions (extended with above columns)
- `solutions` — user code submissions history
- `user_progress` — per-topic/per-question completion
- `study_sessions` — daily tracker entries
- `spaced_repetition_cards` — SM-2 scheduling
- `leaderboard` — weekly/monthly rankings

---

## 6. API Endpoints

### New Endpoints (Python-specific)

#### Code Execution
```
POST /api/execute
  body: { code: str, question_id?: int, time_limit_ms?: int }
  returns: { stdout, stderr, is_correct, execution_time_ms, pep8_violations }

POST /api/execute/batch
  body: { code: str, test_cases: [{input, expected_output}] }
  returns: { results: [{passed, actual_output, error}], score: int }
```

#### Snippets
```
GET  /api/snippets                   — list all (filterable by module/tag)
GET  /api/snippets/{slug}            — single snippet detail
POST /api/snippets                   — create snippet (admin)
GET  /api/snippets/featured          — featured snippets for dashboard
```

#### PEP 8 Linting
```
POST /api/lint
  body: { code: str }
  returns: { violations: [{line, col, code, message}], score: int }
```

#### Module Progress (Extended)
```
GET  /api/modules/{slug}/project     — get end-of-module project spec
POST /api/modules/{slug}/project     — submit project solution
```

### Reused Endpoints (Unchanged)

```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
GET  /api/topics                     — returns 25 Python modules
GET  /api/topics/{slug}/questions
GET  /api/questions/{id}
POST /api/questions/{id}/attempt
GET  /api/user/dashboard
GET  /api/user/streak
GET  /api/user/spaced-repetition
POST /api/user/spaced-repetition/{card_id}
GET  /api/leaderboard
POST /api/questions/import
```

---

## 7. Frontend Pages & Components

### Pages

| Route | Description |
|---|---|
| `/` | Landing page |
| `/dashboard` | User dashboard (streak, modules, recent activity) |
| `/modules` | All 25 modules grid view |
| `/modules/[slug]` | Module detail (subtopics, questions, project) |
| `/modules/[slug]/[level]` | Level questions list (basic/intermediate/advanced) |
| `/practice/[id]` | Question page with Monaco Editor + run button |
| `/snippets` | Snippet library browser |
| `/snippets/[slug]` | Single snippet with runnable editor |
| `/tracker` | Daily study tracker + heatmap |
| `/analytics` | Personal progress analytics |
| `/leaderboard` | Weekly/monthly rankings |
| `/tutor` | AI Python Tutor chat |
| `/import` | Import questions from file/URL |
| `/settings` | User preferences, editor theme |

### Key New Components

#### `<CodeEditor />`
- Monaco Editor instance
- Language: `python`
- Theme: `vs-dark` (default) or `vs-light`
- Features: syntax highlight, autocomplete, minimap, multi-cursor
- Props: `initialCode`, `readOnly`, `onCodeChange`

#### `<RunButton />`
- Triggers Pyodide execution
- Shows spinner during run
- Displays stdout/stderr in `<OutputPane />`

#### `<OutputPane />`
- Split: stdout (green) / stderr (red)
- Shows "✅ Correct" or "❌ Wrong output" with diff view
- Execution time badge

#### `<PEP8Badge />`
- Live linting score (0–100)
- Inline violation markers in editor gutter
- Click to show violation list

#### `<ModuleProgressRing />`
- Circular progress per module
- Shows Basic/Intermediate/Advanced completion %

#### `<SnippetCard />`
- Collapsible code preview
- Copy button + Open in Editor button
- Tags display

---

## 8. AI Tutor Configuration

### System Prompt

```python
PYTHON_TUTOR_SYSTEM_PROMPT = """
You are an expert Python tutor with deep knowledge of Python 3.11+.
Your teaching style is:
  - Practical and example-driven
  - Focused on Pythonic idioms over verbose code
  - PEP 8 and PEP 20 (Zen of Python) aware
  - Able to explain errors clearly (SyntaxError, TypeError, AttributeError, etc.)

When a user shares code:
  1. Identify bugs or style issues
  2. Explain WHY it's wrong (not just what to fix)
  3. Show the corrected Pythonic version
  4. Add a brief explanation of the concept used

When teaching concepts:
  - Use concrete runnable examples
  - Show what NOT to do alongside what to do
  - Reference the Python docs when relevant
  - Mention performance implications when relevant

Keep responses concise. Prefer short code blocks over long explanations.
Never write code that violates PEP 8 unless demonstrating what NOT to do.
"""
```

### Tutor Capabilities
- Debug Python errors from stack traces
- Explain output: "Why does this print X?"
- Review code for Pythonic style
- Answer concept questions
- Generate practice exercises on demand
- Explain time/space complexity of Python operations

---

## 9. Live Code Execution Engine

### Primary: Pyodide (Browser WASM)

```javascript
// frontend/lib/pyodide-runner.ts
import { loadPyodide } from 'pyodide';

let pyodide = null;

export async function initPyodide() {
  pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
  });
}

export async function runPython(code: string, timeoutMs = 5000): Promise<RunResult> {
  if (!pyodide) await initPyodide();

  // Capture stdout/stderr
  pyodide.runPython(`
    import sys, io
    _stdout_capture = io.StringIO()
    _stderr_capture = io.StringIO()
    sys.stdout = _stdout_capture
    sys.stderr = _stderr_capture
  `);

  try {
    const start = performance.now();
    await Promise.race([
      pyodide.runPythonAsync(code),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Time limit exceeded')), timeoutMs)
      )
    ]);
    const elapsed = performance.now() - start;

    const stdout = pyodide.runPython("_stdout_capture.getvalue()");
    const stderr = pyodide.runPython("_stderr_capture.getvalue()");
    return { stdout, stderr, error: null, executionTimeMs: Math.round(elapsed) };
  } catch (err) {
    const stderr = pyodide.runPython("_stderr_capture.getvalue()");
    return { stdout: '', stderr, error: err.message, executionTimeMs: 0 };
  } finally {
    // Reset stdout/stderr
    pyodide.runPython("sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__");
  }
}
```

### Output Assertion (Auto-Grader)

```python
# backend/services/grader.py

def grade_submission(
    actual_output: str,
    expected_output: str,
    check_type: str = 'exact'
) -> GradeResult:
    actual = actual_output.strip()
    expected = expected_output.strip()

    if check_type == 'exact':
        passed = actual == expected
    elif check_type == 'contains':
        passed = expected in actual
    elif check_type == 'regex':
        import re
        passed = bool(re.fullmatch(expected, actual))
    elif check_type == 'custom':
        # Run custom validator function stored in question
        passed = run_custom_validator(actual, expected)

    return GradeResult(
        passed=passed,
        actual=actual,
        expected=expected,
        diff=generate_diff(actual, expected) if not passed else None
    )
```

### PEP 8 Linter (Real-time)

```python
# backend/services/linter.py
import pyflakes.api
import pycodestyle

def lint_code(code: str) -> LintResult:
    # pycodestyle for PEP 8
    style_guide = pycodestyle.StyleGuide(quiet=True)
    result = style_guide.check_files(code=code)

    violations = []
    for error in result.messages:
        violations.append({
            "line": error.row,
            "col": error.col,
            "code": error.code,
            "message": error.text
        })

    score = max(0, 100 - len(violations) * 5)
    return LintResult(violations=violations, score=score)
```

### Fallback: Server-side Sandbox

For questions with I/O, file ops, or packages not in Pyodide:

```python
# backend/services/sandbox.py
import subprocess, resource, tempfile, os

def run_python_sandbox(code: str, time_limit: float = 5.0) -> SandboxResult:
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ['python3', '-c', code],
            capture_output=True,
            text=True,
            timeout=time_limit,
            # Resource limits
            preexec_fn=lambda: resource.setrlimit(
                resource.RLIMIT_AS, (50 * 1024 * 1024, 50 * 1024 * 1024)  # 50MB
            )
        )
        return SandboxResult(
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode
        )
    except subprocess.TimeoutExpired:
        return SandboxResult(stdout='', stderr='Time limit exceeded', returncode=-1)
    finally:
        os.unlink(tmp_path)
```

---

## 10. Spaced Repetition & Tracker

### SM-2 Algorithm (Unchanged from PyTorch Studio)

```python
def sm2_update(card: SpacedRepetitionCard, quality: int) -> SpacedRepetitionCard:
    """
    quality: 0-5 (0=blackout, 5=perfect)
    """
    if quality >= 3:
        if card.repetition == 0:
            card.interval = 1
        elif card.repetition == 1:
            card.interval = 6
        else:
            card.interval = round(card.interval * card.ease_factor)
        card.repetition += 1
    else:
        card.repetition = 0
        card.interval = 1

    card.ease_factor = max(
        1.3,
        card.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    )
    card.next_review = datetime.now() + timedelta(days=card.interval)
    return card
```

### Daily Tracker Metrics
- Questions attempted per day
- Questions correct per day
- Time spent coding (tracked via editor focus events)
- Module completion progress
- Streak counter with freeze mechanic
- Weekly study goal (configurable: 5/10/20 questions/day)

---

## 11. Question Format Specification

### Example Question (Module 8 — Functions, Intermediate)

```json
{
  "id": 801,
  "module_slug": "functions",
  "level": "intermediate",
  "title": "Default Mutable Argument Trap",
  "description": "Fix the function below. It has a classic Python gotcha with mutable default arguments. Make `add_item` work correctly so each call without an argument gets a fresh list.",
  "starter_code": "def add_item(item, items=[]):\n    items.append(item)\n    return items\n\nprint(add_item('a'))  # Should print ['a']\nprint(add_item('b'))  # Should print ['b']",
  "expected_output": "['a']\n['b']",
  "expected_output_type": "exact",
  "solution": "def add_item(item, items=None):\n    if items is None:\n        items = []\n    items.append(item)\n    return items\n\nprint(add_item('a'))\nprint(add_item('b'))",
  "explanation": "Mutable default arguments are evaluated once at function definition time, not per call. Use None as default and initialize inside the function body.",
  "hints": [
    "What happens to the default list between calls?",
    "Try using None as the default instead",
    "Check the Python docs on default argument evaluation"
  ],
  "tags": ["functions", "mutable-defaults", "gotchas", "common-mistakes"],
  "run_in_browser": true,
  "pep8_required": false,
  "time_limit_ms": 3000,
  "difficulty_rating": 3.2,
  "estimated_minutes": 8
}
```

---

## 12. Seed Data Summary

### Target Question Count

| Module | Basic | Intermediate | Advanced | Total |
|---|---|---|---|---|
| Python Basics | 10 | 8 | 6 | 24 |
| Variables & Types | 10 | 8 | 6 | 24 |
| Strings | 12 | 10 | 8 | 30 |
| Control Flow | 10 | 8 | 6 | 24 |
| Loops | 10 | 10 | 8 | 28 |
| Lists & Tuples | 12 | 10 | 8 | 30 |
| Dicts & Sets | 12 | 10 | 8 | 30 |
| Functions | 12 | 12 | 10 | 34 |
| OOP | 10 | 12 | 10 | 32 |
| Dunder Methods | 8 | 10 | 8 | 26 |
| Modules & Packages | 8 | 8 | 6 | 22 |
| File I/O | 10 | 8 | 6 | 24 |
| Exceptions | 10 | 8 | 6 | 24 |
| Iterators & Generators | 8 | 10 | 10 | 28 |
| Decorators | 8 | 10 | 8 | 26 |
| Functional Programming | 8 | 8 | 6 | 22 |
| Comprehensions | 10 | 8 | 6 | 24 |
| Type Hints | 8 | 10 | 8 | 26 |
| Testing | 8 | 10 | 8 | 26 |
| Standard Library | 10 | 10 | 8 | 28 |
| Concurrency | 6 | 8 | 8 | 22 |
| Async | 6 | 8 | 8 | 22 |
| Performance | 6 | 8 | 8 | 22 |
| Design Patterns | 6 | 8 | 8 | 22 |
| Data & Scripting | 8 | 10 | 8 | 26 |
| **TOTAL** | **234** | **232** | **194** | **660** |

### Snippet Library Target: 500 snippets across all 25 modules

---

## 13. Implementation Roadmap

### Phase 1 — Foundation Fork (Week 1–2)
- [ ] Fork Unified PyTorch Studio repo
- [ ] Rename to `unified-python-studio`
- [ ] Update all module references and topic seeds
- [ ] Run DB migrations (new columns)
- [ ] Retheme frontend (Python blue #3776AB / yellow #FFD43B)
- [ ] Update chatbot system prompt

### Phase 2 — Live Execution Engine (Week 3–4)
- [ ] Integrate Monaco Editor into question page
- [ ] Integrate Pyodide (load once, cache)
- [ ] Implement RunButton + OutputPane components
- [ ] Build auto-grader (exact/contains/regex modes)
- [ ] Add PEP 8 linter (pycodestyle via API)
- [ ] Server-side sandbox fallback (Docker subprocess)

### Phase 3 — Content Seeding (Week 5–7)
- [ ] Seed all 25 topic rows
- [ ] Write 100 starter questions (Modules 1–5)
- [ ] Write 100 questions (Modules 6–10)
- [ ] Write 100 questions (Modules 11–15)
- [ ] Write 130 questions (Modules 16–20)
- [ ] Write 130 questions (Modules 21–25)
- [ ] Seed 100 starter snippets

### Phase 4 — Advanced Features (Week 8–10)
- [ ] End-of-module projects (25 project specs)
- [ ] Snippet library browser + editor
- [ ] Multi-test-case batch grader
- [ ] Colab notebook launcher (per question)
- [ ] Question import from `.py` files

### Phase 5 — Polish & Launch (Week 11–12)
- [ ] AI tutor integration + Python-specific prompts
- [ ] Leaderboard activation
- [ ] Mobile responsiveness
- [ ] SEO / OG tags
- [ ] Docker + AWS deployment
- [ ] GitHub Actions CI/CD

---

## 14. Environment Variables

```env
# App
APP_NAME=unified-python-studio
APP_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/python_studio

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI (for AI tutor)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# AWS (production)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=ca-central-1
S3_BUCKET=python-studio-assets

# Pyodide (CDN version pin)
NEXT_PUBLIC_PYODIDE_VERSION=0.25.0
```

---

## 15. Project Folder Structure

```
unified-python-studio/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── user.py
│   │   ├── topic.py
│   │   ├── question.py
│   │   ├── submission.py       # NEW
│   │   └── snippet.py          # NEW
│   ├── routes/
│   │   ├── auth.py
│   │   ├── topics.py
│   │   ├── questions.py
│   │   ├── execute.py          # NEW
│   │   ├── lint.py             # NEW
│   │   ├── snippets.py         # NEW
│   │   ├── tracker.py
│   │   └── leaderboard.py
│   ├── services/
│   │   ├── chatbot.py          # Updated system prompt
│   │   ├── grader.py           # NEW
│   │   ├── linter.py           # NEW
│   │   ├── sandbox.py          # NEW
│   │   └── spaced_repetition.py
│   ├── seeds/
│   │   ├── topics.py           # 25 Python modules
│   │   ├── questions/
│   │   │   ├── module_01_basics.json
│   │   │   ├── module_02_types.json
│   │   │   └── ... (25 files)
│   │   └── snippets.json
│   └── migrations/
│       └── 001_python_studio_schema.sql
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Landing
│   │   ├── dashboard/
│   │   ├── modules/
│   │   │   └── [slug]/
│   │   │       └── [level]/
│   │   ├── practice/
│   │   │   └── [id]/
│   │   ├── snippets/
│   │   ├── tracker/
│   │   ├── analytics/
│   │   ├── leaderboard/
│   │   └── tutor/
│   ├── components/
│   │   ├── CodeEditor.tsx      # NEW — Monaco Editor wrapper
│   │   ├── RunButton.tsx       # NEW
│   │   ├── OutputPane.tsx      # NEW
│   │   ├── PEP8Badge.tsx       # NEW
│   │   ├── SnippetCard.tsx     # NEW
│   │   ├── ModuleGrid.tsx
│   │   ├── QuestionCard.tsx
│   │   └── TrackerHeatmap.tsx
│   └── lib/
│       ├── pyodide-runner.ts   # NEW
│       ├── api.ts
│       └── auth.ts
│
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .github/workflows/
│   └── ci-cd.yml
├── CLAUDE.md                   # This file
└── README.md
```

---

## Architecture Origin Chain

```
Unified DSA Studio
       ↓ (domain swap: DSA → PyTorch)
Unified PyTorch Studio
       ↓ (domain swap: PyTorch → Python)
       + Added: Live code execution (Pyodide + Monaco)
       + Added: Auto-grader + PEP 8 linter
       + Added: Snippet library
       + Expanded: 25 modules (vs 13)
Unified Python Learning Studio  ← YOU ARE HERE
```
