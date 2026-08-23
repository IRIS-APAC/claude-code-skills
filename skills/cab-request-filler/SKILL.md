---
name: cab-request-filler
description: Drafts a Change Advisory Board (CAB) request submission — the CAB Requests form fields plus the attached Risk & Mitigation Register — from a developer's own project artefacts. Use when the user explicitly mentions a CAB by name, including "CAB request", "CAB form", "CAB submission", "change advisory board", "prep the CAB", "raise a CAB", or "emergency CAB", and when they ask to fill in, draft, or complete a CAB submission for a specific change. Also use when the user asks to prepare the approval paperwork for a named production deployment and the CAB is unambiguously the approval route. Do NOT use for general questions about what a CAB is, who sits on it, when it meets, or how the process works — answer those directly. Do NOT trigger merely because a deployment doc, PR, or release notes were shared.
---

# CAB Request Filler

Drafts a submission for the internal CAB Requests form: answers for each form field, plus a filled-in Risk & Mitigation Register attached to the register field.

This skill drafts. It does not attest. The named business approver and the CAB itself are the controls that decide whether a change is safe to deploy.

---

## The anti-fabrication rule

**Every answer must trace to something the user supplied** — a pull request, a diff, a repository, a deployment document, a ticket, test output, infrastructure or pipeline configuration, or an explicit statement from the developer.

If a field cannot be answered from supplied context, write:

```
[NEEDS INPUT: <specific question>]
```

Never infer an answer from what changes like this usually involve, from what sounds plausible for the technology in play, or from anything in this skill's own guidance. This skill describes what a good answer *contains*; it does not supply answers.

A visible gap is a safe outcome. A plausible-sounding wrong answer is not: it can carry a change into production on the strength of a claim nobody made. When in doubt, mark it `[NEEDS INPUT]` and let the developer close it.

This applies with equal force to the register. Do not populate a risk row because the change resembles a category in `references/risk-patterns.md`. That file is a prompt for reading the change, not a source of risks.

---

## Workflow

### Step 1 — Gather context

Ask for the following in a single message, then wait. Do not begin drafting on the assumption the answers will arrive.

- **The change itself** — repository and branch, pull request, diff, release notes, or deployment document. Read what is supplied directly rather than asking the developer to summarise it.
- **Client or internal, and project name.**
- **Change window** — date, start time, end time, timezone.
- **Business approver** — the named person, and where their approval is recorded.
- **Testing** — what was run, coverage, whether UAT happened, and where the evidence lives.
- **Rollback** — the mechanism, and whether any data change is reversible.
- **Impacted users** — who is affected, and roughly how many.
- **Security posture** — internet exposure, infrastructure or endpoint changes, penetration testing status.

If an artefact already answers one of these, do not ask for it again. If the developer says to draft with what is on hand, do so and mark the rest `[NEEDS INPUT]`.

### Step 2 — Read the change

Before drafting any field, read the supplied artefacts and build your own picture of what changes: which components, which endpoints, which tables, which jobs, which configuration. Note anything that changes behaviour rather than only implementation, and anything irreversible.

You cannot draft the deployment, verification, rollback, or risk fields honestly without this step. If the artefacts are too thin to support it, say so and ask for more rather than drafting around the gap.

### Step 3 — Draft the fields

Work through the form in order, using `references/field-guide.md`. That file holds the field numbering, what each field is really asking, where the answer is normally found in a project, and the criteria an answer must meet to pass.

Apply the rules in `references/style-guide.md` to every field.

### Step 4 — Build the Risk & Mitigation Register

Copy `assets/risk-register-template.md` to a working location and fill it in. The template holds only the two tables — a change metadata block and an empty risk table with six columns. It carries no completion rules, so the rules for filling it in are here.

**Structure of the template.** The metadata block has six labelled rows: Client, Project, Change ID, Change date, CAB date, Prepared by. The risk table has six columns in this order: ID, Risk, Likelihood, Impact if realised, Mitigation, Owner. Five empty rows are provided; add or delete rows to match the number of risks. Do not add columns, rename headers, or reorder them — the CAB reads these registers side by side across submissions.

**Completing the metadata block.** Fill every row from the developer's supplied context. Change ID is whatever identifier the change is tracked under — ticket, release, or change number; if the developer has not supplied one, mark it `[NEEDS INPUT]` rather than inventing a format. CAB date is the meeting the change is being submitted to, which is not the same as the change date. Prepared by is the person drafting the submission, who may differ from the risk owners.

**Completing the risk table.**

1. Add one row per material risk identified by reading the change in Step 2. Risks come from the artefacts, never from the categories in `references/risk-patterns.md`.
2. Order rows most severe first and number them R1, R2, R3 upward. Severity is likelihood weighed against impact, not likelihood alone.
3. Every row must name the specific component, table, endpoint, service, queue, or job that this change affects. A row that would read as sensible with the project name removed is too generic and does not belong in the register.
4. **Likelihood** is High, Medium, or Low — the honest chance with the controls that already exist, not before them. A failure mode that has never run in production should not be recorded as Low purely because it has not happened yet.
5. **Impact if realised** states the consequence for the business, its users, or its data. Describe the outcome, not the internal code behaviour that produces it.
6. **Mitigation** states a specific action that reduces likelihood or impact. Monitoring qualifies only if the row names the signal watched, who watches it, and the action that follows. Removing the risk from the cutover — for example by disabling the affected path at go-live — is stronger than observing it.
7. **Owner** is a named individual accountable for the mitigation, including after go-live. Not a team.
8. Delete any unused empty rows before saving.
9. Save as `<client>-<project>-cab-risk-register-<yyyymmdd>.md`. If the CAB requires a Word document, convert this file to `.docx` as the final step.

See `references/risk-patterns.md` for how to identify risks from the change and for the failure modes to avoid when writing rows.

**Relationship to the form.** The register is the source of truth for risk. The top risk summary field on the form is a one-sentence rendering of R1, and the risk rating field must be consistent with the most severe row here.

**If the change genuinely has no material risk,** record one row stating that and the reason it holds for this specific change. Do not leave the table empty. Pressure-test that conclusion before accepting it.

### Step 5 — Verify before presenting

Re-read every drafted field and every register row. For each one, identify the specific artefact or statement it came from. Anything you cannot trace becomes `[NEEDS INPUT: <specific question>]` — including content that feels obviously correct.

Then run the cross-field consistency checks at the end of `references/field-guide.md`.

This self-check reduces fabrication. It does not eliminate it: a drafted answer can be internally consistent, well-sourced in appearance, and still wrong about the change. The named business approver and the CAB remain the real controls.

### Step 6 — Present

Deliver:

1. A document containing the drafted field answers, grouped by form section, ready to transfer into the form.
2. The filled-in register, via `present_files`.

Open the covering note with the list of `[NEEDS INPUT]` gaps the developer must close before submitting. Put it first, not last.

Do not submit the form. A human submits it.

---

## Guardrails

These are not advisory. If a change fails one of them, say plainly that it is not CAB-ready rather than drafting around it.

- **No named business approver means not CAB-ready.** The approver field requires an individual, and the approval-evidence field requires the record of them agreeing. A team name, "the client", or a verbal recollection does not satisfy this.
- **Rollback is mandatory.** If there is no rollback mechanism, the change is not ready. Absent or unreversible rollback must be stated, not smoothed over.
- **Emergency changes still require a register.** Emergency is a change type, not a bypass. The register may be short; it may not be missing.
- **The risk rating must be consistent with the register.** If the register carries a High-likelihood row, or a row whose impact reaches money, customer data, or production availability, the rating cannot be Low. Where the developer's stated rating and the register disagree, raise it with them rather than silently adopting either.
- **Flag internet-facing changes that have not been penetration tested.** If the change is reachable from the public internet and no penetration testing has been done, state that explicitly in the covering note. The CAB will ask; do not let it arrive as a surprise.

---

## Maintenance

| | |
|---|---|
| **Owner** | [NEEDS INPUT: who owns this skill and maintains it?] |
| **Last reviewed** | 18 August 2026 |
| **Form version** | CAB Requests, Microsoft Forms, structure as at 18 August 2026 — six sections, twenty-five fields |

The field numbering in `references/field-guide.md` is tied to that form version. If the Microsoft Form changes — fields added, removed, reordered, or moved between sections — re-verify the field guide against the live form before relying on this skill. Numbering drift is silent and will misfile answers.

---

## References

- `references/field-guide.md` — Field numbering, what each field asks, where the answer is found, pass and fail criteria, and cross-field consistency checks.
- `references/risk-patterns.md` — Checklist for reading a change and identifying real risks; rules for what a register row must contain.
- `references/style-guide.md` — Writing rules for every field.
- `assets/risk-register-template.md` — Empty register template: metadata block and six-column risk table, no instructions. Copy before filling in. Completion rules are in Step 4 above.
