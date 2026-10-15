---
name: cab-request
description: "Prepare a CAB (Change Advisory Board) request for a production release. Drafts the CAB form answers (what is being deployed, risk rating, testing completed, testing evidence, deployment / PVT / rollback steps, impacted users, top risk summary, security questions) and generates the testing-evidence file, deployment document and risk & mitigation register. Use whenever the user mentions CAB, a change request, change approval, a release going to prod that needs sign-off, or asks for deployment, PVT or rollback steps or a risk register for a release, even if they don't say 'CAB'."
---

# CAB Request

Prepare a CAB request for a production release: answers ready to paste into the CAB form, plus the three files the form asks for.

## Outputs

Put the files in `cab/<repo>-release-<YYYY-MM-DD>/` in the repo's **parent** folder (the date is the change window). Keeping them outside the repo means nothing gets committed by accident.

| File | Form question |
|---|---|
| `testing-evidence.txt` | 10 |
| `deployment-document.docx` | 17 |
| `risk-and-mitigation-register.docx` | 20 |

## Writing rules

- **No PR or issue numbers**, in the answers or the documents. Describe each change in words ("the review model moves to Sonnet 5.5"), not "#119". CAB approvers don't work in the repo, so the numbers mean nothing to them.
- **Every set of steps is a numbered list**: deployment, PVT and rollback, in both the answers and the documents. Steps are run in order and people refer back to them by number ("repeat PVT steps 1–4").
- Use plain English, short sentences and active voice. Write for an approver who knows the service but not the code.
- Never invent a test result, version, image tag or command. If you can't find something or can't run it, list it as a gap and ask.

## Rollback: one procedure that redeploys the previous version

The rollback is **one** numbered procedure, not a menu of options. At 2 a.m. with something broken, the person rolling back should not have to choose.

A proper rollback redeploys the **exact version that was live before**, using the **same pipeline** that deployed the release: the same artifact (release tag, commit or image), the same infrastructure code and no new code. The previous version is known to work in production, and a pipeline run leaves an audit trail and keeps state in step with the account.

These are not rollbacks, so leave them out:
- **A hotfix or revert PR.** This is new code written under pressure that has never run in production.
- **Manual console changes or admin click-ops.** These cause drift between the code, the IaC state and the account, and they leave no audit trail.
- **"Roll forward with a fix."** That is a new change, not a rollback.

The procedure covers, in order:
1. Redeploying the previous version through the pipeline, plan first if the pipeline has a plan step.
2. Data, if the release changed any: run the down-migration, or restore the snapshot taken in the pre-deployment checks.
3. Re-running the PVT steps against the previous version.
4. Notifying users and recording the cause.

The deployment document lists the rollback **triggers** (for example, a failed PVT step or an alarm firing) before the procedure, with a rough duration.

**If the pipeline can't redeploy a previous version**, stop and tell the user. For example, it may only deploy the head of a branch and have no version or ref input. Don't cover the gap with a hotfix or console steps. The gap must be closed before CAB, for example by adding a version input to the deploy workflow. Record it as a High risk in the register until it is closed.

## Workflow

### 1. Establish the release
Find these in the repo and with `gh`. Ask the user only for what you can't find.
- The service, the repo, the release branch → target, and the head commit.
- The environment, account and region.
- The change window (date, time, timezone and duration) and the implementer.
- **What is live now**: version, tag, commit, image and config such as the model, plus the last deploy date. This is the rollback target, so confirm that its artifact still exists, for example the image in the registry.
- **Everything going live**: all changes merged since the last production deploy, not just the release headline. Take the baseline from the last deploy run or release tag.

### 2. Read how this repo deploys
Read the deploy workflow, the IaC and any runbooks, so the steps match reality. Check whether it is a manual dispatch or deploys on merge, and whether a plan step comes before apply. Check **whether it can deploy a previous version**; the rollback depends on this (see above). Note what the deploy touches. Note what must never be replaced: databases, buckets, keys and stored state.

### 3. Work out the security answers (Q21–Q25)
Answer from the repo and the account as they are configured, not as intended.
- **Q21 First deployment:** No if step 1 found a live version in this environment. Yes only if the solution has never run there.
- **Q22 Public internet:** Yes if anything in the solution accepts inbound traffic from the internet: a public URL, API gateway, load balancer, function URL or webhook receiver. Authentication doesn't change the answer.
- **Q23 Infra or endpoint changes:** Yes if the IaC diff or plan between the live version and the release adds, removes or changes any resource, endpoint, permission or network path. Check the plan, not the PR titles.
- **Q24 Security/penetration testing:** Yes only if someone tested this solution by trying to break it, through a penetration test or a security assessment. Scanners (Semgrep, Trivy, dependency scans) and code review are not penetration testing, so list them under Q9 Other.
- **Q25 Evidence:** the path to the penetration test report. Leave it blank if Q24 is No.

If Q22 is Yes and Q24 is No, add a risk row to the register and point it out when presenting the answers. The CAB will ask, so it should hear it from you first.

### 4. Run the tests and capture evidence (Q9, Q10)
On the release head, run the unit tests with coverage. Also run every other check the repo has: integration tests, fixtures, lint and security scans. Add the CI results for the head (`gh pr checks`). Write `testing-evidence.txt` from the real output:

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
```

If the user supplies screenshots instead, give their paths in Q10.

### 5. Generate the documents (Q17, Q20)
Write both as Word .docx files. Use the docx skill if it's available; otherwise use python-docx. Make PDF only if asked. Under each title, add one line: service — release · version · prepared date · author.

**Deployment document**
1. Change summary: a table of Service, Release, Environment, Change window, Deploy mechanism, Currently live (the rollback target), Target and Implementer.
2. What is being deployed: the list of changes and features going live, and the infrastructure touched. Say explicitly whether there is a data migration.
3. Pre-deployment checks: include recording the live version and confirming its artifact exists. Take a data snapshot if the release changes data.
4. Deployment steps: numbered, with the exact commands.
5. Post-deployment verification (PVT): numbered checks, each with its expected result.
6. Rollback: the triggers, then the single numbered procedure with exact commands, then a rough duration.
7. Impacted users and communication: what users see during the window and after it.
8. Testing summary: a table of Test | Result | Detail, pointing to `testing-evidence.txt`.
9. Security: first deployment, internet exposure, infrastructure and endpoint changes, and security testing, each with its basis.

**Risk & mitigation register** (landscape)
- **Overall risk rating** (Low, Medium or High): the highest rating that remains after mitigation, with one paragraph explaining why. This is also the Q4 answer.
- A table of ID | Risk | Impact | Likelihood | Severity | Rating | Mitigation | Contingency | Owner.
- A rating key for High, Medium and Low.

Find risks in these places: behaviour changes (model, library, config), how many changes go live at once, first use of a new pipeline or permission, state that could be replaced, external dependencies, rollback limits, gaps in alerting, approval and compliance gaps, and cost. Each mitigation cites evidence from step 4 or a step in the deployment doc. The contingency is the rollback procedure, or a named step in it.

### 6. Answer the form
Print the answers in chat in this format, keeping the CAB form's numbering.

**Q9 is not a checklist to complete.** Tick (✅) only the categories where testing was actually done, and mark the rest ❌. One ticked box is enough, and that box can be Other. Don't run new kinds of testing or stretch a result to fit a category just to tick more boxes. An honest "Other: integration tests passed" is better than a padded form.

```
3. What is being deployed?
<The service, the target environment and how it is deployed, in one or two sentences.>
- <change or feature going live, in plain words: what it does>
- <...>

<Data migration: yes/no.>

4. Risk Rating: <Low | Medium | High>

9. Testing Completed:
- ✅/❌ Unit testing: <N passed>
- ✅/❌ Code coverage > 80%: <X%>
- ✅/❌ UAT: <done, or not done and what covers it>
- ✅/❌ Other:
  - <check: result>

10. Testing Evidence: <absolute path>

14. Deployment Steps
1. <step summarised; the exact commands stay in the doc>

15. PVT Steps
1. <check and its expected result>

16. Rollback Steps
1. <step: redeploy the previous version through the pipeline>

17. Deployment Doc: <absolute path>

18. Impacted Users: <who; internal or external; client impact>

19. Top Risk Summary
<One paragraph: the 2–3 biggest risks, what covers them, and any known gap.>

20. Risk & Mitigation Register: <absolute path>

21. Is this the first time the solution is being deployed: <Yes | No> (<basis>)

22. Is this solution available on the public internet: <Yes | No> (<what is reachable>)

23. Are there changes to infra or additional endpoints: <Yes | No> (<what changes>)

24. Has there been a security/penetration testing: <Yes | No>

25. Security/Penetration testing evidence: <absolute path, or blank>
```

### 7. Check before handing over
- Search the answers and both docs for `#\d+`. Any match is a PR or issue number, so remove it.
- Confirm that every number in the answers (tests passed, coverage, versions) appears in `testing-evidence.txt` or the doc.
- Confirm that the Q4 rating matches the register's overall rating.
- Read the rollback steps once more. They must form one procedure that redeploys the previous version through the pipeline, with no hotfix, revert PR or console step.
- If Q22 is Yes and Q24 is No, confirm the register has a row for it.
