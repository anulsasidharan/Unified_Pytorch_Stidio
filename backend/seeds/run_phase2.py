"""Run Phase 2 seeds: modules 04–07 questions."""

import asyncio

from seeds import (
    questions_cnns,
    questions_datasets,
    questions_loss_functions,
    questions_training_loops,
)
from seeds.ensure_topics import ensure_all_topics


async def main() -> None:
    await ensure_all_topics()
    await questions_training_loops.main()
    await questions_loss_functions.main()
    await questions_datasets.main()
    await questions_cnns.main()
    print("Phase 2 seed complete (modules 04–07).")


if __name__ == "__main__":
    asyncio.run(main())
