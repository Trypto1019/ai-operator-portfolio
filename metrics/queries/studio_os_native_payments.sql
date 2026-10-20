-- SaunaticaOS: payments processed natively (excludes history migrated from the old platform).
-- Result (2026-05-21 -> 2026-10-20): 963 completed payments, $97K.
-- Caveat: all native card and cash revenue (POS, memberships, renewals). Not attributable to any single feature or to the AI agent.
SELECT
    MIN("createdAt")::date  AS first_payment,
    MAX("createdAt")::date  AS last_payment,
    COUNT(*)                AS payments,
    ROUND(SUM(amount))      AS total_amount
FROM "Payment"
WHERE status = 'completed'
  AND "hapanaPaymentId" IS NULL;   -- NULL = created natively, not imported
