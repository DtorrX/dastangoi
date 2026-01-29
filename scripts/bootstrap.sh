#!/usr/bin/env bash
set -euo pipefail

echo "[bootstrap] Starting Huginn stack"
docker compose up -d postgres redis huginn

echo "[bootstrap] Waiting for Huginn to be ready"
for i in {1..20}; do
  if curl -fsS http://localhost:3000/ >/dev/null; then
    echo "[bootstrap] Huginn is up"
    exit 0
  fi
  sleep 3
done

echo "[bootstrap] Huginn not ready yet. Check logs with: docker compose logs huginn"
exit 1
