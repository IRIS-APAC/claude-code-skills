# Style guide

Writing rules for CAB submissions. These are stated in full so they can be followed by someone who has never seen a previous submission.

---

## Language

- **Plain English.** Short words over long ones. If a shorter word carries the same meaning, use it.
- **Sentence length: aim for twenty words or fewer.** Sentences above roughly thirty words should be split. One idea per sentence.
- **Active voice with a stated actor.** Write who does the thing. "The trigger is re-enabled after verification" hides the actor; name the role or person who re-enables it.
- **Present or simple future tense.** Describe what the change does and what will be done, not what has been contemplated.
- **No marketing language.** No seamlessly, robustly, leverages, enables, unlocks, streamlines, cutting-edge, best-in-class. A CAB is assessing risk, not being sold to.
- **No confidence padding.** Best effort, should be fine, unlikely to be an issue, and minimal impact assert a conclusion without evidence. Either state the evidence or state the uncertainty.
- **No hedging into vagueness.** Some, various, certain, a number of, and potentially conceal information the CAB needs. Give the number, or say the number is unknown.
- **One term per concept throughout the submission.** If a component has a name, use that name every time. Do not alternate between the service name, the repository name, and a colloquial shorthand.
- **One referent for the team.** Pick we, the delivery team, or named individuals, and hold it consistent within a field.
- **Expand every acronym on first use** in each field. Fields are read independently and often out of order.
- **No emoji, and no decorative characters** used to structure text. Numbered lists and short headings carry structure. The one exception is Testing Completed, where ✅ and ❌ mirror the form's checkboxes.

## Numbers, dates, and identifiers

- Give timezones with every time.
- Give versions, branches, and commit identifiers exactly as they appear in the repository.
- Describe each change in plain words. A ticket, PR or change reference may follow as an identifier, never in place of the description.
- Give counts where a count is knowable. Where it is not, say so rather than gesturing at scale.

## How much detail each field warrants

- **Change identification fields** (client, project, approver, impacted users): a single specific line. No prose.
- **What is being deployed**: enough for a technically literate reader who has not seen the code to understand what changes in production and why it carries risk. Group by component. Distinguish behavioural change from implementation change. Implementation detail belongs in the attached deployment document.
- **Deployment steps**: an ordered list, one action per step, naming the actual mechanism and the parameters that matter. Written so a competent colleague who is not the author could execute it.
- **Verification steps**: an ordered list, one check per step. Each names where to look and what signal confirms success.
- **Rollback steps**: one ordered list — a single procedure back to the previously-live version. Names the mechanism and the version, states data reversibility, states execution time, and names anything that cannot be reversed.
- **Top risk summary**: one short paragraph — the two or three most severe risks, R1 first, what covers them, and any known gap. Not a list.
- **Register rows**: one or two sentences per cell. Specific to the component affected.
- **Security fields**: the selection, with any compensating control described in the deployment description rather than argued in the security field.

## The risk row format

Every register row has six cells, in this order:

1. **ID** — R1, R2, R3, ordered most severe first.
2. **Risk** — the failure mode in one sentence, naming the specific component, table, endpoint, service, queue, or job affected by this change.
3. **Likelihood** — High, Medium, or Low. The honest chance with existing controls in place.
4. **Impact if realised** — the consequence for the business, its users, or its data. The outcome, not the internal code behaviour.
5. **Mitigation** — a specific action that reduces likelihood or impact. Monitoring qualifies only with the signal, the watcher, and the follow-up action stated.
6. **Owner** — a named individual, not a team.

Do not open a risk cell with "There is a risk that". State the failure mode directly.

## Structural conventions

- Number sequential steps. Do not bullet things that must happen in order.
- Keep headings short and factual.
- Where a field's content has natural groups, label the groups. Do not run three subjects together in one block of prose.
- Do not paste design-document prose into a CAB field unedited. Design documents explain and persuade; CAB fields state and evidence.

## Marking gaps

Where an answer is not available from supplied context, write `[NEEDS INPUT: <specific question>]` in place of the answer. The question must be answerable — name the artefact or decision needed. A gap marked this way is a correct outcome, not a failure of the draft.
