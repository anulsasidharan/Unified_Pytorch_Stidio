#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running Alembic migrations..."
  alembic upgrade head
fi

if [ "${SEED_TOPICS:-true}" = "true" ]; then
  echo "Seeding PyTorch module topics..."
  python -m seeds.topics
fi

exec "$@"
