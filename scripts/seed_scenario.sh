#!/usr/bin/env bash
set -euo pipefail

SCENARIO_JSON="huginn/scenarios/disinfo_daily_digest.json"
HUGINN_URL=${HUGINN_URL:-http://localhost:3000}

if [[ ! -f "$SCENARIO_JSON" ]]; then
  echo "Scenario JSON not found: $SCENARIO_JSON" >&2
  exit 1
fi

echo "[seed] Importing Huginn scenario"
# The Huginn import endpoint expects authenticated requests; this is a template.
# In production, set HUGINN_API_KEY and use the API endpoint.

echo "[seed] TODO: Use HUGINN_API_KEY to POST $SCENARIO_JSON to $HUGINN_URL"
