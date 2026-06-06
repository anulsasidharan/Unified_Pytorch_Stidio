"""
seeds/topics.py
---------------
Seed script for all 25 Python Learning Studio modules.

Usage:
    python -m seeds.topics

Requires DATABASE_URL in environment (or .env file loaded).
"""

import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/python_studio",
)

PYTHON_BLUE = "#3776AB"
PYTHON_YELLOW = "#FFD43B"

TOPICS = [
    {
        "module_number": 1,
        "name": "Python Basics & Setup",
        "slug": "python-basics",
        "description": (
            "Python installation, REPL, print(), comments, and indentation. "
            "Script execution, virtual environments, and Python runtime internals."
        ),
        "levels": {
            "basic": "Python installation, REPL, print(), comments, indentation rules",
            "intermediate": (
                "Script execution, __name__ == '__main__', shebang lines, virtual environments"
            ),
            "advanced": "Python versions (2 vs 3), CPython vs PyPy vs Jython, bytecode, .pyc files",
        },
        "mini_project": "Hello World+ — CLI tool that greets the user by name with timestamp",
        "icon": "🐍",
        "color": PYTHON_BLUE,
        "order_index": 1,
    },
    {
        "module_number": 2,
        "name": "Variables, Data Types & Operators",
        "slug": "variables-types",
        "description": (
            "int, float, str, bool, None; assignment and type(). "
            "Coercion, identity, and Python's memory model for objects."
        ),
        "levels": {
            "basic": "int, float, str, bool, None; variable assignment; type()",
            "intermediate": "Type coercion, implicit vs explicit conversion, id() and is",
            "advanced": "Memory model, object identity, mutable vs immutable, sys.getsizeof()",
        },
        "mini_project": "Type Inspector — CLI that reports types and sizes of user inputs",
        "icon": "🔢",
        "color": PYTHON_BLUE,
        "order_index": 2,
    },
    {
        "module_number": 3,
        "name": "Strings & String Operations",
        "slug": "strings",
        "description": (
            "Literals, indexing, slicing, and string methods. "
            "f-strings, Unicode, encoding, and regex basics."
        ),
        "levels": {
            "basic": "String literals, concatenation, indexing, slicing, len()",
            "intermediate": "split, join, strip, replace, find, f-strings, format()",
            "advanced": "Unicode handling, encode/decode, regex with re, str interning",
        },
        "mini_project": "Text Formatter — normalize and summarize multi-line user text",
        "icon": "📝",
        "color": PYTHON_YELLOW,
        "order_index": 3,
    },
    {
        "module_number": 4,
        "name": "Control Flow",
        "slug": "control-flow",
        "description": (
            "if/elif/else, comparisons, and logical operators. "
            "match-case, guard clauses, and truthy/falsy semantics."
        ),
        "levels": {
            "basic": "if/elif/else, comparison operators, and/or/not",
            "intermediate": "Nested conditions, ternary, short-circuit, match-case (3.10+)",
            "advanced": "State machines with match-case, guard clauses, truthy/falsy deep dive",
        },
        "mini_project": "Grade Calculator — classify scores with match-case and validation",
        "icon": "🔀",
        "color": PYTHON_BLUE,
        "order_index": 4,
    },
    {
        "module_number": 5,
        "name": "Loops & Iteration",
        "slug": "loops",
        "description": (
            "for/while loops, range(), break, continue, pass. "
            "enumerate, zip, loop-else, and the iteration protocol."
        ),
        "levels": {
            "basic": "for loops, while loops, range(), break, continue, pass",
            "intermediate": "enumerate(), zip(), nested loops, loop-else clause",
            "advanced": "__iter__/__next__, infinite generators, loop performance patterns",
        },
        "mini_project": "Number Guessing Game — loop-driven CLI with attempt tracking",
        "icon": "🔁",
        "color": PYTHON_YELLOW,
        "order_index": 5,
    },
    {
        "module_number": 6,
        "name": "Data Structures — Lists & Tuples",
        "slug": "lists-tuples",
        "description": (
            "List creation, mutation, slicing, and comprehensions. "
            "Tuples, unpacking, and list internals."
        ),
        "levels": {
            "basic": "List creation, indexing, append, remove, pop, slicing",
            "intermediate": "List comprehensions, sorted(), key functions, tuple unpacking",
            "advanced": "Memory layout, amortized append, array module, namedtuple",
        },
        "mini_project": "Todo List CLI — CRUD operations on an in-memory task list",
        "icon": "📋",
        "color": PYTHON_BLUE,
        "order_index": 6,
    },
    {
        "module_number": 7,
        "name": "Data Structures — Dictionaries & Sets",
        "slug": "dicts-sets",
        "description": (
            "Dict and set operations, comprehensions, defaultdict, Counter. "
            "Hash table internals and merge operators."
        ),
        "levels": {
            "basic": "Dict creation, get/set/delete, keys/values/items, set operations",
            "intermediate": "Dict/set comprehensions, defaultdict, Counter, OrderedDict",
            "advanced": "Hash collisions, frozenset, dict merge (3.9+), ordering guarantee",
        },
        "mini_project": "Word Frequency Counter — count tokens from stdin or a file",
        "icon": "🗂️",
        "color": PYTHON_YELLOW,
        "order_index": 7,
    },
    {
        "module_number": 8,
        "name": "Functions & Scope",
        "slug": "functions",
        "description": (
            "def, return, args, defaults, *args/**kwargs, and LEGB scope. "
            "Closures, functools, and higher-order functions."
        ),
        "levels": {
            "basic": "def, return, positional/default args, calling functions",
            "intermediate": "*args, **kwargs, keyword-only args, docstrings, type hints, LEGB",
            "advanced": "Closures, nonlocal, functools partial/lru_cache/reduce, annotations",
        },
        "mini_project": "Calculator Library — reusable pure functions with tests",
        "icon": "⚙️",
        "color": PYTHON_BLUE,
        "order_index": 8,
    },
    {
        "module_number": 9,
        "name": "Object-Oriented Programming",
        "slug": "oop",
        "description": (
            "Classes, __init__, self, inheritance, and properties. "
            "MRO, ABCs, metaclasses, and __slots__."
        ),
        "levels": {
            "basic": "class, __init__, self, instance vs class attributes, methods",
            "intermediate": "Inheritance, super(), @classmethod, @staticmethod, @property",
            "advanced": "Multiple inheritance, MRO, __slots__, ABC, metaclasses",
        },
        "mini_project": "Bank Account Model — OOP design with validation and history",
        "icon": "🏗️",
        "color": PYTHON_YELLOW,
        "order_index": 9,
    },
    {
        "module_number": 10,
        "name": "Dunder Methods & Operator Overloading",
        "slug": "dunder-methods",
        "description": (
            "__str__, __repr__, __len__, __eq__, and rich comparisons. "
            "Context managers, descriptors, and operator overloading."
        ),
        "levels": {
            "basic": "__str__, __repr__, __len__, __eq__",
            "intermediate": "__lt__/__gt__, __add__, __getitem__, __contains__, __call__",
            "advanced": "__enter__/__exit__, descriptors, __missing__, __class_getitem__",
        },
        "mini_project": "Vector2D Class — arithmetic dunder methods with repr/str",
        "icon": "✨",
        "color": PYTHON_BLUE,
        "order_index": 10,
    },
    {
        "module_number": 11,
        "name": "Modules, Packages & Imports",
        "slug": "modules-packages",
        "description": (
            "import styles, packages, __all__, and importlib. "
            "Namespace packages and circular import resolution."
        ),
        "levels": {
            "basic": "import, from/import, aliases, standard library overview",
            "intermediate": "Packages (__init__.py), relative imports, __all__, importlib",
            "advanced": "sys.path, custom importers, namespace packages, lazy imports",
        },
        "mini_project": "Mini Package — split code into a reusable installable package",
        "icon": "📦",
        "color": PYTHON_YELLOW,
        "order_index": 11,
    },
    {
        "module_number": 12,
        "name": "File I/O & Serialization",
        "slug": "file-io",
        "description": (
            "open(), with statement, pathlib, CSV, and JSON. "
            "Binary I/O, pickle, shelve, and mmap."
        ),
        "levels": {
            "basic": "open(), read/write modes, with, readlines(), writelines()",
            "intermediate": "pathlib, os.path, shutil, csv, JSON read/write",
            "advanced": "Binary files, struct, pickle, shelve, mmap",
        },
        "mini_project": "JSON Config Manager — load, validate, and save app settings",
        "icon": "💾",
        "color": PYTHON_BLUE,
        "order_index": 12,
    },
    {
        "module_number": 13,
        "name": "Exception Handling & Debugging",
        "slug": "exceptions",
        "description": (
            "try/except/finally, custom exceptions, and logging. "
            "traceback, pdb, and exception groups."
        ),
        "levels": {
            "basic": "try/except/finally, common exceptions, raise",
            "intermediate": "Custom exceptions, chaining, else clause, logging basics",
            "advanced": "Exception groups (3.11+), traceback, pdb, sys.exc_info()",
        },
        "mini_project": "Robust File Parser — graceful errors with structured logging",
        "icon": "🐛",
        "color": PYTHON_YELLOW,
        "order_index": 13,
    },
    {
        "module_number": 14,
        "name": "Iterators & Generators",
        "slug": "iterators-generators",
        "description": (
            "iter/next, yield, generator expressions, and itertools. "
            "Generator pipelines and coroutine basics."
        ),
        "levels": {
            "basic": "iter(), next(), for loop under the hood",
            "intermediate": "yield, generator functions/expressions, send()",
            "advanced": "yield from, infinite generators, itertools pipelines",
        },
        "mini_project": "Log Pipeline — lazy generator chain filtering large files",
        "icon": "♾️",
        "color": PYTHON_BLUE,
        "order_index": 14,
    },
    {
        "module_number": 15,
        "name": "Decorators",
        "slug": "decorators",
        "description": (
            "Function decorators, @wraps, decorators with args, and stacking. "
            "Memoization, rate limiting, and retry patterns."
        ),
        "levels": {
            "basic": "What decorators are, @functools.wraps, simple decorator pattern",
            "intermediate": "Decorators with arguments, class decorators, stacking",
            "advanced": "Descriptor-based decorators, memoization, rate limiters, retry",
        },
        "mini_project": "Timing Decorator Suite — measure and log function runtime",
        "icon": "🎀",
        "color": PYTHON_YELLOW,
        "order_index": 15,
    },
    {
        "module_number": 16,
        "name": "Functional Programming",
        "slug": "functional",
        "description": (
            "map, filter, lambda, reduce, and the operator module. "
            "Pure functions, composition, and immutability patterns."
        ),
        "levels": {
            "basic": "map(), filter(), lambda, sorted() with key",
            "intermediate": "functools.reduce(), partial(), operator module",
            "advanced": "Immutability, composition, toolz patterns, monadic patterns",
        },
        "mini_project": "Data Pipeline — compose small pure functions over records",
        "icon": "λ",
        "color": PYTHON_BLUE,
        "order_index": 16,
    },
    {
        "module_number": 17,
        "name": "Comprehensions & Expressions",
        "slug": "comprehensions",
        "description": (
            "List/dict/set comprehensions and nested forms. "
            "Generator expressions, walrus operator, and expression trees."
        ),
        "levels": {
            "basic": "List comprehensions, conditional comprehensions",
            "intermediate": "Dict/set comprehensions, nested comprehensions",
            "advanced": "Generator expressions vs lists, walrus operator (:=), expression trees",
        },
        "mini_project": "Report Builder — nested comprehensions over nested JSON",
        "icon": "🧩",
        "color": PYTHON_YELLOW,
        "order_index": 17,
    },
    {
        "module_number": 18,
        "name": "Type Hints & Static Typing",
        "slug": "type-hints",
        "description": (
            "Annotations, Optional, Union, Generics, Protocol, TypedDict. "
            "mypy configuration and runtime checking."
        ),
        "levels": {
            "basic": "Basic annotations, return types, Optional",
            "intermediate": "Union, List[T], Dict[K,V], TypeVar, Generic classes",
            "advanced": "Protocol, TypedDict, Literal, overload, mypy, beartype",
        },
        "mini_project": "Typed API Client — fully annotated HTTP wrapper with validation",
        "icon": "🏷️",
        "color": PYTHON_BLUE,
        "order_index": 18,
    },
    {
        "module_number": 19,
        "name": "Testing with pytest",
        "slug": "testing",
        "description": (
            "Writing tests, fixtures, parametrize, and mocking. "
            "Coverage, Hypothesis, and TDD workflow."
        ),
        "levels": {
            "basic": "assert, test functions, running pytest, discovery",
            "intermediate": "fixtures, parametrize, conftest.py, unittest.mock",
            "advanced": "pytest plugins, coverage.py, Hypothesis, TDD, integration tests",
        },
        "mini_project": "Test Suite — pytest coverage for a small library module",
        "icon": "✅",
        "color": PYTHON_YELLOW,
        "order_index": 19,
    },
    {
        "module_number": 20,
        "name": "Standard Library Deep Dive",
        "slug": "stdlib",
        "description": (
            "os, sys, datetime, collections, itertools, pathlib, and more. "
            "dataclasses, enum, inspect, ast, and dis."
        ),
        "levels": {
            "basic": "os, sys, math, random, datetime, time",
            "intermediate": "collections, itertools, functools, pathlib, re, json, csv",
            "advanced": "dataclasses, enum, contextlib, weakref, gc, inspect, ast, dis",
        },
        "mini_project": "CLI File Stats Tool — pathlib + collections + argparse",
        "icon": "📚",
        "color": PYTHON_BLUE,
        "order_index": 20,
    },
    {
        "module_number": 21,
        "name": "Concurrency — Threading & Multiprocessing",
        "slug": "concurrency",
        "description": (
            "GIL, threading, multiprocessing, pools, and locks. "
            "Race conditions, deadlocks, and concurrent.futures."
        ),
        "levels": {
            "basic": "GIL, threading.Thread, multiprocessing.Process",
            "intermediate": "ThreadPoolExecutor, process pools, Queue, Lock, Event",
            "advanced": "Race conditions, deadlocks, semaphores, shared memory",
        },
        "mini_project": "Parallel Downloader — thread pool fetching URLs safely",
        "icon": "🧵",
        "color": PYTHON_YELLOW,
        "order_index": 21,
    },
    {
        "module_number": 22,
        "name": "Async Programming & asyncio",
        "slug": "async",
        "description": (
            "async/await, asyncio.run, gather, tasks, and aiohttp. "
            "Event loop internals and structured concurrency."
        ),
        "levels": {
            "basic": "async/await syntax, coroutines, asyncio.run()",
            "intermediate": "asyncio.gather(), create_task(), aiohttp, async generators",
            "advanced": "Event loop internals, asyncio.Queue, TaskGroup (3.11+)",
        },
        "mini_project": "Async URL Fetcher — concurrent HTTP requests with asyncio",
        "icon": "⚡",
        "color": PYTHON_BLUE,
        "order_index": 22,
    },
    {
        "module_number": 23,
        "name": "Performance & Optimization",
        "slug": "performance",
        "description": (
            "timeit, cProfile, Big O in Python, and memory profiling. "
            "Cython, Numba, ctypes, and vectorization."
        ),
        "levels": {
            "basic": "timeit, cProfile, Big O in Python context",
            "intermediate": "memory_profiler, __slots__, common bottlenecks",
            "advanced": "Cython, Numba JIT, ctypes/cffi, NumPy vectorization, PyPy",
        },
        "mini_project": "Benchmark Harness — compare implementations with timeit",
        "icon": "🚀",
        "color": PYTHON_YELLOW,
        "order_index": 23,
    },
    {
        "module_number": 24,
        "name": "Design Patterns in Python",
        "slug": "design-patterns",
        "description": (
            "Singleton, Factory, Observer, Strategy, Command, and Builder. "
            "Pythonic alternatives and SOLID with Protocol."
        ),
        "levels": {
            "basic": "Singleton, Factory, Observer patterns",
            "intermediate": "Strategy, Decorator pattern, Command, Builder",
            "advanced": "Pythonic GoF alternatives, SOLID, dataclass patterns, Protocol",
        },
        "mini_project": "Plugin System — Strategy + Factory for swappable handlers",
        "icon": "🧱",
        "color": PYTHON_BLUE,
        "order_index": 24,
    },
    {
        "module_number": 25,
        "name": "Python for Data & Scripting",
        "slug": "data-scripting",
        "description": (
            "CSV/JSON/XML, argparse, pandas basics, requests, dotenv. "
            "SQLAlchemy, Pydantic, Typer/Click, and subprocess."
        ),
        "levels": {
            "basic": "CSV, JSON, XML; argparse for CLI tools",
            "intermediate": "pandas basics, requests/httpx, dotenv",
            "advanced": "SQLAlchemy ORM, Pydantic, Typer/Click, subprocess scripting",
        },
        "mini_project": "ETL Script — ingest CSV, validate with Pydantic, export JSON",
        "icon": "📊",
        "color": PYTHON_YELLOW,
        "order_index": 25,
    },
]


def _seed_row(topic: dict) -> dict:
    """Strip non-DB fields before insert."""
    return {
        "module_number": topic["module_number"],
        "name": topic["name"],
        "slug": topic["slug"],
        "description": topic["description"],
        "icon": topic["icon"],
        "color": topic["color"],
        "order_index": topic["order_index"],
    }


async def seed_topics():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM topics"))
        count = result.scalar()

        if count > 0:
            print(f"[skip] Topics table already has {count} rows. Skipping seed.")
            print("    To re-seed, run: DELETE FROM topics; then re-run this script.")
            return

        for topic in TOPICS:
            await session.execute(
                text("""
                    INSERT INTO topics (
                        module_number, name, slug, description,
                        icon, color, order_index, total_questions, is_active
                    ) VALUES (
                        :module_number, :name, :slug, :description,
                        :icon, :color, :order_index, 0, TRUE
                    )
                """),
                _seed_row(topic),
            )

        await session.commit()
        print(f"[ok] Seeded {len(TOPICS)} Python modules successfully.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_topics())
