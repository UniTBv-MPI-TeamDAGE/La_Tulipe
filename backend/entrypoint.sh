#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be ready..."

until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}"; do
  echo "   postgres not ready yet, sleeping 1s..."
  sleep 1
done

echo "PostgreSQL is ready."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000