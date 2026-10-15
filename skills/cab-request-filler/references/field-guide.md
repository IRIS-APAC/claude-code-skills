# Field guide

Field numbering for the CAB Requests form (structure as at 15 October 2026: six sections, twenty-five fields; Testing Completed includes Other). This file is the only place field numbers appear — SKILL.md refers to fields by name.

For each field: what the CAB is actually trying to establish, where the answer is normally found in a project, and the criteria that separate an answer that passes from one that gets sent back.

**No sample answers appear in this file by design.** Criteria describe the shape of a good answer. They are not content to be adapted. Every answer must come from the developer's own artefacts — see the anti-fabrication rule in SKILL.md.

---

## Section 1 — Change Details

### Q1. Client (or Internal) — single line, required

**What it is asking.** Whose risk this is, and therefore whose contractual and reputational exposure sits behind the change. It also determines whether client-side approval is needed at all.

**Where the answer is found.** The engagement or project record; the repository owner or naming convention; the developer.

**Passes when** it names the specific client, or states `Internal` for changes to systems the organisation owns and operates itself.

**Sent back when** it carries a generic placeholder that does not identify the party — the literal word "Client" with no name attached does not tell the CAB whose exposure is in play. Confirm the intended convention with the CAB chair if the form does not state it.

---

### Q2. Project Name — single line, required

**What it is asking.** Which body of work this change belongs to, in the terms the CAB uses to track it across submissions.

**Where the answer is found.** The engagement or delivery plan; the board or workstream name; the developer.

**Passes when** it is the name the CAB will recognise and can match to earlier submissions for the same work.

**Sent back when** it is a repository name, a branch name, or an internal abbreviation that only the delivery team uses.

---

### Q3. What is being deployed? — multi-line, required

**What it is asking.** What will be different in production after this change, in enough detail that the CAB can judge the risk without reading the code. This field carries the submission: a CAB member who understands this field can approve; one who does not will send the change back regardless of how complete the rest is.

**Where the answer is found.** The pull request description and the diff; the commit range between the current production release and the release candidate; release notes; the deployment document; migration files; configuration diffs.

**Passes when** it states which components are deployed and from which branch or commit to which environment; separates behavioural change from implementation change; names any components that must be released together and why; and calls out changes that alter automated decisions, routing, eligibility, or anything that moves money or grants access.

**Sent back when** it lists commit messages or ticket titles instead of describing behaviour; describes implementation at a level of detail that belongs in the deployment document; or omits a coupling between components that the diff shows exists.

**Depth.** Enough for a technically literate reader who has not seen the code. Not a code review.

---

### Q4. Risk Rating — single choice (High / Medium / Low), required

**What it is asking.** The submitter's own severity judgement, which the CAB uses to decide how much scrutiny to apply and whether the change needs discussion or can be approved on the papers.

**Where the answer is found.** Derived from the completed register — not chosen independently of it.

**Passes when** it is consistent with the most severe row in the register. If the developer has stated no rating, give the register's and say that is where it came from.

**Sent back when** it is lower than the register supports. A register carrying a High-likelihood row, or a row whose impact reaches money, customer data, or production availability, cannot sit under a Low rating. Where the developer's stated rating and the register disagree, raise it with them; do not silently adopt either.

---

### Q5. Change Type — single choice (Standard / Emergency Change / Pre Approved Change), required

**What it is asking.** Which approval path applies, and therefore what lead time and evidence the CAB expects.

**Where the answer is found.** The developer, informed by the change window and whether a documented pre-approval covers this change class.

**Passes when** the type matches the actual circumstances: Standard for normal lead time; Emergency where the change is needed inside that lead time, with the reason stated in the deployment description; Pre Approved only where a documented pre-approval covers exactly this class of change.

**Sent back when** Emergency is used to compress lead time without a stated reason, or Pre Approved is claimed without a pre-approval that can be pointed to.

---

### Q6. Is this an ongoing pre-approved change? — single choice (No / Yes (Without Notification) / Yes (With CAB Notification)), optional

**What it is asking.** Whether this change recurs under a standing approval, and if so whether the CAB still wants to be told each time.

**Where the answer is found.** The standing approval record, if one exists; the developer.

**Passes when** it is No, or Yes with a pre-approval that can be identified.

**Sent back when** Yes is selected and no standing approval can be produced.

---

## Section 2 — Business Approval

### Q7. Business Approver — single line, required

**What it is asking.** Which named individual on the business side has accepted the change and its consequences. This is the accountability anchor of the whole submission.

**Where the answer is found.** The approval email, chat message, or ticket; the developer; the engagement lead.

**Passes when** it names an individual with the standing to accept the change on the business's behalf.

**Sent back when** it names a team, a role with no person attached, or the client organisation generally. Per the guardrails in SKILL.md, absence of a named approver means the change is not CAB-ready — do not draft around it.

---

### Q8. Attach Approval (Email, Teams screenshot, etc) — file upload, required

**What it is asking.** Evidence that the named approver actually agreed, so approval does not rest on the submitter's recollection.

**Where the answer is found.** The approver's email, chat message, or ticket comment.

**Passes when** the attachment shows the approver, the change they approved, and the date.

**Sent back when** it is a summary of the approval written by the submitter, an approval for a different or earlier version of the change, or a link to a location the CAB cannot open.

**Note.** This field takes a file. The skill cannot produce it; flag it as an attachment the developer must supply.

---

## Section 3 — Testing

### Q9. Testing Completed — multiple choice (Unit Testing / Code coverage > 80% / UAT Testing / Other), required

**What it is asking.** Which categories of verification have actually been completed, so the CAB can weigh how much confidence the change has earned before production.

**Where the answer is found.** CI pipeline output; coverage reports; the test suite; UAT sign-off records; the developer.

**Passes when** every ticked option reflects work that has been completed and can be evidenced.

**Sent back when** an option is ticked because it is planned, in progress, or usually done. Coverage above eighty per cent requires a coverage figure, not an impression. UAT requires that user acceptance testing occurred, not that the change was demonstrated to someone.

**Not a checklist to complete.** One ticked option is enough, and it can be Other. Security scans, fixture harnesses, infrastructure plan runs and end-to-end runs belong under Other, each with its result.

---

### Q10. Testing Evidence — file upload, optional

**What it is asking.** Proof for the claims made in the testing field.

**Where the answer is found.** Coverage report output; CI run summaries; UAT sign-off; test result exports.

**Passes when** the evidence corresponds to the options ticked and to the code being deployed.

**Sent back when** the evidence predates the final state of the change, or covers a different component.

---

## Section 4 — Deployment

### Q11. Change Date — date, required

**What it is asking.** When production will be touched, so the CAB can check the window against other changes, business calendars, and support cover.

**Where the answer is found.** The developer; the deployment plan; the agreed client window.

**Passes when** it is a specific date consistent with the change type — an Emergency change dated three weeks out is a contradiction the CAB will notice.

---

### Q12. Start Time — single line, required

**What it is asking.** When the window opens, in a form that is unambiguous to readers in other timezones.

**Where the answer is found.** The developer; the agreed window.

**Passes when** it states a time and a timezone.

**Sent back when** the timezone is missing.

---

### Q13. End Time — single line, required

**What it is asking.** When the window closes — the point by which the change is either verified or rolled back.

**Where the answer is found.** The developer; the deployment plan's own timings.

**Passes when** it is a realistic close covering deployment, verification, and the decision to keep or reverse. Not the moment the last deploy command finishes.

**Sent back when** the window is too short to contain the verification steps listed elsewhere in the submission.

---

### Q14. Deployment Steps — multi-line, required

**What it is asking.** Exactly what will be done to production, in order, so the CAB can see the change is planned rather than improvised, and so someone other than the author could execute it.

**Where the answer is found.** The deployment document; pipeline and workflow definitions; infrastructure-as-code plans; migration files; deployment scripts and their parameters.

**Passes when** it is an ordered sequence naming the actual mechanism for each step — pipeline, workflow, script, or command, with the parameters that matter; places any dry-run, plan, or staging step before the step it de-risks; states the required order where components or configuration must be applied in sequence; and names any automation, trigger, or schedule that must be disabled before deployment and re-enabled after verification. The deploy starts from a manual dispatch after approval.

**Sent back when** steps are described in intent rather than mechanism; ordering is left implicit where it matters; a disable step appears with no corresponding re-enable; or the pipeline deploys on push, merge, tag, release or schedule rather than from a manual dispatch.

---

### Q15. PVT Steps — multi-line, required

**What it is asking.** How the submitter will know the change worked, before automation resumes and before the window closes. This is what separates a deployment from a hope.

**Where the answer is found.** The deployment document; monitoring and log destinations for the affected components; acceptance criteria on the ticket; the queries or endpoints used to verify the change in lower environments.

**Passes when** each check names where to look — log group, table, endpoint, queue, dashboard, or screen — and what signal confirms success; the checks cover the behaviour the change actually alters, not only that the service starts; and any known-benign warning that will still appear is called out so verification is not failed on it.

**Sent back when** checks are stated as intentions to observe rather than specific signals; the checks would pass equally well if the change had not been deployed; or the behavioural change described in the deployment field has no corresponding check.

---

### Q16. Rollback Steps — multi-line, required

**What it is asking.** How production gets back to a known-good state if the change fails, and what cannot be undone. The CAB is weighing whether a failure is recoverable.

**Where the answer is found.** Migration files and whether down-migrations exist; infrastructure-as-code state and versioning; artefact or release versioning; configuration versioning and retention; the deployment document.

**Passes when** it is one numbered procedure that returns production to the previously-live version, named by tag, commit or image, through the same pipeline that deployed the release — by redeploying that version or by an exact revert, as defined under Rollback in SKILL.md; covers configuration and data as steps within that procedure, stating whether data changes are reversible and, where they are not, saying so plainly; states how long execution takes, including review and merge time for a revert, so the CAB can judge it against the window; names anything that must not be reversed because the effect has already left the system; and re-runs the PVT steps to confirm recovery.

**Sent back when** it offers a menu of options rather than one procedure; it relies on a hand-written fix, a roll-forward, or manual console changes; it describes redeploying the previous version without naming what that version is or where it comes from; data reversibility is unaddressed where the change includes a migration or backfill; or no execution time is given. Per the guardrails in SKILL.md, no rollback route means the change is not ready.

---

### Q17. Deployment Doc — file upload, optional

**What it is asking.** The full plan, for the detail the form's summary fields deliberately exclude.

**Where the answer is found.** The deployment or runbook document for the change.

**Passes when** the attached document is consistent with the deployment, verification, and rollback fields on the form. Divergence between the two is a common and damaging failure — the CAB approves one and the team executes the other.

---

### Q18. Impacted Users — single line, required

**What it is asking.** Who feels this change, and who to warn if it fails. It also sizes the blast radius the register describes.

**Where the answer is found.** The affected system's user base or access records; the ticket; the client contact; the developer.

**Passes when** it identifies the affected group specifically, and gives a count or scale where one is knowable.

**Sent back when** it names a whole organisation without narrowing to those actually affected, or gives a count with no indication of who they are.

---

## Section 5 — Risks and Mitigations

### Q19. Top Risk Summary — multi-line, required

**What it is asking.** The few risks the CAB should hold in mind while reading the rest of the submission — and whether they have been dealt with. It is a triage signal, not a summary of all risks.

**Where the answer is found.** The most severe rows of the completed register.

**Passes when** it is a short paragraph on the two or three most severe risks, R1 first, saying what could go wrong, what covers each, and any known gap. Every risk it names is in the register.

**Sent back when** it restates the change rather than the risks, leaves out R1, or names a risk the register does not contain.

**Depth.** One paragraph. The register carries the rest.

---

### Q20. Risk & Mitigation Register — file upload, required

**Note on form structure.** In the form (first noted 18 August 2026) this field sits under the Security section heading, immediately after the Top Risk Summary. It belongs with the risks section; the boundary appears misplaced. Treat it as part of the risks section. Recommend the correction to the form owner.

**What it is asking.** The full set of risks the submitter identified, with likelihood, impact, mitigation, and an accountable owner for each — the record of what was known at the time of approval.

**Where the answer is found.** Produced by reading the change. See `references/risk-patterns.md` for how to identify risks and what a row must contain.

**Passes when** it uses the register template; carries one row per material risk, ordered most severe first; every row names the specific component, table, endpoint, service, queue, or job this change affects; and every row has a named individual as owner.

**Sent back when** rows are generic enough to apply to any deployment; every row is rated Low with no reasoning; mitigations amount to intending to watch; or owners are teams rather than people.

---

## Section 6 — Security

### Q21. Is this the first time the solution is being deployed? — single choice, required

**What it is asking.** Whether production has ever run this solution, which governs how much unknown-unknown risk the change carries and whether monitoring and alerting are proven.

**Where the answer is found.** Deployment history; the pipeline's run history for the target environment; the developer.

**Passes when** it reflects the actual deployment history of the solution in that environment.

---

### Q22. Is this solution available on the public internet? — single choice, required

**What it is asking.** Whether an attacker without prior access can reach it. This governs how seriously the CAB treats the remaining security fields.

**Where the answer is found.** Infrastructure-as-code; ingress, gateway, front-door, or load-balancer configuration; network and firewall rules; the developer.

**Passes when** it reflects the network path as configured, not as intended.

**Sent back when** the answer is No but the infrastructure shows a public ingress, or the answer treats authentication as equivalent to not being internet-facing. An authenticated endpoint on the public internet is still on the public internet. So is a webhook receiver or function URL.

---

### Q23. Are there changes to infra or additional endpoints? — single choice, required

**What it is asking.** Whether the change alters the attack surface or the production topology, as distinct from changing behaviour within an existing surface.

**Where the answer is found.** Infrastructure-as-code diffs; the infrastructure plan output; new route, function, or service definitions; API definitions.

**Passes when** it reflects the infrastructure diff or plan between the live version and the release. Any added, removed or changed resource, endpoint, permission or network path is a Yes.

**Sent back when** it is No but the diff adds an endpoint, service, queue, storage account, or database, or changes a network path.

---

### Q24. Has there been security/penetration testing? — single choice, required

**What it is asking.** Whether the exposed surface has been tested by someone trying to break it, rather than only by tests confirming it works.

**Where the answer is found.** Penetration test reports; security review records; the security team; the developer.

**Passes when** it reflects testing that actually occurred against this solution.

**Sent back when** vulnerability scanning, dependency scanning, or a code review is presented as penetration testing.

---

### Q25. Security/Penetration testing evidence — file upload, optional

**What it is asking.** The report or record behind the previous answer.

**Where the answer is found.** The penetration test report or security review record.

**Passes when** the evidence covers the solution being deployed and is current enough to be meaningful.

**Where testing has not been done and the solution is internet-facing,** the guardrails in SKILL.md require this to be stated explicitly in the covering note and recorded as a row in the register. Any compensating controls — private endpoints, gateway rules, authentication, network segmentation — should be described in the deployment description field if they exist in the change, and marked `[NEEDS INPUT]` if the developer has not stated them.

---

## Cross-field consistency checks

Run these before presenting. Each one catches a contradiction the CAB will otherwise find.

1. **Risk rating against the register.** The rating must be consistent with the most severe register row. Raise any disagreement with the developer.
2. **Top risk summary against the register.** It opens with R1, and every risk it names is in the register.
3. **Change type against change date.** An Emergency change with a distant window, or a Standard change dated for tonight, needs explaining.
4. **Security answers against each other.** Public internet exposure, plus infrastructure or endpoint changes, plus no penetration testing, is a combination the CAB will question. Surface it rather than let it be discovered.
5. **Deployment steps against rollback steps.** Every forward step should have a reverse, or an explicit statement that it cannot be reversed. Unpaired steps are where failed deployments become incidents.
6. **Deployment steps against the verification steps.** Any automation disabled during deployment must be re-enabled after verification, and the verification must cover the behaviour the change alters.
7. **Attached deployment document against the form fields.** The two must not diverge.
8. **Impacted users against the register's impact column.** If the register describes impact reaching a group the impacted-users field does not mention, one of them is wrong.
9. **Every field against its source.** Per Step 7 of the workflow, anything that cannot be traced to a supplied artefact or an explicit statement becomes `[NEEDS INPUT]`.
