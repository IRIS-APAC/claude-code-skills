---
name: cab-request-filler
description: Drafts a Change Advisory Board (CAB) request submission for a production or demo release — answers for all twenty-five CAB Requests form fields, plus the testing evidence, deployment document and Risk & Mitigation Register the form asks for — from the developer's own repository and project artefacts. Use when the user explicitly mentions a CAB by name, including "CAB request", "CAB form", "CAB submission", "change advisory board", "prep the CAB", "raise a CAB", or "emergency CAB", and when they ask to fill in, draft, or complete a CAB submission for a specific change. Also use when the user asks to prepare the approval paperwork, the deployment, PVT or rollback steps, or the risk register for a named production or demo deployment and the CAB is unambiguously the approval route. Do NOT use for general questions about what a CAB is, who sits on it, when it meets, or how the process works — answer those directly. Do NOT trigger merely because a deployment doc, PR, or release notes were shared.
---

# CAB Request Filler

Drafts a submission for the internal CAB Requests form: answers for every form field, plus the files attached to it — testing evidence, a deployment document, and a filled-in Risk & Mitigation Register.

A demo release counts as a production release here: it needs a CAB request too.

This skill drafts. It does not attest. The named business approver and the CAB itself are the controls that decide whether a change is safe to deploy.

---

## The anti-fabrication rule

**Every answer must trace to something the user supplied or the repository shows** — a pull request, a diff, a repository, a deployment document, a ticket, test output, infrastructure or pipeline configuration, or an explicit statement from the developer.

If a field cannot be answered from supplied context, write:

```
[NEEDS INPUT: <specific question>]
```

Never infer an answer from what changes like this usually involve, from what sounds plausible for the technology in play, or from anything in this skill's own guidance. This skill describes what a good answer *contains*; it does not supply answers.

A visible gap is a safe outcome. A plausible-sounding wrong answer is not: it can carry a change into production on the strength of a claim nobody made. When in doubt, mark it `[NEEDS INPUT]` and let the developer close it.

This applies with equal force to the register. Do not populate a risk row because the change resembles a category in `references/risk-patterns.md`. That file is a prompt for reading the change, not a source of risks.

---

## Outputs

Write the files to `cab/<repo>-release-<YYYY-MM-DD>/` in the repository's **parent** folder, where the date is the change date. Keeping them outside the repository means nothing is committed by accident.

| File | Form field |
|---|---|
| `testing-evidence.txt` | Testing Evidence |
| `deployment-document.docx` | Deployment Doc (generated only if the developer has none) |
| `risk-and-mitigation-register.docx` | Risk & Mitigation Register |

The developer supplies the business approval (a required upload) and any penetration test report. The skill cannot produce either.

---

## Rollback: one procedure back to the previous version

The rollback is **one** numbered procedure, not a menu of options. Whoever rolls back under pressure should not have to choose.

A rollback returns production to the **exact version that was live before**, through the **same pipeline** that deployed the release. Either of these qualifies:

- **Redeploying the previous version** — its release tag, commit or image — where the pipeline accepts one.
- **An exact revert** — a revert of the release merge(s) that restores the previously-live tree, with `git diff <live-sha> <revert-head>` empty for the deployed paths, merged through the normal PR path and dispatched through the same pipeline. On estates where the deploy credentials trust only branch refs, this is often the only executable route. Revert every merge since the live commit, not just this release's. If the live build matches no commit on the deploy branch — built by hand, or from another branch — no exact revert exists.

These are not rollbacks, so leave them out:
- **A hand-written fix**, or any revert that does not restore the live tree exactly. This is new code that has never run in production.
- **"Roll forward with a fix."** That is a new change.
- **Manual console changes or administrator click-ops.** These cause drift between the code, the infrastructure state and the account, and leave no audit trail.

The procedure covers, in order: getting back to the previous version (plan first if the pipeline has a plan step); reversing data changes if the release made any (a down-migration, or restoring the snapshot taken before deployment); re-running the PVT steps against the previous version; and notifying users and recording the cause. The stated duration includes review and merge time when the route is a revert.

**If neither route exists**, the change is not CAB-ready. Do not cover the gap with a hand-written fix or console steps. Tell the developer, record it as a High-likelihood row in the register, and recommend closing it — for example by giving the deploy workflow a version input.

---

## Workflow

### Step 1 — Gather context

Start from the repository: read the repo, the release branch or PR, and use `gh` for merged PRs, deploy workflow runs and release tags. Then ask for what is still missing in a single message, and wait. Do not begin drafting on the assumption the answers will arrive.

- **The change itself** — repository and branch, pull request, diff, release notes, or deployment document. Read what is supplied directly rather than asking the developer to summarise it.
- **Everything going live** — all changes merged since the last deploy to this environment, not only the release headline. Take the baseline from the commit that is live now: the last successful deploy run, the release tag, or the commit in the live image tag. If none can be established, list the changes from the release PR and mark the baseline `[NEEDS INPUT]`.
- **What is live now** — version, tag, commit, image and configuration such as model or feature flags, and the last deploy date. This is the rollback target, so confirm its artefact still exists.
- **Client or internal, and project name.**
- **Change type and pre-approval status** — Standard, Emergency or Pre Approved, and whether a standing approval applies. Always ask; never infer.
- **Change window** — date, start time, end time, timezone.
- **Business approver** — the named person, and where their approval is recorded. Always ask; never infer.
- **Testing** — anything beyond what the repository and CI show, such as UAT.
- **Impacted users** — who is affected, and roughly how many.
- **Security posture** — penetration testing status, and anything about network exposure the infrastructure code does not show.

If an artefact already answers one of these, do not ask for it again. If the developer says to draft with what is on hand, do so and mark the rest `[NEEDS INPUT]`. If nobody can answer — a scheduled or non-interactive run — do not wait: draft with what is on hand and mark the rest `[NEEDS INPUT]`.

### Step 2 — Read the change and how it deploys

Before drafting any field, read the supplied artefacts and build your own picture of what changes: which components, which endpoints, which tables, which jobs, which configuration. Note anything that changes behaviour rather than only implementation, and anything irreversible.

Then read the deploy workflow, the infrastructure code and any runbooks, so the deployment, verification and rollback fields describe how this repository actually deploys. Note what the deploy touches and what must never be replaced: databases, buckets, keys, stored state. Two findings make the change not CAB-ready, and each becomes a High-likelihood row in the register until it is closed:

- **The deploy is not dispatch-only.** A deploy may start only from a manual `workflow_dispatch` after approval. One that runs on push, merge, tag, release or schedule would deploy without, or before, approval.
- **There is no rollback route** as defined above.

You cannot draft the deployment, verification, rollback, or risk fields honestly without this step. If the artefacts are too thin to support it, say so and ask for more rather than drafting around the gap.

### Step 3 — Run the tests and capture evidence

Run the checks in a temporary git worktree of the release head, so coverage files and caches stay out of the developer's checkout; remove it afterwards. Run the unit tests with coverage and any other checks that are safe to run locally: fixtures, lint, security scans, infrastructure plan or validate. Run linters and pre-commit at the versions the repository pins, in check-only mode with no auto-fix; if a check cannot run at its pinned version, cite CI instead of reporting a local finding. Do not run integration tests against live environments; cite the CI run for the head instead (`gh pr checks`). Write `testing-evidence.txt` from the real output:

```
<Service> — release testing evidence
Release: <branch> -> <target>
Commit under test: <full sha>
Generated: <YYYY-MM-DD HH:MM TZ> on <uname -sr>
<Runtime>: <version>

================================================================
1. <Check name>
   Command: <exact command>
================================================================
<raw output; trim only noise such as deprecation warnings>

================================================================
<N>. CI results for <sha>
   Command: gh pr checks <pr>
================================================================
<output>
```

Testing Completed is not a checklist to complete. Tick only the options where testing was actually done and mark the rest unticked. One tick is enough, and it can be Other. Do not run new kinds of testing, or stretch a result to fit an option, just to tick more boxes.

### Step 4 — Draft the fields

Work through the form in order, using `references/field-guide.md`. That file holds the field numbering, what each field is really asking, where the answer is normally found in a project, and the criteria an answer must meet to pass.

Apply the rules in `references/style-guide.md` to every field.

### Step 5 — Write the deployment document

If the developer has a deployment document, check it against the deployment, verification and rollback fields; the two must not diverge. If there is none, generate `deployment-document.docx` (use the docx skill if available, otherwise python-docx). Under the title, add one line: service — release · version · prepared date · author. Sections:

1. Change summary: a table of Service, Release, Environment, Change window, Deploy mechanism, Currently live (the rollback target), Target and Implementer.
2. What is being deployed: each change or feature going live, the infrastructure touched, and whether there is a data migration.
3. Pre-deployment checks: include recording the live version, confirming its artefact exists, and taking a data snapshot if the release changes data.
4. Deployment steps: numbered, with the exact commands.
5. Post-deployment verification (PVT): numbered checks, each with where to look and the expected signal.
6. Rollback: the triggers, then the single numbered procedure with exact commands, then its duration.
7. Impacted users and communication: what users see during the window and after it.
8. Testing summary: a table of Test | Result | Detail, pointing to `testing-evidence.txt`.
9. Security: first deployment, internet exposure, infrastructure and endpoint changes, and security testing, each with its basis.

### Step 6 — Build the Risk & Mitigation Register

Copy `assets/risk-register-template.md` to a working location and fill it in. The template holds only the two tables — a change metadata block and an empty risk table with six columns. It carries no completion rules, so the rules for filling it in are here.

**Structure of the template.** The metadata block has six labelled rows: Client, Project, Change ID, Change date, CAB date, Prepared by. The risk table has six columns in this order: ID, Risk, Likelihood, Impact if realised, Mitigation, Owner. Five empty rows are provided; add or delete rows to match the number of risks. Do not add columns, rename headers, or reorder them — the CAB reads these registers side by side across submissions.

**Completing the metadata block.** Fill every row from the developer's supplied context. Change ID is the CAB or change-management number if one exists, otherwise the release tag or branch; use a PR number only if nothing else tracks the change. If none exists, mark it `[NEEDS INPUT]` rather than inventing a format. CAB date is the meeting the change is being submitted to, which is not the same as the change date. Prepared by is the person drafting the submission, who may differ from the risk owners.

**Completing the risk table.**

1. Add one row per material risk identified by reading the change in Step 2. Risks come from the artefacts, never from the categories in `references/risk-patterns.md`.
2. Order rows most severe first and number them R1, R2, R3 upward. Severity is likelihood weighed against impact, not likelihood alone.
3. Every row must name the specific component, table, endpoint, service, queue, or job that this change affects. A row that would read as sensible with the project name removed is too generic and does not belong in the register.
4. **Likelihood** is High, Medium, or Low — the honest chance with the controls that already exist, not before them. A failure mode that has never run in production should not be recorded as Low purely because it has not happened yet.
5. **Impact if realised** states the consequence for the business, its users, or its data. Describe the outcome, not the internal code behaviour that produces it.
6. **Mitigation** states a specific action that reduces likelihood or impact, citing the evidence from Step 3 or the step in the deployment document. Monitoring qualifies only if the row names the signal watched, who watches it, and the action that follows. Removing the risk from the cutover — for example by disabling the affected path at go-live — is stronger than observing it.
7. **Owner** is a named individual accountable for the mitigation, including after go-live. Not a team. If the developer has not named one, write `[NEEDS INPUT: owner for R<n>]`. Do not default to the implementer: owning a mitigation after go-live is a commitment only that person can make.
8. Delete any unused empty rows.
9. Save the result as `risk-and-mitigation-register.docx` in the output folder (use the docx skill if available, otherwise python-docx).

See `references/risk-patterns.md` for how to identify risks from the change and for the failure modes to avoid when writing rows.

**Relationship to the form.** The register is the source of truth for risk. The top risk summary field is a short paragraph on the two or three most severe rows, R1 first, with what covers them and any known gap. The risk rating field must be consistent with the most severe row.

**If the solution is on the public internet and has not been penetration tested,** that is a row in the register as well as a line in the covering note.

**If the change genuinely has no material risk,** record one row stating that and the reason it holds for this specific change. Do not leave the table empty. Pressure-test that conclusion before accepting it.

### Step 7 — Verify before presenting

Re-read every drafted field and every register row. For each one, identify the specific artefact or statement it came from. Anything you cannot trace becomes `[NEEDS INPUT: <specific question>]` — including content that feels obviously correct.

Then run the cross-field consistency checks at the end of `references/field-guide.md`, and these:

- Every number in the answers — tests passed, coverage, versions — appears in `testing-evidence.txt` or the deployment document.
- The rollback steps form one procedure back to the previous version, as defined above.
- Every ticket or PR reference follows a plain-words description; none stands in for one.

This self-check reduces fabrication. It does not eliminate it: a drafted answer can be internally consistent, well-sourced in appearance, and still wrong about the change. The named business approver and the CAB remain the real controls.

### Step 8 — Present

Print the answers in chat, all twenty-five in form order, with the numbering and question wording from the field-guide headings, ready to transfer into the form:

- Choice fields: the option, with a short basis in brackets where the field guide asks for one.
- Testing Completed: one line per option (Unit Testing, Code coverage > 80%, UAT Testing, Other), each marked ✅ or ❌ with its result.
- Deployment, PVT and Rollback Steps: numbered lists.
- Upload fields: the absolute path of the generated file, or what the developer must attach.

Open with the list of `[NEEDS INPUT]` gaps and the files the developer must supply, business approval first. Put it first, not last.

Do not submit the form. A human submits it.

---

## Guardrails

These are not advisory. If a change fails one of them, say plainly that it is not CAB-ready rather than drafting around it.

- **No named business approver means not CAB-ready.** The approver field requires an individual, and the approval-evidence field requires the record of them agreeing. A team name, "the client", or a verbal recollection does not satisfy this.
- **Rollback is mandatory and must be a real rollback.** If neither route to the previous version exists, the change is not ready. Absent or unreversible rollback must be stated, not smoothed over.
- **Deploys start from a manual dispatch after approval.** A pipeline that deploys on push, merge, tag, release or schedule is a gap to close before CAB.
- **Emergency changes still require a register.** Emergency is a change type, not a bypass. The register may be short; it may not be missing.
- **The risk rating must be consistent with the register.** If the register carries a High-likelihood row, or a row whose impact reaches money, customer data, or production availability, the rating cannot be Low. Where the developer's stated rating and the register disagree, raise it with them rather than silently adopting either.
- **Flag internet-facing changes that have not been penetration tested.** If the change is reachable from the public internet and no penetration testing has been done, state that explicitly in the covering note and the register. The CAB will ask; do not let it arrive as a surprise.

---

## Maintenance

| | |
|---|---|
| **Owner** | [NEEDS INPUT: who owns this skill and maintains it?] |
| **Last reviewed** | 15 October 2026 |
| **Form version** | CAB Requests, Microsoft Forms, structure as at 15 October 2026 — six sections, twenty-five fields; Testing Completed includes an Other option |

The field numbering in `references/field-guide.md` is tied to that form version. If the Microsoft Form changes — fields added, removed, reordered, or moved between sections — re-verify the field guide against the live form before relying on this skill. Numbering drift is silent and will misfile answers.

---

## References

- `references/field-guide.md` — Field numbering, what each field asks, where the answer is found, pass and fail criteria, and cross-field consistency checks.
- `references/risk-patterns.md` — Checklist for reading a change and identifying real risks; rules for what a register row must contain.
- `references/style-guide.md` — Writing rules for every field.
- `assets/risk-register-template.md` — Empty register template: metadata block and six-column risk table, no instructions. Copy before filling in. Completion rules are in Step 6 above.
