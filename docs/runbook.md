# Runbook

## Local setup
1. `cp .env.example .env`
2. `make bootstrap`
3. `make seed-scenario`
4. `make smoke-test`

## Production (single VPS)
1. Install Docker + Docker Compose.
2. Set environment variables in `.env`.
3. `docker compose up -d`.
4. Configure DNS + TLS (Nginx or Caddy).
5. Configure Stripe webhooks to `/webhooks/stripe`.
6. Configure SES/Mailgun credentials.

## Operations
- **Daily rollup**: call `POST /rollup` at 06:00 America/Toronto.
- **Backups**: dump Postgres daily, sync `data/archives/`.
- **Upgrades**: `docker compose pull` then `docker compose up -d`.
