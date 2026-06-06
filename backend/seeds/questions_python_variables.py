"""
seeds/questions_python_variables.py
-------------------------------------
Python Learning Studio — Module 02: Variables, Data Types & Operators
18 exercises: 6 basic, 6 intermediate, 6 advanced

Usage:
    python -m seeds.questions_python_variables
"""

import asyncio

from seeds.loader import seed_questions_for_topic

TOPIC_SLUG = "variables-types"

QUESTIONS = [
    # ── BASIC ────────────────────────────────────────────────────────────────
    {
        "title": "Identify Integer Type",
        "slug": "py-var-int-type",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Identify Integer Type\n\n"
            "Print the type of `42`.\n\n"
            "**Expected output:**\n```\n<class 'int'>\n```\n"
        ),
        "starter_code": "# print type of 42\n",
        "expected_output": "<class 'int'>",
        "tags": ["variables", "types"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [{"title": "Solution", "code": "print(type(42))", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Boolean Values",
        "slug": "py-var-bool",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Boolean Values\n\n"
            "Print `True` and `False` on separate lines.\n\n"
            "**Expected output:**\n```\nTrue\nFalse\n```\n"
        ),
        "starter_code": "# print True and False\n",
        "expected_output": "True\nFalse",
        "tags": ["variables", "bool"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [{"title": "Solution", "code": "print(True)\nprint(False)", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "None Type",
        "slug": "py-var-none",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## None Type\n\n"
            "Print the type of `None`.\n\n"
            "**Expected output:**\n```\n<class 'NoneType'>\n```\n"
        ),
        "starter_code": "# print type of None\n",
        "expected_output": "<class 'NoneType'>",
        "tags": ["variables", "none"],
        "xp_reward": 5,
        "time_estimate_mins": 2,
        "solutions": [{"title": "Solution", "code": "print(type(None))", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Float Precision",
        "slug": "py-var-float",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Float Precision\n\n"
            "Print `0.1 + 0.2 == 0.3`.\n\n"
            "**Expected output:**\n```\nFalse\n```\n"
        ),
        "starter_code": "# print comparison\n",
        "expected_output": "False",
        "tags": ["variables", "float", "precision"],
        "xp_reward": 8,
        "time_estimate_mins": 2,
        "solutions": [{"title": "Solution", "code": "print(0.1 + 0.2 == 0.3)", "explanation": "Floating-point representation introduces rounding error.", "is_optimal": True}],
    },
    {
        "title": "String to Integer",
        "slug": "py-var-str-to-int",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## String to Integer\n\n"
            "Convert the string `'42'` to an integer and print the result plus 8.\n\n"
            "**Expected output:**\n```\n50\n```\n"
        ),
        "starter_code": "s = '42'\n# convert and add 8\n",
        "expected_output": "50",
        "tags": ["variables", "conversion"],
        "xp_reward": 8,
        "time_estimate_mins": 3,
        "solutions": [{"title": "Solution", "code": "s = '42'\nprint(int(s) + 8)", "explanation": "int() converts a string to an integer.", "is_optimal": True}],
    },
    {
        "title": "Division Always Returns Float",
        "slug": "py-var-division-float",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": (
            "## Division Always Returns Float\n\n"
            "Print the type of `10 / 2`.\n\n"
            "**Expected output:**\n```\n<class 'float'>\n```\n"
        ),
        "starter_code": "# print type of 10 / 2\n",
        "expected_output": "<class 'float'>",
        "tags": ["variables", "division", "types"],
        "xp_reward": 8,
        "time_estimate_mins": 2,
        "solutions": [{"title": "Solution", "code": "print(type(10 / 2))", "explanation": "In Python 3, / always produces a float.", "is_optimal": True}],
    },
    # ── INTERMEDIATE ─────────────────────────────────────────────────────────
    {
        "title": "Implicit Type Coercion",
        "slug": "py-var-coercion",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Implicit Type Coercion\n\n"
            "Print `True + 1` — Python coerces `True` to `1` automatically.\n\n"
            "**Expected output:**\n```\n2\n```\n"
        ),
        "starter_code": "# print True + 1\n",
        "expected_output": "2",
        "tags": ["variables", "coercion", "bool"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [{"title": "Solution", "code": "print(True + 1)", "explanation": "bool is a subclass of int in Python; True == 1.", "is_optimal": True}],
    },
    {
        "title": "id() — Object Identity",
        "slug": "py-var-id",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## id() — Object Identity\n\n"
            "Show that `a = 256` and `b = 256` point to the same object "
            "(CPython caches small integers).\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "a = 256\nb = 256\n# compare with is\n",
        "expected_output": "True",
        "tags": ["variables", "identity", "internals"],
        "xp_reward": 20,
        "time_estimate_mins": 5,
        "solutions": [{"title": "Solution", "code": "a = 256\nb = 256\nprint(a is b)", "explanation": "CPython caches integers from -5 to 256, so 'is' returns True for this range.", "is_optimal": True}],
    },
    {
        "title": "Augmented Assignment",
        "slug": "py-var-augmented",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Augmented Assignment\n\n"
            "Start with `x = 10`, double it with `*=`, then print.\n\n"
            "**Expected output:**\n```\n20\n```\n"
        ),
        "starter_code": "x = 10\n# double x with *=\nprint(x)\n",
        "expected_output": "20",
        "tags": ["variables", "operators"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [{"title": "Solution", "code": "x = 10\nx *= 2\nprint(x)", "explanation": "x *= 2 is shorthand for x = x * 2.", "is_optimal": True}],
    },
    {
        "title": "Truthiness of Empty Containers",
        "slug": "py-var-truthiness",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Truthiness of Empty Containers\n\n"
            "Print `True` if `[]` is falsy, `False` otherwise.\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "# print whether [] is falsy\n",
        "expected_output": "True",
        "tags": ["variables", "truthiness", "bool"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [{"title": "Solution", "code": "print(not [])", "explanation": "Empty containers are falsy in Python; not [] is True.", "is_optimal": True}],
    },
    {
        "title": "Explicit Conversion Chain",
        "slug": "py-var-convert-chain",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Explicit Conversion Chain\n\n"
            "Convert `3.7` to int (truncation), then to string, then print.\n\n"
            "**Expected output:**\n```\n3\n```\n"
        ),
        "starter_code": "x = 3.7\n# convert to int then string, print\n",
        "expected_output": "3",
        "tags": ["variables", "conversion"],
        "xp_reward": 15,
        "time_estimate_mins": 3,
        "solutions": [{"title": "Solution", "code": "x = 3.7\nprint(str(int(x)))", "explanation": "int(3.7) truncates to 3; str(3) gives '3'.", "is_optimal": True}],
    },
    {
        "title": "Walrus in While",
        "slug": "py-var-walrus-while",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": (
            "## Walrus in While Loop\n\n"
            "Use the walrus operator `:=` to sum values popped from a list "
            "`data = [1, 2, 3]` until it is empty, then print the total.\n\n"
            "**Expected output:**\n```\n6\n```\n"
        ),
        "starter_code": "data = [1, 2, 3]\ntotal = 0\n# use walrus to pop and sum\nprint(total)\n",
        "expected_output": "6",
        "tags": ["variables", "walrus", "loops"],
        "xp_reward": 20,
        "time_estimate_mins": 8,
        "solutions": [
            {
                "title": "Solution",
                "code": "data = [1, 2, 3]\ntotal = 0\nwhile (v := data.pop(0) if data else None) is not None:\n    total += v\nprint(total)",
                "explanation": "The walrus operator assigns and tests the popped value in one step.",
                "is_optimal": True,
            }
        ],
    },
    # ── ADVANCED ─────────────────────────────────────────────────────────────
    {
        "title": "Mutable Default Argument Trap",
        "slug": "py-var-mutable-default",
        "difficulty": "advanced",
        "question_type": "debug_model",
        "problem_statement": (
            "## Mutable Default Argument Trap\n\n"
            "The function below appends to a list and has a bug — "
            "the list persists across calls.\n\n"
            "```python\n"
            "def append_item(item, lst=[]):\n"
            "    lst.append(item)\n"
            "    return lst\n\n"
            "print(append_item(1))\n"
            "print(append_item(2))\n"
            "```\n\n"
            "Fix it so each call gets a fresh list when `lst` is not provided.\n\n"
            "**Expected output:**\n```\n[1]\n[2]\n```\n"
        ),
        "starter_code": (
            "def append_item(item, lst=[]):\n"
            "    lst.append(item)\n"
            "    return lst\n\n"
            "print(append_item(1))\n"
            "print(append_item(2))\n"
        ),
        "expected_output": "[1]\n[2]",
        "tags": ["advanced", "functions", "mutable"],
        "xp_reward": 30,
        "time_estimate_mins": 8,
        "solutions": [
            {
                "title": "Solution",
                "code": (
                    "def append_item(item, lst=None):\n"
                    "    if lst is None:\n"
                    "        lst = []\n"
                    "    lst.append(item)\n"
                    "    return lst\n\n"
                    "print(append_item(1))\n"
                    "print(append_item(2))\n"
                ),
                "explanation": "Default mutable arguments are shared across calls. Use None as the sentinel instead.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Memory Footprint with sys.getsizeof",
        "slug": "py-var-memory-footprint",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## Memory Footprint\n\n"
            "Print `True` if an integer takes fewer bytes than a float.\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "import sys\n# compare int vs float sizes\n",
        "expected_output": "True",
        "tags": ["advanced", "memory", "types"],
        "xp_reward": 25,
        "time_estimate_mins": 5,
        "solutions": [
            {
                "title": "Solution",
                "code": "import sys\nprint(sys.getsizeof(1) <= sys.getsizeof(1.0))",
                "explanation": "In CPython, int (28 bytes) and float (24 bytes) — floats can be smaller or equal.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Integer Overflow — Python Has None",
        "slug": "py-var-bigint",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## Python Has No Integer Overflow\n\n"
            "Print `2 ** 100`. Python integers have arbitrary precision.\n\n"
            "**Expected output:**\n```\n1267650600228229401496703205376\n```\n"
        ),
        "starter_code": "# print 2 ** 100\n",
        "expected_output": "1267650600228229401496703205376",
        "tags": ["advanced", "integers", "precision"],
        "xp_reward": 25,
        "time_estimate_mins": 3,
        "solutions": [{"title": "Solution", "code": "print(2 ** 100)", "explanation": "Python integers support arbitrary precision — no overflow like C/Java.", "is_optimal": True}],
    },
    {
        "title": "Decimal Module for Exact Arithmetic",
        "slug": "py-var-decimal",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## Decimal Module for Exact Arithmetic\n\n"
            "Use the `decimal.Decimal` class to show that `0.1 + 0.2 == 0.3` is `True`.\n\n"
            "**Expected output:**\n```\nTrue\n```\n"
        ),
        "starter_code": "from decimal import Decimal\n# use Decimal to show 0.1 + 0.2 == 0.3\n",
        "expected_output": "True",
        "tags": ["advanced", "decimal", "precision"],
        "xp_reward": 30,
        "time_estimate_mins": 5,
        "solutions": [
            {
                "title": "Solution",
                "code": "from decimal import Decimal\nprint(Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))",
                "explanation": "Decimal uses exact decimal arithmetic, avoiding floating-point rounding.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Type Narrowing with isinstance",
        "slug": "py-var-isinstance",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": (
            "## Type Narrowing with isinstance\n\n"
            "Given a list `items = [1, 'two', 3.0, True, None]`, "
            "count and print how many are strictly `int` (not bool).\n\n"
            "**Expected output:**\n```\n1\n```\n"
        ),
        "starter_code": "items = [1, 'two', 3.0, True, None]\n# count strict ints (not bool)\n",
        "expected_output": "1",
        "tags": ["advanced", "types", "isinstance"],
        "xp_reward": 30,
        "time_estimate_mins": 8,
        "solutions": [
            {
                "title": "Solution",
                "code": "items = [1, 'two', 3.0, True, None]\nprint(sum(isinstance(x, int) and not isinstance(x, bool) for x in items))",
                "explanation": "isinstance(True, int) is True because bool subclasses int, so we must exclude bools explicitly.",
                "is_optimal": True,
            }
        ],
    },
]


async def main() -> None:
    n = await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 02 — Variables & Types")
    print(f"Seeded {n} questions for {TOPIC_SLUG}")


if __name__ == "__main__":
    asyncio.run(main())
