# Threat Model & Security Checklist

## Threat Model
- **Adversarial manipulation**: false narratives injected via public sources.
- **Data poisoning**: coordinated spam to skew heuristics.
- **Credential leaks**: API keys or Stripe secrets exposed.
- **Email abuse**: spam or spoofing issues.

## Mitigations
- Only ingest **public, ToS-compliant** sources.
- Deduplicate and label all outputs as **signals**.
- Strict schema validation for LLM responses.
- Rotate secrets and avoid logging subscriber emails.
- Maintain suppression list and unsubscribe mechanisms.

## Security Checklist
- [ ] Secrets stored in env or a vault (never in git).
- [ ] TLS enabled on all public endpoints.
- [ ] Webhooks validated with signatures.
- [ ] Rate limits for API endpoints.
- [ ] Audit logs for admin actions.
