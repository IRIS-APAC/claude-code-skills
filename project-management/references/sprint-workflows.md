# Sprint Workflows

Agile sprint management best practices.

## Sprint Planning

### Pre-Planning Preparation

**Before the sprint planning meeting**:
1. **Product backlog is refined** - Stories have clear acceptance criteria and estimates
2. **Dependencies identified** - Blockers resolved or documented
3. **Team velocity known** - Average points from last 2-3 sprints
4. **Sprint goal drafted** - High-level objective for the sprint

### Sprint Planning Meeting

**Agenda** (typically 2 hours for 2-week sprint):

1. **Review sprint goal** (15 min)
   - Product Owner presents objective
   - Team discusses feasibility
   - Agreement on priority

2. **Review team capacity** (10 min)
   - Calculate available points based on velocity
   - Account for holidays, planned absences
   - Adjust for known constraints

3. **Select stories** (60 min)
   - Start with highest priority
   - Ensure stories meet Definition of Ready
   - Discuss technical approach
   - Confirm estimates still accurate
   - Stop when capacity reached

4. **Define sprint backlog** (20 min)
   - Finalize list of committed stories
   - Identify dependencies
   - Plan story sequencing

5. **Confirm sprint goal** (15 min)
   - Verify selected stories achieve goal
   - Get team commitment

### Definition of Ready

Before adding story to sprint, verify:
- [ ] Story has clear, testable acceptance criteria
- [ ] Story is estimated with story points
- [ ] Story has no unresolved blockers or dependencies
- [ ] Story is appropriately sized (ideally S or M, max L)
- [ ] Technical approach is understood
- [ ] Required resources/access available

### Capacity Planning

**Calculate team capacity**:
```
Available Points = Average Velocity × Capacity Factor
```

**Capacity factors**:
- Full sprint, no holidays: 1.0
- Minor holidays/PTO: 0.8-0.9
- Major holidays/conference: 0.5-0.7
- New team member onboarding: 0.6-0.8

**Example**:
- Average velocity: 22 points/sprint
- Sprint has 2 days of public holidays
- Capacity factor: 0.8 (10 working days instead of 14)
- Available capacity: 22 × 0.8 = ~18 points

### Sprint Goal Examples

**Good sprint goals**:
- ✅ "Enable users to search documents with semantic queries"
- ✅ "Complete OpenSearch infrastructure setup for Phase 2a"
- ✅ "Implement authentication and basic RBAC"

**Bad sprint goals**:
- ❌ "Complete 25 story points" (focused on quantity, not value)
- ❌ "Work on search features" (too vague)
- ❌ "Fix bugs and add features" (unfocused)

## Daily Standup

**Format** (15 minutes max):

Each team member answers:
1. **Yesterday**: What did I complete?
2. **Today**: What will I work on?
3. **Blockers**: What's blocking me?

**Best practices**:
- Keep it brief (1-2 min per person)
- Focus on progress toward sprint goal
- Raise blockers, don't solve them in standup
- Update task board before standup
- Take detailed discussions offline

**Example**:
```
Yesterday: Completed Story 1.3 - hybrid search implementation
Today: Starting PR review and addressing feedback
Blockers: Need access to staging OpenSearch cluster for testing
```

## Sprint Review

**Purpose**: Demonstrate completed work to stakeholders

**Agenda** (1 hour for 2-week sprint):

1. **Review sprint goal** (5 min)
   - Restate original objective
   - Overview of what was achieved

2. **Demo completed stories** (40 min)
   - Show working software (not slides)
   - Highlight user value
   - Get stakeholder feedback

3. **Review incomplete work** (5 min)
   - Explain why stories didn't complete
   - Plan for next sprint

4. **Product backlog update** (10 min)
   - Adjust priorities based on feedback
   - Add new stories discovered during sprint

**Demo best practices**:
- Show working software in realistic environment
- Use real data, not mocked examples
- Focus on user value, not technical details
- Invite feedback and questions
- Keep demos short (5-10 min per story)

## Sprint Retrospective

**Purpose**: Continuous team improvement

**Agenda** (1 hour for 2-week sprint):

1. **Set the stage** (5 min)
   - Review retrospective purpose
   - Remind team of safe environment for feedback

2. **Gather data** (15 min)
   - What went well?
   - What could be improved?
   - What puzzles us?

3. **Generate insights** (20 min)
   - Group similar feedback
   - Identify patterns
   - Discuss root causes

4. **Decide what to do** (15 min)
   - Choose 1-3 actions for next sprint
   - Make actions specific and measurable
   - Assign owners

5. **Close** (5 min)
   - Recap action items
   - Appreciation round (optional)

**Retrospective formats**:
- **Start/Stop/Continue** - What should we start, stop, or continue doing?
- **Glad/Sad/Mad** - What made you glad, sad, or mad this sprint?
- **4Ls** - What did we Loved, Learned, Lacked, Longed for?
- **Sailboat** - What's the wind (helping us) and anchor (holding us back)?

**Example action items**:
- ✅ "Add integration tests before merging PRs (owner: Jane)"
- ✅ "Timebox PR reviews to 2 hours (owner: Team)"
- ❌ "Improve code quality" (too vague, not measurable)

## Velocity Tracking

### Calculating Velocity

**Velocity** = Total story points completed per sprint

**Example**:
- Sprint 1: Completed 18, 21, 23, 19, 22, 20 points
- Average velocity: ~20.5 points/sprint
- Use for planning: Round to 20 points

### Using Velocity for Planning

**Short term** (next 1-2 sprints):
- Use recent average (last 2-3 sprints)
- Adjust for known capacity changes

**Long term** (release planning):
- Use rolling average (last 5-6 sprints)
- Add buffer for unknowns (0.8× capacity)

**Example release plan**:
- Average velocity: 20 points/sprint
- Total remaining work: 120 points
- Estimated sprints: 120 ÷ 20 = 6 sprints
- With buffer: 6 ÷ 0.8 = ~8 sprints

### Velocity Anti-Patterns

❌ **Don't**:
- Use velocity for performance reviews
- Compare velocity across teams
- Pressure team to increase velocity
- Change point values to inflate velocity
- Cherry-pick easy stories to boost velocity

✅ **Do**:
- Use velocity for planning, not evaluation
- Track trends over time
- Investigate sudden changes
- Focus on sustainable pace

## Definition of Done

**Sprint-level DoD**:
- [ ] All acceptance criteria met
- [ ] Tests written and passing (>80% coverage)
- [ ] Code reviewed and approved
- [ ] Documentation updated (if needed)
- [ ] Deployed to dev/staging environment
- [ ] No known critical bugs
- [ ] Product Owner accepted story

**Release-level DoD** (additional):
- [ ] User acceptance testing passed
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] Production deployment successful
- [ ] Monitoring/alerts configured
- [ ] User documentation updated

## Sprint Metrics

### Key Metrics to Track

1. **Velocity** - Points completed per sprint
2. **Commitment reliability** - % of committed points completed
3. **Scope change** - Stories added/removed mid-sprint
4. **Carry-over** - Points moved to next sprint
5. **Defect escape rate** - Bugs found after release

### Healthy Sprint Indicators

✅ **Good signs**:
- Velocity is stable (±20%)
- Commitment reliability >80%
- Minimal mid-sprint scope changes
- Low carry-over (<10% of sprint)
- Team completing sprint goal consistently

⚠️ **Warning signs**:
- Velocity highly volatile
- Frequent incomplete stories
- Many stories added/removed mid-sprint
- High carry-over rate
- Sprint goal rarely achieved

## Sprint Anti-Patterns

### Scope Creep

**Problem**: Adding stories mid-sprint without removing others

**Solution**:
- Protect sprint commitment
- Add urgent work only if equal work removed
- Track interruptions and discuss in retrospective

### Gold Plating

**Problem**: Adding features beyond acceptance criteria

**Solution**:
- Stick to acceptance criteria
- Log enhancement ideas for backlog
- Review stories for over-engineering

### Technical Debt Neglect

**Problem**: Never addressing technical debt

**Solution**:
- Reserve 10-20% sprint capacity for tech debt
- Make technical stories visible in backlog
- Balance features with improvements

### Hero Culture

**Problem**: Relying on individuals to save sprints

**Solution**:
- Pair programming for knowledge sharing
- Sustainable pace, avoid overtime
- Address capacity issues in retrospective

## Sprint Ceremonies Summary

| Ceremony | When | Duration | Purpose |
|----------|------|----------|---------|
| **Sprint Planning** | Start of sprint | 2 hours (2-week sprint) | Select and commit to work |
| **Daily Standup** | Every day | 15 minutes | Sync progress, identify blockers |
| **Sprint Review** | End of sprint | 1 hour | Demo completed work |
| **Sprint Retrospective** | End of sprint | 1 hour | Reflect and improve |

**Total ceremony time**: ~7% of 2-week sprint (4.5 hours / 80 hours)

## Tools and Board Setup

### Using agile-board skill

For board-specific operations (creating stories, moving to sprint, etc.), use the `agile-board` skill:
- Creating sprint backlog
- Moving stories between pipelines
- Adding issues to sprint
- Tracking sprint progress

See `agile-board` skill documentation for board-specific workflows.

### Sprint Workflow Example

1. **Planning**: Use `agile-board` to move stories from Product Backlog to Sprint Backlog
2. **Execution**: Move stories through In Progress → In Review → Done
3. **Review**: Demo stories marked Done
4. **Retrospective**: Discuss process improvements
5. **Cleanup**: Move incomplete stories back to Product Backlog

## Remote Sprint Best Practices

### Virtual Sprint Planning

- Use collaborative tools (Miro, Mural, FigJam)
- Share screen for backlog review
- Use voting tools for consensus
- Take breaks every 30-45 minutes

### Virtual Daily Standup

- Video on (builds team connection)
- Use round-robin order (avoid silence)
- Update board before standup
- Record for async team members

### Virtual Sprint Review

- Screen share for demos
- Interactive demos (not pre-recorded)
- Chat for questions/feedback
- Record for stakeholders who can't attend

### Virtual Retrospective

- Anonymous feedback tools (Retrium, EasyRetro)
- Breakout rooms for small group discussions
- Digital sticky notes for ideas
- Clear action items in shared doc

## Further Reading

- Scrum Guide: https://scrumguides.org/
- Agile Manifesto: https://agilemanifesto.org/
- Sprint planning techniques: Planning poker, t-shirt sizing
- Team health checks: Squad Health Check model
