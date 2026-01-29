# Implementation Plan (A–I)

## A) Architecture diagram + data flow
See `docs/architecture.md` for the ASCII diagram and flow.

## B) Step-by-step setup instructions
See `docs/runbook.md` for local + production setup.

## C) Threat model + security checklist
See `docs/security.md`.

## D) Huginn scenario JSON + agent explanations + env vars
- Scenario JSON: `huginn/scenarios/disinfo_daily_digest.json`.
- Agent templates: `huginn/templates/`.
- Environment variables: `.env.example`.

## E) Reporter code
- Service: `reporter/src/`.
- Generates HTML + Markdown + JSON and a PDF placeholder.
- Archives to `data/archives/`.

## F) Mailer code
- Service: `mailer/src/`.
- SES client with batch sending and unsubscribe tokens.
- Bounce webhook stub for suppression lists.

## G) Stripe billing
- Service: `billing/src/`.
- Checkout endpoint + webhook handler.
- Plan mapping in `config/plans.yaml`.

## H) Tests
- Unit tests in `services/*/tests`.
- Include a dry run by calling `/rollup` with mock events.

## I) Guerrilla profitability playbook
See `docs/monetization.md`.
