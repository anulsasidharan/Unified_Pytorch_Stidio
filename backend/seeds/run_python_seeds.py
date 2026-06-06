"""Run all Python Learning Studio question + snippet seeds (idempotent).

Usage:
    python -m seeds.run_python_seeds
"""

import asyncio

import seeds.questions_python_basics as questions_python_basics
import seeds.questions_python_control_flow as questions_python_control_flow
import seeds.questions_python_loops as questions_python_loops
import seeds.questions_python_modules_06_10 as questions_python_modules_06_10
import seeds.questions_python_modules_11_15 as questions_python_modules_11_15
import seeds.questions_python_modules_16_20 as questions_python_modules_16_20
import seeds.questions_python_modules_21_25 as questions_python_modules_21_25
import seeds.questions_python_strings as questions_python_strings
import seeds.questions_python_variables as questions_python_variables
from seeds.seed_snippets import seed_snippets


async def main() -> None:
    print("=== Seeding Python Learning Studio questions (modules 01-25) ===")
    await questions_python_basics.main()
    await questions_python_variables.main()
    await questions_python_strings.main()
    await questions_python_control_flow.main()
    await questions_python_loops.main()
    await questions_python_modules_06_10.main()
    await questions_python_modules_11_15.main()
    await questions_python_modules_16_20.main()
    await questions_python_modules_21_25.main()
    print("=== Seeding starter snippet library ===")
    await seed_snippets()
    print("=== Python seed complete ===")


if __name__ == "__main__":
    asyncio.run(main())
