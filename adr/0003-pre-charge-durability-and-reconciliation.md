# ADR 0003: Pre-charge durability and reconciliation

- **Status:** Accepted
- **Context systems:** SaunaticaOS payments (lesson first learned on PrepareQuick webhooks)

## Context

A card charge spans two systems: our database and the gateway. A crash, timeout or retry between them can produce a charge with no record, a record with no charge, or a double charge. Webhook retries can double-grant credits if the handler isn't idempotent.

## Decision

1. **Tx A:** insert a `PENDING` payment row with a unique idempotency key and a hash of the request, *before* calling the gateway.
2. Reusing a key with a different request hash returns **409** (key misuse).
3. Call the gateway.
4. **Tx B:** `SELECT ... FOR UPDATE` the row, record the result, run fulfilment and write an audit row, all in one transaction.
5. A **reconciler every 5 minutes** resolves stuck `PENDING` rows by querying the gateway, marks them `UNKNOWN` after N attempts and opens a staff task. It also re-runs fulfilment for paid-but-unfulfilled rows.
6. Webhooks verify signatures on the raw body and store each event as an append-only audit row that doubles as the idempotency guard.
7. Refunds follow the same pattern.

## Consequences

- No lost or double charges from crashes or retries. Every anomaly becomes a visible task, not a silent discrepancy.
- More states to reason about (`PENDING`, `UNKNOWN`). That complexity is the honest shape of distributed payments.
