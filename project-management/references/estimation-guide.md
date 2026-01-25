# Story Estimation Guide

T-shirt sizing methodology for estimating story complexity.

## T-Shirt Size to Story Points Mapping

| Size | Story Points | Complexity Description |
|------|--------------|------------------------|
| **XS** | 1 | **Trivial** - Well-defined, minimal complexity, no dependencies |
| **S** | 3 | **Simple** - Clear requirements, limited scope, few dependencies |
| **M** | 5 | **Moderate** - Some complexity, multiple components, standard patterns |
| **L** | 8 | **Complex** - Significant complexity, cross-module changes, new patterns |
| **XL** | 13 | **Very Complex** - High complexity, architectural changes, many dependencies |

## Sizing Guidelines

### XS (1 point) - Trivial

**Characteristics**:
- Simple configuration change
- Single file modification
- Well-established pattern to follow
- No external dependencies
- Minimal testing required

**Examples**:
- Add environment variable to configuration
- Update documentation
- Simple bug fix with known solution
- Add logging statement

**Time Estimate**: < 2 hours with AI assistance

---

### S (3 points) - Simple

**Characteristics**:
- Clear, well-defined requirements
- 1-3 files modified
- Follows existing patterns in codebase
- Limited external dependencies
- Straightforward testing

**Examples**:
- Add new API endpoint using existing patterns
- Implement simple validation logic
- Add new filter to existing query
- Simple integration with existing service

**Time Estimate**: 2-6 hours with AI assistance

---

### M (5 points) - Moderate

**Characteristics**:
- Moderate complexity
- 3-8 files modified
- May introduce new patterns
- Multiple component interaction
- Requires integration testing
- Some uncertainty in requirements

**Examples**:
- Implement new search feature with multiple filters
- Add new document parser type
- Create new service module with standard CRUD operations
- Implement authentication middleware

**Time Estimate**: 1-2 days with AI assistance

---

### L (8 points) - Complex

**Characteristics**:
- Significant complexity
- 8-15 files modified
- Introduces new architectural patterns
- Multiple service integration
- Requires careful error handling
- Comprehensive testing needed
- Some research/spike work required

**Examples**:
- Implement hybrid search with score normalisation
- Build complete indexing pipeline for new source
- Implement RBAC policy enforcement
- Create monitoring dashboard with multiple metrics

**Time Estimate**: 2-4 days with AI assistance

**Note**: Consider breaking L stories into smaller stories.

---

### XL (13 points) - Very Complex

**Characteristics**:
- Very high complexity
- 15+ files modified or new major subsystem
- Significant architectural decisions
- Multiple external service integrations
- Extensive error handling and edge cases
- Comprehensive testing across layers
- Significant research/prototyping needed
- **Should be broken down into sub-stories**

**Examples**:
- Implement complete OpenSearch Serverless setup with hybrid search
- Build end-to-end pipeline orchestration with Step Functions
- Create multi-source document processing with captioning
- Implement complete access control system

**Time Estimate**: 4-8 days with AI assistance

**IMPORTANT**: Stories sized XL should generally be broken down into smaller stories (see breakdown strategies below).

---

## AI-Assisted Development Assumptions

These estimates assume developers have access to AI coding assistants (e.g., Claude Code, GitHub Copilot) which provide:

- **Code generation** for boilerplate and standard patterns
- **Documentation** assistance for understanding codebases
- **Testing** code generation
- **Debugging** assistance
- **Refactoring** suggestions

Without AI assistance, multiply estimates by approximately 1.5-2x.

---

## Estimation Process

1. **Review story requirements** and acceptance criteria
2. **Identify complexity factors**:
   - Number of files/modules affected
   - New vs. existing patterns
   - External dependencies
   - Testing requirements
   - Uncertainty level
3. **Choose t-shirt size** based on dominant complexity factors
4. **Apply story points** using the mapping above
5. **Document assumptions** in story comments if needed

---

## Complexity Factor Checklist

Use this checklist to help determine story size:

| Factor | XS | S | M | L | XL |
|--------|----|----|----|----|-----|
| **Files Modified** | 1 | 1-3 | 3-8 | 8-15 | 15+ |
| **New Patterns** | None | None | 1-2 | 2-3 | 3+ |
| **External APIs** | 0 | 0-1 | 1-2 | 2-3 | 3+ |
| **Testing Layers** | Unit only | Unit + basic integration | Unit + integration | Unit + integration + E2E | Comprehensive all layers |
| **Research Needed** | None | Minimal | Some | Significant | Extensive |
| **Uncertainty** | Very low | Low | Medium | High | Very high |
| **Dependencies** | 0-1 | 1-2 | 2-3 | 3-5 | 5+ |

---

## Breaking Down Large Stories

If a story is estimated at **L (8)** or **XL (13)**, consider breaking it down:

### Vertical Slicing (Preferred)

Break by **end-to-end functionality**:

**Example**: "Implement hybrid search"
- Story 1a: Basic BM25 + vector search (happy path) - M (5)
- Story 1b: Error handling and edge cases - S (3)
- Story 1c: Performance optimisation - S (3)
- Story 1d: Advanced filters - M (5)

**Benefits**:
- Each story delivers working functionality
- Can deploy incrementally
- Easier to test and review
- Better for sprint planning

### Horizontal Slicing (Use Sparingly)

Break by **technical layer** (only when vertical slicing not possible):

**Example**: "Set up OpenSearch"
- Story 1a: Collection setup and access policies - M (5)
- Story 1b: Index schema definition - S (3)
- Story 1c: Search pipeline configuration - M (5)

**Drawbacks**:
- No working feature until all stories complete
- Dependencies between stories
- Harder to demonstrate progress

### When to Break Down

**Always break down when**:
- Story is XL (13 points)
- Multiple team members need to work in parallel
- Story has unrelated acceptance criteria

**Consider breaking down when**:
- Story is L (8 points)
- Sprint capacity is limited
- Story has high uncertainty

---

## Re-estimation

Stories should be re-estimated when:
- Requirements change significantly
- New technical constraints discovered
- Actual complexity differs from initial estimate
- Dependencies added or removed

Use retrospective data to calibrate future estimates.

---

## Notes on Story Points

- Story points are **relative** measures, not absolute time
- Points represent **complexity + effort + uncertainty**, not just time
- Team velocity will stabilise over 2-3 sprints
- Focus on **consistency** rather than accuracy
- AI assistance is factored into the baseline estimates
- Don't compare points across teams (each team has own baseline)

---

## Estimation Best Practices

**DO**:
- ✅ Estimate stories as a team (planning poker, etc.)
- ✅ Use complexity factors checklist
- ✅ Break down L/XL stories
- ✅ Re-estimate when requirements change
- ✅ Track actual vs. estimated for calibration

**DON'T**:
- ❌ Convert story points directly to hours
- ❌ Use estimates for performance reviews
- ❌ Estimate implementation details (estimate outcomes)
- ❌ Estimate epics (points roll up from children)
- ❌ Change point values after sprint starts
