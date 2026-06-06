"""
seeds/questions_python_basics.py
---------------------------------
Python Learning Studio — Module 01: Python Basics & Setup
24 exercises: 8 basic, 8 intermediate, 8 advanced

Usage:
    python -m seeds.questions_python_basics
"""

import asyncio

from seeds.loader import seed_questions_for_topic

TOPIC_SLUG = "python-basics"

QUESTIONS = [
    # ── BASIC ────────────────────────────────────────────────────────────────
    {
        "title": "Hello, Python!",
        "slug": "py-hello-python",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Hello, Python!\n\n"
            "Print the text `Hello, Python!` to the console.\n\n"
            "### Requirements\n- Use the built-in `print()` function.\n"
        ),
        "constraints": "Use print() with the exact string Hello, Python!",
        "starter_code": "# Print Hello, Python!\n",
        "expected_output": "Hello, Python!",
        "tags": ["basics", "print"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [
            {
                "title": "Solution",
                "code": "print('Hello, Python!')",
                "explanation": "print() writes to stdout followed by a newline.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Greet the User",
        "slug": "py-greet-user",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Greet the User\n\n"
            "Store your name in a variable `name` and print `Hello, <name>!`.\n\n"
            "**Example output** (if name is `Alice`):\n```\nHello, Alice!\n```\n"
        ),
        "starter_code": "name = 'Alice'\n# print the greeting\n",
        "expected_output": "Hello, Alice!",
        "tags": ["basics", "variables", "print"],
        "xp_reward": 5,
        "time_estimate_mins": 3,
        "solutions": [
            {
                "title": "f-string solution",
                "code": "name = 'Alice'\nprint(f'Hello, {name}!')",
                "explanation": "f-strings let you embed expressions directly in string literals.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Print a Multi-Line Message",
        "slug": "py-multiline-print",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Print a Multi-Line Message\n\n"
            "Print the following two lines using two separate `print()` calls:\n"
            "```\nLine 1\nLine 2\n```\n"
        ),
        "starter_code": "# Print Line 1 and Line 2\n",
        "expected_output": "Line 1\nLine 2",
        "tags": ["basics", "print"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [
            {
                "title": "Solution",
                "code": "print('Line 1')\nprint('Line 2')",
                "explanation": "Each print() call outputs to a new line.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Basic Arithmetic",
        "slug": "py-basic-arithmetic",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Basic Arithmetic\n\n"
            "Calculate `7 + 3` and print the result.\n\n"
            "**Expected output:**\n```\n10\n```\n"
        ),
        "starter_code": "# Calculate 7 + 3\n",
        "expected_output": "10",
        "tags": ["basics", "arithmetic"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [
            {
                "title": "Solution",
                "code": "print(7 + 3)",
                "explanation": "Python evaluates 7 + 3 to 10 and print() converts it to '10'.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Use type()",
        "slug": "py-use-type",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Use type()\n\n"
            "Print the type of the value `42` using `type()`.\n\n"
            "**Expected output:**\n```\n<class 'int'>\n```\n"
        ),
        "starter_code": "# Print the type of 42\n",
        "expected_output": "<class 'int'>",
        "tags": ["basics", "types"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [
            {
                "title": "Solution",
                "code": "print(type(42))",
                "explanation": "type() returns the class of the object.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Single-line Comment",
        "slug": "py-comment",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Single-line Comment\n\n"
            "Add a comment `# Python is fun` above a line that prints `42`.\n\n"
            "**Expected output:**\n```\n42\n```\n"
        ),
        "starter_code": "# Add your comment above this line\nprint(42)\n",
        "expected_output": "42",
        "tags": ["basics", "comments"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [
            {
                "title": "Solution",
                "code": "# Python is fun\nprint(42)",
                "explanation": "Lines starting with # are comments and are ignored at runtime.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Concatenate Strings",
        "slug": "py-concat-strings",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Concatenate Strings\n\n"
            "Join `'Hello'` and `'World'` with a space and print the result.\n\n"
            "**Expected output:**\n```\nHello World\n```\n"
        ),
        "starter_code": "a = 'Hello'\nb = 'World'\n# concatenate and print\n",
        "expected_output": "Hello World",
        "tags": ["basics", "strings"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [
            {
                "title": "Solution",
                "code": "a = 'Hello'\nb = 'World'\nprint(a + ' ' + b)",
                "explanation": "The + operator concatenates strings in Python.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Integer Division and Modulo",
        "slug": "py-int-div-mod",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Integer Division and Modulo\n\n"
            "Print the integer division `17 // 5` and the remainder `17 % 5` on separate lines.\n\n"
            "**Expected output:**\n```\n3\n2\n```\n"
        ),
        "starter_code": "# Print 17 // 5 and 17 % 5\n",
        "expected_output": "3\n2",
        "tags": ["basics", "arithmetic"],
        "xp_reward": 8,
        "time_estimate_mins": 3,
        "solutions": [
            {
                "title": "Solution",
                "code": "print(17 // 5)\nprint(17 % 5)",
                "explanation": "// is floor division, % is the modulo operator.",
                "is_optimal": True,
            }
        ],
    },
    # ── INTERMEDIATE ─────────────────────────────────────────────────────────
    {
        "title": "__name__ Guard",
        "slug": "py-name-guard",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## __name__ Guard\n\n"
            "Write a `greet()` function that prints `Hello from greet!`, then call it inside an "
            "`if __name__ == '__main__':` guard.\n\n"
            "**Expected output:**\n```\nHello from greet!\n```\n"
        ),
        "starter_code": "def greet():\n    # YOUR CODE\n    pass\n\n# call greet inside __name__ guard\n",
        "expected_output": "Hello from greet!",
        "tags": ["basics", "functions", "entrypoint"],
        "xp_reward": 15,
        "time_estimate_mins": 5,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "def greet():\n"
                    "    print('Hello from greet!')\n\n"
                    "if __name__ == '__main__':\n"
                    "    greet()\n"
                ),
                "explanation": (
                    "The __name__ == '__main__' guard ensures code runs only when the script "
                    "is executed directly, not when imported as a module."
                ),
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "f-string Formatting",
        "slug": "py-fstring-format",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## f-string Formatting\n\n"
            "Format a float to 2 decimal places using an f-string.\n\n"
            "Given `pi = 3.14159`, print `Pi is approximately 3.14`.\n\n"
            "**Expected output:**\n```\nPi is approximately 3.14\n```\n"
        ),
        "starter_code": "pi = 3.14159\n# print using f-string with :.2f\n",
        "expected_output": "Pi is approximately 3.14",
        "tags": ["basics", "strings", "f-strings"],
        "xp_reward": 15,
        "time_estimate_mins": 5,
        "solutions": [
            {
                "title": "Solution",
                "code": "pi = 3.14159\nprint(f'Pi is approximately {pi:.2f}')",
                "explanation": ":.2f inside {} formats the float to 2 decimal places.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Swap Two Variables",
        "slug": "py-swap-variables",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Swap Two Variables\n\n"
            "Swap `a = 10` and `b = 20` using Python's tuple unpacking, then print both.\n\n"
            "**Expected output:**\n```\n20\n10\n```\n"
        ),
        "starter_code": "a = 10\nb = 20\n# swap a and b\nprint(a)\nprint(b)\n",
        "expected_output": "20\n10",
        "tags": ["basics", "variables"],
        "xp_reward": 15,
        "time_estimate_mins": 4,
        "solutions": [
            {
                "title": "Solution",
                "code": "a = 10\nb = 20\na, b = b, a\nprint(a)\nprint(b)",
                "explanation": "Python's tuple unpacking allows swapping in a single line.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Multiple Assignment",
        "slug": "py-multiple-assignment",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Multiple Assignment\n\n"
            "Assign `x, y, z = 1, 2, 3` in one line and print their sum.\n\n"
            "**Expected output:**\n```\n6\n```\n"
        ),
        "starter_code": "# Assign x, y, z in one line\n# print their sum\n",
        "expected_output": "6",
        "tags": ["basics", "variables"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [
            {
                "title": "Solution",
                "code": "x, y, z = 1, 2, 3\nprint(x + y + z)",
                "explanation": "Python supports unpacking tuple literals on the right-hand side.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Shebang and Script Mode",
        "slug": "py-shebang",
        "difficulty": "intermediate",
        "question_type": "conceptual_mcq",
        "problem_statement": (
            "## Shebang and Script Mode\n\n"
            "Which shebang line makes a Python 3 script directly executable on Unix?\n\n"
            "A) `#!/usr/bin/python`\n"
            "B) `#!/usr/bin/env python3`\n"
            "C) `# python3`\n"
            "D) `#!/bin/python3`\n\n"
            "Type `B` as your answer.\n\n"
            "**Expected output:**\n```\nB\n```\n"
        ),
        "starter_code": "# Type the correct answer letter\nprint('B')\n",
        "expected_output": "B",
        "tags": ["basics", "scripting"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [
            {
                "title": "Answer",
                "code": "print('B')",
                "explanation": (
                    "#!/usr/bin/env python3 uses the system PATH to locate python3, "
                    "making it portable across different Unix installations."
                ),
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Check Python Version in Code",
        "slug": "py-check-version",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Check Python Version in Code\n\n"
            "Import `sys` and print the Python major version number.\n\n"
            "**Expected output:**\n```\n3\n```\n"
        ),
        "starter_code": "import sys\n# print major version\n",
        "expected_output": "3",
        "tags": ["basics", "sys"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [
            {
                "title": "Solution",
                "code": "import sys\nprint(sys.version_info.major)",
                "explanation": "sys.version_info is a named tuple with major, minor, micro fields.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Print Without Newline",
        "slug": "py-print-no-newline",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Print Without Newline\n\n"
            "Print `Hello` and `World` on the **same line** separated by a space, "
            "using the `end` parameter of `print()`.\n\n"
            "**Expected output:**\n```\nHello World\n```\n"
        ),
        "starter_code": "# print Hello and World on same line\n",
        "expected_output": "Hello World",
        "tags": ["basics", "print"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [
            {
                "title": "Solution",
                "code": "print('Hello', end=' ')\nprint('World')",
                "explanation": "The end='' parameter replaces the default newline character.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Walrus Operator",
        "slug": "py-walrus-operator",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Walrus Operator (Python 3.8+)\n\n"
            "Use the walrus operator `:=` to assign and test in one expression. "
            "If `n := 10` is greater than 5, print `n is n` where n is replaced by its value.\n\n"
            "**Expected output:**\n```\n10 is large\n```\n"
        ),
        "starter_code": "# Use walrus operator\n",
        "expected_output": "10 is large",
        "tags": ["basics", "walrus", "python38"],
        "xp_reward": 20,
        "time_estimate_mins": 5,
        "solutions": [
            {
                "title": "Solution",
                "code": "if (n := 10) > 5:\n    print(f'{n} is large')",
                "explanation": ":= assigns and evaluates in a single expression.",
                "is_optimal": True,
            }
        ],
    },
    # ── ADVANCED ─────────────────────────────────────────────────────────────
    {
        "title": "CPython Bytecode",
        "slug": "py-bytecode-dis",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## CPython Bytecode\n\n"
            "Use the `dis` module to disassemble a simple function and print whether "
            "`LOAD_FAST` appears in the output.\n\n"
            "Define `def add(a, b): return a + b` and check the disassembly.\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "import dis, io\n\ndef add(a, b):\n    return a + b\n\n# Capture dis output and check for LOAD_FAST\n",
        "expected_output": "True",
        "tags": ["advanced", "bytecode", "internals"],
        "xp_reward": 30,
        "time_estimate_mins": 10,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "import dis, io\n\n"
                    "def add(a, b):\n"
                    "    return a + b\n\n"
                    "buf = io.StringIO()\n"
                    "dis.dis(add, file=buf)\n"
                    "print('LOAD_FAST' in buf.getvalue())\n"
                ),
                "explanation": (
                    "dis.dis() emits the CPython bytecode instructions. "
                    "Local variable access uses LOAD_FAST."
                ),
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "sys.getsizeof Comparison",
        "slug": "py-getsizeof",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## sys.getsizeof Comparison\n\n"
            "Print `True` if an empty list `[]` takes fewer bytes than "
            "a list with 100 integers `list(range(100))`.\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "import sys\n# compare sizes\n",
        "expected_output": "True",
        "tags": ["advanced", "memory", "sys"],
        "xp_reward": 30,
        "time_estimate_mins": 5,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "import sys\n"
                    "print(sys.getsizeof([]) < sys.getsizeof(list(range(100))))\n"
                ),
                "explanation": "sys.getsizeof() returns the shallow byte size of an object.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "PyPy vs CPython",
        "slug": "py-pypy-vs-cpython",
        "difficulty": "advanced",
        "question_type": "conceptual_mcq",
        "problem_statement": (
            "## PyPy vs CPython\n\n"
            "Which statement best describes PyPy's main advantage?\n\n"
            "A) Better standard library compatibility\n"
            "B) Faster execution via JIT compilation\n"
            "C) Smaller memory footprint always\n"
            "D) Native async support\n\n"
            "Print the letter of the correct answer.\n\n"
            "**Expected output:**\n```\nB\n```\n"
        ),
        "starter_code": "print('B')\n",
        "expected_output": "B",
        "tags": ["advanced", "interpreters", "pypy"],
        "xp_reward": 25,
        "time_estimate_mins": 3,
        "solutions": [
            {
                "title": "Answer",
                "code": "print('B')",
                "explanation": (
                    "PyPy uses a tracing JIT compiler that compiles hot code paths to machine "
                    "code at runtime, often giving 5-10× speedups over CPython for pure Python."
                ),
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Frozen Modules and .pyc Files",
        "slug": "py-pyc-files",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## Frozen Modules and .pyc Files\n\n"
            "Use `importlib.util` to check whether the `os` module has a cached "
            "bytecode file and print `True`.\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "import importlib.util\n# check for cached bytecode of 'os'\n",
        "expected_output": "True",
        "tags": ["advanced", "bytecode", "importlib"],
        "xp_reward": 30,
        "time_estimate_mins": 8,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "import importlib.util\n"
                    "spec = importlib.util.find_spec('os')\n"
                    "print(spec is not None)\n"
                ),
                "explanation": (
                    "find_spec() locates the module spec. If it exists, CPython will use "
                    "a .pyc cached bytecode file in __pycache__ on subsequent imports."
                ),
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Object Identity vs Equality",
        "slug": "py-identity-equality",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## Object Identity vs Equality\n\n"
            "Demonstrate that two lists with equal contents are NOT the same object.\n"
            "Create `a = [1, 2, 3]` and `b = [1, 2, 3]`.\n"
            "Print `True` then `False` on separate lines.\n\n"
            "**Expected output:**\n```\nTrue\nFalse\n```\n"
        ),
        "starter_code": "a = [1, 2, 3]\nb = [1, 2, 3]\n# print equality then identity\n",
        "expected_output": "True\nFalse",
        "tags": ["advanced", "identity", "memory"],
        "xp_reward": 25,
        "time_estimate_mins": 5,
        "solutions": [
            {
                "title": "Solution",
                "code": "a = [1, 2, 3]\nb = [1, 2, 3]\nprint(a == b)\nprint(a is b)",
                "explanation": (
                    "== checks value equality; 'is' checks object identity (same memory address). "
                    "Two separately created lists always have different ids."
                ),
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "String Interning",
        "slug": "py-string-interning",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## String Interning\n\n"
            "CPython interns short strings that look like identifiers. "
            "Show that `'hello' is 'hello'` evaluates to `True`.\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "# demonstrate string interning\n",
        "expected_output": "True",
        "tags": ["advanced", "internals", "strings"],
        "xp_reward": 25,
        "time_estimate_mins": 4,
        "solutions": [
            {
                "title": "Solution",
                "code": "print('hello' is 'hello')",
                "explanation": (
                    "CPython automatically interns string literals that look like identifiers "
                    "(no spaces, alphanumeric + underscore). Both 'hello' references point to "
                    "the same interned object."
                ),
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Compile and Exec Bytecode",
        "slug": "py-compile-exec",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": (
            "## Compile and Exec Bytecode\n\n"
            "Use `compile()` and `exec()` to dynamically execute the string "
            "`\"print('dynamic')\"` and capture the output.\n\n"
            "**Expected output:**\n```\ndynamic\n```\n"
        ),
        "starter_code": "source = \"print('dynamic')\"\n# compile and exec\n",
        "expected_output": "dynamic",
        "tags": ["advanced", "bytecode", "metaprogramming"],
        "xp_reward": 35,
        "time_estimate_mins": 8,
        "solutions": [
            {
                "title": "Solution",
                "code": "source = \"print('dynamic')\"\ncode = compile(source, '<string>', 'exec')\nexec(code)",
                "explanation": (
                    "compile() turns source into a code object; exec() runs it. "
                    "This mirrors how CPython processes source files internally."
                ),
                "is_optimal": True,
            }
        ],
    },
]


async def main() -> None:
    n = await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 01 — Python Basics")
    print(f"Seeded {n} questions for {TOPIC_SLUG}")


if __name__ == "__main__":
    asyncio.run(main())
