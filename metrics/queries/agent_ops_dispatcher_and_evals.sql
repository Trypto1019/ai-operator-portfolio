-- Governed agent ops: dispatcher outcomes and model-eval runs.
-- Results (as of 2026-10-20): 4,486 ok / 6 suspicious / 2 failed runs; 4 automatic suspensions; 673 model-eval runs.
-- Caveat: the production run tallies were taken from the dispatcher's run log, not SQL.
-- These are the equivalent aggregates against an illustrative schema
-- (job_runs.status, events.type, eval_runs); adapt names to your schema.
SELECT status, COUNT(*) AS runs
FROM job_runs
GROUP BY status;

SELECT COUNT(*) AS auto_suspensions
FROM events
WHERE type = 'job_auto_disabled';

SELECT COUNT(*) AS model_eval_runs
FROM eval_runs;
