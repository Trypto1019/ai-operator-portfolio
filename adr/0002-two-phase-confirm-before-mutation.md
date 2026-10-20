# ADR 0002: Two-phase confirmation before any mutation

- **Status:** Accepted
- **Context systems:** Sarah AI

## Context

An agent that books, reschedules and cancels can misread intent: "can I move Thursday?" is not "cancel Thursday". A wrong mutation costs a customer a slot and costs the business trust. Models also tend to *say* an action happened when it didn't.

## Decision

1. Write tools never mutate directly. They create a **pending intent** (`NEEDS_CONFIRMATION → OPEN → RESOLVED / EXPIRED`) and the agent asks the customer to reply YES.
2. A deterministic router, not the model, recognizes the YES and executes the intent in a database transaction.
3. Explicit-assent detection: negations veto a yes ("yes, but not Thursday" does not confirm).
4. **Grounded confirmation:** when a customer asks about a booking, the server re-reads the database and composes the reply. The model's draft is discarded for that turn.
5. Every tool has a zod schema and a database-driven autonomy level (`auto_read`, `auto_write_guarded`). A dry-run mode lets evals and replays exercise tools safely.

## Consequences

- No booking changes without explicit customer consent, and no false "you're booked!" messages.
- One extra message per mutation. In practice customers accept it, and it doubles as a receipt.
- Pending intents expire, so stale confirmations can't fire later.
