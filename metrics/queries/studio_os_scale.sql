-- SaunaticaOS: scale of records migrated and managed.
-- Results (as of 2026-10-20): 9,985 customers; ~57K sessions; 10 active workflow templates; 9,122 workflow runs.
-- Caveat: customers and sessions include records migrated from the previous platforms.
SELECT COUNT(*) AS customers          FROM "Customer";
SELECT COUNT(*) AS sessions           FROM "Session";
SELECT COUNT(*) AS active_workflows   FROM "WorkflowTemplate" WHERE "isActive";
SELECT COUNT(*) AS workflow_runs      FROM "WorkflowInstance";
