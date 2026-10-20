# ADR 0004: Release identity and immutable cron releases

- **Status:** Accepted
- **Context systems:** SaunaticaOS operations

## Context

The app and about 20 scheduled jobs (billing, reconciliation, workflows, no-shows) run on one host. Jobs that execute from a working checkout can pick up uncommitted edits. An incident confirmed the risk: a job ran code that had never been deployed.

## Decision

1. **Publish releases** as detached, immutable worktrees per commit, with an atomic `current` symlink. Keep the last three.
2. **Every scheduled job runs from `current`**, never from the development checkout.
3. **Deploy** is serialized with a lock. It typechecks, builds into a staging directory, runs critical smoke tests *before* restart, swaps atomically, then runs post-deploy smoke tests. Rollback is documented.
4. **Service start hooks verify identity:** before start, reject source or build-ID drift; after start, confirm the live process and HTTP endpoint report the expected release. Restart limits and an on-failure alert unit catch crash loops.
5. **Every cron is wrapped** to alert on non-zero exit, with a cooldown and a consecutive-failure threshold, and the wrapper preserves the job's exit code.

## Consequences

- What runs is exactly what was released, and you can prove it.
- Slightly slower deploys and some disk overhead for kept releases.
- The public reference adds CI and non-root hardened units, which the original lacked.
