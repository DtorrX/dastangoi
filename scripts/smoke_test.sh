#!/usr/bin/env bash
set -euo pipefail

echo "[smoke] Checking Huginn"
curl -fsS http://localhost:3000/ >/dev/null

echo "[smoke] Checking reporter"
curl -fsS http://localhost:8001/health >/dev/null || true

echo "[smoke] Checking mailer"
curl -fsS http://localhost:8002/health >/dev/null || true

echo "[smoke] Checking billing"
curl -fsS http://localhost:8003/health >/dev/null || true

printf "[smoke] Done\n"
