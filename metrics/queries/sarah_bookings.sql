-- Sarah AI: sessions created by the agent's own tool path.
-- Result (May -> Oct 2026): 382 sessions for 196 distinct customers; 63% completed.
-- Caveat: bookings, not revenue. No payment figure is attributed to Sarah.

-- Totals
SELECT
    COUNT(*)                     AS sessions,
    COUNT(DISTINCT "customerId") AS distinct_customers
FROM "Session"
WHERE source = 'sarah_ai';

-- Outcome mix (completed share = completed / total)
SELECT status, COUNT(*) AS sessions
FROM "Session"
WHERE source = 'sarah_ai'
GROUP BY status
ORDER BY sessions DESC;
