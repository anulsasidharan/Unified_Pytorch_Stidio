/** Static module metadata — 25 Python Learning Studio modules. */
export type ModuleLevelBreakdown = {
  basic: string;
  intermediate: string;
  advanced: string;
};

export type ModuleMeta = {
  module_number: number;
  name: string;
  icon: string;
  description: string;
  levels: ModuleLevelBreakdown;
  mini_project: string;
};

const PYTHON_BLUE = "#3776AB";

function mod(
  n: number,
  slug: string,
  name: string,
  icon: string,
  description: string,
  levels: ModuleLevelBreakdown,
  mini_project: string,
): [string, ModuleMeta] {
  return [
    slug,
    { module_number: n, name, icon, description, levels, mini_project },
  ];
}

export const MODULE_META: Record<string, ModuleMeta> = Object.fromEntries([
  mod(1, "python-basics", "Python Basics & Setup", "🐍", "Installation, REPL, print(), comments, and indentation.", { basic: "Python installation, REPL, print(), comments, indentation rules", intermediate: "Script execution, __name__ == '__main__', shebang lines, virtual environments", advanced: "Python versions (2 vs 3), CPython vs PyPy vs Jython, bytecode, .pyc files" }, "Hello World+ — CLI tool that greets the user by name with timestamp"),
  mod(2, "variables-types", "Variables, Data Types & Operators", "🔢", "int, float, str, bool, None; assignment, type(), and operators.", { basic: "int, float, str, bool, None; variable assignment; type()", intermediate: "Type coercion, implicit vs explicit conversion, id() and is", advanced: "Memory model, object identity, mutable vs immutable, sys.getsizeof()" }, "Type Inspector — CLI that reports types and sizes of user inputs"),
  mod(3, "strings", "Strings & String Operations", "📝", "Literals, slicing, methods, f-strings, Unicode, and regex.", { basic: "String literals, concatenation, indexing, slicing, len()", intermediate: "split, join, strip, replace, find, f-strings, format()", advanced: "Unicode handling, encode/decode, regex with re, str interning" }, "Text Formatter — normalize and summarize multi-line user text"),
  mod(4, "control-flow", "Control Flow", "🔀", "if/elif/else, comparisons, logical operators, match-case.", { basic: "if/elif/else, comparison operators, and/or/not", intermediate: "Nested conditions, ternary, short-circuit, match-case (3.10+)", advanced: "State machines with match-case, guard clauses, truthy/falsy deep dive" }, "Grade Calculator — classify scores with match-case and validation"),
  mod(5, "loops", "Loops & Iteration", "🔁", "for/while, range(), break/continue, enumerate, zip.", { basic: "for loops, while loops, range(), break, continue, pass", intermediate: "enumerate(), zip(), nested loops, loop-else clause", advanced: "__iter__/__next__, infinite generators, loop performance patterns" }, "Number Guessing Game — loop-driven CLI with attempt tracking"),
  mod(6, "lists-tuples", "Data Structures — Lists & Tuples", "📋", "List mutation, comprehensions, tuples, and unpacking.", { basic: "List creation, indexing, append, remove, pop, slicing", intermediate: "List comprehensions, sorted(), key functions, tuple unpacking", advanced: "Memory layout, amortized append, array module, namedtuple" }, "Todo List CLI — CRUD operations on an in-memory task list"),
  mod(7, "dicts-sets", "Data Structures — Dictionaries & Sets", "🗂️", "Dict/set ops, comprehensions, defaultdict, Counter.", { basic: "Dict creation, get/set/delete, keys/values/items, set operations", intermediate: "Dict/set comprehensions, defaultdict, Counter, OrderedDict", advanced: "Hash collisions, frozenset, dict merge (3.9+), ordering guarantee" }, "Word Frequency Counter — count tokens from stdin or a file"),
  mod(8, "functions", "Functions & Scope", "⚙️", "def, args, *args/**kwargs, scope, closures, functools.", { basic: "def, return, positional/default args, calling functions", intermediate: "*args, **kwargs, keyword-only args, docstrings, type hints, LEGB", advanced: "Closures, nonlocal, functools partial/lru_cache/reduce, annotations" }, "Calculator Library — reusable pure functions with tests"),
  mod(9, "oop", "Object-Oriented Programming", "🏗️", "Classes, inheritance, properties, MRO, ABCs.", { basic: "class, __init__, self, instance vs class attributes, methods", intermediate: "Inheritance, super(), @classmethod, @staticmethod, @property", advanced: "Multiple inheritance, MRO, __slots__, ABC, metaclasses" }, "Bank Account Model — OOP design with validation and history"),
  mod(10, "dunder-methods", "Dunder Methods & Operator Overloading", "✨", "__str__, __repr__, rich comparisons, context managers.", { basic: "__str__, __repr__, __len__, __eq__", intermediate: "__lt__/__gt__, __add__, __getitem__, __contains__, __call__", advanced: "__enter__/__exit__, descriptors, __missing__, __class_getitem__" }, "Vector2D Class — arithmetic dunder methods with repr/str"),
  mod(11, "modules-packages", "Modules, Packages & Imports", "📦", "import styles, packages, __all__, importlib.", { basic: "import, from/import, aliases, standard library overview", intermediate: "Packages (__init__.py), relative imports, __all__, importlib", advanced: "sys.path, custom importers, namespace packages, lazy imports" }, "Mini Package — split code into a reusable installable package"),
  mod(12, "file-io", "File I/O & Serialization", "💾", "open(), with, pathlib, CSV, JSON, pickle.", { basic: "open(), read/write modes, with, readlines(), writelines()", intermediate: "pathlib, os.path, shutil, csv, JSON read/write", advanced: "Binary files, struct, pickle, shelve, mmap" }, "JSON Config Manager — load, validate, and save app settings"),
  mod(13, "exceptions", "Exception Handling & Debugging", "🐛", "try/except/finally, custom exceptions, logging, pdb.", { basic: "try/except/finally, common exceptions, raise", intermediate: "Custom exceptions, chaining, else clause, logging basics", advanced: "Exception groups (3.11+), traceback, pdb, sys.exc_info()" }, "Robust File Parser — graceful errors with structured logging"),
  mod(14, "iterators-generators", "Iterators & Generators", "♾️", "iter/next, yield, generator expressions, itertools.", { basic: "iter(), next(), for loop under the hood", intermediate: "yield, generator functions/expressions, send()", advanced: "yield from, infinite generators, itertools pipelines" }, "Log Pipeline — lazy generator chain filtering large files"),
  mod(15, "decorators", "Decorators", "🎀", "Function decorators, @wraps, stacking, memoization.", { basic: "What decorators are, @functools.wraps, simple decorator pattern", intermediate: "Decorators with arguments, class decorators, stacking", advanced: "Descriptor-based decorators, memoization, rate limiters, retry" }, "Timing Decorator Suite — measure and log function runtime"),
  mod(16, "functional", "Functional Programming", "λ", "map, filter, lambda, reduce, operator module.", { basic: "map(), filter(), lambda, sorted() with key", intermediate: "functools.reduce(), partial(), operator module", advanced: "Immutability, composition, toolz patterns, monadic patterns" }, "Data Pipeline — compose small pure functions over records"),
  mod(17, "comprehensions", "Comprehensions & Expressions", "🧩", "List/dict/set comprehensions, walrus operator.", { basic: "List comprehensions, conditional comprehensions", intermediate: "Dict/set comprehensions, nested comprehensions", advanced: "Generator expressions vs lists, walrus operator (:=), expression trees" }, "Report Builder — nested comprehensions over nested JSON"),
  mod(18, "type-hints", "Type Hints & Static Typing", "🏷️", "Annotations, Optional, Union, Generics, Protocol.", { basic: "Basic annotations, return types, Optional", intermediate: "Union, List[T], Dict[K,V], TypeVar, Generic classes", advanced: "Protocol, TypedDict, Literal, overload, mypy, beartype" }, "Typed API Client — fully annotated HTTP wrapper with validation"),
  mod(19, "testing", "Testing with pytest", "✅", "Test functions, fixtures, parametrize, mocking.", { basic: "assert, test functions, running pytest, discovery", intermediate: "fixtures, parametrize, conftest.py, unittest.mock", advanced: "pytest plugins, coverage.py, Hypothesis, TDD, integration tests" }, "Test Suite — pytest coverage for a small library module"),
  mod(20, "stdlib", "Standard Library Deep Dive", "📚", "os, sys, datetime, collections, itertools, pathlib.", { basic: "os, sys, math, random, datetime, time", intermediate: "collections, itertools, functools, pathlib, re, json, csv", advanced: "dataclasses, enum, contextlib, weakref, gc, inspect, ast, dis" }, "CLI File Stats Tool — pathlib + collections + argparse"),
  mod(21, "concurrency", "Concurrency — Threading & Multiprocessing", "🧵", "GIL, threading, multiprocessing, pools, locks.", { basic: "GIL, threading.Thread, multiprocessing.Process", intermediate: "ThreadPoolExecutor, process pools, Queue, Lock, Event", advanced: "Race conditions, deadlocks, semaphores, shared memory" }, "Parallel Downloader — thread pool fetching URLs safely"),
  mod(22, "async", "Async Programming & asyncio", "⚡", "async/await, asyncio.run, gather, aiohttp.", { basic: "async/await syntax, coroutines, asyncio.run()", intermediate: "asyncio.gather(), create_task(), aiohttp, async generators", advanced: "Event loop internals, asyncio.Queue, TaskGroup (3.11+)" }, "Async URL Fetcher — concurrent HTTP requests with asyncio"),
  mod(23, "performance", "Performance & Optimization", "🚀", "timeit, cProfile, memory profiling, Cython/Numba.", { basic: "timeit, cProfile, Big O in Python context", intermediate: "memory_profiler, __slots__, common bottlenecks", advanced: "Cython, Numba JIT, ctypes/cffi, NumPy vectorization, PyPy" }, "Benchmark Harness — compare implementations with timeit"),
  mod(24, "design-patterns", "Design Patterns in Python", "🧱", "Singleton, Factory, Observer, Strategy, SOLID.", { basic: "Singleton, Factory, Observer patterns", intermediate: "Strategy, Decorator pattern, Command, Builder", advanced: "Pythonic GoF alternatives, SOLID, dataclass patterns, Protocol" }, "Plugin System — Strategy + Factory for swappable handlers"),
  mod(25, "data-scripting", "Python for Data & Scripting", "📊", "CSV/JSON, argparse, pandas, requests, Pydantic.", { basic: "CSV, JSON, XML; argparse for CLI tools", intermediate: "pandas basics, requests/httpx, dotenv", advanced: "SQLAlchemy ORM, Pydantic, Typer/Click, subprocess scripting" }, "ETL Script — ingest CSV, validate with Pydantic, export JSON"),
]);

export const MODULE_LIST = Object.entries(MODULE_META)
  .map(([slug, meta]) => ({ slug, ...meta }))
  .sort((a, b) => a.module_number - b.module_number);

export function getModuleMeta(slug: string): ModuleMeta | undefined {
  return MODULE_META[slug];
}

export const PYTHON_THEME = {
  blue: PYTHON_BLUE,
  yellow: "#FFD43B",
};
