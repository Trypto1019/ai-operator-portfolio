# ADR 0006: LLMs propose, deterministic code disposes

- **Status:** Accepted (the umbrella decision behind ADRs 0001–0005)
- **Context systems:** all

## Context

LLMs are excellent at language, synthesis and judgment calls, and unreliable at arithmetic, policy enforcement and remembering what is true in a database. Systems that let the model *decide* inherit that unreliability in the places that matter most: money, compliance and customer trust.

## Decision

Across every system, the model's output is a **proposal**. A deterministic layer that the model cannot override decides what happens:

| System | Model proposes | Code disposes |
|---|---|---|
| AI receptionist | Reply text, tool calls | Opt-out routers, pending-intent confirmation, grounded replies, URL allow-list |
| Studio OS | — (no model on the money path) | Durable two-phase charges, reconciliation |
| Agent ops | Plans, drafts, analyses | Tool allow-lists, PII filter, budget keys, compliance rules, approvals, verifier |
| Trading committee | Direction votes, vetoes | Majority rule, veto whitelist, Risk Marshal limits |
| AI tutor | Conversation | Grading, mastery, routing, exact math |

Rules of thumb:

1. If it moves money, changes a record or touches compliance, code decides.
2. Model authority is **narrowed**, never widened, by later stages (for example, a veto-only arbiter).
3. Every decision is logged with the model, the prompt version and the deterministic verdict.
4. The system should degrade gracefully when the model is unavailable.

## Consequences

- Predictable behavior in the places buyers and regulators care about.
- More code to write than "just prompt it". That code is the product.
