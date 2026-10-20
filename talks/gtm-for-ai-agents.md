# GTM for AI agents: a sales leader's field notes

*Talk notes. Twenty years of carrying a number, plus a year of building and running agents in production.*

## The one-sentence thesis

**Buyers don't buy agents. They buy outcomes they can trust, with a blast radius they can live with.**

Every objection you will hear is a version of "what happens when it's wrong?" Win the deal by answering that question better than anyone else in the room.

## 1. Sell the job, not the model

- Lead with the job to be done and the unit of value: *bookings made after hours*, *tickets resolved without a human*, *renewals that didn't silently fail*.
- Nobody renews because of a model name. Models change quarterly; the job doesn't.
- Price against the job (per resolved outcome, per seat replaced, per location), not tokens. Token pricing pushes the buyer's risk onto you without the upside.

## 2. The trust stack is the product

When I deployed an AI receptionist that books real appointments, nobody asked about accuracy benchmarks. The questions that mattered were:

| Buyer question | What actually answers it |
|---|---|
| "Will it text someone who said stop?" | Opt-out handling in deterministic code, before the model runs |
| "Will it book the wrong thing?" | Two-phase confirmation: the agent proposes, the customer says YES, the server executes |
| "Will it lie about a booking?" | Grounded replies: the server re-reads the database and composes the answer |
| "Will it take payments?" | No. The server issues tokenized links; the model never touches money |
| "Can it run up a bill?" | Spend caps enforced at the API key, per role |
| "Will it leak customer data?" | PII scan on every tool result before the model sees it |
| "How do we know it still works next month?" | Eval gates on deploys and model changes; an independent verifier that checks outcomes |

Put this table in your deck. It is the security review, the procurement review and the champion's internal pitch in one page.

## 3. SMB vs. enterprise: same agent, different motion

**SMB (owner-operator):**
- The owner is the buyer, the user and the security team. Show the agent working on *their* calendar in the first meeting.
- Time-to-value beats configurability. Ship one job, done well, within a week.
- Trust comes from transparency: daily digests, a visible audit trail, an easy "hand off to a human" path.
- Churn risk is one embarrassing message. Guardrails are retention features.

**Enterprise:**
- There are five buyers: the economic buyer, the operational owner, security, legal/compliance and IT. Map them early.
- Lead with **where the AI has authority and where it doesn't**. "LLMs propose, deterministic code disposes" is a sentence a CISO can repeat.
- Expect a pilot. Design it like a preregistered experiment: one hypothesis, one success metric, a fixed window and a kill criterion, agreed in writing *before* the pilot starts.
- Shadow mode first. Let the agent decide alongside humans without acting, then compare. It turns "trust us" into evidence.

## 4. Deploying: the forward-deployed playbook

1. **Charter.** Write the agent's mandate, authority tier, "must never" list, KPIs and kill criterion. One page.
2. **Inventory the deterministic rules.** Opt-outs, consent, licensing, approvals, money movement. These become code, not prompt text.
3. **Typed tools with autonomy levels.** Read tools run freely; write tools are guarded or confirmed; anything irreversible needs a human.
4. **Synthetic golden set.** Build evals from the customer's real scenarios, rewritten with synthetic data. Include injection attempts.
5. **Shadow, then supervised, then autonomous,** with a written promotion criterion at each step.
6. **Verify effects, not execution.** Monitor whether the bookings exist and the records changed, not whether the job "ran".
7. **Report honestly.** Turns are not conversations. Correlation is not attribution. Under-claiming early buys credibility for the renewal.

## 5. Metrics that survive diligence

- **Volume:** tasks handled (be precise about the unit).
- **Autonomy:** share completed without a human.
- **Quality:** share completed *correctly*, verified against the system of record.
- **Safety:** guard firings, escalations, opt-out compliance (target: 100%, enforced in code).
- **Value:** the outcome the buyer pays for, with attribution rules agreed in advance.

If you can't measure one of these yet, say so. "Not measured yet, here's how we will" beats a made-up number every time. Diligence finds made-up numbers.

## 6. What kills AI deals

- Demo magic that falls apart on the customer's own data. Demo on their data.
- Unbounded autonomy. One bad action ends the program.
- No owner on the customer side. Agents need an operator, the way a CRM needs an admin.
- Inflated metrics in the pilot readout. The renewal is where they get checked.

## Closing

The best AI sellers will be the ones who can open the hood: who can say exactly what the model decides, what the code decides, and how they know it worked. That is a sales skill now.

*Case studies behind these notes: [Sarah AI](../case-studies/01-sarah-ai-receptionist.md), [Governed agent ops](../case-studies/03-governed-agent-ops.md), [Killing a strategy with evidence](../case-studies/07-killing-a-strategy-with-evidence.md).*
