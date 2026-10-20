-- Sarah AI: AI-handled SMS turns (one inbound text -> one AI reply).
-- Result (2026-05-29 -> 2026-10-19): 2,873 turns across 631 distinct contacts.
-- Caveat: these are turns, not conversations.
SELECT
    COUNT(*)                                   AS turns,
    COUNT(DISTINCT phone)                      AS distinct_contacts,
    COUNT(*) FILTER (WHERE error IS NOT NULL)  AS turns_with_error,
    MIN("createdAt")::date                     AS first_turn,
    MAX("createdAt")::date                     AS last_turn
FROM "SmsAgentTurn";
