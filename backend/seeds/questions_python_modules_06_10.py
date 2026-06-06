"""
seeds/questions_python_modules_06_10.py
---------------------------------------
Python Learning Studio — Modules 06-10

- lists-tuples: 30 exercises (12 basic, 10 intermediate, 8 advanced)
- dicts-sets: 30 exercises (10 basic, 10 intermediate, 10 advanced)
- functions: 34 exercises (12 basic, 12 intermediate, 10 advanced)
- oop: 32 exercises (10 basic, 12 intermediate, 10 advanced)
- dunder-methods: 26 exercises (8 basic, 10 intermediate, 8 advanced)

Usage:
    python -m seeds.questions_python_modules_06_10
"""

import asyncio

from seeds.loader import seed_questions_for_topic
from seeds.python_exercise import build_python_exercise


def _problem(title: str, instruction: str, expected_output: str) -> str:
    return (
        f"## {title}\n\n"
        f"{instruction}\n\n"
        "**Expected output:**\n"
        f"```\n{expected_output}\n```\n"
    )


def _exercise(
    *,
    title: str,
    slug: str,
    difficulty: str,
    instruction: str,
    starter_code: str,
    expected_output: str,
    tags: list[str],
    solution_code: str,
    explanation: str = "",
) -> dict:
    return build_python_exercise(
        title=title,
        slug=slug,
        difficulty=difficulty,
        problem_statement=_problem(title, instruction, expected_output),
        starter_code=starter_code,
        expected_output=expected_output,
        tags=tags,
        solution_code=solution_code,
        solution_explanation=explanation,
    )


def build_lists_tuples_questions() -> list[dict]:
    questions: list[dict] = []

    basic_specs = [
        ("List Length", "py-lt-basic-len", "nums = [3, 5, 7, 9]\n# print list length\n", "4", "nums = [3, 5, 7, 9]\nprint(len(nums))", ["lists", "len"]),
        ("List First and Last", "py-lt-basic-first-last", "letters = ['a', 'b', 'c', 'd']\n# print first then last item\n", "a\nd", "letters = ['a', 'b', 'c', 'd']\nprint(letters[0])\nprint(letters[-1])", ["lists", "indexing"]),
        ("Append to List", "py-lt-basic-append", "colors = ['red', 'blue']\n# append 'green' and print the list\n", "['red', 'blue', 'green']", "colors = ['red', 'blue']\ncolors.append('green')\nprint(colors)", ["lists", "append"]),
        ("Pop Last Item", "py-lt-basic-pop", "values = [10, 20, 30]\n# remove last item and print removed value\n", "30", "values = [10, 20, 30]\nprint(values.pop())", ["lists", "pop"]),
        ("Tuple Length", "py-lt-basic-tuple-len", "point = (4, 8)\n# print tuple length\n", "2", "point = (4, 8)\nprint(len(point))", ["tuples", "len"]),
        ("Tuple Unpacking", "py-lt-basic-unpack", "coords = (2, 5)\n# unpack to x and y, print x + y\n", "7", "coords = (2, 5)\nx, y = coords\nprint(x + y)", ["tuples", "unpacking"]),
        ("List Membership", "py-lt-basic-membership", "items = ['pen', 'book', 'lamp']\n# print whether 'book' is in items\n", "True", "items = ['pen', 'book', 'lamp']\nprint('book' in items)", ["lists", "membership"]),
        ("Count in List", "py-lt-basic-count", "nums = [1, 2, 2, 3, 2]\n# count how many times 2 appears\n", "3", "nums = [1, 2, 2, 3, 2]\nprint(nums.count(2))", ["lists", "count"]),
        ("Slice Middle", "py-lt-basic-slice", "data = [0, 1, 2, 3, 4]\n# print [1, 2, 3] using slicing\n", "[1, 2, 3]", "data = [0, 1, 2, 3, 4]\nprint(data[1:4])", ["lists", "slicing"]),
        ("Join from Tuple", "py-lt-basic-join-tuple", "words = ('learn', 'python')\n# print them joined by a space\n", "learn python", "words = ('learn', 'python')\nprint(' '.join(words))", ["tuples", "strings"]),
        ("Reverse with Slicing", "py-lt-basic-reverse", "nums = [1, 2, 3, 4]\n# print reversed list using slicing\n", "[4, 3, 2, 1]", "nums = [1, 2, 3, 4]\nprint(nums[::-1])", ["lists", "slicing"]),
        ("Tuple Single Item", "py-lt-basic-single-tuple", "single = (42,)\n# print type(single)\n", "<class 'tuple'>", "single = (42,)\nprint(type(single))", ["tuples", "types"]),
    ]

    for title, slug, starter, expected, solution, tags in basic_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="basic",
                instruction=starter.split("\n#")[1].replace("\n", "").strip().capitalize() if "\n#" in starter else "Complete the exercise.",
                starter_code=starter,
                expected_output=expected,
                tags=["lists-tuples"] + tags,
                solution_code=solution,
            )
        )

    intermediate_specs = [
        ("Enumerate Start Index", "py-lt-int-enumerate", "names = ['Ana', 'Ben']\n# print index and value starting from 1\n", "1 Ana\n2 Ben", "names = ['Ana', 'Ben']\nfor idx, name in enumerate(names, start=1):\n    print(idx, name)", ["lists", "enumerate"]),
        ("Zip Two Lists", "py-lt-int-zip", "keys = ['a', 'b', 'c']\nvals = [1, 2, 3]\n# zip and print as list of tuples\n", "[('a', 1), ('b', 2), ('c', 3)]", "keys = ['a', 'b', 'c']\nvals = [1, 2, 3]\nprint(list(zip(keys, vals)))", ["lists", "zip"]),
        ("Flatten One Level", "py-lt-int-flatten", "nested = [[1, 2], [3], [4, 5]]\n# flatten one level and print\n", "[1, 2, 3, 4, 5]", "nested = [[1, 2], [3], [4, 5]]\nflat = [n for group in nested for n in group]\nprint(flat)", ["lists", "comprehension"]),
        ("Deduplicate Keep Order", "py-lt-int-dedupe-order", "items = ['a', 'b', 'a', 'c', 'b']\n# remove duplicates but preserve order\n", "['a', 'b', 'c']", "items = ['a', 'b', 'a', 'c', 'b']\nseen = set()\nresult = []\nfor item in items:\n    if item not in seen:\n        seen.add(item)\n        result.append(item)\nprint(result)", ["lists", "set"]),
        ("Transpose 2x2 Matrix", "py-lt-int-transpose", "m = [[1, 2], [3, 4]]\n# print transposed matrix\n", "[[1, 3], [2, 4]]", "m = [[1, 2], [3, 4]]\nprint([list(row) for row in zip(*m)])", ["lists", "matrix"]),
        ("List Stack Behavior", "py-lt-int-stack", "stack = []\n# push 1 then 2, pop once, print stack\n", "[1]", "stack = []\nstack.append(1)\nstack.append(2)\nstack.pop()\nprint(stack)", ["lists", "stack"]),
        ("Tuple Sorting by Second", "py-lt-int-sort-second", "pairs = [(1, 3), (2, 1), (3, 2)]\n# sort by second value and print\n", "[(2, 1), (3, 2), (1, 3)]", "pairs = [(1, 3), (2, 1), (3, 2)]\nprint(sorted(pairs, key=lambda x: x[1]))", ["tuples", "sorting"]),
        ("Chunk List Size Two", "py-lt-int-chunk", "nums = [1, 2, 3, 4, 5]\n# chunk into size 2 lists and print\n", "[[1, 2], [3, 4], [5]]", "nums = [1, 2, 3, 4, 5]\nchunks = [nums[i:i + 2] for i in range(0, len(nums), 2)]\nprint(chunks)", ["lists", "slicing"]),
        ("Nested Index Access", "py-lt-int-nested-index", "grid = [[10, 11], [20, 21], [30, 31]]\n# print 21\n", "21", "grid = [[10, 11], [20, 21], [30, 31]]\nprint(grid[1][1])", ["lists", "nested"]),
        ("Pairwise Sum with Zip", "py-lt-int-pairwise-sum", "a = [1, 2, 3]\nb = [4, 5, 6]\n# print pairwise sums as list\n", "[5, 7, 9]", "a = [1, 2, 3]\nb = [4, 5, 6]\nprint([x + y for x, y in zip(a, b)])", ["lists", "zip", "comprehension"]),
    ]

    for title, slug, starter, expected, solution, tags in intermediate_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="intermediate",
                instruction="Complete the task described in the starter code comment.",
                starter_code=starter,
                expected_output=expected,
                tags=["lists-tuples"] + tags,
                solution_code=solution,
            )
        )

    advanced_specs = [
        ("Rotate List Right", "py-lt-adv-rotate-right", "nums = [1, 2, 3, 4, 5]\n# rotate right by 2 and print\n", "[4, 5, 1, 2, 3]", "nums = [1, 2, 3, 4, 5]\nk = 2\nprint(nums[-k:] + nums[:-k])", ["lists", "rotation"]),
        ("Sliding Window Sums", "py-lt-adv-sliding-window", "nums = [2, 4, 6, 8]\n# window size 2, print window sums list\n", "[6, 10, 14]", "nums = [2, 4, 6, 8]\nprint([nums[i] + nums[i + 1] for i in range(len(nums) - 1)])", ["lists", "windows"]),
        ("Deep Copy Nested List", "py-lt-adv-deepcopy", "import copy\nitems = [[1], [2]]\n# deep copy, mutate copy first inner list, print original\n", "[[1], [2]]", "import copy\nitems = [[1], [2]]\nclone = copy.deepcopy(items)\nclone[0].append(9)\nprint(items)", ["lists", "copy"]),
        ("Tuple as Dict Key", "py-lt-adv-tuple-key", "cache = {(1, 2): 3, (2, 3): 5}\n# print value for key (2, 3)\n", "5", "cache = {(1, 2): 3, (2, 3): 5}\nprint(cache[(2, 3)])", ["tuples", "hashing"]),
        ("Immutable Tuple Update", "py-lt-adv-immutable-update", "t = (10, 20, 30)\n# create a new tuple where middle value is 99\n", "(10, 99, 30)", "t = (10, 20, 30)\nupdated = t[:1] + (99,) + t[2:]\nprint(updated)", ["tuples", "immutability"]),
        ("Diagonal Sum Matrix", "py-lt-adv-diagonal-sum", "m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n# print main diagonal sum\n", "15", "m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nprint(sum(m[i][i] for i in range(len(m))))", ["lists", "matrix"]),
        ("Stable Sort by Length", "py-lt-adv-stable-sort", "words = ['pear', 'fig', 'apple', 'kiwi']\n# sort by length then print\n", "['fig', 'pear', 'kiwi', 'apple']", "words = ['pear', 'fig', 'apple', 'kiwi']\nprint(sorted(words, key=len))", ["lists", "sorting"]),
        ("Unzip List of Tuples", "py-lt-adv-unzip", "pairs = [('x', 1), ('y', 2), ('z', 3)]\n# unzip into two tuples and print second tuple\n", "(1, 2, 3)", "pairs = [('x', 1), ('y', 2), ('z', 3)]\n_, values = zip(*pairs)\nprint(values)", ["tuples", "zip"]),
    ]

    for title, slug, starter, expected, solution, tags in advanced_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="advanced",
                instruction="Complete the task described in the starter code comment.",
                starter_code=starter,
                expected_output=expected,
                tags=["lists-tuples"] + tags,
                solution_code=solution,
            )
        )

    return questions


def build_dicts_sets_questions() -> list[dict]:
    questions: list[dict] = []

    basic_specs = [
        ("Dictionary Lookup", "py-ds-basic-lookup", "student = {'name': 'Asha', 'score': 92}\n# print the score\n", "92", "student = {'name': 'Asha', 'score': 92}\nprint(student['score'])", ["dicts", "lookup"]),
        ("Dictionary Add Key", "py-ds-basic-add-key", "profile = {'user': 'neo'}\n# add key 'active' with value True, print profile\n", "{'user': 'neo', 'active': True}", "profile = {'user': 'neo'}\nprofile['active'] = True\nprint(profile)", ["dicts", "mutation"]),
        ("Set from List", "py-ds-basic-set-from-list", "nums = [1, 1, 2, 3, 3]\n# print unique values as a sorted list\n", "[1, 2, 3]", "nums = [1, 1, 2, 3, 3]\nprint(sorted(set(nums)))", ["sets", "dedupe"]),
        ("Set Membership", "py-ds-basic-membership", "letters = {'a', 'b', 'c'}\n# print whether 'b' exists in the set\n", "True", "letters = {'a', 'b', 'c'}\nprint('b' in letters)", ["sets", "membership"]),
        ("Dictionary Keys Count", "py-ds-basic-keys-count", "data = {'x': 1, 'y': 2, 'z': 3}\n# print number of keys\n", "3", "data = {'x': 1, 'y': 2, 'z': 3}\nprint(len(data))", ["dicts", "keys"]),
        ("Get with Default", "py-ds-basic-get-default", "config = {'mode': 'dev'}\n# print config.get('port', 8000)\n", "8000", "config = {'mode': 'dev'}\nprint(config.get('port', 8000))", ["dicts", "get"]),
        ("Set Add and Remove", "py-ds-basic-add-remove", "vals = {1, 2}\n# add 3, remove 1, print sorted list of set values\n", "[2, 3]", "vals = {1, 2}\nvals.add(3)\nvals.remove(1)\nprint(sorted(vals))", ["sets", "mutation"]),
        ("Dictionary Items Loop", "py-ds-basic-items-loop", "prices = {'tea': 2, 'cake': 4}\n# print each key:value sorted by key\n", "cake:4\ntea:2", "prices = {'tea': 2, 'cake': 4}\nfor key in sorted(prices):\n    print(f'{key}:{prices[key]}')", ["dicts", "iteration"]),
        ("Set Length", "py-ds-basic-len", "s = {'python', 'java', 'go'}\n# print set length\n", "3", "s = {'python', 'java', 'go'}\nprint(len(s))", ["sets", "len"]),
        ("Dictionary Pop", "py-ds-basic-pop", "record = {'id': 1, 'name': 'Lia'}\n# pop 'name' and print popped value\n", "Lia", "record = {'id': 1, 'name': 'Lia'}\nprint(record.pop('name'))", ["dicts", "pop"]),
    ]

    for title, slug, starter, expected, solution, tags in basic_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="basic",
                instruction="Complete the dictionary/set exercise from the starter code.",
                starter_code=starter,
                expected_output=expected,
                tags=["dicts-sets"] + tags,
                solution_code=solution,
            )
        )

    intermediate_specs = [
        ("Merge Dictionaries", "py-ds-int-merge", "a = {'x': 1, 'y': 2}\nb = {'y': 9, 'z': 3}\n# merge with b overriding a, print result\n", "{'x': 1, 'y': 9, 'z': 3}", "a = {'x': 1, 'y': 2}\nb = {'y': 9, 'z': 3}\nprint(a | b)", ["dicts", "merge"]),
        ("Dictionary Comprehension", "py-ds-int-comprehension", "nums = [1, 2, 3, 4]\n# build dict mapping n -> n*n, print it\n", "{1: 1, 2: 4, 3: 9, 4: 16}", "nums = [1, 2, 3, 4]\nprint({n: n * n for n in nums})", ["dicts", "comprehension"]),
        ("Set Intersection", "py-ds-int-intersection", "a = {1, 2, 3, 4}\nb = {3, 4, 5}\n# print sorted intersection list\n", "[3, 4]", "a = {1, 2, 3, 4}\nb = {3, 4, 5}\nprint(sorted(a & b))", ["sets", "intersection"]),
        ("Set Difference", "py-ds-int-difference", "a = {'a', 'b', 'c'}\nb = {'b'}\n# print sorted elements in a not in b\n", "['a', 'c']", "a = {'a', 'b', 'c'}\nb = {'b'}\nprint(sorted(a - b))", ["sets", "difference"]),
        ("Count Frequencies", "py-ds-int-frequency", "text = 'banana'\n# build frequency dict and print count for 'a'\n", "3", "text = 'banana'\nfreq = {}\nfor ch in text:\n    freq[ch] = freq.get(ch, 0) + 1\nprint(freq['a'])", ["dicts", "frequency"]),
        ("Invert Simple Dictionary", "py-ds-int-invert", "d = {'a': 1, 'b': 2}\n# invert keys and values, print result\n", "{1: 'a', 2: 'b'}", "d = {'a': 1, 'b': 2}\nprint({v: k for k, v in d.items()})", ["dicts", "comprehension"]),
        ("Sort by Dict Value", "py-ds-int-sort-value", "scores = {'Ana': 88, 'Bob': 91, 'Cia': 85}\n# print names sorted by score descending as list\n", "['Bob', 'Ana', 'Cia']", "scores = {'Ana': 88, 'Bob': 91, 'Cia': 85}\nprint(sorted(scores, key=scores.get, reverse=True))", ["dicts", "sorting"]),
        ("Symmetric Difference", "py-ds-int-symmetric-diff", "a = {1, 2, 3}\nb = {3, 4}\n# print sorted symmetric difference list\n", "[1, 2, 4]", "a = {1, 2, 3}\nb = {3, 4}\nprint(sorted(a ^ b))", ["sets", "set-algebra"]),
        ("Update Nested Dict", "py-ds-int-nested-update", "user = {'name': 'Rey', 'meta': {'xp': 10}}\n# increase xp by 5 and print xp\n", "15", "user = {'name': 'Rey', 'meta': {'xp': 10}}\nuser['meta']['xp'] += 5\nprint(user['meta']['xp'])", ["dicts", "nested"]),
        ("Set Comprehension", "py-ds-int-set-comp", "nums = [1, 2, 2, 3, 3, 4]\n# build set of even numbers and print sorted list\n", "[2, 4]", "nums = [1, 2, 2, 3, 3, 4]\nprint(sorted({n for n in nums if n % 2 == 0}))", ["sets", "comprehension"]),
    ]

    for title, slug, starter, expected, solution, tags in intermediate_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="intermediate",
                instruction="Complete the dictionary/set exercise from the starter code.",
                starter_code=starter,
                expected_output=expected,
                tags=["dicts-sets"] + tags,
                solution_code=solution,
            )
        )

    advanced_specs = [
        ("Group Words by First Letter", "py-ds-adv-group-first-letter", "words = ['apple', 'ant', 'banana', 'boat']\n# group by first letter and print group for 'a'\n", "['apple', 'ant']", "words = ['apple', 'ant', 'banana', 'boat']\ngroups = {}\nfor w in words:\n    groups.setdefault(w[0], []).append(w)\nprint(groups['a'])", ["dicts", "grouping"]),
        ("Dictionary of Lists Totals", "py-ds-adv-dict-list-total", "sales = {'north': [3, 4], 'south': [5, 1]}\n# print total of all numbers\n", "13", "sales = {'north': [3, 4], 'south': [5, 1]}\nprint(sum(sum(vals) for vals in sales.values()))", ["dicts", "aggregation"]),
        ("Frozen Set in Set", "py-ds-adv-frozenset", "a = {frozenset({1, 2}), frozenset({3})}\n# print whether frozenset({1,2}) exists\n", "True", "a = {frozenset({1, 2}), frozenset({3})}\nprint(frozenset({1, 2}) in a)", ["sets", "frozenset"]),
        ("Conflict-Free Merge Counts", "py-ds-adv-merge-counts", "a = {'x': 2, 'y': 1}\nb = {'x': 5, 'z': 3}\n# merge by summing overlapping values\n", "{'x': 7, 'y': 1, 'z': 3}", "a = {'x': 2, 'y': 1}\nb = {'x': 5, 'z': 3}\nout = dict(a)\nfor k, v in b.items():\n    out[k] = out.get(k, 0) + v\nprint(out)", ["dicts", "merge"]),
        ("Detect Duplicate Rows", "py-ds-adv-duplicate-rows", "rows = [(1, 2), (2, 3), (1, 2), (3, 4)]\n# print True if duplicates exist\n", "True", "rows = [(1, 2), (2, 3), (1, 2), (3, 4)]\nprint(len(rows) != len(set(rows)))", ["sets", "duplicates"]),
        ("Top Two Frequencies", "py-ds-adv-top-two", "nums = [1, 2, 2, 3, 3, 3, 4]\n# print top two (num, count) sorted by count desc\n", "[(3, 3), (2, 2)]", "nums = [1, 2, 2, 3, 3, 3, 4]\nfreq = {}\nfor n in nums:\n    freq[n] = freq.get(n, 0) + 1\nprint(sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:2])", ["dicts", "frequency"]),
        ("Set Subset Check", "py-ds-adv-subset", "required = {'read', 'write'}\nuser = {'read', 'write', 'delete'}\n# print whether required is subset of user\n", "True", "required = {'read', 'write'}\nuser = {'read', 'write', 'delete'}\nprint(required.issubset(user))", ["sets", "subset"]),
        ("Normalize Nested Keys", "py-ds-adv-normalize-keys", "data = {'Name': 'Ari', 'Age': 21}\n# build new dict with lowercase keys\n", "{'name': 'Ari', 'age': 21}", "data = {'Name': 'Ari', 'Age': 21}\nprint({k.lower(): v for k, v in data.items()})", ["dicts", "normalization"]),
        ("Unique Word Set from Sentence", "py-ds-adv-unique-words", "text = 'to be or not to be'\n# print sorted unique words list\n", "['be', 'not', 'or', 'to']", "text = 'to be or not to be'\nprint(sorted(set(text.split())))", ["sets", "text"]),
        ("Adjacency Dict Build", "py-ds-adv-adjacency", "edges = [('A', 'B'), ('A', 'C'), ('B', 'C')]\n# build adjacency dict and print neighbors of A\n", "['B', 'C']", "edges = [('A', 'B'), ('A', 'C'), ('B', 'C')]\nadj = {}\nfor u, v in edges:\n    adj.setdefault(u, []).append(v)\nprint(adj['A'])", ["dicts", "graph"]),
    ]

    for title, slug, starter, expected, solution, tags in advanced_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="advanced",
                instruction="Complete the dictionary/set exercise from the starter code.",
                starter_code=starter,
                expected_output=expected,
                tags=["dicts-sets"] + tags,
                solution_code=solution,
            )
        )

    return questions


def build_functions_questions() -> list[dict]:
    questions: list[dict] = []

    basic_specs = [
        ("Define and Call Function", "py-fn-basic-define-call", "Define `greet()` that prints `Hello` and call it once.", "def greet():\n    # print Hello\n\n# call greet()\n", "Hello", "def greet():\n    print('Hello')\n\ngreet()", ["functions", "basics"]),
        ("Function with One Argument", "py-fn-basic-one-arg", "Define `double(n)` and print result of `double(6)`.", "def double(n):\n    # return doubled value\n\nprint(double(6))\n", "12", "def double(n):\n    return n * 2\n\nprint(double(6))", ["functions", "parameters"]),
        ("Function Returning Sum", "py-fn-basic-sum", "Create `add(a, b)` and print `add(3, 4)`.", "def add(a, b):\n    # return sum\n\nprint(add(3, 4))\n", "7", "def add(a, b):\n    return a + b\n\nprint(add(3, 4))", ["functions", "return"]),
        ("Default Argument", "py-fn-basic-default", "Define `power(base, exp=2)` and print `power(5)`.", "def power(base, exp=2):\n    # return base**exp\n\nprint(power(5))\n", "25", "def power(base, exp=2):\n    return base ** exp\n\nprint(power(5))", ["functions", "defaults"]),
        ("Keyword Arguments", "py-fn-basic-keyword", "Define `area(w, h)` and print `area(h=3, w=4)`.", "def area(w, h):\n    # return area\n\nprint(area(h=3, w=4))\n", "12", "def area(w, h):\n    return w * h\n\nprint(area(h=3, w=4))", ["functions", "kwargs"]),
        ("Local Variable Scope", "py-fn-basic-scope", "Inside function create x=10 and print x; then call function.", "def show():\n    # create local x and print it\n\nshow()\n", "10", "def show():\n    x = 10\n    print(x)\n\nshow()", ["functions", "scope"]),
        ("Return Boolean", "py-fn-basic-bool", "Write `is_even(n)` and print `is_even(8)`.", "def is_even(n):\n    # return True for even numbers\n\nprint(is_even(8))\n", "True", "def is_even(n):\n    return n % 2 == 0\n\nprint(is_even(8))", ["functions", "booleans"]),
        ("Docstring Access", "py-fn-basic-docstring", "Add docstring `Return greeting` to `hello()` and print `hello.__doc__`.", "def hello():\n    \"\"\"Return greeting\"\"\"\n    # return text\n\nprint(hello.__doc__)\n", "Return greeting", "def hello():\n    \"\"\"Return greeting\"\"\"\n    return 'hi'\n\nprint(hello.__doc__)", ["functions", "docstring"]),
        ("Function with List Input", "py-fn-basic-list-input", "Define `first_item(values)` and print first item from `[9, 8, 7]`.", "def first_item(values):\n    # return first element\n\nprint(first_item([9, 8, 7]))\n", "9", "def first_item(values):\n    return values[0]\n\nprint(first_item([9, 8, 7]))", ["functions", "lists"]),
        ("Simple Recursion Base Case", "py-fn-basic-recursion", "Write recursive `countdown(n)` that prints n down to 1. Call with 3.", "def countdown(n):\n    # recursive print\n\ncountdown(3)\n", "3\n2\n1", "def countdown(n):\n    if n == 0:\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)", ["functions", "recursion"]),
        ("Variable Number Arguments", "py-fn-basic-args", "Define `total(*nums)` and print `total(1, 2, 3)`.", "def total(*nums):\n    # return sum\n\nprint(total(1, 2, 3))\n", "6", "def total(*nums):\n    return sum(nums)\n\nprint(total(1, 2, 3))", ["functions", "args"]),
        ("Lambda for Sorting Key", "py-fn-basic-lambda", "Sort `['aaa', 'b', 'cc']` by length and print.", "words = ['aaa', 'b', 'cc']\n# sort by length\n", "['b', 'cc', 'aaa']", "words = ['aaa', 'b', 'cc']\nprint(sorted(words, key=lambda w: len(w)))", ["functions", "lambda"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in basic_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="basic",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["functions"] + tags,
                solution_code=solution,
            )
        )

    intermediate_specs = [
        ("Mutable Default Fix", "py-fn-int-mutable-default", "Fix function so two calls do not share the same list.", "def add_item(x, bucket=[]):\n    bucket.append(x)\n    return bucket\n\nprint(add_item(1))\nprint(add_item(2))\n", "[1]\n[2]", "def add_item(x, bucket=None):\n    if bucket is None:\n        bucket = []\n    bucket.append(x)\n    return bucket\n\nprint(add_item(1))\nprint(add_item(2))", ["functions", "defaults", "debugging"]),
        ("Closure Counter", "py-fn-int-closure-counter", "Create closure `make_counter()` and print two increments.", "def make_counter():\n    # return inner function\n    pass\n\nc = make_counter()\nprint(c())\nprint(c())\n", "1\n2", "def make_counter():\n    count = 0\n    def inc():\n        nonlocal count\n        count += 1\n        return count\n    return inc\n\nc = make_counter()\nprint(c())\nprint(c())", ["functions", "closures"]),
        ("Map and Lambda", "py-fn-int-map-lambda", "Use map with lambda to square [1,2,3], print as list.", "nums = [1, 2, 3]\n# map square and print list\n", "[1, 4, 9]", "nums = [1, 2, 3]\nprint(list(map(lambda n: n * n, nums)))", ["functions", "lambda", "map"]),
        ("Filter Function", "py-fn-int-filter", "Use filter to keep odd values from [1,2,3,4,5].", "nums = [1, 2, 3, 4, 5]\n# keep odd numbers and print list\n", "[1, 3, 5]", "nums = [1, 2, 3, 4, 5]\nprint(list(filter(lambda n: n % 2 == 1, nums)))", ["functions", "filter"]),
        ("Higher-Order Function", "py-fn-int-hof", "Write `apply_twice(fn, x)` and print result for double and 3.", "def double(n):\n    return n * 2\n\ndef apply_twice(fn, x):\n    # apply fn twice\n\nprint(apply_twice(double, 3))\n", "12", "def double(n):\n    return n * 2\n\ndef apply_twice(fn, x):\n    return fn(fn(x))\n\nprint(apply_twice(double, 3))", ["functions", "higher-order"]),
        ("Keyword-Only Arguments", "py-fn-int-kw-only", "Define `greet(*, name)` and print `greet(name='Mia')`.", "def greet(*, name):\n    # return greeting\n\nprint(greet(name='Mia'))\n", "Hi Mia", "def greet(*, name):\n    return f'Hi {name}'\n\nprint(greet(name='Mia'))", ["functions", "kwargs"]),
        ("Positional-Only Arguments", "py-fn-int-pos-only", "Define `ratio(a, b, /)` and print `ratio(8, 2)`.", "def ratio(a, b, /):\n    # return a/b\n\nprint(ratio(8, 2))\n", "4.0", "def ratio(a, b, /):\n    return a / b\n\nprint(ratio(8, 2))", ["functions", "parameters"]),
        ("Decorator Basics", "py-fn-int-decorator", "Add decorator that prints 'start' before wrapped function output.", "def log_start(fn):\n    # return wrapper\n    pass\n\n@log_start\ndef greet():\n    print('hello')\n\ngreet()\n", "start\nhello", "def log_start(fn):\n    def wrapper():\n        print('start')\n        fn()\n    return wrapper\n\n@log_start\ndef greet():\n    print('hello')\n\ngreet()", ["functions", "decorators"]),
        ("Function Annotations", "py-fn-int-annotations", "Annotate `to_int(text: str) -> int` and print `to_int('7')`.", "def to_int(text: str) -> int:\n    # convert and return\n\nprint(to_int('7'))\n", "7", "def to_int(text: str) -> int:\n    return int(text)\n\nprint(to_int('7'))", ["functions", "annotations"]),
        ("Recursive Factorial", "py-fn-int-factorial", "Write recursive factorial and print factorial(5).", "def factorial(n):\n    # recursion\n\nprint(factorial(5))\n", "120", "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))", ["functions", "recursion"]),
        ("Generator Function", "py-fn-int-generator", "Create generator `first_three()` yielding 1,2,3 and print list of it.", "def first_three():\n    # yield numbers\n\nprint(list(first_three()))\n", "[1, 2, 3]", "def first_three():\n    yield 1\n    yield 2\n    yield 3\n\nprint(list(first_three()))", ["functions", "generators"]),
        ("Function as Dictionary Value", "py-fn-int-fn-dispatch", "Use dict dispatch to call add function on (2,3), then print.", "def add(a, b):\n    return a + b\n\nops = {'add': add}\n# print result of add\n", "5", "def add(a, b):\n    return a + b\n\nops = {'add': add}\nprint(ops['add'](2, 3))", ["functions", "dispatch"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in intermediate_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="intermediate",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["functions"] + tags,
                solution_code=solution,
            )
        )

    advanced_specs = [
        ("Memoized Fibonacci", "py-fn-adv-memo-fib", "Use `functools.lru_cache` on fib and print fib(10).", "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    # implement recursive fib\n\nprint(fib(10))\n", "55", "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n\nprint(fib(10))", ["functions", "memoization"]),
        ("Timing Decorator", "py-fn-adv-timing-decorator", "Decorator should run function and return value; print wrapped result for 5.", "def passthrough(fn):\n    # keep signature simple\n    pass\n\n@passthrough\ndef square(n):\n    return n * n\n\nprint(square(5))\n", "25", "def passthrough(fn):\n    def wrapper(n):\n        return fn(n)\n    return wrapper\n\n@passthrough\ndef square(n):\n    return n * n\n\nprint(square(5))", ["functions", "decorators"]),
        ("Partial Application", "py-fn-adv-partial", "Use functools.partial to make add10 from add(a,b), print add10(7).", "from functools import partial\n\ndef add(a, b):\n    return a + b\n\n# create add10 and print add10(7)\n", "17", "from functools import partial\n\ndef add(a, b):\n    return a + b\n\nadd10 = partial(add, 10)\nprint(add10(7))", ["functions", "partial"]),
        ("Unpack Args and Kwargs", "py-fn-adv-unpack", "Call function with tuple and dict unpacking to print 12.", "def combine(a, b, c=0):\n    return a + b + c\n\nnums = (3, 4)\nextra = {'c': 5}\n# print combine with unpacking\n", "12", "def combine(a, b, c=0):\n    return a + b + c\n\nnums = (3, 4)\nextra = {'c': 5}\nprint(combine(*nums, **extra))", ["functions", "unpacking"]),
        ("Nonlocal Running Total", "py-fn-adv-nonlocal-total", "Build closure adder and print cumulative results for 3 then 4.", "def make_adder():\n    # return function add(n)\n    pass\n\nadd = make_adder()\nprint(add(3))\nprint(add(4))\n", "3\n7", "def make_adder():\n    total = 0\n    def add(n):\n        nonlocal total\n        total += n\n        return total\n    return add\n\nadd = make_adder()\nprint(add(3))\nprint(add(4))", ["functions", "closures"]),
        ("Any and All Predicates", "py-fn-adv-any-all", "Given predicate function, print all_even then any_even for [1,2,3,4].", "def is_even(n):\n    return n % 2 == 0\n\nnums = [1, 2, 3, 4]\n# print all-even then any-even\n", "False\nTrue", "def is_even(n):\n    return n % 2 == 0\n\nnums = [1, 2, 3, 4]\nprint(all(is_even(n) for n in nums))\nprint(any(is_even(n) for n in nums))", ["functions", "predicates"]),
        ("Custom Key Factory", "py-fn-adv-key-factory", "Create key function with closure using multiplier 10 and sort [3,1,2].", "def key_factory(multiplier):\n    # return key function\n    pass\n\nnums = [3, 1, 2]\nprint(sorted(nums, key=key_factory(10)))\n", "[1, 2, 3]", "def key_factory(multiplier):\n    def key(n):\n        return n * multiplier\n    return key\n\nnums = [3, 1, 2]\nprint(sorted(nums, key=key_factory(10)))", ["functions", "closures"]),
        ("Retry Wrapper", "py-fn-adv-retry-wrapper", "Implement wrapper that catches exception and returns 'failed'; print output.", "def safe_call(fn):\n    # call fn and catch exceptions\n    pass\n\ndef boom():\n    raise ValueError('x')\n\nprint(safe_call(boom))\n", "failed", "def safe_call(fn):\n    try:\n        return fn()\n    except Exception:\n        return 'failed'\n\ndef boom():\n    raise ValueError('x')\n\nprint(safe_call(boom))", ["functions", "exceptions"]),
        ("Generator Expression Sum", "py-fn-adv-genexpr", "Print sum of squares from 1..5 using generator expression.", "# print sum of squares\n", "55", "print(sum(n * n for n in range(1, 6)))", ["functions", "generator-expression"]),
        ("Callable Class in Function API", "py-fn-adv-callable-class", "Use callable object in map to add 1 to [1,2,3], print list.", "class AddOne:\n    def __call__(self, n):\n        # return incremented n\n        pass\n\nprint(list(map(AddOne(), [1, 2, 3])))\n", "[2, 3, 4]", "class AddOne:\n    def __call__(self, n):\n        return n + 1\n\nprint(list(map(AddOne(), [1, 2, 3])))", ["functions", "callable"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in advanced_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="advanced",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["functions"] + tags,
                solution_code=solution,
            )
        )

    return questions


def build_oop_questions() -> list[dict]:
    questions: list[dict] = []

    basic_specs = [
        ("Create Basic Class", "py-oop-basic-class", "Define class `Dog` with class attribute `species='canine'` and print it.", "class Dog:\n    # define class attribute\n\nprint(Dog.species)\n", "canine", "class Dog:\n    species = 'canine'\n\nprint(Dog.species)", ["oop", "class"]),
        ("Instantiate Object", "py-oop-basic-instantiate", "Define class `User` with `__init__(name)` and print instance name.", "class User:\n    def __init__(self, name):\n        # assign name\n        pass\n\nu = User('Ria')\nprint(u.name)\n", "Ria", "class User:\n    def __init__(self, name):\n        self.name = name\n\nu = User('Ria')\nprint(u.name)", ["oop", "init"]),
        ("Instance Method", "py-oop-basic-method", "Add method `speak` to print `meow` for Cat.", "class Cat:\n    def speak(self):\n        # print meow\n        pass\n\nCat().speak()\n", "meow", "class Cat:\n    def speak(self):\n        print('meow')\n\nCat().speak()", ["oop", "methods"]),
        ("Class vs Instance Attribute", "py-oop-basic-class-instance", "Show class attr shared by printing same value from two instances.", "class Box:\n    kind = 'storage'\n\na = Box()\nb = Box()\n# print a.kind then b.kind\n", "storage\nstorage", "class Box:\n    kind = 'storage'\n\na = Box()\nb = Box()\nprint(a.kind)\nprint(b.kind)", ["oop", "attributes"]),
        ("Simple Inheritance", "py-oop-basic-inheritance", "Create `Car(Vehicle)` where Vehicle has move() returning 'moving'. Print car.move().", "class Vehicle:\n    def move(self):\n        return 'moving'\n\nclass Car(Vehicle):\n    pass\n\nprint(Car().move())\n", "moving", "class Vehicle:\n    def move(self):\n        return 'moving'\n\nclass Car(Vehicle):\n    pass\n\nprint(Car().move())", ["oop", "inheritance"]),
        ("Method Override", "py-oop-basic-override", "Override `sound()` in Child to return 'beep'.", "class Parent:\n    def sound(self):\n        return 'base'\n\nclass Child(Parent):\n    # override sound\n    pass\n\nprint(Child().sound())\n", "beep", "class Parent:\n    def sound(self):\n        return 'base'\n\nclass Child(Parent):\n    def sound(self):\n        return 'beep'\n\nprint(Child().sound())", ["oop", "polymorphism"]),
        ("Use super()", "py-oop-basic-super", "Call parent __init__ using super and print combined name.", "class Person:\n    def __init__(self, name):\n        self.name = name\n\nclass Student(Person):\n    def __init__(self, name, grade):\n        # use super, store grade\n        pass\n\ns = Student('Ava', 9)\nprint(s.name)\n", "Ava", "class Person:\n    def __init__(self, name):\n        self.name = name\n\nclass Student(Person):\n    def __init__(self, name, grade):\n        super().__init__(name)\n        self.grade = grade\n\ns = Student('Ava', 9)\nprint(s.name)", ["oop", "super"]),
        ("Encapsulation Convention", "py-oop-basic-private", "Store `_pin` and print it from method `show_pin`.", "class Account:\n    def __init__(self):\n        self._pin = 1234\n\n    def show_pin(self):\n        # print _pin\n        pass\n\nAccount().show_pin()\n", "1234", "class Account:\n    def __init__(self):\n        self._pin = 1234\n\n    def show_pin(self):\n        print(self._pin)\n\nAccount().show_pin()", ["oop", "encapsulation"]),
        ("Class Method Constructor", "py-oop-basic-classmethod", "Implement `from_full_name` classmethod and print created first name.", "class Person:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n\n    @classmethod\n    def from_full_name(cls, full_name):\n        # split and return cls(...)\n        pass\n\np = Person.from_full_name('Lia Kim')\nprint(p.first)\n", "Lia", "class Person:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n\n    @classmethod\n    def from_full_name(cls, full_name):\n        first, last = full_name.split()\n        return cls(first, last)\n\np = Person.from_full_name('Lia Kim')\nprint(p.first)", ["oop", "classmethod"]),
        ("Static Method Utility", "py-oop-basic-staticmethod", "Add static method `is_even(n)` and print result for 10.", "class Math:\n    @staticmethod\n    def is_even(n):\n        # return bool\n        pass\n\nprint(Math.is_even(10))\n", "True", "class Math:\n    @staticmethod\n    def is_even(n):\n        return n % 2 == 0\n\nprint(Math.is_even(10))", ["oop", "staticmethod"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in basic_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="basic",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["oop"] + tags,
                solution_code=solution,
            )
        )

    intermediate_specs = [
        ("Property Getter", "py-oop-int-property-getter", "Create `@property` full_name and print it.", "class User:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n\n    @property\n    def full_name(self):\n        # return combined name\n        pass\n\nu = User('Noa', 'Lee')\nprint(u.full_name)\n", "Noa Lee", "class User:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n\n    @property\n    def full_name(self):\n        return f'{self.first} {self.last}'\n\nu = User('Noa', 'Lee')\nprint(u.full_name)", ["oop", "property"]),
        ("Property Setter", "py-oop-int-property-setter", "Add setter for celsius and print fahrenheit for 0C.", "class Temp:\n    def __init__(self, c):\n        self._c = c\n\n    @property\n    def celsius(self):\n        return self._c\n\n    @celsius.setter\n    def celsius(self, value):\n        # assign value\n        pass\n\n    @property\n    def fahrenheit(self):\n        return self._c * 9 / 5 + 32\n\nt = Temp(10)\nt.celsius = 0\nprint(t.fahrenheit)\n", "32.0", "class Temp:\n    def __init__(self, c):\n        self._c = c\n\n    @property\n    def celsius(self):\n        return self._c\n\n    @celsius.setter\n    def celsius(self, value):\n        self._c = value\n\n    @property\n    def fahrenheit(self):\n        return self._c * 9 / 5 + 32\n\nt = Temp(10)\nt.celsius = 0\nprint(t.fahrenheit)", ["oop", "property"]),
        ("Composition Example", "py-oop-int-composition", "Create `Engine` and `Car` that composes engine; print start message.", "class Engine:\n    def start(self):\n        return 'engine on'\n\nclass Car:\n    def __init__(self, engine):\n        self.engine = engine\n\n    def start(self):\n        # delegate to engine\n        pass\n\nc = Car(Engine())\nprint(c.start())\n", "engine on", "class Engine:\n    def start(self):\n        return 'engine on'\n\nclass Car:\n    def __init__(self, engine):\n        self.engine = engine\n\n    def start(self):\n        return self.engine.start()\n\nc = Car(Engine())\nprint(c.start())", ["oop", "composition"]),
        ("Abstract Base Class", "py-oop-int-abc", "Use ABC with abstract area(), implement in Square and print area 4*4.", "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        # return area\n        pass\n\nprint(Square(4).area())\n", "16", "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        return self.side * self.side\n\nprint(Square(4).area())", ["oop", "abc"]),
        ("Multiple Inheritance", "py-oop-int-multiple-inheritance", "Create class C(A,B) where A.msg='A', B.msg='B'; print C().msg().", "class A:\n    def msg(self):\n        return 'A'\n\nclass B:\n    def msg(self):\n        return 'B'\n\nclass C(A, B):\n    pass\n\nprint(C().msg())\n", "A", "class A:\n    def msg(self):\n        return 'A'\n\nclass B:\n    def msg(self):\n        return 'B'\n\nclass C(A, B):\n    pass\n\nprint(C().msg())", ["oop", "mro"]),
        ("Polymorphic Function", "py-oop-int-polymorphic-fn", "Write function that calls .speak() on Dog and Cat objects.", "class Dog:\n    def speak(self):\n        return 'woof'\n\nclass Cat:\n    def speak(self):\n        return 'meow'\n\ndef call_speak(animal):\n    # return speech\n    pass\n\nprint(call_speak(Dog()))\nprint(call_speak(Cat()))\n", "woof\nmeow", "class Dog:\n    def speak(self):\n        return 'woof'\n\nclass Cat:\n    def speak(self):\n        return 'meow'\n\ndef call_speak(animal):\n    return animal.speak()\n\nprint(call_speak(Dog()))\nprint(call_speak(Cat()))", ["oop", "polymorphism"]),
        ("Dataclass Basics", "py-oop-int-dataclass", "Create dataclass Point(x,y) and print x+y for Point(2,3).", "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n\n# create point and print sum\n", "5", "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n\np = Point(2, 3)\nprint(p.x + p.y)", ["oop", "dataclass"]),
        ("Class Variable Counter", "py-oop-int-class-counter", "Track created instances using class variable count, print after 3 objects.", "class User:\n    count = 0\n\n    def __init__(self):\n        # increment class counter\n        pass\n\nUser()\nUser()\nUser()\nprint(User.count)\n", "3", "class User:\n    count = 0\n\n    def __init__(self):\n        User.count += 1\n\nUser()\nUser()\nUser()\nprint(User.count)", ["oop", "class-variables"]),
        ("Method Chaining", "py-oop-int-chaining", "Return self from add() so chain works; print final value.", "class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def add(self, n):\n        self.value += n\n        # return self\n        pass\n\nc = Counter()\nc.add(2).add(3)\nprint(c.value)\n", "5", "class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def add(self, n):\n        self.value += n\n        return self\n\nc = Counter()\nc.add(2).add(3)\nprint(c.value)", ["oop", "patterns"]),
        ("Private Name Mangling", "py-oop-int-name-mangling", "Use __secret in class and print via method reveal().", "class Vault:\n    def __init__(self):\n        self.__secret = 'xyz'\n\n    def reveal(self):\n        # return secret\n        pass\n\nprint(Vault().reveal())\n", "xyz", "class Vault:\n    def __init__(self):\n        self.__secret = 'xyz'\n\n    def reveal(self):\n        return self.__secret\n\nprint(Vault().reveal())", ["oop", "encapsulation"]),
        ("Factory Classmethod by Dict", "py-oop-int-factory-dict", "Implement classmethod from_dict and print created title.", "class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n    @classmethod\n    def from_dict(cls, data):\n        # return cls with data values\n        pass\n\nb = Book.from_dict({'title': 'Py', 'pages': 100})\nprint(b.title)\n", "Py", "class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n    @classmethod\n    def from_dict(cls, data):\n        return cls(data['title'], data['pages'])\n\nb = Book.from_dict({'title': 'Py', 'pages': 100})\nprint(b.title)", ["oop", "factory"]),
        ("Simple Mixins", "py-oop-int-mixin", "Use mixin to add hello() to User class and print hello output.", "class HelloMixin:\n    def hello(self):\n        return 'hello'\n\nclass User(HelloMixin):\n    pass\n\nprint(User().hello())\n", "hello", "class HelloMixin:\n    def hello(self):\n        return 'hello'\n\nclass User(HelloMixin):\n    pass\n\nprint(User().hello())", ["oop", "mixins"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in intermediate_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="intermediate",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["oop"] + tags,
                solution_code=solution,
            )
        )

    advanced_specs = [
        ("Slots Memory Optimization", "py-oop-adv-slots", "Define class with __slots__ for x,y and print object x.", "class Point:\n    __slots__ = ('x', 'y')\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\np = Point(2, 3)\nprint(p.x)\n", "2", "class Point:\n    __slots__ = ('x', 'y')\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\np = Point(2, 3)\nprint(p.x)", ["oop", "slots"]),
        ("Custom Descriptor", "py-oop-adv-descriptor", "Implement descriptor enforcing int values and print stored value.", "class IntField:\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, owner):\n        return obj.__dict__[self.name]\n\n    def __set__(self, obj, value):\n        # enforce int\n        pass\n\nclass User:\n    age = IntField()\n\nu = User()\nu.age = 21\nprint(u.age)\n", "21", "class IntField:\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, owner):\n        return obj.__dict__[self.name]\n\n    def __set__(self, obj, value):\n        if not isinstance(value, int):\n            raise TypeError('int required')\n        obj.__dict__[self.name] = value\n\nclass User:\n    age = IntField()\n\nu = User()\nu.age = 21\nprint(u.age)", ["oop", "descriptor"]),
        ("MRO Demonstration", "py-oop-adv-mro", "Print first class name after C in MRO for class C(A,B).", "class A: pass\nclass B: pass\nclass C(A, B): pass\n# print class name at index 1 in C.__mro__\n", "A", "class A: pass\nclass B: pass\nclass C(A, B): pass\nprint(C.__mro__[1].__name__)", ["oop", "mro"]),
        ("Context Manager Class", "py-oop-adv-context-manager", "Build context manager class whose __enter__ returns 'open'; print value in with block.", "class Resource:\n    def __enter__(self):\n        # return marker\n        pass\n\n    def __exit__(self, exc_type, exc, tb):\n        return False\n\nwith Resource() as state:\n    print(state)\n", "open", "class Resource:\n    def __enter__(self):\n        return 'open'\n\n    def __exit__(self, exc_type, exc, tb):\n        return False\n\nwith Resource() as state:\n    print(state)", ["oop", "context-manager"]),
        ("Callable Objects", "py-oop-adv-callable", "Create class Adder(base) with __call__(x) returning base+x; print Adder(10)(5).", "class Adder:\n    def __init__(self, base):\n        self.base = base\n\n    def __call__(self, x):\n        # return base + x\n        pass\n\nprint(Adder(10)(5))\n", "15", "class Adder:\n    def __init__(self, base):\n        self.base = base\n\n    def __call__(self, x):\n        return self.base + x\n\nprint(Adder(10)(5))", ["oop", "callable"]),
        ("Dataclass Ordering", "py-oop-adv-dataclass-order", "Create ordered dataclass Task(priority,name), sort list, print first task name.", "from dataclasses import dataclass\n\n@dataclass(order=True)\nclass Task:\n    priority: int\n    name: str\n\ntasks = [Task(2, 'b'), Task(1, 'a')]\n# sort and print first name\n", "a", "from dataclasses import dataclass\n\n@dataclass(order=True)\nclass Task:\n    priority: int\n    name: str\n\ntasks = [Task(2, 'b'), Task(1, 'a')]\nprint(sorted(tasks)[0].name)", ["oop", "dataclass"]),
        ("Cooperative Multiple Inheritance", "py-oop-adv-cooperative-super", "Use cooperative super in diamond and print call chain marker.", "class A:\n    def run(self):\n        return 'A'\n\nclass B(A):\n    def run(self):\n        return super().run() + 'B'\n\nclass C(A):\n    def run(self):\n        return super().run() + 'C'\n\nclass D(B, C):\n    def run(self):\n        return super().run() + 'D'\n\nprint(D().run())\n", "ACBD", "class A:\n    def run(self):\n        return 'A'\n\nclass B(A):\n    def run(self):\n        return super().run() + 'B'\n\nclass C(A):\n    def run(self):\n        return super().run() + 'C'\n\nclass D(B, C):\n    def run(self):\n        return super().run() + 'D'\n\nprint(D().run())", ["oop", "inheritance"]),
        ("Registry Pattern", "py-oop-adv-registry", "Use class variable registry appended in __init__, print registry length after two objects.", "class Plugin:\n    registry = []\n\n    def __init__(self, name):\n        self.name = name\n        # append self to registry\n        pass\n\nPlugin('a')\nPlugin('b')\nprint(len(Plugin.registry))\n", "2", "class Plugin:\n    registry = []\n\n    def __init__(self, name):\n        self.name = name\n        Plugin.registry.append(self)\n\nPlugin('a')\nPlugin('b')\nprint(len(Plugin.registry))", ["oop", "patterns"]),
        ("Property Validation", "py-oop-adv-property-validation", "Validate age property to reject negatives; set 7 and print age.", "class Person:\n    def __init__(self):\n        self._age = 0\n\n    @property\n    def age(self):\n        return self._age\n\n    @age.setter\n    def age(self, value):\n        # validate non-negative\n        pass\n\np = Person()\np.age = 7\nprint(p.age)\n", "7", "class Person:\n    def __init__(self):\n        self._age = 0\n\n    @property\n    def age(self):\n        return self._age\n\n    @age.setter\n    def age(self, value):\n        if value < 0:\n            raise ValueError('age must be non-negative')\n        self._age = value\n\np = Person()\np.age = 7\nprint(p.age)", ["oop", "property"]),
        ("Metaclass Name Capture", "py-oop-adv-metaclass", "Create metaclass storing class name in `label`, print label for class Demo.", "class NameMeta(type):\n    def __new__(mcls, name, bases, namespace):\n        namespace['label'] = name.lower()\n        return super().__new__(mcls, name, bases, namespace)\n\nclass Demo(metaclass=NameMeta):\n    pass\n\nprint(Demo.label)\n", "demo", "class NameMeta(type):\n    def __new__(mcls, name, bases, namespace):\n        namespace['label'] = name.lower()\n        return super().__new__(mcls, name, bases, namespace)\n\nclass Demo(metaclass=NameMeta):\n    pass\n\nprint(Demo.label)", ["oop", "metaclass"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in advanced_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="advanced",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["oop"] + tags,
                solution_code=solution,
            )
        )

    return questions


def build_dunder_questions() -> list[dict]:
    questions: list[dict] = []

    basic_specs = [
        ("Dunder Init", "py-dunder-basic-init", "Create class User with __init__ storing name; print name.", "class User:\n    def __init__(self, name):\n        # store name\n        pass\n\nu = User('Nia')\nprint(u.name)\n", "Nia", "class User:\n    def __init__(self, name):\n        self.name = name\n\nu = User('Nia')\nprint(u.name)", ["dunder", "__init__"]),
        ("Dunder Str", "py-dunder-basic-str", "Implement __str__ returning `Item(pen)` and print object.", "class Item:\n    def __init__(self, name):\n        self.name = name\n\n    def __str__(self):\n        # return formatted text\n        pass\n\nprint(Item('pen'))\n", "Item(pen)", "class Item:\n    def __init__(self, name):\n        self.name = name\n\n    def __str__(self):\n        return f'Item({self.name})'\n\nprint(Item('pen'))", ["dunder", "__str__"]),
        ("Dunder Repr", "py-dunder-basic-repr", "Implement __repr__ returning `Point(2,3)` and print repr(obj).", "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __repr__(self):\n        # return repr string\n        pass\n\nprint(repr(Point(2, 3)))\n", "Point(2,3)", "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __repr__(self):\n        return f'Point({self.x},{self.y})'\n\nprint(repr(Point(2, 3)))", ["dunder", "__repr__"]),
        ("Dunder Len", "py-dunder-basic-len", "Implement __len__ for Box to return item count.", "class Box:\n    def __init__(self, items):\n        self.items = items\n\n    def __len__(self):\n        # return number of items\n        pass\n\nprint(len(Box([1, 2, 3])))\n", "3", "class Box:\n    def __init__(self, items):\n        self.items = items\n\n    def __len__(self):\n        return len(self.items)\n\nprint(len(Box([1, 2, 3])))", ["dunder", "__len__"]),
        ("Dunder Contains", "py-dunder-basic-contains", "Implement __contains__ for Inventory and print `'pen' in inv`.", "class Inventory:\n    def __init__(self, items):\n        self.items = items\n\n    def __contains__(self, item):\n        # membership check\n        pass\n\ninv = Inventory(['pen', 'paper'])\nprint('pen' in inv)\n", "True", "class Inventory:\n    def __init__(self, items):\n        self.items = items\n\n    def __contains__(self, item):\n        return item in self.items\n\ninv = Inventory(['pen', 'paper'])\nprint('pen' in inv)", ["dunder", "__contains__"]),
        ("Dunder Add", "py-dunder-basic-add", "Implement __add__ for Score and print sum of 7 and 5.", "class Score:\n    def __init__(self, value):\n        self.value = value\n\n    def __add__(self, other):\n        # return new Score with summed value\n        pass\n\nprint((Score(7) + Score(5)).value)\n", "12", "class Score:\n    def __init__(self, value):\n        self.value = value\n\n    def __add__(self, other):\n        return Score(self.value + other.value)\n\nprint((Score(7) + Score(5)).value)", ["dunder", "__add__"]),
        ("Dunder Eq", "py-dunder-basic-eq", "Implement __eq__ comparing value field and print equality.", "class Tag:\n    def __init__(self, value):\n        self.value = value\n\n    def __eq__(self, other):\n        # compare values\n        pass\n\nprint(Tag('x') == Tag('x'))\n", "True", "class Tag:\n    def __init__(self, value):\n        self.value = value\n\n    def __eq__(self, other):\n        return isinstance(other, Tag) and self.value == other.value\n\nprint(Tag('x') == Tag('x'))", ["dunder", "__eq__"]),
        ("Dunder Bool", "py-dunder-basic-bool", "Implement __bool__ where Wallet is truthy if money > 0.", "class Wallet:\n    def __init__(self, money):\n        self.money = money\n\n    def __bool__(self):\n        # return truthiness\n        pass\n\nprint(bool(Wallet(1)))\n", "True", "class Wallet:\n    def __init__(self, money):\n        self.money = money\n\n    def __bool__(self):\n        return self.money > 0\n\nprint(bool(Wallet(1)))", ["dunder", "__bool__"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in basic_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="basic",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["dunder-methods"] + tags,
                solution_code=solution,
            )
        )

    intermediate_specs = [
        ("Dunder Lt Sorting", "py-dunder-int-lt", "Implement __lt__ for Task(priority) and print sorted priorities.", "class Task:\n    def __init__(self, priority):\n        self.priority = priority\n\n    def __lt__(self, other):\n        # compare priority\n        pass\n\ntasks = [Task(3), Task(1), Task(2)]\nprint([t.priority for t in sorted(tasks)])\n", "[1, 2, 3]", "class Task:\n    def __init__(self, priority):\n        self.priority = priority\n\n    def __lt__(self, other):\n        return self.priority < other.priority\n\ntasks = [Task(3), Task(1), Task(2)]\nprint([t.priority for t in sorted(tasks)])", ["dunder", "__lt__"]),
        ("Dunder Iter", "py-dunder-int-iter", "Implement iterable Range3 yielding 0,1,2 and print list().", "class Range3:\n    def __iter__(self):\n        # return iterator\n        pass\n\nprint(list(Range3()))\n", "[0, 1, 2]", "class Range3:\n    def __iter__(self):\n        return iter([0, 1, 2])\n\nprint(list(Range3()))", ["dunder", "__iter__"]),
        ("Dunder Next", "py-dunder-int-next", "Build iterator Countdown(2) and print next three calls with Stop at end handled.", "class Countdown:\n    def __init__(self, start):\n        self.current = start\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        # implement countdown\n        pass\n\nc = Countdown(2)\nprint(next(c))\nprint(next(c))\ntry:\n    print(next(c))\nexcept StopIteration:\n    print('stop')\n", "2\n1\nstop", "class Countdown:\n    def __init__(self, start):\n        self.current = start\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        val = self.current\n        self.current -= 1\n        return val\n\nc = Countdown(2)\nprint(next(c))\nprint(next(c))\ntry:\n    print(next(c))\nexcept StopIteration:\n    print('stop')", ["dunder", "__next__"]),
        ("Dunder Getitem", "py-dunder-int-getitem", "Implement __getitem__ forwarding to internal list; print index 1.", "class Deck:\n    def __init__(self, cards):\n        self.cards = cards\n\n    def __getitem__(self, idx):\n        # return indexed card\n        pass\n\nprint(Deck(['A', 'K', 'Q'])[1])\n", "K", "class Deck:\n    def __init__(self, cards):\n        self.cards = cards\n\n    def __getitem__(self, idx):\n        return self.cards[idx]\n\nprint(Deck(['A', 'K', 'Q'])[1])", ["dunder", "__getitem__"]),
        ("Dunder Setitem", "py-dunder-int-setitem", "Implement __setitem__ to set internal list values; update index 0 and print.", "class Row:\n    def __init__(self, values):\n        self.values = values\n\n    def __setitem__(self, idx, value):\n        # set value\n        pass\n\nr = Row([1, 2])\nr[0] = 9\nprint(r.values)\n", "[9, 2]", "class Row:\n    def __init__(self, values):\n        self.values = values\n\n    def __setitem__(self, idx, value):\n        self.values[idx] = value\n\nr = Row([1, 2])\nr[0] = 9\nprint(r.values)", ["dunder", "__setitem__"]),
        ("Dunder Call", "py-dunder-int-call", "Implement __call__ in Multiplier and print m(7) where factor=3.", "class Multiplier:\n    def __init__(self, factor):\n        self.factor = factor\n\n    def __call__(self, n):\n        # return multiplied\n        pass\n\nm = Multiplier(3)\nprint(m(7))\n", "21", "class Multiplier:\n    def __init__(self, factor):\n        self.factor = factor\n\n    def __call__(self, n):\n        return n * self.factor\n\nm = Multiplier(3)\nprint(m(7))", ["dunder", "__call__"]),
        ("Dunder Hash with Eq", "py-dunder-int-hash", "Implement __hash__ and __eq__ for Key(id), print len of set with duplicate ids.", "class Key:\n    def __init__(self, ident):\n        self.ident = ident\n\n    def __eq__(self, other):\n        # compare id\n        pass\n\n    def __hash__(self):\n        # hash by id\n        pass\n\ns = {Key(1), Key(1), Key(2)}\nprint(len(s))\n", "2", "class Key:\n    def __init__(self, ident):\n        self.ident = ident\n\n    def __eq__(self, other):\n        return isinstance(other, Key) and self.ident == other.ident\n\n    def __hash__(self):\n        return hash(self.ident)\n\ns = {Key(1), Key(1), Key(2)}\nprint(len(s))", ["dunder", "__hash__", "__eq__"]),
        ("Dunder Format", "py-dunder-int-format", "Implement __format__ to support 'upper' spec and print formatted value.", "class Label:\n    def __init__(self, text):\n        self.text = text\n\n    def __format__(self, spec):\n        # support 'upper' else default\n        pass\n\nprint(format(Label('python'), 'upper'))\n", "PYTHON", "class Label:\n    def __init__(self, text):\n        self.text = text\n\n    def __format__(self, spec):\n        if spec == 'upper':\n            return self.text.upper()\n        return self.text\n\nprint(format(Label('python'), 'upper'))", ["dunder", "__format__"]),
        ("Dunder Enter Exit", "py-dunder-int-enter-exit", "Implement context manager methods and print 'inside' in with block.", "class Session:\n    def __enter__(self):\n        # return self\n        pass\n\n    def __exit__(self, exc_type, exc, tb):\n        return False\n\nwith Session() as s:\n    print('inside')\n", "inside", "class Session:\n    def __enter__(self):\n        return self\n\n    def __exit__(self, exc_type, exc, tb):\n        return False\n\nwith Session() as s:\n    print('inside')", ["dunder", "__enter__", "__exit__"]),
        ("Dunder Missing in Dict Subclass", "py-dunder-int-missing", "Subclass dict with __missing__ returning 0, print value for absent key.", "class ScoreMap(dict):\n    def __missing__(self, key):\n        # return default 0\n        pass\n\ns = ScoreMap({'a': 1})\nprint(s['z'])\n", "0", "class ScoreMap(dict):\n    def __missing__(self, key):\n        return 0\n\ns = ScoreMap({'a': 1})\nprint(s['z'])", ["dunder", "__missing__"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in intermediate_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="intermediate",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["dunder-methods"] + tags,
                solution_code=solution,
            )
        )

    advanced_specs = [
        ("Total Ordering", "py-dunder-adv-total-ordering", "Use functools.total_ordering with __eq__ and __lt__, compare two versions.", "from functools import total_ordering\n\n@total_ordering\nclass Version:\n    def __init__(self, major):\n        self.major = major\n\n    def __eq__(self, other):\n        return self.major == other.major\n\n    def __lt__(self, other):\n        # compare major versions\n        pass\n\nprint(Version(1) < Version(2))\n", "True", "from functools import total_ordering\n\n@total_ordering\nclass Version:\n    def __init__(self, major):\n        self.major = major\n\n    def __eq__(self, other):\n        return self.major == other.major\n\n    def __lt__(self, other):\n        return self.major < other.major\n\nprint(Version(1) < Version(2))", ["dunder", "ordering"]),
        ("Dunder Matmul", "py-dunder-adv-matmul", "Implement __matmul__ for 2D vectors as dot product, print result.", "class Vec2:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __matmul__(self, other):\n        # return dot product\n        pass\n\nprint(Vec2(1, 2) @ Vec2(3, 4))\n", "11", "class Vec2:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __matmul__(self, other):\n        return self.x * other.x + self.y * other.y\n\nprint(Vec2(1, 2) @ Vec2(3, 4))", ["dunder", "__matmul__"]),
        ("Dunder Radd", "py-dunder-adv-radd", "Implement __radd__ so 10 + Score(5) prints 15.", "class Score:\n    def __init__(self, value):\n        self.value = value\n\n    def __radd__(self, other):\n        # support int + Score\n        pass\n\nprint(10 + Score(5))\n", "15", "class Score:\n    def __init__(self, value):\n        self.value = value\n\n    def __radd__(self, other):\n        return other + self.value\n\nprint(10 + Score(5))", ["dunder", "__radd__"]),
        ("Dunder Getattr Fallback", "py-dunder-adv-getattr", "Use __getattr__ to return 'N/A' for missing attributes; print obj.city.", "class Profile:\n    def __init__(self, name):\n        self.name = name\n\n    def __getattr__(self, item):\n        # fallback for unknown attrs\n        pass\n\np = Profile('Uma')\nprint(p.city)\n", "N/A", "class Profile:\n    def __init__(self, name):\n        self.name = name\n\n    def __getattr__(self, item):\n        return 'N/A'\n\np = Profile('Uma')\nprint(p.city)", ["dunder", "__getattr__"]),
        ("Dunder Setattr Validation", "py-dunder-adv-setattr", "Use __setattr__ to block negative balance; set positive and print.", "class Wallet:\n    def __setattr__(self, name, value):\n        # disallow negative for balance\n        pass\n\nw = Wallet()\nw.balance = 20\nprint(w.balance)\n", "20", "class Wallet:\n    def __setattr__(self, name, value):\n        if name == 'balance' and value < 0:\n            raise ValueError('negative balance')\n        super().__setattr__(name, value)\n\nw = Wallet()\nw.balance = 20\nprint(w.balance)", ["dunder", "__setattr__"]),
        ("Dunder Delattr", "py-dunder-adv-delattr", "Intercept delete to remove key from __dict__, then print hasattr result.", "class Store:\n    def __init__(self):\n        self.code = 'A1'\n\n    def __delattr__(self, name):\n        # custom delete then delegate\n        pass\n\ns = Store()\ndel s.code\nprint(hasattr(s, 'code'))\n", "False", "class Store:\n    def __init__(self):\n        self.code = 'A1'\n\n    def __delattr__(self, name):\n        super().__delattr__(name)\n\ns = Store()\ndel s.code\nprint(hasattr(s, 'code'))", ["dunder", "__delattr__"]),
        ("Dunder Reduce for Pickle", "py-dunder-adv-reduce", "Implement __reduce__ for Token and print restored value.", "import pickle\n\nclass Token:\n    def __init__(self, value):\n        self.value = value\n\n    def __reduce__(self):\n        # return constructor tuple\n        pass\n\nt = Token('abc')\ndata = pickle.dumps(t)\nobj = pickle.loads(data)\nprint(obj.value)\n", "abc", "import pickle\n\nclass Token:\n    def __init__(self, value):\n        self.value = value\n\n    def __reduce__(self):\n        return (Token, (self.value,))\n\nt = Token('abc')\ndata = pickle.dumps(t)\nobj = pickle.loads(data)\nprint(obj.value)", ["dunder", "__reduce__"]),
        ("Dunder Index for int()", "py-dunder-adv-index", "Implement __index__ in class Level and print hex(Level(15)).", "class Level:\n    def __init__(self, value):\n        self.value = value\n\n    def __index__(self):\n        # return integer index value\n        pass\n\nprint(hex(Level(15)))\n", "0xf", "class Level:\n    def __init__(self, value):\n        self.value = value\n\n    def __index__(self):\n        return self.value\n\nprint(hex(Level(15)))", ["dunder", "__index__"]),
    ]

    for title, slug, instruction, starter, expected, solution, tags in advanced_specs:
        questions.append(
            _exercise(
                title=title,
                slug=slug,
                difficulty="advanced",
                instruction=instruction,
                starter_code=starter,
                expected_output=expected,
                tags=["dunder-methods"] + tags,
                solution_code=solution,
            )
        )

    return questions


LISTS_TUPLES_TOPIC_SLUG = "lists-tuples"
DICTS_SETS_TOPIC_SLUG = "dicts-sets"
FUNCTIONS_TOPIC_SLUG = "functions"
OOP_TOPIC_SLUG = "oop"
DUNDER_TOPIC_SLUG = "dunder-methods"

LISTS_TUPLES_QUESTIONS = build_lists_tuples_questions()
DICTS_SETS_QUESTIONS = build_dicts_sets_questions()
FUNCTIONS_QUESTIONS = build_functions_questions()
OOP_QUESTIONS = build_oop_questions()
DUNDER_QUESTIONS = build_dunder_questions()


async def main() -> None:
    totals: list[tuple[str, int]] = []

    seeded = await seed_questions_for_topic(
        LISTS_TUPLES_TOPIC_SLUG,
        LISTS_TUPLES_QUESTIONS,
        "Module 06 — Lists & Tuples",
    )
    totals.append((LISTS_TUPLES_TOPIC_SLUG, seeded))

    seeded = await seed_questions_for_topic(
        DICTS_SETS_TOPIC_SLUG,
        DICTS_SETS_QUESTIONS,
        "Module 07 — Dictionaries & Sets",
    )
    totals.append((DICTS_SETS_TOPIC_SLUG, seeded))

    seeded = await seed_questions_for_topic(
        FUNCTIONS_TOPIC_SLUG,
        FUNCTIONS_QUESTIONS,
        "Module 08 — Functions",
    )
    totals.append((FUNCTIONS_TOPIC_SLUG, seeded))

    seeded = await seed_questions_for_topic(
        OOP_TOPIC_SLUG,
        OOP_QUESTIONS,
        "Module 09 — OOP",
    )
    totals.append((OOP_TOPIC_SLUG, seeded))

    seeded = await seed_questions_for_topic(
        DUNDER_TOPIC_SLUG,
        DUNDER_QUESTIONS,
        "Module 10 — Dunder Methods",
    )
    totals.append((DUNDER_TOPIC_SLUG, seeded))

    for topic, count in totals:
        print(f"Seeded {count} questions for {topic}")


if __name__ == "__main__":
    asyncio.run(main())
