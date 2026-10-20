-- Governed agent ops: verifier pass rate over all recorded results.
-- Result (as of 2026-10-20): 86.9% of recorded verifier results passing; 72 distinct outcome checks.
-- Caveat: a pass rate over check results, not "share of jobs that work".
-- Column names are illustrative (verifier_results: check_name, passed); adapt to your schema.
SELECT
    COUNT(*)                                             AS results,
    COUNT(*) FILTER (WHERE passed)                       AS passing,
    ROUND(100.0 * COUNT(*) FILTER (WHERE passed) / COUNT(*), 1) AS pct_passing,
    COUNT(DISTINCT check_name)                           AS distinct_checks
FROM verifier_results;
