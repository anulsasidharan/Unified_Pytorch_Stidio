"""Run all Phase 1 seeds: topics + modules 01-03 questions."""

import asyncio

from seeds import questions_autograd, questions_nn_module, questions_tensors, topics


async def main() -> None:
    await topics.seed_topics()
    await questions_tensors.seed_questions_tensors()
    await questions_autograd.main()
    await questions_nn_module.main()
    print("Phase 1 seed complete.")


if __name__ == "__main__":
    asyncio.run(main())
