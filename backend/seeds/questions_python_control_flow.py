"""
seeds/questions_python_control_flow.py
-----------------------------------------
Python Learning Studio — Module 04: Control Flow
18 exercises: 6 basic, 6 intermediate, 6 advanced

Usage:
    python -m seeds.questions_python_control_flow
"""

import asyncio

from seeds.loader import seed_questions_for_topic

TOPIC_SLUG = "control-flow"

QUESTIONS = [
    # ── BASIC ────────────────────────────────────────────────────────────────
    {
        "title": "Even or Odd",
        "slug": "py-cf-even-odd",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Even or Odd\n\nPrint `'even'` if `n = 4` is even, otherwise print `'odd'`.\n\n**Expected output:**\n```\neven\n```\n",
        "starter_code": "n = 4\n# check even or odd\n",
        "expected_output": "even",
        "tags": ["control-flow", "if"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "n = 4\nif n % 2 == 0:\n    print('even')\nelse:\n    print('odd')", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Classify a Number",
        "slug": "py-cf-classify-number",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Classify a Number\n\nFor `n = 0`, print `'zero'`, if positive print `'positive'`, if negative print `'negative'`.\n\n**Expected output:**\n```\nzero\n```\n",
        "starter_code": "n = 0\n# classify as positive, negative, or zero\n",
        "expected_output": "zero",
        "tags": ["control-flow", "if-elif-else"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "n = 0\nif n > 0:\n    print('positive')\nelif n < 0:\n    print('negative')\nelse:\n    print('zero')", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Comparison Operators",
        "slug": "py-cf-comparisons",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Comparison Operators\n\nPrint `True` if `10 > 5 and 3 < 7`.\n\n**Expected output:**\n```\nTrue\n```\n",
        "starter_code": "# print the comparison\n",
        "expected_output": "True",
        "tags": ["control-flow", "comparisons"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "print(10 > 5 and 3 < 7)", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Logical not",
        "slug": "py-cf-logical-not",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Logical not\n\nPrint `not False`.\n\n**Expected output:**\n```\nTrue\n```\n",
        "starter_code": "# print not False\n",
        "expected_output": "True",
        "tags": ["control-flow", "logical"],
        "xp_reward": 5,
        "solutions": [{"title": "Solution", "code": "print(not False)", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Grade Letter",
        "slug": "py-cf-grade",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Grade Letter\n\nFor `score = 85`, print `'B'` (80-89 = B, 90-100 = A, <80 = C).\n\n**Expected output:**\n```\nB\n```\n",
        "starter_code": "score = 85\n# print grade letter\n",
        "expected_output": "B",
        "tags": ["control-flow", "elif"],
        "xp_reward": 8,
        "solutions": [{"title": "Solution", "code": "score = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelse:\n    print('C')", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Short-Circuit Evaluation",
        "slug": "py-cf-short-circuit",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": "## Short-Circuit Evaluation\n\nPrint the result of `False and 1/0`. Python should NOT raise a ZeroDivisionError.\n\n**Expected output:**\n```\nFalse\n```\n",
        "starter_code": "# print False and 1/0\n",
        "expected_output": "False",
        "tags": ["control-flow", "short-circuit"],
        "xp_reward": 8,
        "solutions": [{"title": "Solution", "code": "print(False and 1/0)", "explanation": "With 'and', if the left operand is False, the right is never evaluated.", "is_optimal": True}],
    },
    # ── INTERMEDIATE ─────────────────────────────────────────────────────────
    {
        "title": "Ternary Expression",
        "slug": "py-cf-ternary",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Ternary Expression\n\nPrint `'adult'` if `age = 20 >= 18` else `'minor'` — use a one-line ternary.\n\n**Expected output:**\n```\nadult\n```\n",
        "starter_code": "age = 20\n# one-line ternary\n",
        "expected_output": "adult",
        "tags": ["control-flow", "ternary"],
        "xp_reward": 15,
        "solutions": [{"title": "Solution", "code": "age = 20\nprint('adult' if age >= 18 else 'minor')", "explanation": "'value_if_true if condition else value_if_false' is Python's ternary.", "is_optimal": True}],
    },
    {
        "title": "Chained Comparisons",
        "slug": "py-cf-chained",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Chained Comparisons\n\nPrint `True` if `1 < 5 < 10`.\n\n**Expected output:**\n```\nTrue\n```\n",
        "starter_code": "# print chained comparison\n",
        "expected_output": "True",
        "tags": ["control-flow", "comparisons"],
        "xp_reward": 10,
        "solutions": [{"title": "Solution", "code": "print(1 < 5 < 10)", "explanation": "Python supports chained comparisons: 1 < 5 < 10 means 1 < 5 and 5 < 10.", "is_optimal": True}],
    },
    {
        "title": "match-case — Day of Week",
        "slug": "py-cf-match-day",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## match-case (Python 3.10+)\n\nUse `match` to print `'Weekend'` for `day = 'Saturday'`, `'Weekday'` otherwise.\n\n**Expected output:**\n```\nWeekend\n```\n",
        "starter_code": "day = 'Saturday'\n# use match-case\n",
        "expected_output": "Weekend",
        "tags": ["control-flow", "match-case"],
        "xp_reward": 20,
        "solutions": [
            {
                "title": "Solution",
                "code": "day = 'Saturday'\nmatch day:\n    case 'Saturday' | 'Sunday':\n        print('Weekend')\n    case _:\n        print('Weekday')",
                "explanation": "match-case supports the | operator for multiple patterns.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Nested Conditions — FizzBuzz",
        "slug": "py-cf-fizzbuzz",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## FizzBuzz\n\nFor `n = 15`, print `'FizzBuzz'` (divisible by 3 and 5), `'Fizz'` (by 3), `'Buzz'` (by 5).\n\n**Expected output:**\n```\nFizzBuzz\n```\n",
        "starter_code": "n = 15\n# FizzBuzz logic\n",
        "expected_output": "FizzBuzz",
        "tags": ["control-flow", "fizzbuzz"],
        "xp_reward": 15,
        "solutions": [{"title": "Solution", "code": "n = 15\nif n % 15 == 0:\n    print('FizzBuzz')\nelif n % 3 == 0:\n    print('Fizz')\nelif n % 5 == 0:\n    print('Buzz')\nelse:\n    print(n)", "explanation": "", "is_optimal": True}],
    },
    {
        "title": "Guard Clause Pattern",
        "slug": "py-cf-guard-clause",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## Guard Clause Pattern\n\nWrite `process(x)` that returns `'invalid'` for `x <= 0` early, else returns `x * 2`. Print `process(-1)` and `process(5)`.\n\n**Expected output:**\n```\ninvalid\n10\n```\n",
        "starter_code": "def process(x):\n    # guard clause\n    pass\n\nprint(process(-1))\nprint(process(5))\n",
        "expected_output": "invalid\n10",
        "tags": ["control-flow", "guard-clause"],
        "xp_reward": 20,
        "solutions": [{"title": "Solution", "code": "def process(x):\n    if x <= 0:\n        return 'invalid'\n    return x * 2\n\nprint(process(-1))\nprint(process(5))", "explanation": "Guard clauses return early for invalid inputs, flattening nested ifs.", "is_optimal": True}],
    },
    {
        "title": "or Default Value",
        "slug": "py-cf-or-default",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": "## or Default Value\n\nUse `or` to provide a default: `name = '' or 'Guest'`. Print name.\n\n**Expected output:**\n```\nGuest\n```\n",
        "starter_code": "name = ''\n# use 'or' to default to Guest\n",
        "expected_output": "Guest",
        "tags": ["control-flow", "logical", "default"],
        "xp_reward": 15,
        "solutions": [{"title": "Solution", "code": "name = ''\nname = name or 'Guest'\nprint(name)", "explanation": "Empty string is falsy, so 'or' returns the right operand.", "is_optimal": True}],
    },
    # ── ADVANCED ─────────────────────────────────────────────────────────────
    {
        "title": "match-case with Guard",
        "slug": "py-cf-match-guard",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## match-case with Guard Clause\n\nMatch `point = (3, 4)`: if both positive print `'Q1'`, else print `'other'`.\n\n**Expected output:**\n```\nQ1\n```\n",
        "starter_code": "point = (3, 4)\n# match with guard\n",
        "expected_output": "Q1",
        "tags": ["advanced", "match-case", "guard"],
        "xp_reward": 30,
        "solutions": [
            {
                "title": "Solution",
                "code": "point = (3, 4)\nmatch point:\n    case (x, y) if x > 0 and y > 0:\n        print('Q1')\n    case _:\n        print('other')",
                "explanation": "Guards in match-case use 'if' after the pattern to add conditions.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "State Machine with match-case",
        "slug": "py-cf-state-machine",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": "## Simple State Machine\n\nImplement a traffic light that cycles: `green → yellow → red → green`.\nGiven `state = 'green'`, print the **next** state.\n\n**Expected output:**\n```\nyellow\n```\n",
        "starter_code": "state = 'green'\n# implement next_state() using match-case\n",
        "expected_output": "yellow",
        "tags": ["advanced", "match-case", "state-machine"],
        "xp_reward": 35,
        "solutions": [
            {
                "title": "Solution",
                "code": "state = 'green'\nmatch state:\n    case 'green':\n        print('yellow')\n    case 'yellow':\n        print('red')\n    case 'red':\n        print('green')",
                "explanation": "match-case cleanly encodes state transitions without if-elif chains.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Truthy Deep Dive — Custom Class",
        "slug": "py-cf-truthy-dunder",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Truthiness via __bool__\n\nCreate a class `Empty` whose `__bool__` returns `False`. Print `bool(Empty())`.\n\n**Expected output:**\n```\nFalse\n```\n",
        "starter_code": "class Empty:\n    pass  # implement __bool__\n\nprint(bool(Empty()))\n",
        "expected_output": "False",
        "tags": ["advanced", "dunder", "truthiness"],
        "xp_reward": 30,
        "solutions": [{"title": "Solution", "code": "class Empty:\n    def __bool__(self):\n        return False\n\nprint(bool(Empty()))", "explanation": "__bool__ controls what bool() returns for custom objects.", "is_optimal": True}],
    },
    {
        "title": "De Morgan's Law Verification",
        "slug": "py-cf-demorgan",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## De Morgan's Law\n\nVerify that `not (a and b) == (not a or not b)` for `a=True, b=False`.\n\n**Expected output:**\n```\nTrue\n```\n",
        "starter_code": "a, b = True, False\n# verify De Morgan's law\n",
        "expected_output": "True",
        "tags": ["advanced", "boolean-algebra"],
        "xp_reward": 25,
        "solutions": [{"title": "Solution", "code": "a, b = True, False\nprint(not (a and b) == (not a or not b))", "explanation": "De Morgan's law: not(A and B) == (not A) or (not B).", "is_optimal": True}],
    },
    {
        "title": "Conditional Import",
        "slug": "py-cf-conditional-import",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Conditional Import\n\nTry to import `ujson`; if unavailable fall back to `json`. Print `'json'` if json was used.\n\n**Expected output:**\n```\njson\n```\n",
        "starter_code": "# conditional import\n",
        "expected_output": "json",
        "tags": ["advanced", "imports", "control-flow"],
        "xp_reward": 25,
        "solutions": [
            {
                "title": "Solution",
                "code": "try:\n    import ujson as _json\n    lib = 'ujson'\nexcept ImportError:\n    import json as _json\n    lib = 'json'\nprint(lib)",
                "explanation": "try/except ImportError is the Pythonic way to handle optional dependencies.",
                "is_optimal": True,
            }
        ],
    },
    {
        "title": "Exception in Boolean Context",
        "slug": "py-cf-exception-bool",
        "difficulty": "advanced",
        "question_type": "code_completion",
        "problem_statement": "## Exception Short-Circuits in and\n\nPrint the result: `True and (1 > 0) and not False`.\n\n**Expected output:**\n```\nTrue\n```\n",
        "starter_code": "# print the chained boolean\n",
        "expected_output": "True",
        "tags": ["advanced", "boolean", "short-circuit"],
        "xp_reward": 20,
        "solutions": [{"title": "Solution", "code": "print(True and (1 > 0) and not False)", "explanation": "All conditions are True, so the result is True.", "is_optimal": True}],
    },
]


async def main() -> None:
    n = await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 04 — Control Flow")
    print(f"Seeded {n} questions for {TOPIC_SLUG}")


if __name__ == "__main__":
    asyncio.run(main())
