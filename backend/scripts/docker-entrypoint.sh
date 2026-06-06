#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running Alembic migrations..."
  alembic upgrade head
fi

if [ "${SEED_TOPICS:-true}" = "true" ]; then
  echo "Seeding Python Learning Studio topics (idempotent)..."
  python -m seeds.topics
  python -m seeds.ensure_topics
fi

if [ "${SEED_QUESTIONS:-true}" = "true" ]; then
  echo "Seeding Python questions for modules 01-05 (idempotent)..."
  python -m seeds.run_python_seeds
fi

exec "$@"
