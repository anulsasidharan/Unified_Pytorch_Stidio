"""Run all Python Learning Studio seeds (idempotent).

Usage:
    python -m seeds.run_python_seeds
"""

import asyncio

import seeds.questions_python_basics as questions_python_basics
import seeds.questions_python_control_flow as questions_python_control_flow
import seeds.questions_python_loops as questions_python_loops
import seeds.questions_python_strings as questions_python_strings
import seeds.questions_python_variables as questions_python_variables


async def main() -> None:
    print("=== Seeding Python Learning Studio questions ===")
    await questions_python_basics.main()
    await questions_python_variables.main()
    await questions_python_strings.main()
    await questions_python_control_flow.main()
    await questions_python_loops.main()
    print("=== Python seed complete ===")


if __name__ == "__main__":
    asyncio.run(main())
