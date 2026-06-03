"""Run Phase 5 seeds: modules 08–13 + bulk expansion to 500+ exercises."""

import asyncio

from seeds import bulk_expand, questions_modules_08_13
from seeds.ensure_topics import ensure_all_topics


async def main() -> None:
    await ensure_all_topics()
    await questions_modules_08_13.main()
    await bulk_expand.main()
    print("Phase 5 seed complete (modules 08–13 + bulk expansion).")


if __name__ == "__main__":
    asyncio.run(main())
