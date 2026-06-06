"""
seeds/questions_python_strings.py
-----------------------------------
Python Learning Studio — Module 03: Strings & String Operations
18 exercises: 6 basic, 6 intermediate, 6 advanced

Usage:
    python -m seeds.questions_python_strings
"""

import asyncio

from seeds.loader import seed_questions_for_topic

TOPIC_SLUG = "strings"

QUESTIONS = [
    # ── BASIC ────────────────────────────────────────────────────────────────
    {
        "title": "String Length",
        "slug": "py-str-len",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## String Length\n\nPrint the length of `'Python'`.\n\n**Expected output:**\n```\n6\n```\n",
        "starter_code": "# print length of 'Python'\n",
        "expected_output": "6",
        "tags": ["strings", "len"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "print(len('Python'))", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "String Indexing",
        "slug": "py-str-index",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## String Indexing\n\nPrint the first and last characters of `'Python'`.\n\n**Expected output:**\n```\nP\nn\n```\n",
        "starter_code": "s = 'Python'\n# print first and last chars\n",
        "expected_output": "P\nn",
        "tags": ["strings", "indexing"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "s = 'Python'\nprint(s[0])\nprint(s[-1])", "explanation": "s[0] is the first char; s[-1] is the last.", "is_optimal": True}],
    },
    {
        "title": "String Slicing",
        "slug": "py-str-slice",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## String Slicing\n\nExtract and print `'ython'` from `'Python'`.\n\n**Expected output:**\n```\nython\n```\n",
        "starter_code": "s = 'Python'\n# slice to get 'ython'\n",
        "expected_output": "ython",
        "tags": ["strings", "slicing"],
        "xp_reward": 8,
        "solutions": [{"title": "Solution", "code": "s = 'Python'\nprint(s[1:])", "explanation": "s[1:] slices from index 1 to end.", "is_optimal": True}],
    },
    {
        "title": "String Upper and Lower",
        "slug": "py-str-upper-lower",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## String Upper and Lower\n\nPrint `'hello'` in uppercase and `'WORLD'` in lowercase.\n\n**Expected output:**\n```\nHELLO\nworld\n```\n",
        "starter_code": "print('hello'.upper())\nprint('WORLD'.lower())\n",
        "expected_output": "HELLO\nworld",
        "tags": ["strings", "methods"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "print('hello'.upper())\nprint('WORLD'.lower())", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "String Replace",
        "slug": "py-str-replace",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## String Replace\n\nReplace `'World'` with `'Python'` in `'Hello, World!'`.\n\n**Expected output:**\n```\nHello, Python!\n```\n",
        "starter_code": "s = 'Hello, World!'\n# replace World with Python\n",
        "expected_output": "Hello, Python!",
        "tags": ["strings", "replace"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "s = 'Hello, World!'\nprint(s.replace('World', 'Python'))", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "String Split and Join",
        "slug": "py-str-split-join",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## String Split and Join\n\nSplit `'a,b,c'` on commas and rejoin with ` - `.\n\n**Expected output:**\n```\na - b - c\n```\n",
        "starter_code": "s = 'a,b,c'\n# split then join with ' - '\n",
        "expected_output": "a - b - c",
        "tags": ["strings", "split", "join"],
        "xp_reward": 8,
        "solutions": [{"title": "Solution", "code": "s = 'a,b,c'\nprint(' - '.join(s.split(',')))", "explanation": "split() returns a list; join() concatenates it with the separator.", "is_optimal": True}],
    },
    # ── INTERMEDIATE ─────────────────────────────────────────────────────────
    {
        "title": "f-string with Expression",
        "slug": "py-str-fstring-expr",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## f-string with Expression\n\nPrint `'2 + 3 = 5'` using an f-string that computes the sum inline.\n\n**Expected output:**\n```\n2 + 3 = 5\n```\n",
        "starter_code": "# use f-string with inline expression\n",
        "expected_output": "2 + 3 = 5",
        "tags": ["strings", "f-strings"],
        "xp_reward": 15,
        "solutions": [{"title": "Solution", "code": "print(f'2 + 3 = {2 + 3}')", "explanation": "f-strings evaluate expressions inside {}.", "is_optimal": True}],
    },
    {
        "title": "Strip Whitespace",
        "slug": "py-str-strip",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Strip Whitespace\n\nStrip leading/trailing spaces from `'  hello  '` and print.\n\n**Expected output:**\n```\nhello\n```\n",
        "starter_code": "s = '  hello  '\n# strip and print\n",
        "expected_output": "hello",
        "tags": ["strings", "strip"],
        "xp_reward": 10,
        "solutions": [{"title": "Solution", "code": "s = '  hello  '\nprint(s.strip())", "explanation": "strip() removes leading and trailing whitespace.", "is_optimal": True}],
    },
    {
        "title": "String find()",
        "slug": "py-str-find",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## String find()\n\nFind the index of `'thon'` in `'Python'`.\n\n**Expected output:**\n```\n2\n```\n",
        "starter_code": "s = 'Python'\n# find index of 'thon'\n",
        "expected_output": "2",
        "tags": ["strings", "find"],
        "xp_reward": 10,
        "solutions": [{"title": "Solution", "code": "s = 'Python'\nprint(s.find('thon'))", "explanation": "find() returns the lowest index or -1 if not found.", "is_optimal": True}],
    },
    {
        "title": "String startswith and endswith",
        "slug": "py-str-starts-ends",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## startswith and endswith\n\nPrint `True True` if `'Python'` starts with `'Py'` and ends with `'on'`.\n\n**Expected output:**\n```\nTrue\nTrue\n```\n",
        "starter_code": "s = 'Python'\n# print startswith and endswith results\n",
        "expected_output": "True\nTrue",
        "tags": ["strings", "methods"],
        "xp_reward": 10,
        "solutions": [{"title": "Solution", "code": "s = 'Python'\nprint(s.startswith('Py'))\nprint(s.endswith('on'))", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Reverse a String",
        "slug": "py-str-reverse",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Reverse a String\n\nReverse `'Python'` using slicing and print.\n\n**Expected output:**\n```\nnohtyP\n```\n",
        "starter_code": "s = 'Python'\n# reverse using slicing\n",
        "expected_output": "nohtyP",
        "tags": ["strings", "slicing"],
        "xp_reward": 15,
        "solutions": [{"title": "Solution", "code": "s = 'Python'\nprint(s[::-1])", "explanation": "s[::-1] creates a reversed copy using a step of -1.", "is_optimal": True}],
    },
    {
        "title": "Count Occurrences",
        "slug": "py-str-count",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Count Occurrences\n\nCount how many times `'a'` appears in `'banana'` and print.\n\n**Expected output:**\n```\n3\n```\n",
        "starter_code": "s = 'banana'\n# count 'a'\n",
        "expected_output": "3",
        "tags": ["strings", "count"],
        "xp_reward": 10,
        "solutions": [{"title": "Solution", "code": "s = 'banana'\nprint(s.count('a'))", "explanation": "", "is_optimal": True}],
    },
    # ── ADVANCED ─────────────────────────────────────────────────────────────
    {
        "title": "Regex Email Validation",
        "slug": "py-str-regex-email",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Regex Email Validation\n\nUse `re.match` to print `True` if `'test@example.com'` is a valid email pattern.\n\n**Expected output:**\n```\nTrue\n```\n",
        "starter_code": "import re\nemail = 'test@example.com'\n# validate with re.match\n",
        "expected_output": "True",
        "tags": ["advanced", "regex", "strings"],
        "xp_reward": 30,
        "solutions": [
            {
                "title": "Solution",
                "code": "import re\nemail = 'test@example.com'\nprint(bool(re.match(r'^[\\w.+-]+@[\\w-]+\\.[\\w.]+$', email)))",
                "explanation": "re.match() checks from the start of the string; bool() converts the match object.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Unicode Encode and Decode",
        "slug": "py-str-unicode",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Unicode Encode/Decode\n\nEncode `'café'` to UTF-8 bytes, then decode back and print.\n\n**Expected output:**\n```\ncafé\n```\n",
        "starter_code": "s = 'café'\n# encode to UTF-8 then decode\n",
        "expected_output": "café",
        "tags": ["advanced", "unicode", "encoding"],
        "xp_reward": 25,
        "solutions": [{"title": "Solution", "code": "s = 'café'\nprint(s.encode('utf-8').decode('utf-8'))", "explanation": "encode() produces bytes; decode() converts back to str.", "is_optimal": True}],
    },
    {
        "title": "String Interning with sys.intern",
        "slug": "py-str-intern-sys",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## String Interning with sys.intern\n\nUse `sys.intern` to ensure two different string objects share the same identity and print `True`.\n\n**Expected output:**\n```\nTrue\n```\n",
        "starter_code": "import sys\na = sys.intern('hello world')\nb = sys.intern('hello world')\n# check identity\n",
        "expected_output": "True",
        "tags": ["advanced", "internals", "memory"],
        "xp_reward": 30,
        "solutions": [{"title": "Solution", "code": "import sys\na = sys.intern('hello world')\nb = sys.intern('hello world')\nprint(a is b)", "explanation": "sys.intern() forces string interning, making 'is' return True.", "is_optimal": True}],
    },
    {
        "title": "Named Groups in Regex",
        "slug": "py-str-regex-groups",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Named Groups in Regex\n\nExtract the year from `'Date: 2026-06-06'` using a named group `year`.\n\n**Expected output:**\n```\n2026\n```\n",
        "starter_code": "import re\ntext = 'Date: 2026-06-06'\n# extract year with named group\n",
        "expected_output": "2026",
        "tags": ["advanced", "regex"],
        "xp_reward": 30,
        "solutions": [{"title": "Solution", "code": "import re\ntext = 'Date: 2026-06-06'\nm = re.search(r'(?P<year>\\d{4})', text)\nprint(m.group('year'))", "explanation": "(?P<name>...) creates a named capture group accessible via .group('name').", "is_optimal": True}],
    },
    {
        "title": "Multiline String and textwrap",
        "slug": "py-str-textwrap",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## textwrap.dedent\n\nUse `textwrap.dedent` to strip common leading whitespace from a multi-line string and print the first word.\n\n**Expected output:**\n```\nHello\n```\n",
        "starter_code": "import textwrap\ntext = '''\n    Hello\n    World\n'''\n# dedent and print first non-empty line stripped\n",
        "expected_output": "Hello",
        "tags": ["advanced", "strings", "textwrap"],
        "xp_reward": 25,
        "solutions": [{"title": "Solution", "code": "import textwrap\ntext = '''\n    Hello\n    World\n'''\nlines = textwrap.dedent(text).strip().splitlines()\nprint(lines[0])", "explanation": "dedent() removes common leading whitespace; strip().splitlines() gives clean lines.", "is_optimal": True}],
    },
    {
        "title": "Format String vs f-string Performance",
        "slug": "py-str-format-perf",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## str.format() vs f-string\n\nProduce `'Hello, Alice! You are 30.'` using **both** `str.format()` and an f-string.\nPrint the result of the f-string version.\n\n**Expected output:**\n```\nHello, Alice! You are 30.\n```\n",
        "starter_code": "name = 'Alice'\nage = 30\n# use both methods; print f-string result\n",
        "expected_output": "Hello, Alice! You are 30.",
        "tags": ["advanced", "strings", "formatting"],
        "xp_reward": 25,
        "solutions": [
            {
                "title": "Solution",
                "code": "name = 'Alice'\nage = 30\n_ = 'Hello, {}! You are {}.'.format(name, age)\nresult = f'Hello, {name}! You are {age}.'\nprint(result)",
                "explanation": "f-strings are faster and more readable than .format() for Python 3.6+.",
                "is_optimal": True,
            }
        ],
    },
]


async def main() -> None:
    n = await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 03 — Strings")
    print(f"Seeded {n} questions for {TOPIC_SLUG}")


if __name__ == "__main__":
    asyncio.run(main())
