# Risk patterns

A checklist for reading a change and finding the risks that are actually in it.

## How to use this file

Work through the categories and ask, for each: *does this change touch this, and if so, what specifically breaks?* The answer must come from the diff, the migration files, the infrastructure configuration, or the developer — not from the category itself.

**This file is not a source of risks.** A category matching the change is not evidence that the risk exists. It is a prompt to go and look. If you cannot point to the line, file, or statement that establishes a risk, it does not go in the register — it becomes `[NEEDS INPUT: <specific question>]`.

---

## The specificity requirement

Every register row must name the specific component, table, endpoint, service, queue, or job that **this change** affects.

A row that would be equally true of any deployment of any system is not a risk assessment. It is a signal that the change was not read. Rows of that kind — deployment may fail, the release could introduce bugs, performance may degrade, users may be affected — must be rejected, not softened. If a row survives having the project name removed and still reads as sensible, it is too generic.

The test: could a reader of the row identify which part of the system to look at if it went wrong? If not, rewrite it or drop it.

The same applies to mitigations and owners. A mitigation must name the mechanism; an owner must name a person.

---

## Categories to work through

### Behavioural and decision logic

- A decision that was deterministic becomes non-deterministic, or vice versa — rules replaced by a model, thresholds replaced by inference, or the reverse. Ask what the decision governs and what happens when it is wrong in each direction.
- The proportion of work bypassing human review changes, in either direction. More bypass risks incorrect outcomes being actioned unseen; less bypass risks queues growing beyond the capacity to clear them.
- Routing changes — work items, messages, requests, or traffic arrive somewhere different, or in a different shape.
- Validation is loosened or tightened. Both carry risk: loosening admits input that previously failed; tightening rejects input that previously passed, which surfaces as volume moving to manual handling.
- Eligibility, entitlement, pricing, or permission logic changes. Establish what the wrong answer costs in each direction.

### Data and calculation

- A formula, aggregation, unit, or rounding rule changes. Identify every consumer of the affected value — reports, invoices, dashboards, downstream systems.
- Historical data is or is not restated. Either answer is acceptable; leaving it unstated is not, because someone will ask.
- Reference, mapping, or configuration data changes. These fail silently: the system works and the answers are wrong.
- A migration or backfill runs. Establish whether it is reversible, what happens if it fails partway, and how long it takes at production volume.

### Integration and downstream

- A payload contract changes — a field added, removed, renamed, or retyped. Identify who consumes it.
- Log or event format changes. Low severity, frequently missed: parsers, alerts, and dashboards built on the old shape break quietly.
- A new call is added to a request path, adding latency, cost, and a new failure surface.
- An existing dependency's version, endpoint, or authentication changes.

### Infrastructure

- New components — endpoints, functions, services, queues, storage, databases. This drives the infrastructure-change and internet-exposure answers on the form.
- Network or authentication path changes — gateway, ingress, public to private, new authentication contract or callback. Failure modes run both ways: legitimate users locked out, or the wrong parties admitted.
- Schema changes, index changes, or anything altering query plans at production scale.
- Environment variables, secrets, or configuration values change. Establish what happens if a value is wrong or absent at startup.

### Deployment mechanics

- Components must be released together. Establish what production looks like in the window where one has landed and the other has not.
- Configuration and code must be applied in a particular order. Establish what the wrong order does.
- Automation, triggers, or schedules resume after deployment. Establish whether verification completes before they do.
- A step cannot be reversed because its effect has already left the system. This must be named in the register and in the rollback field.

### Load and performance

- A new call, query, or operation enters a hot path or a loop. Quantify at production volume, not test volume.
- Producer or consumer rates change on a queue or stream. Establish what happens to depth and to any dead-letter path.
- Quotas, rate limits, or cost ceilings could be reached that were previously out of range.

### Security

- Something becomes reachable from the public internet that was not. Establish the authentication and network controls that stand in front of it.
- New credentials, roles, or permissions are introduced. Establish scope and whether it exceeds what the component needs.
- The handling path for personal or sensitive data changes — where it flows, where it is stored, where it is logged.

### Operational readiness

- First deployment of a solution into the target environment: monitoring and alerting are unproven, so failures may not surface promptly.
- The rollback path exists but has not been executed by anyone. Untested rollback is a partial mitigation, and the register should say so.
- The window falls outside supported hours. Establish who responds if it fails.

---

## Writing the row

- **Risk** — the failure mode, in one sentence, naming the specific component involved. Present tense, plain statement, not hedged into meaninglessness.
- **Likelihood** — High, Medium, or Low: the honest chance with the controls that already exist. A failure mode that has never run in production should not be Low purely because it has not happened yet.
- **Impact if realised** — the consequence for the business, its users, or its data. The outcome, not the internal code behaviour that produces it.
- **Mitigation** — a specific action reducing likelihood or impact. Monitoring alone qualifies only if it states the signal, the person watching, and the action that follows. Removing the risk from the cutover, for example by disabling the affected path at go-live, is stronger than observing it.
- **Owner** — a named individual accountable for the mitigation, including after go-live.

## Failure modes in register writing

- Padding with categories from this file that the change does not touch. An unnecessary row costs credibility for every other row.
- Rating everything Low so the change reads as safe. Transparent to the CAB, and it devalues the register as a record.
- Mitigations that describe an intention to be careful rather than an action taken.
- Omitting the largest risk because it feels self-evident to the person who wrote the code. The risk most obvious to the author is often the one the CAB has never seen.
- Recording a risk without recording who owns the mitigation after go-live.
