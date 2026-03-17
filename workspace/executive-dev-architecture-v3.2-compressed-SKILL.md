---
name: executive-dev-architecture
description: >-
  Organizational operating system for executive developers leading multi-agent
  systems. Modular tier-routed architecture — agents read the Static Core plus
  ONLY their tier module (T1/T2/T3). Defines tiered agent cognition, delegation
  protocols, ADRs, inter-agent communication, and systemic thinking across all
  dimensions. Use when structuring agent teams, defining architecture, or
  establishing organizational protocols.
license: MIT
metadata:
  author: CJ
  version: '3.2'
---

# Executive Dev Architecture v3.2

## Tier Routing — READ THIS FIRST

Modular skill. Do NOT read the entire document.

**Step 1:** Read **STATIC CORE** (all tiers).
**Step 2:** Identify your cognition tier from delegation brief or task.
**Step 3:** Read ONLY your tier's module. Skip the other two.
**Step 4:** Reference **SHARED INFRASTRUCTURE** as needed.

```
STATIC CORE .............. ALL tiers read (philosophy, cost, ideation, anti-patterns)
T1 EXECUTIVE MODULE ...... T1 ONLY (SWOT, council, delegation, ADRs, governance, state machines, contracts, orchestration, observability, secrets, RACI, incident response)
T2 SPECIALIST MODULE ..... T2 ONLY (pipeline, upward challenge, scoped ideation, operational checklists)
T3 EXECUTOR MODULE ....... T3 ONLY (I/O contracts, quality gates, failure signals)
SHARED INFRASTRUCTURE .... Reference as needed (agents, contracts, platforms)
```

Brief says "Tier 2" → read Static Core + T2 Module + reference Shared Infrastructure. Do NOT read T1 or T3. Controls context window cost.

---

# ═══════════════════════════════════════════════════════════════
# STATIC CORE — ALL TIERS
# ═══════════════════════════════════════════════════════════════

## The Philosophy

Not a coding methodology. An organizational operating system.

Every decision evaluated against the FULL cost surface.

**Cost = any expendable resource consumed to produce an outcome.**

| Cost Dimension | What It Measures |
|---------------|-----------------|
| Tokens / Credits | AI compute consumed |
| Time | Wall clock from start to outcome |
| Compute | CPU, memory, bandwidth, API calls |
| Lines of Code | Maintenance burden, attack surface, review time |
| Cognitive Load | How hard to understand, modify, or hand off |
| Context Window | The scarcest resource in agentic flows |
| Human Interventions | Every time a person must touch, review, or fix |
| Technical Debt | Future cost created by today's shortcut |

Applies to: agentic flows, codebases, architecture, extensions, websites, UGC video pipelines, content workflows, data pipelines, reconciliation engines, team operations, process design.

Ideation engine is the METABOLISM. Operates on EVERYTHING — ideas, architecture, workflow, cost surface, paradigm, approach. Cost is one dimension, not the frame. Systemic thinking — not a tool, checklist, or style guide.

### The Systemic Cost Test

Before any decision ships:

1. What does this cost across ALL dimensions, not just the obvious one?
2. Is there a path that reduces cost in one dimension without materially increasing it in another?
3. Does this decision create future cost (debt) that someone else will pay?
4. Could a different tier of agent or a different scope boundary have produced the same outcome at lower total cost?

Can't answer these → haven't finished thinking.

---

## Ideation Engine (All Tiers — Scoped by Authority)

Every tier gets ideation. SCOPE differs, not quality.

**Operates on:** architecture, workflow, ideas, cost surface, paradigm, approach.

**T1 scope:** Cross-domain, full system, competing proposals, SWOT.
**T2 scope:** Within domain, pipeline-aware, can challenge upstream.
**T3 scope:** Within I/O contract — multi-path on HOW to execute, flag wrong inputs, propose better output formats. Does NOT explore alternatives outside its contract.

### How to Ideate (All Tiers)

1. **Define the outcome.** What must be true when done?
2. **Generate 2+ paths.** Different approaches, trade-offs, architectures. (T3: within contract only)
3. **Evaluate each path** against the systemic cost test.
4. **Pick the best.** Or propose multiple to tier above.
5. **Document why.** Decision incomplete without rationale.

---

## Tiered Agent Cognition Model

Intelligence FLOOR here exceeds most systems' CEILING. Tiers differ in SCOPE and AUTHORITY, not intelligence. Every tier reads cost identically — all 8 dimensions, all time horizons. Scope limits what you ACT on, not what you UNDERSTAND.

### Tier Assignment Rule

```
Is there more than one valid approach?
  YES → Does the decision cross domains or affect the pipeline?
    YES → Tier 1 (Executive)
    NO  → Tier 2 (Contextual Specialist)
  NO  → Is the blast radius local (only your scope affected)?
    YES → Tier 3 (Elite Executor)
    NO  → Tier 2 (Contextual Specialist)
```

### The Anti-Pattern: Copy of a Copy

```
NEVER: Smart parent → dumber child → even dumber grandchild
       (each layer loses fidelity, like a fax of a fax)

ALWAYS: Architect assigns tier based on task ambiguity
        Every tier operates at its full cognitive capacity
        Output quality is identical regardless of tier
        The only difference is scope and authority
```

---

## Reference Index Architecture

### The Principle

Never embed domain knowledge in the skill. Maintain a reference index of canonical URLs. Fetch on demand at decision time. Keeps skill lean, always current, forces verification over hallucination. Minimizes context window cost.

### How to Use

1. Hit a domain-specific decision
2. Check reference index for canonical URL
3. Fetch with specific prompt extracting ONLY what this decision needs
4. Apply and move on — do not cache in skill

### Core Reference Index

| Domain | Canonical URL | Fetch When |
|--------|--------------|------------|
| Python stdlib | `https://docs.python.org/3/library/` | Standard library usage |
| Python style | `https://peps.python.org/pep-0008/` | Python code standards |
| Pandas | `https://pandas.pydata.org/docs/reference/` | DataFrame operations |
| Node.js | `https://nodejs.org/api/` | Server-side JS |
| MDN Web APIs | `https://developer.mozilla.org/en-US/docs/Web/API` | Browser APIs |
| MDN CSS | `https://developer.mozilla.org/en-US/docs/Web/CSS` | Styling, layout |
| MDN JavaScript | `https://developer.mozilla.org/en-US/docs/Web/JavaScript` | JS language reference |
| Tailwind CSS | `https://tailwindcss.com/docs` | Utility CSS classes |
| Chrome Extensions | `https://developer.chrome.com/docs/extensions/reference/api` | Extension APIs |
| Google Apps Script | `https://developers.google.com/apps-script/reference` | Sheets/Drive/Gmail |
| Google Cloud Run | `https://cloud.google.com/run/docs` | Container deployment |
| Google Secret Manager | `https://cloud.google.com/secret-manager/docs` | Secrets |
| BigQuery | `https://cloud.google.com/bigquery/docs/reference` | SQL warehouse |
| pdf-lib | `https://pdf-lib.js.org/docs/api/` | PDF generation (JS) |
| Veeqo API | `https://developer.veeqo.com/docs` | Shipping/orders |
| Amazon SP-API | `https://developer-docs.amazon.com/sp-api/` | Amazon seller |
| Shopify API | `https://shopify.dev/docs/api` | Shopify integrations |
| OAuth 2.0 | `https://datatracker.ietf.org/doc/html/rfc6749` | Auth flows |
| Docker | `https://docs.docker.com/reference/` | Containers |
| Ollama | `https://github.com/ollama/ollama/blob/main/docs/api.md` | Local model API |

### Extending the Index

New domain → find canonical docs URL → add to project-level index → all agents fetch on demand.

---

## Code Standards (All Tiers)

### Universal Rules

- Naming: descriptive, consistent, grep-friendly
- Error handling: never swallow silently. Catch → log → recover or escalate
- Dependencies: add only when reimplementing would cost more across ALL dimensions. Pin versions. Document why.
- Comments: explain WHY, not WHAT
- Functions: single responsibility

### Language-Specific Standards

Do NOT embed here. Fetch from reference index: Python → PEP 8, JavaScript → MDN, Apps Script → Google reference, SQL → target engine's guide.

### Code Review Gate

1. Does it work? (tested per `persistent-ideation-engine`)
2. Is it readable? (new engineer understands without walkthrough)
3. Is it safe? (error handling, validation, no exposed secrets)
4. Is it modular? (replaceable without rewriting the system)
5. What is the systemic cost? (tokens, time, lines, maintenance, debt)

---

## Anti-Patterns (All Tiers)

- Copy-of-a-copy delegation (context degradation through agent chains)
- Embedding domain knowledge that should be fetched from reference docs
- Delegating without tier-appropriate context
- Optimizing for one cost dimension while ignoring others
- Hard-coding business rules without documentation
- Silently coercing bad data or swallowing errors
- Generating outputs from unreviewed data
- Skipping dead-letter queues
- Credentials in notebooks or spreadsheets
- Pretty reports masking unresolved exceptions
- Skipping SWOT before T1 proposals (building without analyzing the field)
- Reading tier modules that aren't yours (context window waste)

---

# ═══════════════════════════════════════════════════════════════
# T1 EXECUTIVE MODULE — T1 AGENTS ONLY
# ═══════════════════════════════════════════════════════════════

## T1: Executive Cognition

Full architectural reasoning. COMPETING ideation across all dimensions — architecture, workflow, ideas, systemic cost, paradigm. Cross-domain trade-offs.

**Gets:** Full ideation engine (multi-path on architecture, workflow, ideas, cost, approach), full architecture standards + systemic cost awareness, full decision authority within scope, restructuring permission, reference index access.

**Used when:** Multiple valid approaches AND cross-domain impact. Requires judgment, not execution.

### The T1 Ideation Council

High-stakes decisions: 2-3 T1 agents on the SAME problem, competing independently on EVERYTHING — architecture, workflow, systemic cost, paradigms, trade-offs. Each produces full proposal: approach, architecture, workflow, cost surface, rationale. Architect evaluates, picks best, synthesizes, or sends back. Multi-path exploration at ARCHITECTURE, WORKFLOW, and IDEAS level.

### The T1 SWOT Protocol

Every T1 proposal — single agent or council — MUST include SWOT. Not optional.

**S — Strengths:** What does the current state / proposed approach do well? What existing assets, architecture, patterns, or decisions give leverage? What to PRESERVE because it's already working?

**W — Weaknesses:** Where is the current state vague, incomplete, or fragile? What sections are thin? What works but barely? Where would a hostile audit, scaling, or handoff expose cracks? Be ruthless — unnamed weaknesses become unpredicted failures.

**O — Opportunities:** What's possible but unbuilt? What in reference material, source docs, prior work, domain knowledge isn't captured? What capabilities compound value? What would a competitor build that we haven't?

**T — Threats:** What breaks if we act blindly? Second-order consequences? Where does bloat, duplication, scope creep, or philosophy violation hide? What looks like improvement but actually increases systemic cost?

Evaluated across ALL cost dimensions. Strength in simplicity may be Weakness in extensibility. Opportunity in observability may threaten context window cost. Hold tensions, don't flatten.

**When to run:** Before building/rewriting systems, before council proposals, evaluating current state, reviewing T1 proposals, T2 challenge re-evaluation.

**Output:** Four labeled sections. S and W analyze WHAT IS. O and T analyze WHAT COULD BE. Gap between = where work lives.

**Anti-Pattern — SWOT Theater:** Only strengths = marketing. Only weaknesses = despair. Empty Threats = naive optimism. Send it back.

### T1: Agentic Delegation Protocol

1. **Map dependency graph.** Parallel vs. sequential vs. data-dependent.
2. **Assign tiers.** Each subtask by ambiguity.
3. **Write delegation brief:**

**For T1 (Executive):** Business objective + why, full system context, cost constraints across all dimensions, authority boundaries, reference pointers.

**For T2 (Contextual Specialist):** Outcome (not steps), pipeline position (feeds in / consumes output), downstream reqs, challenge rights ("propose better with cost analysis"), relevant reference URLs.

**For T3 (Elite Executor):** Input spec (exact), output spec (exact), success criteria, execution environment and constraints (language, libraries, platform). No pipeline context.

### T1: Context Passing Rules

- **By file reference, not inline.** Context window = scarcest resource.
- **Summarize upstream for T2, don't dump.**
- **T3 gets ONLY what it needs.** Every extra token = measurable waste.

### T1: Result Aggregation

1. Validate output against success criteria
2. Check T2 challenges — evaluate against systemic cost
3. Better suggestion → adopt, log ADR
4. Merge via workspace files
5. Failures per failure model

### T1: Architecture Decision Records (ADRs)

**When to Write:** Major version bumps, choosing between architectural approaches, adding/removing agents, changing data contracts/schemas, any "why?" decision, accepted T2 challenges.

**Template:**
```
# ADR-{number}: {Title}
## Status: Proposed | Accepted | Deprecated | Superseded by ADR-{n}
## Context: What prompted this decision?
## Decision: What was decided and why?
## Systemic Cost Analysis:
  - Tokens/compute: {impact}
  - Time: {impact}
  - Lines of code / maintenance: {impact}
  - Cognitive load: {impact}
  - Human interventions: {impact}
  - Technical debt: {impact}
## Alternatives Considered:
  | Alternative | Pros | Cons | Systemic Cost | Why Rejected |
## Consequences: What changes? What's easier? What's harder?
## Review: Approved by, date, linked release
```

### T1: Cost and Performance Governance

| Tier | Budget Guidance |
|------|----------------|
| T1 Executive | Full — ideation loops, multi-path exploration, ADRs, SWOT, competing proposals |
| T2 Specialist | Moderate — pipeline context + domain reference fetches + challenge analysis |
| T3 Executor | Minimal context — short prompt, precise execution. Quality floor unchanged. |

**Efficiency Rules:**
- Don't fetch known data (workspace, memory, conversation)
- Don't pass unneeded context (tier-appropriate only)
- Don't re-derive unchanged state (read the file, don't recompute)
- Cache expensive results to workspace for reuse
- Kill idle agents — output lives in workspace, context doesn't need to

### T1: Human-in-the-Loop Protocol

**Require approval:** Financial materiality, irreversible actions (delete/publish/send), architecture changes, override of prior human instruction.

**Time-Boxing:** No response → non-blocking continue "Awaiting Approval" → blocking escalate → 2 attempts → notify Architect.

**Override Audit:** Who, what, when, why (REQUIRED if override contradicts system logic).

### T1: Cascading Failure

- T3 fails → parent retries once, then reroutes
- T2 fails → parent reviews context, may re-classify task as T1 (new agent, not upgrade)
- T1 fails → escalate to human with full context and what was attempted

### T1: Workflow State Machine

Every multi-step pipeline: ONE authoritative state. States explicit, named, persisted — not inferred from side effects.

```
STATES:  intake → validated → processing → review → complete → archived
EDGES:  Each transition has: trigger, guard condition, side effects, rollback
RULES:
- No implicit state (if it's not in the state store, it didn't happen)
- Failed transitions land in a hold state, not limbo
- State is queryable — any agent can ask "where is X right now?"
- Human overrides are a state transition, not a backdoor
```

T1 defines state machine. T2s execute transitions. T3s validate outputs match expected post-transition state.

### T1: Formal Agent Contracts

Every catalog agent has a contract — agreement between system and agent.

```
CONTRACT:
  agent: AgentName
  version: contract schema version
  accepts: [input schemas with types, required fields, constraints]
  produces: [output schemas with types, guarantees, location]
  sla: max duration, retry policy, timeout behavior
  failure_modes: [enumerated — what can go wrong and what happens]
  escalation: who gets notified, at what threshold
  dependencies: [other agents or services this agent requires]
```

Versioned. Breaking changes require ADR + migration. No agent without contract. No contract without review.

### T1: Orchestration Runtime

3+ agents or data-dependent fan-out → explicit orchestration, not ad hoc delegation chains.

```
ORCHESTRATION RULES:
- DAG or sequential — pick one per pipeline, document it
- Each node: agent, tier, input_ref, output_ref, timeout, retry
- Fan-out: define merge strategy BEFORE spawning parallel agents
- Checkpoints: persist state at each node so recovery doesn't restart from zero
- Dead-letter: any node that fails after retries writes to dead-letter, not /dev/null
```

Orchestration = T1 artifact. T2s execute within. T3s see only their contract.

### T1: Environment Promotion Protocol

```
ENVIRONMENTS:  dev → staging → production
PROMOTION GATES:
  dev → staging:  All tests pass. No hardcoded values. Dependencies pinned.
  staging → prod: Parallel-run validation. Rollback plan documented. ADR if architecture changed.
RULES:
- Never skip staging for "quick fixes" — that's how production breaks
- Staging uses production-shaped data (sanitized, not toy data)
- Secrets are environment-specific — never copy prod secrets to dev
- Rollback is tested before promotion, not after failure
```

### T1: Observability Framework

Can't see it → can't fix it. Observability ≠ logging — ability to ask arbitrary questions about system behavior.

```
THREE PILLARS:
  Logs:    Structured (JSON), leveled (debug/info/warn/error), correlated by trace_id
  Metrics: Counters, gauges, histograms for: throughput, latency, error rate, queue depth
  Traces:  End-to-end request/pipeline traces across agent boundaries

RULES:
- Every agent emits structured logs with agent_name, tier, trace_id, timestamp
- Every pipeline has a dashboard answering: is it healthy? how fast? where are errors?
- Alerts fire on SYMPTOMS (error rate spike), not just causes (disk full)
- Dead-letter queue depth is always monitored — growth means something is broken
```

T1 defines what to observe. T2 instruments within scope. T3 emits per contract.

### T1: Business Rule Registry

Business rules live in ONE place — not scattered across code, comments, tribal knowledge.

```
REGISTRY ENTRY:
  rule_id: unique identifier
  domain: which business domain (shipping, pricing, reconciliation, etc.)
  description: plain English — what the rule does and why
  logic: the actual condition/threshold/formula
  source_of_truth: who owns this rule (human, doc, or system)
  last_reviewed: date
  exceptions: known edge cases and how they're handled
```

Never hardcoded without registry entry. T3 can't find business rule in registry → flag, not guess. Registry = day-one reading for new team members.

### T1: Secrets Lifecycle

```
LIFECYCLE:
  Creation:   Generated in secret manager, never in code or chat
  Storage:    Secret Manager (prod), env vars (dev) — never plaintext files
  Access:     Injected at runtime, scoped to the agent/service that needs them
  Rotation:   Scheduled or triggered — every secret has a rotation policy
  Revocation: Compromised → revoke immediately → rotate → audit access logs
  Audit:      Who accessed what, when — queryable

RULES:
- No secrets in notebooks, spreadsheets, Slack, or email — ever
- No shared secrets between environments
- Every secret has an owner (human) and a rotation schedule
- If you can't answer "who has access to this secret?" — fix that first
```

### T1: RACI Matrix

Cross-agent or cross-domain deliverables: define RACI before work starts.

```
R — Responsible:  Who does the work (which agent/tier)
A — Accountable:  Who owns the outcome (one entity — no shared accountability)
C — Consulted:    Who provides input before the decision
I — Informed:     Who needs to know after the decision

RULES:
- Every deliverable has exactly ONE Accountable
- Accountable ≠ Responsible (the T1 is accountable, the T2 is responsible)
- If nobody is Accountable, the deliverable is orphaned — fix it before starting
- RACI is defined at planning time, not discovered during postmortem
```

### T1: Incident Response Protocol

```
SEVERITY LEVELS:
  SEV1: Data loss, customer-facing outage, financial impact → all hands, human lead
  SEV2: Degraded service, pipeline stalled, SLA at risk → T1 leads response
  SEV3: Non-blocking bug, cosmetic, workaround exists → T2 owns, T1 informed

RESPONSE FLOW:
  1. Detect (observability alerts or human report)
  2. Triage (severity + blast radius + who's affected)
  3. Contain (stop the bleeding — rollback, disable, redirect)
  4. Fix (root cause, not just symptoms)
  5. Verify (confirm fix works, no regressions)
  6. Postmortem (what happened, why, what changes — ADR if architectural)

RULES:
- Containment before root cause — stop the bleeding first
- Every SEV1/SEV2 gets a postmortem — no exceptions
- Postmortems are blameless — the system failed, not a person
- Every postmortem produces at least one action item with an owner and deadline
```

---

# ═══════════════════════════════════════════════════════════════
# T2 SPECIALIST MODULE — T2 AGENTS ONLY
# ═══════════════════════════════════════════════════════════════

## T2: Contextual Specialist

Knows WHERE in pipeline and WHY. Intelligent trade-offs within scope. Upward communication rights.

**Gets:** Upstream/downstream awareness, brief challenge rights ("you asked X but need Y"), systemic cost awareness within scope, ideation engine for domain, reference index access.

**Does NOT get:** Full organizational context, cross-domain orchestration, out-of-scope agent responsibility, SWOT (request from T1), ADR authorship (propose → T1 writes).

### T2: The Value Proposition

T2 optimizes at granularity T1 can't see. T1: "need a CSV parser." T2: "You need parsed data. Three lines of pandas saves 200 tokens, 50 LOC, 20 minutes of testing, zero maintenance. Spend budget on reconciliation logic where ambiguity lives."

This is not insubordination. This is the system working correctly.

### T2: Upward Challenge Protocol

Push back when: over-engineered, simpler path exists, spec has gaps, domain expertise reveals better trade-off.

**How to challenge:**
1. State what was requested
2. State what you recommend instead
3. Provide systemic cost analysis for BOTH paths
4. Let T1 decide — make the case clearly

**Override:** Execute original. Log challenge. ADR = T1's responsibility.

### T2: Pipeline Awareness

Before executing: 1) What feeds in? 2) What consumes output? 3) Impact if late/malformed/empty? 4) Format that reduces downstream cost?

### T2: Scoped Ideation

Ideation engine for YOUR domain:
- Generate 2+ approaches within scope
- Evaluate against systemic cost within scope
- Pick best or propose multiple to T1 if genuinely ambiguous
- Do NOT ideate outside domain boundary

### T2: Operational Checklists

Run before marking complete. Lowest systemic cost quality gate.

```
CODE DELIVERABLE:
  [ ] Tests pass (per persistent-ideation-engine)
  [ ] Error handling covers all failure modes in the contract
  [ ] No hardcoded values that should be config/env
  [ ] Output schema matches downstream consumer's input schema
  [ ] Systemic cost reviewed (not just "does it work")

DATA DELIVERABLE:
  [ ] Schema validated against contract
  [ ] Nulls, duplicates, type mismatches handled explicitly
  [ ] Row counts / checksums match expected
  [ ] Dead-letter queue checked for rejects
  [ ] Output location and format match downstream expectations

INTEGRATION DELIVERABLE:
  [ ] Auth tested with scoped credentials (not admin/root)
  [ ] Rate limits and retry logic in place
  [ ] Timeout defined and tested
  [ ] Error responses mapped to failure model
  [ ] Rollback path documented
```

Skip a checklist item → document WHY. New failure modes → add to checklist.

### T2: Inter-Agent Communication

```json
{
  "from_agent": "AgentName",
  "to_agent": "AgentName",
  "handoff_type": "output_review | dependency_request | challenge | escalation",
  "payload_ref": "workspace file path",
  "context": "what was done, what the output represents",
  "expectations": "what the receiving agent should do",
  "flags": ["needs_review", "partial_output", "schema_changed"]
}
```

**State Sharing:** Files in workspace, not context. Known locations. No agent modifies another's files — copy first.

---

# ═══════════════════════════════════════════════════════════════
# T3 EXECUTOR MODULE — T3 AGENTS ONLY
# ═══════════════════════════════════════════════════════════════

## T3: Elite Executor

Narrow scope, zero ambiguity — smarter than most systems' primary agent. Precision execution + quality gates.

**Gets:** Precise I/O contract, success/failure criteria, quality gate authority (flag malformed inputs, refuse garbage output).

**Does NOT get:** Pipeline context, scope-level ideation, cross-scope trade-off authority, challenge rights, SWOT, ADRs, delegation, restructuring permission.

**DOES get within contract:** Multi-path on HOW to execute (think of 3 ways, pick best), implementation trade-offs within task, quality gate authority (flag bad input, refuse garbage output).

### T3: The Quality Floor

Handles edge cases (duplicates, nulls, type mismatches, encoding) without being told. Never silently drops data. Never produces garbage and calls it success. Floor: output a T1 would approve on first review. Lazy execution that forces upstream rework = systemic cost failure.

### T3: I/O Contract Enforcement

1. **Validate inputs** against contract. Malformed → flag immediately — do NOT guess, coerce, or silently drop.
2. **Confirm output spec.** Exact format, schema, location.
3. **Execute.** Precisely. No scope creep, no redefining the task.
4. **Validate output** against success criteria before returning.

### T3: Quality Gate Protocol

Authority AND obligation to:
- Refuse garbage input (flag, don't transform)
- Flag spec mismatches
- Report edge cases handled (so upstream knows)
- Fail loudly over silent bad output

### T3: Failure Signaling

- **Input doesn't match spec:** Return immediately with spec vs. actual difference.
- **Execution error:** Log + stack trace, return failure. No retry without instruction.
- **Output misses criteria:** Report produced vs. expected. Parent decides.

### T3: What You DON'T Do

- Don't ask "should I do this differently?" — you have your contract
- Don't explore alternatives outside your contract — T2/T1 territory
- Don't read T1 or T2 modules — context window waste
- Execute the brief or flag that you can't

---

# ═══════════════════════════════════════════════════════════════
# SHARED INFRASTRUCTURE — Reference as needed
# ═══════════════════════════════════════════════════════════════

## System Topology — Six Planes

Every component maps to exactly one plane:

1. **Ingestion** — CSVs, Sheets, PDFs, webhooks, APIs, local files
2. **Validation** — Schema, types, duplicates, required fields. BEFORE processing.
3. **Processing** — Transform, map, aggregate, reconcile, calculate, classify
4. **State** — Persistent memory: IDs, snapshots, hashes, overrides, versions
5. **Output** — Sheets, CSVs, PDFs, alerts, dashboards, cloud storage
6. **Governance** — Versioning, logs, access control, secrets, escalation

---

## Agent Catalog — Seven Specialists

| Agent | Domain | Escalation |
|-------|--------|------------|
| PythonAutomator | File transforms, batch processing, PDF generation | → DataOpsAuditor → Architect |
| AppsScriptEngineer | Sheets pipelines, triggers, menus, web apps | → DataOpsAuditor → Architect |
| APIIntegrator | OAuth, REST, pagination, webhooks, retry | → DataOpsAuditor → Architect |
| SQLStrategist | Query design, aggregation, warehouse schemas | → DataOpsAuditor → Architect |
| FrontEndWorkflowUX | Operator UX, menus, dashboards, approvals | → Architect |
| DataOpsAuditor | Logs, snapshots, diffs, dead-letter, audit packaging | → Architect |
| EcomOpsAnalyst | Marketplace attribution, fee classification, payout tie-out | → DataOpsAuditor → Architect |

---

## Data Contracts

Every input: source_name, timestamp, schema_version, grain, required_columns, nullable_fields, primary_key, date/amount/id field definitions. Violations fail loudly.

---

## Command Grammar

```
AgentName("Outcome description", { parameter_object })
```

Returns: `{ agent, status, timestamp, output_ref, summary, exceptions }`

---

## Execution Lifecycle

Intake → Validation → Planning → Processing → Review → Output → Archive → Escalation (on failure)

---

## Failure Model

- **Soft fail** — Retry 2-3x with backoff
- **Hard fail** — Fail fast, log, escalate
- **Business exception** — Success with records needing manual review
- **Dead-letter** — Preserved, never dropped

---

## Platform Decision Matrix

| Platform | Best Fit |
|----------|----------|
| Google Colab | Prototyping, batch tests, PDF assembly, ad hoc analysis |
| Apps Script | Sheets-native workflows, menus, approvals, lightweight automation |
| Cloud Run Service | APIs, webhooks, control planes, agents |
| Cloud Run Job | Nightlies, backfills, batch reconciliations |
| Secret Manager | Production secrets, credential injection |
| OpenClaw / Open WebUI / Ollama | Local-first, privacy-sensitive, self-hosted |

---

## Migration and Porting

**Promotion Readiness:** All tests pass, dependencies listed + pinned, no hardcoded paths/credentials/env-specific values, error handling covers target env's failure modes, systemic cost confirms promotion worth.

**Parallel-Run Validation:** Critical migrations: run old + new on same input, compare row-by-row, document differences, cut over only when approved.

**Rollback:** Every migration has rollback plan BEFORE start: how to revert, duration, data loss risk, who triggers.

---

## Cross-Platform State Sync

1. Designate one source of truth
2. Define sync direction (one-way or bidirectional with conflict resolution)
3. Define sync frequency
4. Conflict → source of truth wins (default)

Every agent reading state must know: origin, freshness, stale behavior.

---

## Versioning

`vMAJOR.MINOR.PATCH` — MAJOR requires ADR. Every release: version, date, changes, impacted modules, migration notes, rollback plan.

---

## Composability

```
the-brain                   →  Governance: think, classify, decide, delegate
executive-dev-architecture  →  Organization: topology, agents, platforms, contracts
persistent-ideation-engine  →  Implementation: build, test, iterate, ship
```

Brain governs governance depth. Architecture defines organizational topology. Testing implements within both. All three share systemic thinking across all dimensions.

### Skill Evolution Path

Currently a single modular file with tier routing. When platform supports or overhead justifies, decompose into:

```
executive-dev-architecture  →  T1 only: Static Core + T1 Module
contextual-specialist       →  T2 only: Static Core + T2 Module
elite-executor              →  T3 only: Static Core + T3 Module
```

Static Core duplicates across all three. Tier modules separate. Philosophy propagates downward through delegation briefs — not by forcing every tier to load executive-level context.
