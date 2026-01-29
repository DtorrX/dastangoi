# Huginn Disinfo Digest (Guerrilla Micro-SaaS)

This repository contains a production-ready, **signals-only** disinformation monitoring micro-SaaS built on top of Huginn. It focuses on **public, lawful sources** (RSS/Atom, official APIs, and other permissive public web pages) and produces **daily reports** that label findings as *signals/indicators*, not verified facts.

> **Important**: This is not a truth engine. It surfaces *possible* coordinated narratives and gives confidence scores and rationale so humans can decide what to do next.

## Quickstart (Local)

```bash
cp .env.example .env
make bootstrap
make seed-scenario
make smoke-test
```

## What’s inside
- **Huginn** for orchestration and event capture.
- **Reporter** service to aggregate daily signals and generate HTML/MD/JSON.
- **Mailer** service to send reports to subscribers with unsubscribe support.
- **Billing** service for Stripe Checkout and webhook handling.
- **Config** YAMLs for sources, watchlists, and thresholds.
- **Docs** for architecture, runbook, and compliance notes.

## MVP scope (first 7 days)
- Ingest from RSS + GDELT/MediaCloud public endpoints (BYO API keys).
- Normalize + dedupe + enrich in Huginn.
- LLM-based narrative classification with guardrails.
- Daily report generation + SES/Mailgun sending.
- Stripe Checkout for paid daily plan and basic free weekly plan.

**Postponed**: full admin UI, Slack/CSV exports, and advanced WHOIS/bot analysis.

See `docs/` for the complete implementation plan and operational guidance.
