"""
seeds/questions_python_modules_21_25.py
---------------------------------------
Python Learning Studio - Modules 21-25:
- Module 21: Concurrency (22 exercises)
- Module 22: Async (22 exercises)
- Module 23: Performance (22 exercises)
- Module 24: Design Patterns (22 exercises)
- Module 25: Data Scripting (26 exercises)

Usage:
    python -m seeds.questions_python_modules_21_25
"""

import asyncio
from collections import Counter

from seeds.loader import seed_questions_for_topic


TOPIC_ORDER = [
    ("concurrency", "Module 21 - Concurrency"),
    ("async", "Module 22 - Async Python"),
    ("performance", "Module 23 - Performance"),
    ("design-patterns", "Module 24 - Design Patterns"),
    ("data-scripting", "Module 25 - Data Scripting"),
]

QUESTIONS_BY_TOPIC: dict[str, list[dict]] = {slug: [] for slug, _ in TOPIC_ORDER}


def _xp_for(difficulty: str) -> int:
    return {"basic": 8, "intermediate": 18, "advanced": 30}[difficulty]


def add_question(
    *,
    topic_slug: str,
    title: str,
    slug: str,
    difficulty: str,
    task: str,
    starter_code: str,
    solution_code: str,
    expected_output: str,
    tags: list[str],
    question_type: str = "code_completion",
    time_estimate_mins: int | None = None,
) -> None:
    mins = time_estimate_mins or {"basic": 4, "intermediate": 8, "advanced": 12}[difficulty]
    QUESTIONS_BY_TOPIC[topic_slug].append(
        {
            "title": title,
            "slug": slug,
            "difficulty": difficulty,
            "question_type": question_type,
            "problem_statement": (
                f"## {title}\n\n"
                f"{task}\n\n"
                f"**Expected output:**\n```\n{expected_output}\n```\n"
            ),
            "starter_code": starter_code,
            "expected_output": expected_output,
            "tags": tags,
            "xp_reward": _xp_for(difficulty),
            "time_estimate_mins": mins,
            "solutions": [
                {
                    "title": "Solution",
                    "code": solution_code,
                    "explanation": "",
                    "is_optimal": True,
                }
            ],
        }
    )


# ---------------------------------------------------------------------------
# Module 21: Concurrency (22 = 6 basic, 8 intermediate, 8 advanced)
# ---------------------------------------------------------------------------
add_question(
    topic_slug="concurrency",
    title="Start and Join One Thread",
    slug="py-concurrency-start-join",
    difficulty="basic",
    task="Create one thread that prints `worker done`, then join it and print `main done`.",
    starter_code="import threading\n# create thread and join\n",
    solution_code=(
        "import threading\n\n"
        "def worker():\n"
        "    print('worker done')\n\n"
        "t = threading.Thread(target=worker)\n"
        "t.start()\n"
        "t.join()\n"
        "print('main done')"
    ),
    expected_output="worker done\nmain done",
    tags=["python", "concurrency", "threading"],
)
add_question(
    topic_slug="concurrency",
    title="Thread Name",
    slug="py-concurrency-thread-name",
    difficulty="basic",
    task="Start a thread named `io-worker` and print `io-worker` from inside the target function.",
    starter_code="import threading\n# print current thread name\n",
    solution_code=(
        "import threading\n\n"
        "def worker():\n"
        "    print(threading.current_thread().name)\n\n"
        "t = threading.Thread(target=worker, name='io-worker')\n"
        "t.start()\n"
        "t.join()"
    ),
    expected_output="io-worker",
    tags=["python", "concurrency", "threading"],
)
add_question(
    topic_slug="concurrency",
    title="Queue Put and Get",
    slug="py-concurrency-queue-put-get",
    difficulty="basic",
    task="Put `10` and `20` into a queue and print their sum after getting both values.",
    starter_code="from queue import Queue\nq = Queue()\n# put, get, and sum\n",
    solution_code="from queue import Queue\nq = Queue()\nq.put(10)\nq.put(20)\nprint(q.get() + q.get())",
    expected_output="30",
    tags=["python", "concurrency", "queue"],
)
add_question(
    topic_slug="concurrency",
    title="Lock Around Shared Counter",
    slug="py-concurrency-lock-counter",
    difficulty="basic",
    task="Increment a shared counter 1000 times in one thread using a lock, then print the final value.",
    starter_code="import threading\ncounter = 0\nlock = threading.Lock()\n# increment with lock\n",
    solution_code=(
        "import threading\ncounter = 0\nlock = threading.Lock()\n\n"
        "def worker():\n"
        "    global counter\n"
        "    for _ in range(1000):\n"
        "        with lock:\n"
        "            counter += 1\n\n"
        "t = threading.Thread(target=worker)\n"
        "t.start()\n"
        "t.join()\n"
        "print(counter)"
    ),
    expected_output="1000",
    tags=["python", "concurrency", "lock"],
)
add_question(
    topic_slug="concurrency",
    title="Event Signal",
    slug="py-concurrency-event-signal",
    difficulty="basic",
    task="Create a `threading.Event`, set it, then print whether it is set.",
    starter_code="import threading\nevent = threading.Event()\n# set and print state\n",
    solution_code="import threading\nevent = threading.Event()\nevent.set()\nprint(event.is_set())",
    expected_output="True",
    tags=["python", "concurrency", "event"],
)
add_question(
    topic_slug="concurrency",
    title="Two Worker Threads",
    slug="py-concurrency-two-workers",
    difficulty="basic",
    task="Run two threads that each append one number to a list under lock. Print the sorted list.",
    starter_code="import threading\nout = []\nlock = threading.Lock()\n# append from two workers\n",
    solution_code=(
        "import threading\nout = []\nlock = threading.Lock()\n\n"
        "def worker(v):\n"
        "    with lock:\n"
        "        out.append(v)\n\n"
        "t1 = threading.Thread(target=worker, args=(2,))\n"
        "t2 = threading.Thread(target=worker, args=(1,))\n"
        "t1.start(); t2.start()\n"
        "t1.join(); t2.join()\n"
        "print(sorted(out))"
    ),
    expected_output="[1, 2]",
    tags=["python", "concurrency", "threading"],
)
add_question(
    topic_slug="concurrency",
    title="Thread Pool Map",
    slug="py-concurrency-pool-map",
    difficulty="intermediate",
    task="Use `ThreadPoolExecutor` to square `[1, 2, 3, 4]` and print the result list.",
    starter_code="from concurrent.futures import ThreadPoolExecutor\nnums = [1, 2, 3, 4]\n# map square\n",
    solution_code=(
        "from concurrent.futures import ThreadPoolExecutor\nnums = [1, 2, 3, 4]\n"
        "with ThreadPoolExecutor(max_workers=2) as ex:\n"
        "    print(list(ex.map(lambda x: x * x, nums)))"
    ),
    expected_output="[1, 4, 9, 16]",
    tags=["python", "concurrency", "thread-pool"],
)
add_question(
    topic_slug="concurrency",
    title="Future Result",
    slug="py-concurrency-future-result",
    difficulty="intermediate",
    task="Submit one callable that returns `42` and print the future result.",
    starter_code="from concurrent.futures import ThreadPoolExecutor\n# submit and print result\n",
    solution_code=(
        "from concurrent.futures import ThreadPoolExecutor\n"
        "with ThreadPoolExecutor(max_workers=1) as ex:\n"
        "    f = ex.submit(lambda: 42)\n"
        "    print(f.result())"
    ),
    expected_output="42",
    tags=["python", "concurrency", "future"],
)
add_question(
    topic_slug="concurrency",
    title="Wait for First Completed",
    slug="py-concurrency-wait-first",
    difficulty="intermediate",
    task="Submit two immediate futures and use `wait(..., return_when=FIRST_COMPLETED)`. Print number of done futures.",
    starter_code="from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED\n# submit and wait\n",
    solution_code=(
        "from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED\n"
        "with ThreadPoolExecutor(max_workers=2) as ex:\n"
        "    futures = [ex.submit(lambda: 1), ex.submit(lambda: 2)]\n"
        "    done, _ = wait(futures, return_when=FIRST_COMPLETED)\n"
        "    print(len(done))"
    ),
    expected_output="1",
    tags=["python", "concurrency", "future"],
)
add_question(
    topic_slug="concurrency",
    title="Barrier Synchronization",
    slug="py-concurrency-barrier",
    difficulty="intermediate",
    task="Create a barrier for two threads; each thread waits, then appends `passed`. Print list length.",
    starter_code="import threading\n# use Barrier(2)\n",
    solution_code=(
        "import threading\nbarrier = threading.Barrier(2)\nout = []\nlock = threading.Lock()\n\n"
        "def worker():\n"
        "    barrier.wait()\n"
        "    with lock:\n"
        "        out.append('passed')\n\n"
        "t1 = threading.Thread(target=worker)\n"
        "t2 = threading.Thread(target=worker)\n"
        "t1.start(); t2.start()\n"
        "t1.join(); t2.join()\n"
        "print(len(out))"
    ),
    expected_output="2",
    tags=["python", "concurrency", "barrier"],
)
add_question(
    topic_slug="concurrency",
    title="Semaphore Limit",
    slug="py-concurrency-semaphore",
    difficulty="intermediate",
    task="Use a semaphore with capacity 1 to protect two critical section appends. Print the number of records.",
    starter_code="import threading\nsem = threading.Semaphore(1)\nout = []\n# critical section under semaphore\n",
    solution_code=(
        "import threading\nsem = threading.Semaphore(1)\nout = []\n\n"
        "def worker(v):\n"
        "    with sem:\n"
        "        out.append(v)\n\n"
        "t1 = threading.Thread(target=worker, args=(1,))\n"
        "t2 = threading.Thread(target=worker, args=(2,))\n"
        "t1.start(); t2.start()\n"
        "t1.join(); t2.join()\n"
        "print(len(out))"
    ),
    expected_output="2",
    tags=["python", "concurrency", "semaphore"],
)
add_question(
    topic_slug="concurrency",
    title="Producer Consumer Queue",
    slug="py-concurrency-producer-consumer",
    difficulty="intermediate",
    task="Producer puts `1,2,3` then sentinel `None`; consumer sums until sentinel. Print sum.",
    starter_code="import threading\nfrom queue import Queue\n# implement producer/consumer\n",
    solution_code=(
        "import threading\nfrom queue import Queue\nq = Queue()\nresult = {'sum': 0}\n\n"
        "def producer():\n"
        "    for v in [1, 2, 3]:\n"
        "        q.put(v)\n"
        "    q.put(None)\n\n"
        "def consumer():\n"
        "    while True:\n"
        "        item = q.get()\n"
        "        if item is None:\n"
        "            break\n"
        "        result['sum'] += item\n\n"
        "tp = threading.Thread(target=producer)\n"
        "tc = threading.Thread(target=consumer)\n"
        "tp.start(); tc.start()\n"
        "tp.join(); tc.join()\n"
        "print(result['sum'])"
    ),
    expected_output="6",
    tags=["python", "concurrency", "queue"],
)
add_question(
    topic_slug="concurrency",
    title="Thread Safe Dictionary Update",
    slug="py-concurrency-safe-dict",
    difficulty="intermediate",
    task="Use a lock while two threads increment `counts['ok']` 500 times each. Print value.",
    starter_code="import threading\ncounts = {'ok': 0}\nlock = threading.Lock()\n# update dict safely\n",
    solution_code=(
        "import threading\ncounts = {'ok': 0}\nlock = threading.Lock()\n\n"
        "def worker():\n"
        "    for _ in range(500):\n"
        "        with lock:\n"
        "            counts['ok'] += 1\n\n"
        "t1 = threading.Thread(target=worker)\n"
        "t2 = threading.Thread(target=worker)\n"
        "t1.start(); t2.start()\n"
        "t1.join(); t2.join()\n"
        "print(counts['ok'])"
    ),
    expected_output="1000",
    tags=["python", "concurrency", "lock"],
)
add_question(
    topic_slug="concurrency",
    title="Reentrant Lock Usage",
    slug="py-concurrency-rlock",
    difficulty="intermediate",
    task="Use `threading.RLock` to acquire the same lock twice in one function and print `ok`.",
    starter_code="import threading\n# use RLock reentrantly\n",
    solution_code=(
        "import threading\nlock = threading.RLock()\n\n"
        "def worker():\n"
        "    with lock:\n"
        "        with lock:\n"
        "            print('ok')\n\n"
        "worker()"
    ),
    expected_output="ok",
    tags=["python", "concurrency", "rlock"],
)
add_question(
    topic_slug="concurrency",
    title="ThreadPool with as_completed",
    slug="py-concurrency-as-completed",
    difficulty="advanced",
    task="Submit tasks returning `1,2,3` and collect with `as_completed`. Print sorted results.",
    starter_code="from concurrent.futures import ThreadPoolExecutor, as_completed\n# collect results\n",
    solution_code=(
        "from concurrent.futures import ThreadPoolExecutor, as_completed\n"
        "with ThreadPoolExecutor(max_workers=3) as ex:\n"
        "    futures = [ex.submit(lambda x=v: x) for v in [1, 2, 3]]\n"
        "    out = [f.result() for f in as_completed(futures)]\n"
        "print(sorted(out))"
    ),
    expected_output="[1, 2, 3]",
    tags=["python", "concurrency", "thread-pool"],
)
add_question(
    topic_slug="concurrency",
    title="Condition Variable",
    slug="py-concurrency-condition",
    difficulty="advanced",
    task="Use a condition variable so a waiting thread prints `ready` after notifier sets state.",
    starter_code="import threading\n# use Condition for signaling\n",
    solution_code=(
        "import threading\ncond = threading.Condition()\nstate = {'ready': False}\nout = []\n\n"
        "def waiter():\n"
        "    with cond:\n"
        "        while not state['ready']:\n"
        "            cond.wait()\n"
        "        out.append('ready')\n\n"
        "def notifier():\n"
        "    with cond:\n"
        "        state['ready'] = True\n"
        "        cond.notify()\n\n"
        "t1 = threading.Thread(target=waiter)\n"
        "t2 = threading.Thread(target=notifier)\n"
        "t1.start(); t2.start()\n"
        "t1.join(); t2.join()\n"
        "print(out[0])"
    ),
    expected_output="ready",
    tags=["python", "concurrency", "condition"],
)
add_question(
    topic_slug="concurrency",
    title="Race Condition Fix",
    slug="py-concurrency-race-fix",
    difficulty="advanced",
    task="Fix shared counter increments with lock in four threads (250 each). Print final counter.",
    starter_code="import threading\ncounter = 0\n# fix race condition with lock\n",
    solution_code=(
        "import threading\ncounter = 0\nlock = threading.Lock()\n\n"
        "def worker():\n"
        "    global counter\n"
        "    for _ in range(250):\n"
        "        with lock:\n"
        "            counter += 1\n\n"
        "threads = [threading.Thread(target=worker) for _ in range(4)]\n"
        "for t in threads:\n"
        "    t.start()\n"
        "for t in threads:\n"
        "    t.join()\n"
        "print(counter)"
    ),
    expected_output="1000",
    tags=["python", "concurrency", "race-condition"],
    question_type="debug_model",
)
add_question(
    topic_slug="concurrency",
    title="Queue Task Done and Join",
    slug="py-concurrency-queue-join",
    difficulty="advanced",
    task="Use `task_done()` and `join()` for queue items `[2,4,6]`; print processed sum.",
    starter_code="import threading\nfrom queue import Queue\n# process queue with join\n",
    solution_code=(
        "import threading\nfrom queue import Queue\nq = Queue()\nout = {'sum': 0}\n\n"
        "def consumer():\n"
        "    while True:\n"
        "        item = q.get()\n"
        "        if item is None:\n"
        "            q.task_done()\n"
        "            break\n"
        "        out['sum'] += item\n"
        "        q.task_done()\n\n"
        "t = threading.Thread(target=consumer)\n"
        "t.start()\n"
        "for v in [2, 4, 6]:\n"
        "    q.put(v)\n"
        "q.put(None)\n"
        "q.join()\n"
        "t.join()\n"
        "print(out['sum'])"
    ),
    expected_output="12",
    tags=["python", "concurrency", "queue"],
)
add_question(
    topic_slug="concurrency",
    title="Deadlock Avoidance by Lock Ordering",
    slug="py-concurrency-lock-ordering",
    difficulty="advanced",
    task="Acquire two locks in consistent order inside a worker and print `ok` after two threads finish.",
    starter_code="import threading\n# acquire locks in same order\n",
    solution_code=(
        "import threading\nlock_a = threading.Lock()\nlock_b = threading.Lock()\n\n"
        "def worker():\n"
        "    first, second = sorted([lock_a, lock_b], key=id)\n"
        "    with first:\n"
        "        with second:\n"
        "            pass\n\n"
        "t1 = threading.Thread(target=worker)\n"
        "t2 = threading.Thread(target=worker)\n"
        "t1.start(); t2.start()\n"
        "t1.join(); t2.join()\n"
        "print('ok')"
    ),
    expected_output="ok",
    tags=["python", "concurrency", "deadlock"],
)
add_question(
    topic_slug="concurrency",
    title="Thread Local Storage",
    slug="py-concurrency-thread-local",
    difficulty="advanced",
    task="Use `threading.local()` so each thread stores different value and print sorted results.",
    starter_code="import threading\n# use threading.local\n",
    solution_code=(
        "import threading\nlocal_data = threading.local()\nout = []\nlock = threading.Lock()\n\n"
        "def worker(v):\n"
        "    local_data.value = v\n"
        "    with lock:\n"
        "        out.append(local_data.value)\n\n"
        "threads = [threading.Thread(target=worker, args=(v,)) for v in [3, 1, 2]]\n"
        "for t in threads:\n"
        "    t.start()\n"
        "for t in threads:\n"
        "    t.join()\n"
        "print(sorted(out))"
    ),
    expected_output="[1, 2, 3]",
    tags=["python", "concurrency", "thread-local"],
)
add_question(
    topic_slug="concurrency",
    title="CPU Bound with Process Pool",
    slug="py-concurrency-process-pool",
    difficulty="advanced",
    task="Use `ProcessPoolExecutor` to square `[2,3,4]` and print the sum of results.",
    starter_code="from concurrent.futures import ProcessPoolExecutor\n# map square and sum\n",
    solution_code=(
        "from concurrent.futures import ProcessPoolExecutor\n\n"
        "def square(x):\n"
        "    return x * x\n\n"
        "if __name__ == '__main__':\n"
        "    with ProcessPoolExecutor(max_workers=2) as ex:\n"
        "        print(sum(ex.map(square, [2, 3, 4])))"
    ),
    expected_output="29",
    tags=["python", "concurrency", "multiprocessing"],
    question_type="build_from_scratch",
)
add_question(
    topic_slug="concurrency",
    title="Bounded Queue Backpressure",
    slug="py-concurrency-bounded-queue",
    difficulty="advanced",
    task="Create `Queue(maxsize=2)`, put two items, and print queue size.",
    starter_code="from queue import Queue\n# bounded queue size\n",
    solution_code="from queue import Queue\nq = Queue(maxsize=2)\nq.put(1)\nq.put(2)\nprint(q.qsize())",
    expected_output="2",
    tags=["python", "concurrency", "queue"],
)


# ---------------------------------------------------------------------------
# Module 22: Async (22 = 6 basic, 8 intermediate, 8 advanced)
# ---------------------------------------------------------------------------
add_question(
    topic_slug="async",
    title="First Coroutine",
    slug="py-async-first-coroutine",
    difficulty="basic",
    task="Write `async def hello()` that prints `hello async`, and run it with `asyncio.run`.",
    starter_code="import asyncio\n# define and run coroutine\n",
    solution_code=(
        "import asyncio\n\n"
        "async def hello():\n"
        "    print('hello async')\n\n"
        "asyncio.run(hello())"
    ),
    expected_output="hello async",
    tags=["python", "asyncio", "coroutine"],
)
add_question(
    topic_slug="async",
    title="Await Sleep",
    slug="py-async-await-sleep",
    difficulty="basic",
    task="Await `asyncio.sleep(0)` inside a coroutine, then print `done`.",
    starter_code="import asyncio\n# await sleep and print done\n",
    solution_code=(
        "import asyncio\n\n"
        "async def main():\n"
        "    await asyncio.sleep(0)\n"
        "    print('done')\n\n"
        "asyncio.run(main())"
    ),
    expected_output="done",
    tags=["python", "asyncio", "await"],
)
add_question(
    topic_slug="async",
    title="Gather Two Values",
    slug="py-async-gather-two",
    difficulty="basic",
    task="Run two coroutines returning `2` and `3` with `gather`, then print their sum.",
    starter_code="import asyncio\n# gather two coroutines\n",
    solution_code=(
        "import asyncio\n\n"
        "async def a():\n"
        "    return 2\n\n"
        "async def b():\n"
        "    return 3\n\n"
        "async def main():\n"
        "    x, y = await asyncio.gather(a(), b())\n"
        "    print(x + y)\n\n"
        "asyncio.run(main())"
    ),
    expected_output="5",
    tags=["python", "asyncio", "gather"],
)
add_question(
    topic_slug="async",
    title="Create Task and Await",
    slug="py-async-create-task",
    difficulty="basic",
    task="Create a task returning `7`, await it, and print result.",
    starter_code="import asyncio\n# create_task and await\n",
    solution_code=(
        "import asyncio\n\n"
        "async def worker():\n"
        "    return 7\n\n"
        "async def main():\n"
        "    task = asyncio.create_task(worker())\n"
        "    print(await task)\n\n"
        "asyncio.run(main())"
    ),
    expected_output="7",
    tags=["python", "asyncio", "task"],
)
add_question(
    topic_slug="async",
    title="Async Function Parameters",
    slug="py-async-params",
    difficulty="basic",
    task="Create coroutine `add(a, b)` and print result of awaiting `add(4, 5)`.",
    starter_code="import asyncio\n# async add\n",
    solution_code=(
        "import asyncio\n\n"
        "async def add(a, b):\n"
        "    return a + b\n\n"
        "async def main():\n"
        "    print(await add(4, 5))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="9",
    tags=["python", "asyncio", "coroutine"],
)
add_question(
    topic_slug="async",
    title="Async Loop Sequential",
    slug="py-async-loop-sequential",
    difficulty="basic",
    task="Sequentially await three coroutines returning `1,2,3` and print total.",
    starter_code="import asyncio\n# sequential awaits\n",
    solution_code=(
        "import asyncio\n\n"
        "async def one(v):\n"
        "    return v\n\n"
        "async def main():\n"
        "    total = 0\n"
        "    for v in [1, 2, 3]:\n"
        "        total += await one(v)\n"
        "    print(total)\n\n"
        "asyncio.run(main())"
    ),
    expected_output="6",
    tags=["python", "asyncio", "await"],
)
add_question(
    topic_slug="async",
    title="Gather Preserves Order",
    slug="py-async-gather-order",
    difficulty="intermediate",
    task="Gather coroutines yielding `'A'`, `'B'`, `'C'` and print result list.",
    starter_code="import asyncio\n# gather and print ordered list\n",
    solution_code=(
        "import asyncio\n\n"
        "async def tag(v):\n"
        "    await asyncio.sleep(0)\n"
        "    return v\n\n"
        "async def main():\n"
        "    print(await asyncio.gather(tag('A'), tag('B'), tag('C')))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="['A', 'B', 'C']",
    tags=["python", "asyncio", "gather"],
)
add_question(
    topic_slug="async",
    title="wait_for Timeout Success",
    slug="py-async-wait-for-success",
    difficulty="intermediate",
    task="Use `asyncio.wait_for` with timeout 1 on quick coroutine returning `ok`. Print value.",
    starter_code="import asyncio\n# wait_for with enough timeout\n",
    solution_code=(
        "import asyncio\n\n"
        "async def quick():\n"
        "    await asyncio.sleep(0)\n"
        "    return 'ok'\n\n"
        "async def main():\n"
        "    print(await asyncio.wait_for(quick(), timeout=1))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="ok",
    tags=["python", "asyncio", "timeout"],
)
add_question(
    topic_slug="async",
    title="Handle TimeoutError",
    slug="py-async-timeout-error",
    difficulty="intermediate",
    task="Use `wait_for` with timeout 0 on sleeping coroutine and print `timeout` on exception.",
    starter_code="import asyncio\n# catch TimeoutError\n",
    solution_code=(
        "import asyncio\n\n"
        "async def slow():\n"
        "    await asyncio.sleep(0.01)\n\n"
        "async def main():\n"
        "    try:\n"
        "        await asyncio.wait_for(slow(), timeout=0)\n"
        "    except asyncio.TimeoutError:\n"
        "        print('timeout')\n\n"
        "asyncio.run(main())"
    ),
    expected_output="timeout",
    tags=["python", "asyncio", "timeout"],
    question_type="debug_model",
)
add_question(
    topic_slug="async",
    title="Task Cancellation",
    slug="py-async-task-cancel",
    difficulty="intermediate",
    task="Create a long task, cancel it, catch `CancelledError`, and print `cancelled`.",
    starter_code="import asyncio\n# cancel a task and handle error\n",
    solution_code=(
        "import asyncio\n\n"
        "async def worker():\n"
        "    await asyncio.sleep(1)\n\n"
        "async def main():\n"
        "    t = asyncio.create_task(worker())\n"
        "    t.cancel()\n"
        "    try:\n"
        "        await t\n"
        "    except asyncio.CancelledError:\n"
        "        print('cancelled')\n\n"
        "asyncio.run(main())"
    ),
    expected_output="cancelled",
    tags=["python", "asyncio", "cancellation"],
)
add_question(
    topic_slug="async",
    title="Async Context Manager",
    slug="py-async-context-manager",
    difficulty="intermediate",
    task="Create minimal async context manager that returns `42`; print value in `async with`.",
    starter_code="import asyncio\n# define async context manager class\n",
    solution_code=(
        "import asyncio\n\n"
        "class Resource:\n"
        "    async def __aenter__(self):\n"
        "        return 42\n"
        "    async def __aexit__(self, exc_type, exc, tb):\n"
        "        return False\n\n"
        "async def main():\n"
        "    async with Resource() as value:\n"
        "        print(value)\n\n"
        "asyncio.run(main())"
    ),
    expected_output="42",
    tags=["python", "asyncio", "context-manager"],
)
add_question(
    topic_slug="async",
    title="Async Iterator",
    slug="py-async-iterator",
    difficulty="intermediate",
    task="Build async iterator yielding `1,2,3` and print each value.",
    starter_code="import asyncio\n# implement __aiter__ and __anext__\n",
    solution_code=(
        "import asyncio\n\n"
        "class Counter:\n"
        "    def __init__(self):\n"
        "        self.n = 1\n"
        "    def __aiter__(self):\n"
        "        return self\n"
        "    async def __anext__(self):\n"
        "        if self.n > 3:\n"
        "            raise StopAsyncIteration\n"
        "        v = self.n\n"
        "        self.n += 1\n"
        "        return v\n\n"
        "async def main():\n"
        "    async for v in Counter():\n"
        "        print(v)\n\n"
        "asyncio.run(main())"
    ),
    expected_output="1\n2\n3",
    tags=["python", "asyncio", "async-iterator"],
)
add_question(
    topic_slug="async",
    title="as_completed Results",
    slug="py-async-as-completed",
    difficulty="intermediate",
    task="Use `asyncio.as_completed` for tasks returning 1..3 and print sorted collected list.",
    starter_code="import asyncio\n# use as_completed\n",
    solution_code=(
        "import asyncio\n\n"
        "async def f(v):\n"
        "    return v\n\n"
        "async def main():\n"
        "    tasks = [asyncio.create_task(f(v)) for v in [1, 2, 3]]\n"
        "    out = []\n"
        "    for t in asyncio.as_completed(tasks):\n"
        "        out.append(await t)\n"
        "    print(sorted(out))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="[1, 2, 3]",
    tags=["python", "asyncio", "tasks"],
)
add_question(
    topic_slug="async",
    title="Event Coordination",
    slug="py-async-event-coordination",
    difficulty="intermediate",
    task="Use `asyncio.Event` so waiter resumes after setter signals. Print `released`.",
    starter_code="import asyncio\n# coordinate with Event\n",
    solution_code=(
        "import asyncio\n\n"
        "async def main():\n"
        "    event = asyncio.Event()\n"
        "    out = []\n"
        "    async def waiter():\n"
        "        await event.wait()\n"
        "        out.append('released')\n"
        "    async def setter():\n"
        "        event.set()\n"
        "    await asyncio.gather(waiter(), setter())\n"
        "    print(out[0])\n\n"
        "asyncio.run(main())"
    ),
    expected_output="released",
    tags=["python", "asyncio", "event"],
)
add_question(
    topic_slug="async",
    title="Queue Producer Consumer Async",
    slug="py-async-queue-producer-consumer",
    difficulty="advanced",
    task="Use `asyncio.Queue` with producer values `2,4,6` and sentinel `None`; consumer prints sum.",
    starter_code="import asyncio\n# async producer consumer with Queue\n",
    solution_code=(
        "import asyncio\n\n"
        "async def producer(q):\n"
        "    for v in [2, 4, 6]:\n"
        "        await q.put(v)\n"
        "    await q.put(None)\n\n"
        "async def consumer(q):\n"
        "    total = 0\n"
        "    while True:\n"
        "        item = await q.get()\n"
        "        if item is None:\n"
        "            break\n"
        "        total += item\n"
        "    print(total)\n\n"
        "async def main():\n"
        "    q = asyncio.Queue()\n"
        "    await asyncio.gather(producer(q), consumer(q))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="12",
    tags=["python", "asyncio", "queue"],
)
add_question(
    topic_slug="async",
    title="Rate Limit with Semaphore",
    slug="py-async-semaphore-rate-limit",
    difficulty="advanced",
    task="Use `asyncio.Semaphore(2)` around four tasks and print count of completed tasks.",
    starter_code="import asyncio\n# guard tasks with semaphore\n",
    solution_code=(
        "import asyncio\n\n"
        "async def main():\n"
        "    sem = asyncio.Semaphore(2)\n"
        "    done = []\n"
        "    async def worker(v):\n"
        "        async with sem:\n"
        "            await asyncio.sleep(0)\n"
        "            done.append(v)\n"
        "    await asyncio.gather(*(worker(v) for v in [1, 2, 3, 4]))\n"
        "    print(len(done))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="4",
    tags=["python", "asyncio", "semaphore"],
)
add_question(
    topic_slug="async",
    title="run_in_executor",
    slug="py-async-run-in-executor",
    difficulty="advanced",
    task="Use `loop.run_in_executor` to compute `sum([1,2,3,4])` and print result.",
    starter_code="import asyncio\n# run cpu function in executor\n",
    solution_code=(
        "import asyncio\n\n"
        "def calc():\n"
        "    return sum([1, 2, 3, 4])\n\n"
        "async def main():\n"
        "    loop = asyncio.get_running_loop()\n"
        "    result = await loop.run_in_executor(None, calc)\n"
        "    print(result)\n\n"
        "asyncio.run(main())"
    ),
    expected_output="10",
    tags=["python", "asyncio", "executor"],
)
add_question(
    topic_slug="async",
    title="Shielded Task",
    slug="py-async-shield-task",
    difficulty="advanced",
    task="Wrap a quick task in `asyncio.shield` and print its result `ok`.",
    starter_code="import asyncio\n# shield a task\n",
    solution_code=(
        "import asyncio\n\n"
        "async def worker():\n"
        "    await asyncio.sleep(0)\n"
        "    return 'ok'\n\n"
        "async def main():\n"
        "    t = asyncio.create_task(worker())\n"
        "    print(await asyncio.shield(t))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="ok",
    tags=["python", "asyncio", "shield"],
)
add_question(
    topic_slug="async",
    title="asyncio.Lock Shared State",
    slug="py-async-lock-shared-state",
    difficulty="advanced",
    task="Protect shared counter with `asyncio.Lock` across 5 coroutines (200 increments each). Print counter.",
    starter_code="import asyncio\n# lock shared async state\n",
    solution_code=(
        "import asyncio\n\n"
        "async def main():\n"
        "    lock = asyncio.Lock()\n"
        "    counter = {'v': 0}\n"
        "    async def worker():\n"
        "        for _ in range(200):\n"
        "            async with lock:\n"
        "                counter['v'] += 1\n"
        "    await asyncio.gather(*(worker() for _ in range(5)))\n"
        "    print(counter['v'])\n\n"
        "asyncio.run(main())"
    ),
    expected_output="1000",
    tags=["python", "asyncio", "lock"],
)
add_question(
    topic_slug="async",
    title="TaskGroup Success Path",
    slug="py-async-taskgroup",
    difficulty="advanced",
    task="Use `asyncio.TaskGroup` to run tasks appending values 1..3, then print sorted list.",
    starter_code="import asyncio\n# use TaskGroup\n",
    solution_code=(
        "import asyncio\n\n"
        "async def main():\n"
        "    out = []\n"
        "    async def worker(v):\n"
        "        out.append(v)\n"
        "    async with asyncio.TaskGroup() as tg:\n"
        "        for v in [1, 2, 3]:\n"
        "            tg.create_task(worker(v))\n"
        "    print(sorted(out))\n\n"
        "asyncio.run(main())"
    ),
    expected_output="[1, 2, 3]",
    tags=["python", "asyncio", "taskgroup"],
)
add_question(
    topic_slug="async",
    title="Exception Handling in gather",
    slug="py-async-gather-exception",
    difficulty="advanced",
    task="Use `gather(..., return_exceptions=True)` for one successful and one failing coroutine; print exception type name.",
    starter_code="import asyncio\n# gather with return_exceptions\n",
    solution_code=(
        "import asyncio\n\n"
        "async def ok():\n"
        "    return 1\n\n"
        "async def bad():\n"
        "    raise ValueError('x')\n\n"
        "async def main():\n"
        "    r = await asyncio.gather(ok(), bad(), return_exceptions=True)\n"
        "    print(type(r[1]).__name__)\n\n"
        "asyncio.run(main())"
    ),
    expected_output="ValueError",
    tags=["python", "asyncio", "error-handling"],
)
add_question(
    topic_slug="async",
    title="Async Retry Loop",
    slug="py-async-retry-loop",
    difficulty="advanced",
    task="Retry a coroutine that fails once then succeeds, and print `2` attempts used.",
    starter_code="import asyncio\n# implement retry for flaky coroutine\n",
    solution_code=(
        "import asyncio\n\n"
        "async def main():\n"
        "    state = {'tries': 0}\n"
        "    async def flaky():\n"
        "        state['tries'] += 1\n"
        "        if state['tries'] == 1:\n"
        "            raise RuntimeError('retry')\n"
        "        return 'ok'\n"
        "    for _ in range(3):\n"
        "        try:\n"
        "            await flaky()\n"
        "            break\n"
        "        except RuntimeError:\n"
        "            pass\n"
        "    print(state['tries'])\n\n"
        "asyncio.run(main())"
    ),
    expected_output="2",
    tags=["python", "asyncio", "retry"],
    question_type="build_from_scratch",
)


# ---------------------------------------------------------------------------
# Module 23: Performance (22 = 6 basic, 8 intermediate, 8 advanced)
# ---------------------------------------------------------------------------
add_question(
    topic_slug="performance",
    title="timeit Simple Expression",
    slug="py-performance-timeit-basic",
    difficulty="basic",
    task="Use `timeit.timeit('1+1', number=1000)` and print whether the result is non-negative.",
    starter_code="import timeit\n# run timeit and print bool\n",
    solution_code="import timeit\nelapsed = timeit.timeit('1+1', number=1000)\nprint(elapsed >= 0)",
    expected_output="True",
    tags=["python", "performance", "timeit"],
)
add_question(
    topic_slug="performance",
    title="List Comprehension Count",
    slug="py-performance-list-comprehension",
    difficulty="basic",
    task="Build squares for 0..9 using list comprehension and print list length.",
    starter_code="# list comprehension for squares\n",
    solution_code="squares = [i * i for i in range(10)]\nprint(len(squares))",
    expected_output="10",
    tags=["python", "performance", "comprehension"],
)
add_question(
    topic_slug="performance",
    title="Set Membership Speed Idea",
    slug="py-performance-set-membership",
    difficulty="basic",
    task="Create a set from `[1,2,3]` and print result of `2 in set_obj`.",
    starter_code="# set membership check\n",
    solution_code="set_obj = {1, 2, 3}\nprint(2 in set_obj)",
    expected_output="True",
    tags=["python", "performance", "set"],
)
add_question(
    topic_slug="performance",
    title="String Join",
    slug="py-performance-string-join",
    difficulty="basic",
    task="Join `['a', 'b', 'c']` with empty separator and print result.",
    starter_code="# join strings\n",
    solution_code="parts = ['a', 'b', 'c']\nprint(''.join(parts))",
    expected_output="abc",
    tags=["python", "performance", "strings"],
)
add_question(
    topic_slug="performance",
    title="Enumerate Instead of Range Index",
    slug="py-performance-enumerate",
    difficulty="basic",
    task="Use `enumerate(['x','y'])` and print number of produced pairs.",
    starter_code="# enumerate list\n",
    solution_code="pairs = list(enumerate(['x', 'y']))\nprint(len(pairs))",
    expected_output="2",
    tags=["python", "performance", "enumerate"],
)
add_question(
    topic_slug="performance",
    title="Avoid Repeated Attribute Lookup",
    slug="py-performance-local-binding",
    difficulty="basic",
    task="Bind `append = out.append`, append three values, print list length.",
    starter_code="out = []\n# bind append locally\n",
    solution_code="out = []\nappend = out.append\nappend(1)\nappend(2)\nappend(3)\nprint(len(out))",
    expected_output="3",
    tags=["python", "performance", "micro-optimization"],
)
add_question(
    topic_slug="performance",
    title="Profile Function with cProfile",
    slug="py-performance-cprofile",
    difficulty="intermediate",
    task="Profile a small function with `cProfile.Profile`; print whether total calls > 0.",
    starter_code="import cProfile\n# run profile and inspect stats object\n",
    solution_code=(
        "import cProfile\n\n"
        "def f():\n"
        "    return sum(range(10))\n\n"
        "prof = cProfile.Profile()\n"
        "prof.enable()\n"
        "f()\n"
        "prof.disable()\n"
        "stats = prof.getstats()\n"
        "print(len(stats) > 0)"
    ),
    expected_output="True",
    tags=["python", "performance", "profiling"],
)
add_question(
    topic_slug="performance",
    title="functools.lru_cache",
    slug="py-performance-lru-cache",
    difficulty="intermediate",
    task="Cache Fibonacci with `@lru_cache(maxsize=None)` and print `fib(10)`.",
    starter_code="from functools import lru_cache\n# cache fibonacci\n",
    solution_code=(
        "from functools import lru_cache\n\n"
        "@lru_cache(maxsize=None)\n"
        "def fib(n):\n"
        "    if n < 2:\n"
        "        return n\n"
        "    return fib(n - 1) + fib(n - 2)\n\n"
        "print(fib(10))"
    ),
    expected_output="55",
    tags=["python", "performance", "caching"],
)
add_question(
    topic_slug="performance",
    title="Generator Memory Friendly",
    slug="py-performance-generator-sum",
    difficulty="intermediate",
    task="Use generator expression to sum squares of `0..4` and print result.",
    starter_code="# sum generator expression\n",
    solution_code="print(sum(i * i for i in range(5)))",
    expected_output="30",
    tags=["python", "performance", "generator"],
)
add_question(
    topic_slug="performance",
    title="List vs Tuple Size",
    slug="py-performance-list-tuple-size",
    difficulty="intermediate",
    task="Use `sys.getsizeof` to compare `[1,2,3]` and `(1,2,3)`. Print whether tuple is smaller or equal.",
    starter_code="import sys\n# compare memory size\n",
    solution_code="import sys\nprint(sys.getsizeof((1, 2, 3)) <= sys.getsizeof([1, 2, 3]))",
    expected_output="True",
    tags=["python", "performance", "memory"],
)
add_question(
    topic_slug="performance",
    title="Batching with islice",
    slug="py-performance-islice-batch",
    difficulty="intermediate",
    task="Use `itertools.islice` to take first 3 numbers from range(10) and print list.",
    starter_code="import itertools\n# use islice\n",
    solution_code="import itertools\nprint(list(itertools.islice(range(10), 3)))",
    expected_output="[0, 1, 2]",
    tags=["python", "performance", "itertools"],
)
add_question(
    topic_slug="performance",
    title="Avoid O(n) in Loop",
    slug="py-performance-precompute-set",
    difficulty="intermediate",
    task="Convert list `[1,2,3,4]` to set once, then count matches in `[2,4,6]`. Print count.",
    starter_code="# precompute set and count membership\n",
    solution_code="needles = [1, 2, 3, 4]\nlookup = set(needles)\nprint(sum(x in lookup for x in [2, 4, 6]))",
    expected_output="2",
    tags=["python", "performance", "algorithmic"],
)
add_question(
    topic_slug="performance",
    title="time.perf_counter Measurement",
    slug="py-performance-perf-counter",
    difficulty="intermediate",
    task="Measure elapsed time around quick operation and print if elapsed >= 0.",
    starter_code="import time\n# perf_counter measurement\n",
    solution_code="import time\nstart = time.perf_counter()\nsum(range(10))\nelapsed = time.perf_counter() - start\nprint(elapsed >= 0)",
    expected_output="True",
    tags=["python", "performance", "timing"],
)
add_question(
    topic_slug="performance",
    title="Numpy Vectorization Idea Without Numpy",
    slug="py-performance-vectorization-idea",
    difficulty="intermediate",
    task="Compute elementwise sum of two lists with zip and print result.",
    starter_code="a = [1,2,3]\nb = [4,5,6]\n# zip sum\n",
    solution_code="a = [1, 2, 3]\nb = [4, 5, 6]\nprint([x + y for x, y in zip(a, b)])",
    expected_output="[5, 7, 9]",
    tags=["python", "performance", "vectorization"],
)
add_question(
    topic_slug="performance",
    title="Memoization Dictionary",
    slug="py-performance-manual-memo",
    difficulty="advanced",
    task="Implement manual memoized factorial and print `fact(6)`.",
    starter_code="# manual memoization for factorial\n",
    solution_code=(
        "cache = {}\n\n"
        "def fact(n):\n"
        "    if n in cache:\n"
        "        return cache[n]\n"
        "    if n <= 1:\n"
        "        cache[n] = 1\n"
        "    else:\n"
        "        cache[n] = n * fact(n - 1)\n"
        "    return cache[n]\n\n"
        "print(fact(6))"
    ),
    expected_output="720",
    tags=["python", "performance", "memoization"],
)
add_question(
    topic_slug="performance",
    title="Bound Method in Loop",
    slug="py-performance-bound-method-loop",
    difficulty="advanced",
    task="Inside loop append 0..99 using bound method and print last value.",
    starter_code="out = []\n# append in loop efficiently\n",
    solution_code="out = []\nappend = out.append\nfor i in range(100):\n    append(i)\nprint(out[-1])",
    expected_output="99",
    tags=["python", "performance", "loops"],
)
add_question(
    topic_slug="performance",
    title="Heap Top K",
    slug="py-performance-heap-top-k",
    difficulty="advanced",
    task="Use `heapq.nlargest` to get top 2 from `[5,1,9,3]` and print list.",
    starter_code="import heapq\n# nlargest example\n",
    solution_code="import heapq\nprint(heapq.nlargest(2, [5, 1, 9, 3]))",
    expected_output="[9, 5]",
    tags=["python", "performance", "heapq"],
)
add_question(
    topic_slug="performance",
    title="Bisect Search Position",
    slug="py-performance-bisect",
    difficulty="advanced",
    task="Use `bisect_left` in sorted `[10,20,30,40]` for value `25` and print insertion index.",
    starter_code="import bisect\n# bisect_left index\n",
    solution_code="import bisect\nprint(bisect.bisect_left([10, 20, 30, 40], 25))",
    expected_output="2",
    tags=["python", "performance", "bisect"],
)
add_question(
    topic_slug="performance",
    title="Deque for Queue Operations",
    slug="py-performance-deque-queue",
    difficulty="advanced",
    task="Use `collections.deque` to pop left from `[1,2,3]` and print first popped value.",
    starter_code="from collections import deque\n# use popleft\n",
    solution_code="from collections import deque\nd = deque([1, 2, 3])\nprint(d.popleft())",
    expected_output="1",
    tags=["python", "performance", "deque"],
)
add_question(
    topic_slug="performance",
    title="Chunk Processing Generator",
    slug="py-performance-chunk-generator",
    difficulty="advanced",
    task="Create generator yielding chunks of size 2 from `[1,2,3,4,5]`; print first chunk.",
    starter_code="# chunk generator\n",
    solution_code=(
        "def chunks(seq, size):\n"
        "    for i in range(0, len(seq), size):\n"
        "        yield seq[i:i + size]\n\n"
        "gen = chunks([1, 2, 3, 4, 5], 2)\n"
        "print(next(gen))"
    ),
    expected_output="[1, 2]",
    tags=["python", "performance", "generator"],
)
add_question(
    topic_slug="performance",
    title="Avoid Quadratic String Concats",
    slug="py-performance-string-builder",
    difficulty="advanced",
    task="Build `'01234'` using list append + join and print result.",
    starter_code="# efficient string build\n",
    solution_code="parts = []\nfor i in range(5):\n    parts.append(str(i))\nprint(''.join(parts))",
    expected_output="01234",
    tags=["python", "performance", "strings"],
)
add_question(
    topic_slug="performance",
    title="Streaming File Lines Pattern",
    slug="py-performance-streaming-pattern",
    difficulty="advanced",
    task="Simulate streaming by iterating list of 3 lines and counting non-empty lines. Print count.",
    starter_code="lines = ['a', '', 'b', 'c']\n# count non-empty lines\n",
    solution_code="lines = ['a', '', 'b', 'c']\nprint(sum(1 for line in lines if line))",
    expected_output="3",
    tags=["python", "performance", "streaming"],
)


# ---------------------------------------------------------------------------
# Module 24: Design Patterns (22 = 6 basic, 8 intermediate, 8 advanced)
# ---------------------------------------------------------------------------
add_question(
    topic_slug="design-patterns",
    title="Simple Factory Function",
    slug="py-design-factory-basic",
    difficulty="basic",
    task="Write factory function returning `'json'` parser label when input is `'json'`. Print return value.",
    starter_code="# create parser_factory(kind)\n",
    solution_code=(
        "def parser_factory(kind):\n"
        "    if kind == 'json':\n"
        "        return 'json'\n"
        "    return 'unknown'\n\n"
        "print(parser_factory('json'))"
    ),
    expected_output="json",
    tags=["python", "design-patterns", "factory"],
)
add_question(
    topic_slug="design-patterns",
    title="Singleton with Class Attribute",
    slug="py-design-singleton-basic",
    difficulty="basic",
    task="Implement basic singleton via classmethod `instance()`. Print whether two calls are same object.",
    starter_code="# singleton class with instance()\n",
    solution_code=(
        "class Config:\n"
        "    _inst = None\n\n"
        "    @classmethod\n"
        "    def instance(cls):\n"
        "        if cls._inst is None:\n"
        "            cls._inst = cls()\n"
        "        return cls._inst\n\n"
        "print(Config.instance() is Config.instance())"
    ),
    expected_output="True",
    tags=["python", "design-patterns", "singleton"],
)
add_question(
    topic_slug="design-patterns",
    title="Strategy as Function",
    slug="py-design-strategy-function",
    difficulty="basic",
    task="Apply strategy function `double` to value 5 and print result.",
    starter_code="# strategy function example\n",
    solution_code="def double(x):\n    return x * 2\n\nprint(double(5))",
    expected_output="10",
    tags=["python", "design-patterns", "strategy"],
)
add_question(
    topic_slug="design-patterns",
    title="Adapter Method Name",
    slug="py-design-adapter-basic",
    difficulty="basic",
    task="Create adapter exposing `request()` that delegates to `specific_request()` and print adapted text.",
    starter_code="# adapter class\n",
    solution_code=(
        "class Legacy:\n"
        "    def specific_request(self):\n"
        "        return 'legacy'\n\n"
        "class Adapter:\n"
        "    def __init__(self, adaptee):\n"
        "        self.adaptee = adaptee\n"
        "    def request(self):\n"
        "        return self.adaptee.specific_request()\n\n"
        "print(Adapter(Legacy()).request())"
    ),
    expected_output="legacy",
    tags=["python", "design-patterns", "adapter"],
)
add_question(
    topic_slug="design-patterns",
    title="Observer Listeners",
    slug="py-design-observer-basic",
    difficulty="basic",
    task="Notify two listeners appending to list and print number of notifications recorded.",
    starter_code="# simple observer notify\n",
    solution_code=(
        "listeners = []\nout = []\n\n"
        "def subscribe(fn):\n"
        "    listeners.append(fn)\n\n"
        "def notify(msg):\n"
        "    for fn in listeners:\n"
        "        fn(msg)\n\n"
        "subscribe(lambda m: out.append(m))\n"
        "subscribe(lambda m: out.append(m))\n"
        "notify('ok')\n"
        "print(len(out))"
    ),
    expected_output="2",
    tags=["python", "design-patterns", "observer"],
)
add_question(
    topic_slug="design-patterns",
    title="Builder Pattern Basics",
    slug="py-design-builder-basic",
    difficulty="basic",
    task="Build dict object with chained builder methods and print final `port` value.",
    starter_code="# basic builder class\n",
    solution_code=(
        "class ConfigBuilder:\n"
        "    def __init__(self):\n"
        "        self.cfg = {}\n"
        "    def host(self, h):\n"
        "        self.cfg['host'] = h\n"
        "        return self\n"
        "    def port(self, p):\n"
        "        self.cfg['port'] = p\n"
        "        return self\n"
        "    def build(self):\n"
        "        return self.cfg\n\n"
        "cfg = ConfigBuilder().host('localhost').port(5432).build()\n"
        "print(cfg['port'])"
    ),
    expected_output="5432",
    tags=["python", "design-patterns", "builder"],
)
add_question(
    topic_slug="design-patterns",
    title="Factory with Classes",
    slug="py-design-factory-classes",
    difficulty="intermediate",
    task="Factory returns class instances `CsvParser` or `JsonParser`. Print selected class name for `'csv'`.",
    starter_code="# class-based factory\n",
    solution_code=(
        "class CsvParser:\n"
        "    pass\n\n"
        "class JsonParser:\n"
        "    pass\n\n"
        "def make_parser(kind):\n"
        "    return CsvParser() if kind == 'csv' else JsonParser()\n\n"
        "print(type(make_parser('csv')).__name__)"
    ),
    expected_output="CsvParser",
    tags=["python", "design-patterns", "factory"],
)
add_question(
    topic_slug="design-patterns",
    title="Strategy Object Swap",
    slug="py-design-strategy-object",
    difficulty="intermediate",
    task="Create context object that can swap strategy from add to multiply. Print result for multiply with 3 and 4.",
    starter_code="# context with swappable strategy\n",
    solution_code=(
        "class Add:\n"
        "    def run(self, a, b):\n"
        "        return a + b\n\n"
        "class Mul:\n"
        "    def run(self, a, b):\n"
        "        return a * b\n\n"
        "class Context:\n"
        "    def __init__(self, strat):\n"
        "        self.strat = strat\n"
        "    def set_strategy(self, strat):\n"
        "        self.strat = strat\n"
        "    def execute(self, a, b):\n"
        "        return self.strat.run(a, b)\n\n"
        "ctx = Context(Add())\n"
        "ctx.set_strategy(Mul())\n"
        "print(ctx.execute(3, 4))"
    ),
    expected_output="12",
    tags=["python", "design-patterns", "strategy"],
)
add_question(
    topic_slug="design-patterns",
    title="Decorator Wrapper",
    slug="py-design-decorator-wrapper",
    difficulty="intermediate",
    task="Write decorator that adds 1 to wrapped function result. Print wrapped return for function returning 9.",
    starter_code="# decorator that adjusts result\n",
    solution_code=(
        "def plus_one(fn):\n"
        "    def inner():\n"
        "        return fn() + 1\n"
        "    return inner\n\n"
        "@plus_one\n"
        "def base():\n"
        "    return 9\n\n"
        "print(base())"
    ),
    expected_output="10",
    tags=["python", "design-patterns", "decorator"],
)
add_question(
    topic_slug="design-patterns",
    title="Observer Unsubscribe",
    slug="py-design-observer-unsubscribe",
    difficulty="intermediate",
    task="Implement subscribe/unsubscribe and show only one listener receives message. Print notification count.",
    starter_code="# observer with unsubscribe\n",
    solution_code=(
        "subs = []\nout = []\n\n"
        "def subscribe(fn):\n"
        "    subs.append(fn)\n\n"
        "def unsubscribe(fn):\n"
        "    subs.remove(fn)\n\n"
        "def notify(msg):\n"
        "    for fn in subs:\n"
        "        fn(msg)\n\n"
        "def a(msg):\n"
        "    out.append(msg)\n\n"
        "def b(msg):\n"
        "    out.append(msg)\n\n"
        "subscribe(a)\n"
        "subscribe(b)\n"
        "unsubscribe(b)\n"
        "notify('x')\n"
        "print(len(out))"
    ),
    expected_output="1",
    tags=["python", "design-patterns", "observer"],
)
add_question(
    topic_slug="design-patterns",
    title="Command Pattern Execute",
    slug="py-design-command-execute",
    difficulty="intermediate",
    task="Create `Command` object with `execute` method that appends to log. Print log length after one execute.",
    starter_code="# command pattern mini example\n",
    solution_code=(
        "class Command:\n"
        "    def __init__(self, action):\n"
        "        self.action = action\n"
        "    def execute(self):\n"
        "        self.action()\n\n"
        "log = []\n"
        "cmd = Command(lambda: log.append('done'))\n"
        "cmd.execute()\n"
        "print(len(log))"
    ),
    expected_output="1",
    tags=["python", "design-patterns", "command"],
)
add_question(
    topic_slug="design-patterns",
    title="State Pattern Transition",
    slug="py-design-state-transition",
    difficulty="intermediate",
    task="Create simple state machine from `idle` to `running` and print final state.",
    starter_code="# state transition\n",
    solution_code=(
        "class Machine:\n"
        "    def __init__(self):\n"
        "        self.state = 'idle'\n"
        "    def start(self):\n"
        "        self.state = 'running'\n\n"
        "m = Machine()\n"
        "m.start()\n"
        "print(m.state)"
    ),
    expected_output="running",
    tags=["python", "design-patterns", "state"],
)
add_question(
    topic_slug="design-patterns",
    title="Facade Pattern",
    slug="py-design-facade",
    difficulty="intermediate",
    task="Build facade method `run()` that calls two subsystem methods and returns combined string. Print it.",
    starter_code="# facade wrapping subsystem calls\n",
    solution_code=(
        "class A:\n"
        "    def do(self):\n"
        "        return 'A'\n\n"
        "class B:\n"
        "    def do(self):\n"
        "        return 'B'\n\n"
        "class Facade:\n"
        "    def __init__(self):\n"
        "        self.a = A()\n"
        "        self.b = B()\n"
        "    def run(self):\n"
        "        return self.a.do() + self.b.do()\n\n"
        "print(Facade().run())"
    ),
    expected_output="AB",
    tags=["python", "design-patterns", "facade"],
)
add_question(
    topic_slug="design-patterns",
    title="Mediator for Components",
    slug="py-design-mediator-basic-flow",
    difficulty="intermediate",
    task="Implement mediator relaying `ping` from component A to B and print relayed message.",
    starter_code="# mediator wiring between components\n",
    solution_code=(
        "class Mediator:\n"
        "    def __init__(self):\n"
        "        self.b = None\n"
        "    def send(self, msg):\n"
        "        return self.b.receive(msg)\n\n"
        "class ComponentB:\n"
        "    def receive(self, msg):\n"
        "        return msg + '-ok'\n\n"
        "m = Mediator()\n"
        "m.b = ComponentB()\n"
        "print(m.send('ping'))"
    ),
    expected_output="ping-ok",
    tags=["python", "design-patterns", "mediator"],
)
add_question(
    topic_slug="design-patterns",
    title="Proxy Access Check",
    slug="py-design-proxy-access",
    difficulty="advanced",
    task="Create proxy that allows access only when token equals `'ok'`. Print result for valid token.",
    starter_code="# proxy with access check\n",
    solution_code=(
        "class Service:\n"
        "    def fetch(self):\n"
        "        return 'data'\n\n"
        "class Proxy:\n"
        "    def __init__(self, service):\n"
        "        self.service = service\n"
        "    def fetch(self, token):\n"
        "        if token != 'ok':\n"
        "            return 'denied'\n"
        "        return self.service.fetch()\n\n"
        "print(Proxy(Service()).fetch('ok'))"
    ),
    expected_output="data",
    tags=["python", "design-patterns", "proxy"],
)
add_question(
    topic_slug="design-patterns",
    title="Template Method",
    slug="py-design-template-method",
    difficulty="advanced",
    task="Implement template method `run()` that calls two hooks and print combined output.",
    starter_code="# template method base class\n",
    solution_code=(
        "class Base:\n"
        "    def run(self):\n"
        "        return self.step1() + self.step2()\n"
        "    def step1(self):\n"
        "        raise NotImplementedError\n"
        "    def step2(self):\n"
        "        raise NotImplementedError\n\n"
        "class Impl(Base):\n"
        "    def step1(self):\n"
        "        return 'X'\n"
        "    def step2(self):\n"
        "        return 'Y'\n\n"
        "print(Impl().run())"
    ),
    expected_output="XY",
    tags=["python", "design-patterns", "template-method"],
)
add_question(
    topic_slug="design-patterns",
    title="Chain of Responsibility",
    slug="py-design-chain-responsibility",
    difficulty="advanced",
    task="Build two handlers where first passes and second handles request. Print handler response.",
    starter_code="# chain of responsibility\n",
    solution_code=(
        "class Handler:\n"
        "    def __init__(self, nxt=None):\n"
        "        self.nxt = nxt\n"
        "    def handle(self, req):\n"
        "        if self.nxt:\n"
        "            return self.nxt.handle(req)\n"
        "        return 'unhandled'\n\n"
        "class Second(Handler):\n"
        "    def handle(self, req):\n"
        "        if req == 'ping':\n"
        "            return 'pong'\n"
        "        return super().handle(req)\n\n"
        "h = Handler(Second())\n"
        "print(h.handle('ping'))"
    ),
    expected_output="pong",
    tags=["python", "design-patterns", "chain-of-responsibility"],
)
add_question(
    topic_slug="design-patterns",
    title="Composite Pattern Sum",
    slug="py-design-composite-sum",
    difficulty="advanced",
    task="Implement leaf/composite where composite sums child values `[3,4]`. Print result.",
    starter_code="# composite pattern\n",
    solution_code=(
        "class Leaf:\n"
        "    def __init__(self, v):\n"
        "        self.v = v\n"
        "    def total(self):\n"
        "        return self.v\n\n"
        "class Composite:\n"
        "    def __init__(self, children):\n"
        "        self.children = children\n"
        "    def total(self):\n"
        "        return sum(c.total() for c in self.children)\n\n"
        "print(Composite([Leaf(3), Leaf(4)]).total())"
    ),
    expected_output="7",
    tags=["python", "design-patterns", "composite"],
)
add_question(
    topic_slug="design-patterns",
    title="Flyweight Cache",
    slug="py-design-flyweight-cache",
    difficulty="advanced",
    task="Cache flyweight objects by key and print whether requesting same key returns identical object.",
    starter_code="# flyweight cache\n",
    solution_code=(
        "class FlyweightFactory:\n"
        "    def __init__(self):\n"
        "        self.cache = {}\n"
        "    def get(self, key):\n"
        "        if key not in self.cache:\n"
        "            self.cache[key] = {'key': key}\n"
        "        return self.cache[key]\n\n"
        "f = FlyweightFactory()\n"
        "print(f.get('x') is f.get('x'))"
    ),
    expected_output="True",
    tags=["python", "design-patterns", "flyweight"],
)
add_question(
    topic_slug="design-patterns",
    title="Dependency Injection",
    slug="py-design-dependency-injection",
    difficulty="advanced",
    task="Inject logger dependency into service and print logged message count after one call.",
    starter_code="# dependency injection example\n",
    solution_code=(
        "class Logger:\n"
        "    def __init__(self):\n"
        "        self.msgs = []\n"
        "    def log(self, msg):\n"
        "        self.msgs.append(msg)\n\n"
        "class Service:\n"
        "    def __init__(self, logger):\n"
        "        self.logger = logger\n"
        "    def run(self):\n"
        "        self.logger.log('ran')\n\n"
        "logger = Logger()\n"
        "Service(logger).run()\n"
        "print(len(logger.msgs))"
    ),
    expected_output="1",
    tags=["python", "design-patterns", "dependency-injection"],
)
add_question(
    topic_slug="design-patterns",
    title="Repository Pattern In Memory",
    slug="py-design-repository-memory",
    difficulty="advanced",
    task="Create in-memory repository with add/get and print value for key `'u1'`.",
    starter_code="# repository pattern\n",
    solution_code=(
        "class Repo:\n"
        "    def __init__(self):\n"
        "        self.db = {}\n"
        "    def add(self, key, value):\n"
        "        self.db[key] = value\n"
        "    def get(self, key):\n"
        "        return self.db[key]\n\n"
        "r = Repo()\n"
        "r.add('u1', 'alice')\n"
        "print(r.get('u1'))"
    ),
    expected_output="alice",
    tags=["python", "design-patterns", "repository"],
)
add_question(
    topic_slug="design-patterns",
    title="Event Bus Pattern",
    slug="py-design-event-bus",
    difficulty="advanced",
    task="Implement tiny event bus publish/subscribe and print how many handlers run for one event.",
    starter_code="# event bus\n",
    solution_code=(
        "class Bus:\n"
        "    def __init__(self):\n"
        "        self.subs = {}\n"
        "    def on(self, event, fn):\n"
        "        self.subs.setdefault(event, []).append(fn)\n"
        "    def emit(self, event, data):\n"
        "        for fn in self.subs.get(event, []):\n"
        "            fn(data)\n\n"
        "bus = Bus()\n"
        "out = []\n"
        "bus.on('saved', lambda d: out.append(d))\n"
        "bus.emit('saved', 1)\n"
        "print(len(out))"
    ),
    expected_output="1",
    tags=["python", "design-patterns", "event-bus"],
    question_type="build_from_scratch",
)


# ---------------------------------------------------------------------------
# Module 25: Data Scripting (26 = 8 basic, 10 intermediate, 8 advanced)
# ---------------------------------------------------------------------------
add_question(
    topic_slug="data-scripting",
    title="Read CSV with DictReader",
    slug="py-data-scripting-csv-dictreader",
    difficulty="basic",
    task="Use `csv.DictReader` over in-memory CSV with two rows and print number of rows.",
    starter_code="import csv\nfrom io import StringIO\n# parse csv rows\n",
    solution_code=(
        "import csv\nfrom io import StringIO\n\n"
        "data = 'name,age\\nAna,30\\nBen,25\\n'\n"
        "rows = list(csv.DictReader(StringIO(data)))\n"
        "print(len(rows))"
    ),
    expected_output="2",
    tags=["python", "data-scripting", "csv"],
)
add_question(
    topic_slug="data-scripting",
    title="Write CSV Row",
    slug="py-data-scripting-csv-writer",
    difficulty="basic",
    task="Write one CSV row `['x', '1']` to `StringIO` and print whether output contains `x,1`.",
    starter_code="import csv\nfrom io import StringIO\n# write csv and inspect string\n",
    solution_code=(
        "import csv\nfrom io import StringIO\n\n"
        "buf = StringIO()\n"
        "w = csv.writer(buf)\n"
        "w.writerow(['x', '1'])\n"
        "print('x,1' in buf.getvalue())"
    ),
    expected_output="True",
    tags=["python", "data-scripting", "csv"],
)
add_question(
    topic_slug="data-scripting",
    title="Parse JSON String",
    slug="py-data-scripting-json-loads",
    difficulty="basic",
    task="Parse JSON string `{\"a\": 5}` and print value of key `a`.",
    starter_code="import json\n# parse json\n",
    solution_code="import json\nobj = json.loads('{\"a\": 5}')\nprint(obj['a'])",
    expected_output="5",
    tags=["python", "data-scripting", "json"],
)
add_question(
    topic_slug="data-scripting",
    title="Dump JSON Compact",
    slug="py-data-scripting-json-dumps",
    difficulty="basic",
    task="Dump dict `{'x': 1}` to JSON and print whether output starts with `{`.",
    starter_code="import json\n# dumps and inspect\n",
    solution_code="import json\ns = json.dumps({'x': 1})\nprint(s.startswith('{'))",
    expected_output="True",
    tags=["python", "data-scripting", "json"],
)
add_question(
    topic_slug="data-scripting",
    title="Count Lines in Text",
    slug="py-data-scripting-count-lines",
    difficulty="basic",
    task="Given `'a\\nb\\nc\\n'`, count non-empty lines and print count.",
    starter_code="text = 'a\\nb\\nc\\n'\n# count lines\n",
    solution_code="text = 'a\\nb\\nc\\n'\nprint(sum(1 for line in text.splitlines() if line))",
    expected_output="3",
    tags=["python", "data-scripting", "text-processing"],
)
add_question(
    topic_slug="data-scripting",
    title="Filter Numeric Strings",
    slug="py-data-scripting-filter-digits",
    difficulty="basic",
    task="From `['1','x','3']`, keep digit strings and print result list.",
    starter_code="vals = ['1', 'x', '3']\n# filter digits\n",
    solution_code="vals = ['1', 'x', '3']\nprint([v for v in vals if v.isdigit()])",
    expected_output="['1', '3']",
    tags=["python", "data-scripting", "cleaning"],
)
add_question(
    topic_slug="data-scripting",
    title="Sum Column Values",
    slug="py-data-scripting-sum-column",
    difficulty="basic",
    task="Given row dicts with key `qty`, sum quantities and print total.",
    starter_code="rows = [{'qty': 2}, {'qty': 5}, {'qty': 3}]\n# sum qty\n",
    solution_code="rows = [{'qty': 2}, {'qty': 5}, {'qty': 3}]\nprint(sum(r['qty'] for r in rows))",
    expected_output="10",
    tags=["python", "data-scripting", "aggregation"],
)
add_question(
    topic_slug="data-scripting",
    title="Basic Regex Extract",
    slug="py-data-scripting-regex-extract",
    difficulty="basic",
    task="Use regex to extract all numbers from `'id=7 qty=12'` and print list.",
    starter_code="import re\n# extract numbers\n",
    solution_code="import re\nprint(re.findall(r'\\d+', 'id=7 qty=12'))",
    expected_output="['7', '12']",
    tags=["python", "data-scripting", "regex"],
)
add_question(
    topic_slug="data-scripting",
    title="Group By Key",
    slug="py-data-scripting-groupby-dict",
    difficulty="intermediate",
    task="Group records by `dept` using dict and print count for `eng`.",
    starter_code="rows = [{'dept': 'eng'}, {'dept': 'sales'}, {'dept': 'eng'}]\n# group by dept\n",
    solution_code=(
        "rows = [{'dept': 'eng'}, {'dept': 'sales'}, {'dept': 'eng'}]\n"
        "grouped = {}\n"
        "for r in rows:\n"
        "    grouped.setdefault(r['dept'], []).append(r)\n"
        "print(len(grouped['eng']))"
    ),
    expected_output="2",
    tags=["python", "data-scripting", "grouping"],
)
add_question(
    topic_slug="data-scripting",
    title="Sort Records by Field",
    slug="py-data-scripting-sort-records",
    difficulty="intermediate",
    task="Sort records by `score` descending and print top name.",
    starter_code="rows = [{'name':'a','score':3}, {'name':'b','score':7}]\n# sort by score desc\n",
    solution_code=(
        "rows = [{'name': 'a', 'score': 3}, {'name': 'b', 'score': 7}]\n"
        "rows.sort(key=lambda r: r['score'], reverse=True)\n"
        "print(rows[0]['name'])"
    ),
    expected_output="b",
    tags=["python", "data-scripting", "sorting"],
)
add_question(
    topic_slug="data-scripting",
    title="Normalize Whitespace",
    slug="py-data-scripting-normalize-whitespace",
    difficulty="intermediate",
    task="Normalize `'  data   science  '` to single spaces and print result.",
    starter_code="s = '  data   science  '\n# normalize spaces\n",
    solution_code="s = '  data   science  '\nprint(' '.join(s.split()))",
    expected_output="data science",
    tags=["python", "data-scripting", "cleaning"],
)
add_question(
    topic_slug="data-scripting",
    title="Deduplicate While Preserving Order",
    slug="py-data-scripting-dedup-order",
    difficulty="intermediate",
    task="Deduplicate `[1,2,1,3,2]` preserving first occurrence order and print result.",
    starter_code="vals = [1,2,1,3,2]\n# deduplicate preserving order\n",
    solution_code=(
        "vals = [1, 2, 1, 3, 2]\n"
        "seen = set()\n"
        "out = []\n"
        "for v in vals:\n"
        "    if v not in seen:\n"
        "        seen.add(v)\n"
        "        out.append(v)\n"
        "print(out)"
    ),
    expected_output="[1, 2, 3]",
    tags=["python", "data-scripting", "deduplication"],
)
add_question(
    topic_slug="data-scripting",
    title="Pivot Counts",
    slug="py-data-scripting-pivot-counts",
    difficulty="intermediate",
    task="Build frequency table for `['a','b','a','a']` and print count for `a`.",
    starter_code="vals = ['a','b','a','a']\n# frequency counts\n",
    solution_code=(
        "vals = ['a', 'b', 'a', 'a']\n"
        "freq = {}\n"
        "for v in vals:\n"
        "    freq[v] = freq.get(v, 0) + 1\n"
        "print(freq['a'])"
    ),
    expected_output="3",
    tags=["python", "data-scripting", "aggregation"],
)
add_question(
    topic_slug="data-scripting",
    title="Merge Two Dict Lists by Key",
    slug="py-data-scripting-merge-by-id",
    difficulty="intermediate",
    task="Merge users and scores by `id` and print score of id 2.",
    starter_code="users = [{'id':1},{'id':2}]\nscores = {1:80,2:95}\n# merge score into users\n",
    solution_code=(
        "users = [{'id': 1}, {'id': 2}]\n"
        "scores = {1: 80, 2: 95}\n"
        "merged = [{**u, 'score': scores[u['id']]} for u in users]\n"
        "print(merged[1]['score'])"
    ),
    expected_output="95",
    tags=["python", "data-scripting", "join"],
)
add_question(
    topic_slug="data-scripting",
    title="CSV to JSON Records",
    slug="py-data-scripting-csv-to-json",
    difficulty="intermediate",
    task="Convert two-row CSV to list of dicts and print JSON array length.",
    starter_code="import csv, json\nfrom io import StringIO\n# csv to json records\n",
    solution_code=(
        "import csv, json\nfrom io import StringIO\n\n"
        "data = 'id,name\\n1,A\\n2,B\\n'\n"
        "rows = list(csv.DictReader(StringIO(data)))\n"
        "json_text = json.dumps(rows)\n"
        "print(len(json.loads(json_text)))"
    ),
    expected_output="2",
    tags=["python", "data-scripting", "csv", "json"],
)
add_question(
    topic_slug="data-scripting",
    title="Parse Date Field",
    slug="py-data-scripting-parse-date",
    difficulty="intermediate",
    task="Parse `2026-06-01` with `datetime.strptime` and print month number.",
    starter_code="from datetime import datetime\n# parse date\n",
    solution_code="from datetime import datetime\nd = datetime.strptime('2026-06-01', '%Y-%m-%d')\nprint(d.month)",
    expected_output="6",
    tags=["python", "data-scripting", "datetime"],
)
add_question(
    topic_slug="data-scripting",
    title="Validate Required Keys",
    slug="py-data-scripting-required-keys",
    difficulty="intermediate",
    task="Check all records contain keys `id` and `name`; print boolean result.",
    starter_code="rows = [{'id':1,'name':'a'},{'id':2,'name':'b'}]\n# validate keys\n",
    solution_code=(
        "rows = [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'b'}]\n"
        "required = {'id', 'name'}\n"
        "print(all(required.issubset(r.keys()) for r in rows))"
    ),
    expected_output="True",
    tags=["python", "data-scripting", "validation"],
)
add_question(
    topic_slug="data-scripting",
    title="Chunk Rows for Batching",
    slug="py-data-scripting-chunk-batch",
    difficulty="intermediate",
    task="Split `[1,2,3,4,5]` into chunks of 2 and print number of chunks.",
    starter_code="vals = [1,2,3,4,5]\n# chunk into batches\n",
    solution_code=(
        "vals = [1, 2, 3, 4, 5]\n"
        "chunks = [vals[i:i + 2] for i in range(0, len(vals), 2)]\n"
        "print(len(chunks))"
    ),
    expected_output="3",
    tags=["python", "data-scripting", "batching"],
)
add_question(
    topic_slug="data-scripting",
    title="Streaming Aggregation",
    slug="py-data-scripting-streaming-aggregation",
    difficulty="advanced",
    task="Aggregate running sum over iterator `[5,10,15]` and print final total.",
    starter_code="vals = iter([5,10,15])\n# streaming sum\n",
    solution_code="vals = iter([5, 10, 15])\ntotal = 0\nfor v in vals:\n    total += v\nprint(total)",
    expected_output="30",
    tags=["python", "data-scripting", "streaming"],
)
add_question(
    topic_slug="data-scripting",
    title="Robust JSON Parsing",
    slug="py-data-scripting-robust-json",
    difficulty="advanced",
    task="Try parsing invalid JSON and print `invalid` when `JSONDecodeError` occurs.",
    starter_code="import json\n# robust parse with exception handling\n",
    solution_code=(
        "import json\n\n"
        "try:\n"
        "    json.loads('{bad json}')\n"
        "except json.JSONDecodeError:\n"
        "    print('invalid')"
    ),
    expected_output="invalid",
    tags=["python", "data-scripting", "json", "error-handling"],
)
add_question(
    topic_slug="data-scripting",
    title="Schema Coercion",
    slug="py-data-scripting-schema-coercion",
    difficulty="advanced",
    task="Convert `{'id':'7','active':'1'}` into typed dict with int/bool and print tuple `(id, active)`.",
    starter_code="row = {'id':'7','active':'1'}\n# coerce schema\n",
    solution_code=(
        "row = {'id': '7', 'active': '1'}\n"
        "typed = {'id': int(row['id']), 'active': row['active'] == '1'}\n"
        "print((typed['id'], typed['active']))"
    ),
    expected_output="(7, True)",
    tags=["python", "data-scripting", "schema"],
)
add_question(
    topic_slug="data-scripting",
    title="Windowed Moving Average",
    slug="py-data-scripting-moving-average",
    difficulty="advanced",
    task="Compute moving average (window=2) for `[2,4,6]` and print result list.",
    starter_code="vals = [2,4,6]\n# moving average window 2\n",
    solution_code=(
        "vals = [2, 4, 6]\n"
        "out = []\n"
        "for i in range(len(vals) - 1):\n"
        "    out.append((vals[i] + vals[i + 1]) / 2)\n"
        "print(out)"
    ),
    expected_output="[3.0, 5.0]",
    tags=["python", "data-scripting", "windowing"],
)
add_question(
    topic_slug="data-scripting",
    title="Top N by Metric",
    slug="py-data-scripting-top-n",
    difficulty="advanced",
    task="Select top 2 rows by `score` from list of dicts and print first id.",
    starter_code="rows = [{'id':1,'score':10},{'id':2,'score':30},{'id':3,'score':20}]\n# top 2 by score\n",
    solution_code=(
        "rows = [{'id': 1, 'score': 10}, {'id': 2, 'score': 30}, {'id': 3, 'score': 20}]\n"
        "top = sorted(rows, key=lambda r: r['score'], reverse=True)[:2]\n"
        "print(top[0]['id'])"
    ),
    expected_output="2",
    tags=["python", "data-scripting", "ranking"],
)
add_question(
    topic_slug="data-scripting",
    title="Incremental Upsert Simulation",
    slug="py-data-scripting-upsert-sim",
    difficulty="advanced",
    task="Apply upserts to dict store for ids 1 and 2, then update id 1. Print final value for id 1.",
    starter_code="# simulate upsert into dict store\n",
    solution_code=(
        "store = {}\n"
        "for row in [{'id': 1, 'v': 5}, {'id': 2, 'v': 8}, {'id': 1, 'v': 9}]:\n"
        "    store[row['id']] = row['v']\n"
        "print(store[1])"
    ),
    expected_output="9",
    tags=["python", "data-scripting", "upsert"],
)
add_question(
    topic_slug="data-scripting",
    title="Data Quality Rule Engine",
    slug="py-data-scripting-quality-rules",
    difficulty="advanced",
    task="Apply validation rules (`age >= 18`, `email contains @`) to one record and print `True` if valid.",
    starter_code="row = {'age':21,'email':'a@b.com'}\n# apply validation rules\n",
    solution_code=(
        "row = {'age': 21, 'email': 'a@b.com'}\n"
        "rules = [lambda r: r['age'] >= 18, lambda r: '@' in r['email']]\n"
        "print(all(rule(row) for rule in rules))"
    ),
    expected_output="True",
    tags=["python", "data-scripting", "data-quality"],
)
add_question(
    topic_slug="data-scripting",
    title="Build Mini ETL Pipeline",
    slug="py-data-scripting-mini-etl",
    difficulty="advanced",
    task="Extract numbers as strings, transform to ints, load as sum. Print total.",
    starter_code="raw = ['1','2','3']\n# mini ETL steps\n",
    solution_code=(
        "raw = ['1', '2', '3']\n"
        "extracted = raw\n"
        "transformed = [int(x) for x in extracted]\n"
        "loaded_total = sum(transformed)\n"
        "print(loaded_total)"
    ),
    expected_output="6",
    tags=["python", "data-scripting", "etl"],
    question_type="build_from_scratch",
)


EXPECTED_DISTRIBUTION = {
    "concurrency": {"basic": 6, "intermediate": 8, "advanced": 8, "total": 22},
    "async": {"basic": 6, "intermediate": 8, "advanced": 8, "total": 22},
    "performance": {"basic": 6, "intermediate": 8, "advanced": 8, "total": 22},
    "design-patterns": {"basic": 6, "intermediate": 8, "advanced": 8, "total": 22},
    "data-scripting": {"basic": 8, "intermediate": 10, "advanced": 8, "total": 26},
}


def _validate_distribution() -> None:
    for topic_slug, expected in EXPECTED_DISTRIBUTION.items():
        questions = QUESTIONS_BY_TOPIC[topic_slug]
        counts = Counter(q["difficulty"] for q in questions)
        if len(questions) != expected["total"]:
            raise ValueError(f"{topic_slug}: expected {expected['total']} total, got {len(questions)}")
        for level in ("basic", "intermediate", "advanced"):
            if counts[level] != expected[level]:
                raise ValueError(
                    f"{topic_slug}: expected {expected[level]} {level}, got {counts[level]}"
                )
        for q in questions:
            if not q["slug"].startswith("py-"):
                raise ValueError(f"{topic_slug}: slug must start with py- ({q['slug']})")
            if q.get("expected_output") in (None, ""):
                raise ValueError(f"{topic_slug}: expected_output required ({q['slug']})")


async def main() -> None:
    _validate_distribution()
    total = 0
    for topic_slug, module_label in TOPIC_ORDER:
        seeded = await seed_questions_for_topic(topic_slug, QUESTIONS_BY_TOPIC[topic_slug], module_label)
        total += seeded
    print(f"Seeded {total} questions across modules 21-25")


if __name__ == "__main__":
    asyncio.run(main())
