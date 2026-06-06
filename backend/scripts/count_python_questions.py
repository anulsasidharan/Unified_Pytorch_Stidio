"""Count Python question seeds across all modules."""
from __future__ import annotations

import asyncio
import importlib
import pkgutil
import re

import seeds

PATTERN = re.compile(r'"slug":\s*"py-')

STATIC_TOTAL = 0
for modinfo in pkgutil.iter_modules(seeds.__path__):
    if not modinfo.name.startswith("questions_python"):
        continue
    mod = importlib.import_module(f"seeds.{modinfo.name}")
    text = open(mod.__file__, encoding="utf-8").read()
    STATIC_TOTAL += len(PATTERN.findall(text))
    print(f"{modinfo.name} (static slugs): {len(PATTERN.findall(text))}")

BUILDER_MODULES = [
    "seeds.questions_python_modules_06_10",
    "seeds.questions_python_modules_11_15",
    "seeds.questions_python_modules_16_20",
    "seeds.questions_python_modules_21_25",
]

builder_total = 0
for name in BUILDER_MODULES:
    mod = importlib.import_module(name)
    count = 0
    for attr in dir(mod):
        if attr.endswith("_QUESTIONS"):
            val = getattr(mod, attr)
            if isinstance(val, list):
                count += len(val)
    print(f"{name.split('.')[-1]} (built lists): {count}")
    builder_total += count

print(f"STATIC TOTAL: {STATIC_TOTAL}")
print(f"BUILDER TOTAL: {builder_total}")
print(f"GRAND TOTAL: {STATIC_TOTAL + builder_total}")
