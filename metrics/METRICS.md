# Metrics: every number, where it came from, and what it does not mean

**Last verified:** 2026-10-20.

**Method:** read-only, aggregate-only SQL against production (`COUNT`, `SUM`, `MIN`, `MAX`, `GROUP BY` inside `BEGIN READ ONLY; … ROLLBACK;`). No row-level data was selected or exported. Connection details came from the environment and are not stored in this repo. Where a number came from a log, a repository or a broker statement instead of SQL, the source column says so.

**Rule:** if a number is not on this page, it is not claimed anywhere in this portfolio. Anything else is marked "not measured".

## SaunaticaOS

| Metric | Value | Date range | Source | Caveat |
|---|---|---|---|---|
| Native payments processed | **$97K across 963 payments** | 2026-05-21 → 2026-10-20 | [`studio_os_native_payments.sql`](queries/studio_os_native_payments.sql) | Completed payments created natively; history imported from the previous platform is excluded. This is all native card and cash revenue (POS, memberships, renewals), not a single feature's revenue, and **not attributable to the AI agent** |
| Customers migrated and managed | **9,985** | as of 2026-10-20 | [`studio_os_scale.sql`](queries/studio_os_scale.sql) | Includes customers migrated from the previous platforms |
| Sessions migrated and managed | **~57K** | as of 2026-10-20 | [`studio_os_scale.sql`](queries/studio_os_scale.sql) | Includes historical sessions migrated from the previous booking platform |
| Live automation workflows | **10** templates, **9,122** runs | as of 2026-10-20 | [`studio_os_scale.sql`](queries/studio_os_scale.sql) | Runs = workflow instances started since go-live |
| Data model | **85** Prisma models | as of 2026-10-20 | Repository: count of `model` blocks in the Prisma schema | Code metric, not usage |
| API surface | **318** API routes | as of 2026-10-20 | Repository: count of `route.ts` files under the app router | Code metric, not usage |
| Commits | **970** | 2026-04-18 → 2026-10-19 | Repository: `git rev-list --count main` | Built with AI coding agents; commit count is not a productivity claim |
| Replaced GoHighLevel + Hapana | Yes | cutover 2026-05-21 | Migration records (parallel run, exit-file importers, card-vault carryover) | SaaS cost avoided is not published |

## Sarah AI

| Metric | Value | Date range | Source | Caveat |
|---|---|---|---|---|
| Sessions booked autonomously | **382** for **196** distinct customers | May → Oct 2026 | [`sarah_bookings.sql`](queries/sarah_bookings.sql) | Sessions created by the agent's own tool path. Bookings, not revenue |
| Share of those sessions completed | **63%** | May → Oct 2026 | [`sarah_bookings.sql`](queries/sarah_bookings.sql) (status mix) | The rest were cancelled or no-shows |
| AI-handled SMS turns | **2,873** across **631** contacts | 2026-05-29 → 2026-10-19 | [`sarah_sms_turns.sql`](queries/sarah_sms_turns.sql) | One inbound text → one AI reply. These are **turns, not conversations** |
| Inbound voice calls answered | **182** | 2026-05-28 → 2026-10-19 | [`sarah_voice_calls.sql`](queries/sarah_voice_calls.sql) | Inbound only. A small, paused outbound pilot is excluded |
| Revenue attributable to Sarah | **Not claimed** | — | — | No payment figure is attributed to Sarah. Native payments belong to SaunaticaOS as a whole |

## Governed agent ops

| Metric | Value | Date range | Source | Caveat |
|---|---|---|---|---|
| Dispatcher runs | **4,486 ok / 6 suspicious / 2 failed** | 2026, as of 2026-10-20 | Dispatcher run log (equivalent SQL: [`agent_ops_dispatcher_and_evals.sql`](queries/agent_ops_dispatcher_and_evals.sql)) | "Suspicious" = completed but wrote zero events |
| Automatic job suspensions | **4** | same | Dispatcher run log | Triggered by 2 consecutive failures |
| Model-eval runs | **673** | same | Eval run records ([`agent_ops_dispatcher_and_evals.sql`](queries/agent_ops_dispatcher_and_evals.sql)) | Runs across all eval families and candidate models |
| Verifier | **72** outcome checks; **86.9%** of recorded results passing | same | [`agent_ops_verifier.sql`](queries/agent_ops_verifier.sql) | A pass rate over check results, not a share of jobs that work. Failures are how silent breakage is caught |

## Multi-LLM trading committee (paper only)

| Metric | Value | Date range | Source | Caveat |
|---|---|---|---|---|
| Paper NAV change | **−0.95%** | ~4 weeks, early 2026 | Broker paper-account statements | **Paper account. No live capital. No alpha claimed** |
| Max drawdown | **−7%** | same | Broker paper-account statements | Paper |
| Win rate | **35%** on **205** closed trades | same | Internal execution study over closed paper trades | Break-even at the observed payoff ratio was **46.8%** |
| Backtests | Self-audited as essentially meaningless | before paper trading | Internal backtest audit | Original backtests were simulations, not real fills. Overfit factor results are never quoted |

No SQL is provided here: the project is archived, and its database holds account-specific trade records.

## Other case studies

| Case study | Numbers quoted | Source | Caveat |
|---|---|---|---|
| 06 Programmatic SEO | **~13K** pages generated; **536** kept indexable after the prune | Generator output and page index | Traffic or revenue recovery is not measured to a publishable standard |
| 07 SharpKing | **−8.8%** net on small real stakes | Fee-true ledger reconciled 1:1 to on-chain fills | Retired after a preregistered review returned REVERT |
| 05 PrepareQuick | None | — | Past product; no metrics published |
| 08 AI tutor | None | — | Learning outcomes not measured; learner data never published |

## Owner background

| Claim | Source |
|---|---|
| 20+ years of sales leadership | Employment history |
| $10M+/yr at Sentry Servicing | Employment history |
| $600K+/mo at Liberty Credit Management | Employment history |

## Re-verification

Re-run every query quarterly and update the "Last verified" date. If a number moves, change it here first, then everywhere it appears.
