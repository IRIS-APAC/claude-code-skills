# Requirements & Design Skill

A comprehensive skill for gathering requirements and creating world-class design documentation that enables effective planning, estimation, and implementation.

**This skill actively challenges assumptions, researches alternatives, and suggests improvements** - it's not a passive order-taker.

## Overview

This skill transforms initial ideas and requirements into interconnected documents:

**Core Documents (All Five Always Created)**:
1. **Constraints** - Project boundaries and guiding principles (always created first)
2. **Customer Value** - Why will we win? Value proposition and competitive advantage
   - Press release, FAQs, customer experience mockups (Working Backwards methodology)
   - Audience: Business stakeholders, product managers, executives, investors
3. **Solution Design** - High-level delivery approach
   - Problem statement, solution overview, design decisions, architecture philosophy
   - Audience: Technical stakeholders, architects, engineering teams, product managers
4. **Requirements** - Detailed specifications (WHAT to build)
   - Comprehensive functional/non-functional requirements, user stories
5. **Architecture** - Technical blueprint (HOW to implement)
   - Component diagrams, system design, API contracts, data flows

**Why All Five?**
- **Consistency**: Same structure across all projects
- **Different Audiences**: Customer Value for business, Solution Design bridges both worlds, Requirements/Architecture for technical teams
- **Complete Picture**: Value proposition + Delivery approach + Detailed specs + Implementation blueprint

Additionally, the skill can help:
- **Challenge requirements**: Question vague, inconsistent, or suboptimal requirements
- **Research alternatives**: Use web search and codebase analysis to find better approaches
- **Suggest improvements**: Present 2-3 options with detailed pros/cons/costs
- Break requirements into epics and user stories
- Provide technical pointers (specs, patterns, code references)
- Estimate effort for stories
- Create working backwards documents (Amazon methodology)

## What Makes This Skill World-Class

This skill is based on real-world documentation from successful projects (like the SharePoint search service) and incorporates best practices for:

### Active Architecture Guidance
- **Challenges Assumptions**: Questions vague requirements, stated solutions vs problems
- **Researches Actively**: Uses WebSearch for best practices, Grep for codebase patterns
- **Suggests Alternatives**: Presents 2-3 options with cost/complexity comparisons
- **Asks "Why" Repeatedly**: Digs to root problems using 5 Whys technique
- **Validates Feasibility**: Checks if timelines, costs, scale are realistic

### Documentation Quality
- **Visual Communication**: ASCII diagrams, data flows, component diagrams
- **Decision Rationale**: Every significant choice is explained with alternatives considered
- **Concrete Examples**: JSON schemas, API requests/responses, code patterns
- **Cost & Performance Analysis**: Actual numbers with projections
- **Progressive Detail**: High-level overview → component details → implementation
- **User-Centric Perspective**: "Before and after" comparisons, benefit-focused
- **Future-Proofing**: Extensible designs, multi-phase planning
- **Operational Excellence**: Monitoring, observability, incident handling built-in

## When to Use This Skill

**Use this skill when**:
- Starting a new project or feature
- Have initial requirements but need structure
- Need to document an existing system
- Want to break down requirements into implementable pieces
- Need to estimate effort for planning
- Want to align stakeholders on approach

**Skip this skill if**:
- Requirements are already fully documented
- You just need to implement a small, well-defined feature
- You're only doing research/exploration (use explore agent instead)

## How to Use

### Quick Start

1. Invoke the skill: `/requirements-design`
2. Answer questions about your project
3. Review and iterate on generated documents
4. Optionally create story breakdowns

### Typical Workflow

**Phase 0: Review Existing Documentation** (If applicable, 15-30 minutes)
- Skill asks if you have existing requirements or documentation
- If yes, provide the location/path to existing docs
- Skill reads and analyzes existing content
- Identifies gaps, inconsistencies, or areas needing clarification
- Proposes how to incorporate existing content into new document structure

**Phase 1: Capture Constraints** (15-30 minutes)
- **Always first**: Identify non-negotiable requirements
- Document platform mandates, compliance, budget, timeline, architecture principles
- Creates foundation for all recommendations

**Phase 2: Requirements Gathering** (30-60 minutes)
- Discuss project context, problems, goals
- Identify users and stakeholders
- Explore technical constraints
- Define scope and priorities

**Phase 3: Document Creation** (All Five Documents Always Created)

The skill will recommend an approach that determines **document creation order**, not which documents to create:

**Approach A: Customer-First** (When Value Proposition Needs Clarity)
- Order: Constraints → Customer Value → Solution Design → Requirements → Architecture
- Best for: Greenfield products, unclear value proposition, need stakeholder buy-in
- Start by articulating why customers will choose this, then translate to delivery approach

**Approach B: Technical-First** (When Delivery Approach is Clear)
- Order: Constraints → Solution Design → Customer Value → Requirements → Architecture
- Best for: Clear requirements, technical projects, established products
- Start with delivery approach and design decisions, then frame the customer value

**Approach C: Parallel** (When Time is Critical)
- Order: Constraints → [Customer Value + Solution Design] → Requirements → Architecture
- Best for: Experienced teams, well-understood domain, tight timelines
- Develop both vision documents simultaneously

**All approaches create the same five documents** - only the order and emphasis differ.

**Result**: Every project gets complete documentation with both customer value proposition and high-level delivery approach.

**Phase 4: Story Decomposition** (Optional, 1-2 hours)
- Break requirements into epics (5-10 major feature areas)
- Decompose epics into stories (5-15 stories per epic)
- Add acceptance criteria and estimates
- Sequence stories with dependencies

**Phase 5: Technical Pointers** (Optional, ongoing)
- Add specs and standards references
- Identify implementation patterns
- Link to similar code in codebase
- Provide testing strategies

## How the Skill Challenges & Researches

This skill is **actively challenging, not passively documenting**. It:

### 1. Challenges Assumptions
- Questions vague requirements ("build a dashboard" → "What problem does it solve?")
- Challenges technology choices ("we need Redis" → "What are you caching? What's your scale?")
- Identifies over-engineering ("we need Kubernetes" for 3 services → suggests simpler alternatives)
- Validates feasibility (cost, timeline, operational overhead)

### 2. Researches Proactively
- **WebSearch**: Industry best practices, technology comparisons, cost estimates
- **Grep/Read**: Existing patterns in your codebase
- **Task (Explore)**: Understand codebase architecture
- Presents 2-3 researched options with pros/cons/costs

### 3. Suggests Better Alternatives
- Simpler solutions (in-memory cache vs Redis for small scale)
- Cost-effective approaches (SaaS vs build)
- Industry standards (SAML/OIDC abstraction vs vendor-specific)

### 4. Validates Feasibility
- **Cost reality checks**: "That approach costs $50K/month at your scale. Here's a $5K alternative"
- **Timeline reality checks**: "That's a 6-month project. Here's what's possible in 6 weeks"
- **Technical reality checks**: "10ms latency across continents isn't possible. Here's what is"

**For detailed examples and patterns**, see the [SKILL.md](SKILL.md) file which contains:
- Specific challenge/research/suggest examples
- Anti-patterns to avoid
- How to handle conflicts and prioritization
- Exit criteria and handoff checklists

## Document Templates

### 1. Product Overview

**Purpose**: Communicate vision to stakeholders and team

**Audience**: Product managers, executives, non-technical stakeholders

**Structure**:
- The Big Picture (visual summary)
- Problem Statement
- Solution Overview
- Key Design Decisions (with rationale)
- User Benefits (for different user groups)
- Technical Highlights
- Success Metrics
- FAQs

**Length**: 5-10 pages

**Example**: See template in [product-overview-template.md](references/product-overview-template.md)

---

### 2. Detailed Requirements

**Purpose**: Provide comprehensive specifications for implementation

**Audience**: Developers, QA, architects

**Structure**:
- Project Overview (context, timeline, team)
- Technical Architecture (components and relationships)
- Functional Requirements (user stories, acceptance criteria)
- API Contracts (endpoints, request/response formats)
- Data Models (schemas, relationships)
- Non-Functional Requirements (performance, security, scalability)
- Technical Decisions (ADRs)
- Testing Requirements

**Length**: 20-50 pages

**Example**: See template in [detailed-requirements-template.md](references/detailed-requirements-template.md)

---

### 3. Architecture & System Design

**Purpose**: Provide technical blueprint for implementation

**Audience**: Engineering team, architects, DevOps

**Structure**:
- System Responsibilities (what it does and doesn't do)
- High-Level Architecture (component diagrams)
- Service Elements (internal modules and handlers)
- Data Architecture (storage strategy, schemas)
- API Design (endpoints, contracts, examples)
- Security Architecture (AuthN/AuthZ, encryption)
- Integration Patterns (how components communicate)
- Observability (logging, metrics, tracing)
- Scalability & Performance
- Disaster Recovery

**Length**: 20-40 pages

**Example**: See template in [architecture-template.md](references/architecture-template.md)

---

### 4. Working Backwards (Optional)

**Purpose**: Start with customer experience, work backwards to implementation

**Audience**: Product team, stakeholders, leadership

**Structure**:
- Press Release (external announcement)
- FAQs (external and internal)
- Customer Experience Mockups
- User Manual Draft
- Mapping to Implementation

**Length**: 10-20 pages

**Example**: See `references/working-backwards-template.md`

---

## Reference Materials

The skill includes comprehensive reference materials:

- **[project-constraints-template.md](references/project-constraints-template.md)** - Template for capturing non-negotiable constraints
- **[requirements-gathering.md](references/requirements-gathering.md)** - Structured questionnaire for gathering complete requirements
- **[product-overview-template.md](references/product-overview-template.md)** - Template for high-level vision document
- **[detailed-requirements-template.md](references/detailed-requirements-template.md)** - Template for comprehensive requirements
- **[architecture-template.md](references/architecture-template.md)** - Template for system design document
- **[story-decomposition.md](references/story-decomposition.md)** - Guide for breaking down into epics and stories
- **[technical-pointers.md](references/technical-pointers.md)** - Guide for providing implementation guidance
- **[working-backwards-template.md](references/working-backwards-template.md)** - Amazon's working backwards methodology

## Output Structure

By default, documents are created in `docs/Design/`:

```
docs/Design/
├── constraints-{project-name}.md            # 1. Project Boundaries
├── customer-value-{project-name}.md         # 2. Why Will We Win?
├── solution-design-{project-name}.md        # 3. High-Level Delivery Approach
├── requirements-{project-name}.md           # 4. Detailed Specifications
└── architecture-{project-name}.md           # 5. Technical Blueprint
```

**All five documents are always created** for consistency and completeness.

**Document Creation Order** (varies by approach chosen):
- **Customer-First**: Constraints → Customer Value → Solution Design → Requirements → Architecture
- **Technical-First**: Constraints → Solution Design → Customer Value → Requirements → Architecture
- **Parallel**: Constraints → [Customer Value + Solution Design] → Requirements → Architecture

You can specify a different location if preferred.

## Documentation Quality Standards

### 1. Clear Visual Communication
- ASCII diagrams for architecture
- Data flow diagrams
- Component diagrams
- Tables for comparisons

### 2. Decision Rationale
- Explain WHY for every design choice
- Show alternatives considered
- Use comparison tables
- Make trade-offs explicit

### 3. Concrete Examples
- Show actual JSON examples
- Include API requests/responses
- Provide sample configurations
- Show code patterns

### 4. Cost and Performance
- Estimate costs with actual numbers
- Provide performance targets
- Show scaling projections
- Compare approaches

### 5. Progressive Detail
- High-level overview first
- Then drill into components
- Implementation-level detail where needed

### 6. User-Centric
- Show how decisions benefit users
- Include "before and after"
- Address user experience

### 7. Future-Proofing
- Design for extensibility
- Plan multiple phases
- Consider reusability
- Document what's deferred

### 8. Operational Excellence
- Include monitoring from start
- Address failure scenarios
- Specify logging/metrics
- Plan for maintainability

## Story Decomposition

### Epic Structure

Epics represent major feature areas:
- Epic 0: Foundation/Infrastructure
- Epic 1-N: Core features
- Epic N+1: Operational capabilities

**Typical project has 5-10 epics**

### Story Structure

Stories are implementable units (1-5 days each):
- User story format (As a... I want... So that...)
- Clear acceptance criteria (3-7 criteria)
- Technical notes
- Definition of done
- Estimated effort (story points or hours)
- Dependencies

**Typical epic has 5-15 stories**

### Estimation

**Story Points** (Fibonacci scale):
- 1-2 points: Simple tasks (hours)
- 3-5 points: Moderate complexity (1-2 days)
- 8 points: Complex tasks (3-5 days)
- 13+ points: Too large, break down

**Time-Based** (for waterfall):
- Include buffer (1.5-2x estimate)
- Break down by skill level
- Account for review, testing, docs

## Technical Pointers

For each story, provide:

1. **Specifications**: Links to relevant standards (OAuth 2.0, OpenAPI, etc.)
2. **Implementation Patterns**: Design patterns that apply
3. **Code References**: Similar implementations in codebase (with file:line references)
4. **External Resources**: Official docs, tutorials, examples
5. **Testing Strategy**: Unit, integration, E2E, performance, security tests
6. **Performance Considerations**: Targets, optimizations, monitoring
7. **Security Considerations**: Concerns, mitigations, testing

## Working Backwards Process

The skill supports Amazon's "Working Backwards" methodology:

1. **Press Release**: Write customer-facing announcement
2. **FAQs**: Answer customer and internal questions
3. **Customer Experience**: Mock up user journeys
4. **User Manual**: Draft how customers will use it
5. **Map to Implementation**: Connect customer needs to technical requirements

This approach ensures customer value drives technical decisions.

## Integration with Other Skills

This skill works well with:

- **developer-analysis**: Use requirements to create technical design before implementation
- **project-management**: Use story breakdowns for sprint planning
- **testing**: Use acceptance criteria to define test strategy
- **git-workflow**: Use architecture to understand branching strategy

## Tips for Best Results

### 1. Be Specific
- Provide concrete examples
- Use actual numbers (users, data volume, costs)
- Reference specific technologies

### 2. Iterate
- Start with drafts
- Get feedback
- Refine progressively

### 3. Ask Questions
- The skill will ask clarifying questions
- Use AskUserQuestion for key decisions
- Explore the codebase for context

### 4. Think Customer First
- Start with customer problems
- Define success from user perspective
- Work backwards to implementation

### 5. Document Decisions
- Explain why, not just what
- Show alternatives considered
- Be explicit about trade-offs

### 6. Keep It Fresh
- Update docs as implementation evolves
- Add learnings from implementation
- Refine estimates based on actuals

## Examples

### Example 1: New API Service

**Input**: "We need an API service to search documents"

**Output**:
- Product Overview: Explains semantic search benefits, cost savings, user experience
- Detailed Requirements: 5 epics, 35 stories, API contracts, data models
- Architecture: Component diagram, module structure, OpenSearch integration
- Estimated effort: 160 story points (8 sprints)

### Example 2: Integration Project

**Input**: "Connect our system to SharePoint"

**Output**:
- Product Overview: Problem (data silos), solution (unified search), benefits
- Detailed Requirements: Authentication flow, sync strategy, error handling
- Architecture: Connector pattern, retry logic, incremental sync
- Estimated effort: 40 story points (2 sprints)

### Example 3: Infrastructure Upgrade

**Input**: "Migrate from EC2 to ECS"

**Output**:
- Product Overview: Why migrate (cost, scalability, ops efficiency)
- Detailed Requirements: Container strategy, deployment pipeline, rollback
- Architecture: ECS task definitions, networking, service discovery
- Estimated effort: 65 story points (3 sprints)

## Frequently Asked Questions

**Q: How long does this process take?**
A: Depends on project complexity:
- Small project: 2-4 hours (all documents)
- Medium project: 4-8 hours
- Large project: 1-2 days

**Q: Do I need all three documents?**
A: Not always. You can request specific documents:
- Product Overview only (stakeholder alignment)
- Requirements only (implementation guide)
- Architecture only (technical blueprint)

**Q: Can I use this for existing projects?**
A: Yes! Use it to document existing systems or enhance existing docs.

**Q: What if requirements change?**
A: Update the documents. Keep them as living documents, not one-time artifacts.

**Q: How detailed should acceptance criteria be?**
A: Specific enough to be testable (yes/no, pass/fail). Usually 3-7 criteria per story.

**Q: Should I create stories for all epics upfront?**
A: No. Detail stories 1-2 sprints ahead. Refine as you learn.

**Q: How do I know if estimates are accurate?**
A: Track actuals vs estimates. Adjust estimation approach based on learnings.

## Version History

- **v1.0** (2025-01-30): Initial release
  - Core templates (Product Overview, Requirements, Architecture)
  - Story decomposition guide
  - Technical pointers guide
  - Working backwards template

## Feedback & Contributions

This skill is part of the claude-code-skills repository. To provide feedback or suggest improvements:

1. Open an issue describing the improvement
2. Provide examples of what could be better
3. Share documentation that you found particularly effective

## License

Part of the claude-code-skills project. See repository LICENSE for details.
