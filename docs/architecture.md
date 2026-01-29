# Architecture & Data Flow

```
[Public Sources] -> [Huginn Agents]
   |  RSS/Atom, APIs, public web
   v
[Normalize] -> [Dedup] -> [Enrich] -> [LLM Classify] -> [Heuristic Score]
   v
[High Signal Filter] -> [Reporter Webhook]
   v
[Reporter Service] -> [Daily Report (HTML/MD/JSON/PDF)]
   v
[Mailer Service] -> [Subscribers]
   v
[Billing Service] -> [Stripe Checkout & Webhooks]
```

## Data Flow
1. Huginn ingests **public, ToS-compliant** sources.
2. Normalization enforces a strict schema.
3. Deduplication ensures idempotency.
4. Enrichment adds keywords and n-grams.
5. LLM classifier emits **signals** with a strict schema and quotes.
6. Heuristics score coordination signals.
7. Reporter aggregates daily signals and renders reports.
8. Mailer sends daily/weekly digests by tier.
9. Billing activates or pauses subscribers via Stripe webhooks.
