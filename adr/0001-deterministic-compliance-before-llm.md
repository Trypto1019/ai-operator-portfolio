# ADR 0001: Deterministic compliance runs before the LLM

- **Status:** Accepted
- **Context systems:** Sarah AI (SMS and voice), governed agent ops

## Context

An SMS agent receives opt-outs in many forms: "STOP", "QUIT", "please stop texting me", "take me off your list". Regulations and carrier rules require honoring them in any reasonable form, every time. An LLM gets this right *most* of the time. "Most" is not a compliance posture.

There are also false positives to avoid. "I'll stop by at 5" is not an opt-out.

## Decision

Inbound messages pass through **deterministic routers before any model is called**:

1. Signature verification on the webhook.
2. Opt-out detection from a fixed keyword set, plus natural-language revocation patterns, plus a stripper for visit-sense phrases ("stop by", "stop in").
3. Suppression upsert (idempotent) and a single acknowledgment sent only after commit.
4. Do-not-contact and suppression checks before every outbound send.
5. Only then does the agent loop run.

Every rule change ships with the regression case that motivated it.

## Consequences

- Opt-out handling is testable, auditable and identical on every run.
- The model never sees a message it shouldn't answer.
- Cost: the phrase set needs care to avoid false positives and new phrasings. That cost is paid in tests, not in incidents.
- The same principle appears in agent ops, where compliance rules are versioned YAML and an LLM is used only for judgment calls.
