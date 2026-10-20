-- Sarah AI: voice calls by direction.
-- Result (2026-05-28 -> 2026-10-19): 182 inbound calls answered.
-- Caveat: outbound rows are a small, paused pilot and are not quoted as a headline metric.
SELECT
    direction,
    COUNT(*)                                        AS calls,
    AVG(EXTRACT(EPOCH FROM ("callEnded" - "callStarted"))) AS avg_seconds,
    MIN("createdAt")::date                          AS first_call,
    MAX("createdAt")::date                          AS last_call
FROM "SarahCallTranscript"
GROUP BY direction;
