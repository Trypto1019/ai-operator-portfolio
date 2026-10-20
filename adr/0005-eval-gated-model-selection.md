# ADR 0005: Eval-gated model selection and deploys

- **Status:** Accepted
- **Context systems:** Sarah AI eval harness, governed agent ops

## Context

Model choice and prompt changes are the riskiest changes an agent system makes, and they are usually made on vibes. LLM outputs are also noisy: a single failing run is not proof of a regression.

## Decision

**For a customer-facing agent (Sarah):**

1. The harness runs **production's own code path** against scratch databases with frozen tool fixtures. Network access is restricted to the model provider, and outbound sends are disabled.
2. Deterministic checks (tool schema, must-call, outcome, claims, numbers, opt-out, hygiene) plus an LLM judge with a rubric. The judge is told to treat transcripts as data, to resist injection.
3. **Variance-aware regression:** a 5-run baseline; a regression counts only if a check that never failed in the baseline fails 3 of 3 re-runs.
4. The deploy script runs the comparison when agent code changes. Overrides are possible but logged.

**For back-office role agents:**

1. Eval families: fabrication, tool-calling, authority, role quality, PII leakage, consistency, cost/latency.
2. A role charter may only name a model with a **passing scorecard under 90 days old**.
3. **Cost never affects pass.** Cost is reported, and among passing models it can break ties.

## Consequences

- Model swaps become routine, evidence-backed changes.
- Eval runs cost money and time; that is budgeted like testing.
- Golden datasets must be synthetic or carefully anonymized, enforced by a hygiene test that fails on real-looking phones, emails or names.
