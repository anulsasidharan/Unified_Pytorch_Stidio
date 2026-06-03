#!/bin/sh
set -e

cd /app/apps/api

PRISMA_BIN=/app/apps/api/node_modules/.bin/prisma
TSX_BIN=/app/node_modules/.bin/tsx

echo "[api] Running database migrations..."
"$PRISMA_BIN" migrate deploy

if [ "${SEED_ON_START:-true}" = "true" ]; then
  echo "[api] Seeding database (upsert)..."
  "$TSX_BIN" prisma/seed.ts
fi

echo "[api] Starting server on port ${PORT:-4000}..."
exec node dist/index.js
