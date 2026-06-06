#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running Alembic migrations..."
  alembic upgrade head
fi

if [ "${SEED_TOPICS:-true}" = "true" ]; then
  echo "Ensuring PyTorch module topics (idempotent)..."
  python -m seeds.topics
  python -m seeds.ensure_topics
fi

exec "$@"
