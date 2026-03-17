# T1-C — PIE v4.1 Implementation Gaps

## Governance State

Classification: STRATEGIC (confidence: high). This vector changes suite-wide implementation and testing behavior, has multiple valid approaches, and crosses Brain/ExecDev boundaries, so it is system-level rather than a local wording edit ([classification record](file:///home/user/workspace/governance/classifications/t1-c-pie-v41-implementation-gaps.md)).

## Executive Summary

PIE v4.0 already has strong foundations: multiple-path exploration, harness-first execution, persistent iteration, adversarial probing, progressive scale testing, and path abandonment ([PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).

The main gap is not lack of testing philosophy; it is lack of explicit governance for when testing spans time, interacting agents, measurable completeness, and formal stopping conditions ([context brief](file:///home/user/workspace/swarm/context-brief.md), [PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).

My recommendations:

| Item | Recommendation | Why |
|---|---|---|
| 1. Periodic Execution Patterns | ADAPT | Needed for heartbeat/scheduled agents, but should be framed narrowly as schedule-aware testing inside PIE rather than full runtime scheduling governance. |
| 2. Convergence Metrics | ADOPT | PIE already says “until convergence,” but never defines convergence operationally. Formal criteria reduce endless looping and rationalized stopping. |
| 3. Test Coverage Quantification | ADAPT | Coverage should be required, but not reduced to line coverage alone; PIE needs a multidimensional coverage ledger. |
| 4. Adversarial Testing Protocol | ADOPT | PIE already encourages hostile probing, but v4.1 should formalize required classes of adversarial tests and failure expectations. |
| 5. Cross-Agent Integration Testing | ADOPT | Current PIE is implementation-centric and mostly single-agent; multi-agent pipelines now need first-class end-to-end and contract-chain testing. |

## Design Principle for v4.1

PIE should remain the implementation/testing metabolism, not expand into a full runtime platform ([context brief](file:///home/user/workspace/swarm/context-brief.md)).

So the right pattern is: add test-governance primitives for time, interaction, and completeness, while leaving mission tracing, budget enforcement, orchestration topology, and runtime circuit breakers primarily to Brain and ExecDev ([context brief](file:///home/user/workspace/swarm/context-brief.md)).

---

## 1) Periodic Execution Patterns (Heartbeat Testing)

### Assessment

Paperclip’s heartbeat model exposes a real PIE gap because PIE v4.0 assumes repeated test epochs inside one active work session, not behavior that unfolds across scheduled wakes, persisted state, and elapsed time windows ([context brief](file:///home/user/workspace/swarm/context-brief.md), [PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).

### SWOT

**Strengths**
- Extends PIE from on-demand loops to time-aware systems without abandoning its core ideate → implement → test → analyze loop ([PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).
- Catches failure classes invisible to single-run tests: duplicated work across heartbeats, missed wakeups, stale state, non-idempotent retries, and schedule drift.
- Aligns with Paperclip-style energy-efficient execution without forcing PIE to become the scheduler itself ([context brief](file:///home/user/workspace/swarm/context-brief.md)).

**Weaknesses**
- Adds substantial harness complexity because tests must simulate time passage, persisted state, and repeated invocations.
- Risks overlap with ExecDev state-machine/orchestration governance if PIE tries to define runtime scheduling semantics rather than test expectations.
- Harder to run cheaply because high-confidence schedule tests often require long-duration or accelerated-time simulation.

**Opportunities**
- Introduce a reusable “time-warp harness” pattern for scheduled agents.
- Define idempotency/state-persistence checks as standard gates for any non-on-demand agent.
- Improve reliability for cron-like automations, inbox triage agents, monitor/watcher agents, and maintenance daemons.

**Threats**
- Over-formalizing schedule governance inside PIE could duplicate Brain/ExecDev responsibilities and blur skill boundaries.
- Teams may cargo-cult heartbeat test suites onto simple one-shot tools, inflating cost without value.
- Poorly specified simulated-time tests can create false confidence if production timing semantics differ.

### Systemic Cost Analysis (8 dimensions)

| Dimension | Impact | Analysis |
|---|---|---|
| Tokens/Credits | Medium-High | More planning, more harness logic, more iterations per feature. |
| Time | High | Stateful and elapsed-time scenarios lengthen test cycles. |
| Compute | Medium-High | Repeated schedule runs, storage snapshots, and concurrency simulation increase runtime load. |
| Lines of Code | Medium | Needs helpers for clock control, fixture snapshots, and replay. |
| Cognitive Load | High | Developers must reason about time, persistence, idempotency, and recovery, not just pure function behavior. |
| Context Window | Medium | Test specs must include schedule rules, state invariants, and replay scenarios. |
| Human Interventions | Low-Medium | Good harnesses reduce production debugging, but initial authoring/review burden rises. |
| Technical Debt | Low if scoped well; High if not | Strong upside if standardized; major debt if PIE drifts into runtime scheduling architecture. |

### Recommendation

**ADAPT.** PIE should govern **testing requirements for periodic agents**, but not define the runtime heartbeat system itself.

Rationale: the gap is real, but the control boundary matters. PIE should answer “how do we test scheduled behavior?” rather than “how should all agents schedule themselves?” That keeps PIE implementation-focused while still covering Paperclip’s heartbeat pattern.

### Specification Sketch

Add a v4.1 section: **Periodic / Scheduled Execution Testing**.

Proposed requirements:
1. **Applicability trigger:** If an agent wakes on schedule, on heartbeat, or via polling loop, schedule-aware tests are mandatory.
2. **Minimum harness capabilities:**
   - controllable clock or accelerated-time simulation
   - persisted-state snapshot/load between runs
   - repeated-invocation replay over at least 3 consecutive heartbeats
   - missed-heartbeat and delayed-heartbeat scenarios
3. **Required assertions:**
   - idempotency across repeated heartbeats
   - no duplicate side effects after restart/replay
   - correct persistence and restoration of state
   - correct behavior when no work is present
   - bounded backlog catch-up behavior after downtime
4. **Minimum suite shape:**
   - nominal heartbeat sequence
   - recovery after interruption
   - delayed schedule / drift
   - duplicate invocation / replay
   - empty cycle / no-op cycle
5. **Ship gate:** No scheduled agent ships without evidence that state persistence, replay safety, and multi-heartbeat regression tests pass.

### Boundary Note

PIE should reference ExecDev/Brain for authoritative scheduling/orchestration semantics, not redefine them here.

---

## 2) Convergence Metrics

### Assessment

PIE v4.0 explicitly says to continue until convergence and not stop merely at “10 passes,” but it leaves convergence qualitative rather than operational ([PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).

That is a strong philosophy but a weak governance primitive, because different agents can rationalize both premature stopping and endless looping.

### SWOT

**Strengths**
- Clarifies when to stop iterating and when continued effort is justified.
- Reduces agent thrash and unbounded refinement loops.
- Makes PIE more auditable by turning “convergence” into observable evidence instead of vibe-based judgment.

**Weaknesses**
- Overly rigid convergence rules can terminate too early on rare or high-severity failures.
- Metrics can be gamed if agents optimize the number rather than actual robustness.
- Some work, especially exploratory or UX-heavy work, resists clean convergence measurement.

**Opportunities**
- Standardize a “convergence ledger” across epochs: pass stability, regression count, failure novelty, performance trend, and cost trend.
- Create explicit escalation triggers when convergence stalls or oscillates.
- Make path-abandonment more principled by tying it to stalled improvement curves.

**Threats**
- Metric theater: good-looking charts that hide poor test diversity.
- Teams may stop on pass-rate stabilization even when severe edge cases remain untested.
- A single universal threshold may be wrong across radically different project types.

### Systemic Cost Analysis (8 dimensions)

| Dimension | Impact | Analysis |
|---|---|---|
| Tokens/Credits | Low-Medium | Extra bookkeeping and reporting each epoch. |
| Time | Low-Medium | Some overhead, but often saves time by preventing endless loops. |
| Compute | Low | Minimal additional runtime versus the tests themselves. |
| Lines of Code | Low | Mostly reporting structures, not major runtime machinery. |
| Cognitive Load | Medium | Teams must interpret multi-signal convergence rather than a binary pass/fail. |
| Context Window | Medium | Each epoch may now carry a compact trend summary. |
| Human Interventions | Low | Good criteria reduce unnecessary review escalation and “are we done?” loops. |
| Technical Debt | Low | Strong positive if criteria remain simple and exception-aware. |

### Recommendation

**ADOPT.** PIE v4.1 should define formal convergence criteria as a required decision layer before ship.

Rationale: convergence is already part of PIE’s philosophy; v4.1 should make it executable. This is a clarification and hardening of the existing engine, not a scope expansion.

### Specification Sketch

Add a v4.1 section: **Convergence and Stop Conditions**.

Proposed rule set:
1. **Convergence is multi-signal, not single-metric.**
2. An iteration loop may conclude only when all required conditions are met:
   - full suite pass rate is stable or improving across the last N epochs
   - zero regressions versus prior passing tests
   - no new failure class discovered in the last N epochs
   - severity-weighted open failures = 0 for ship, or explicitly deferred with rationale
   - marginal improvement from the latest epoch is below a defined threshold **and** no risk-critical gap remains
3. **Default evidence window:** last 3 epochs.
4. **Mandatory tracked signals per epoch:**
   - pass count / fail count
   - regression count
   - new failure-class count
   - runtime / resource trend
   - human interventions required
   - dominant root-cause category
5. **Anti-rationalization clauses:**
   - stable failures do not equal convergence
   - low-severity churn cannot hide a high-severity open defect
   - “time pressure” is not convergence
6. **Path-abandonment trigger:** 3 consecutive epochs with no material improvement on the same root issue require re-evaluation of approach, consistent with PIE’s existing abandonment protocol ([PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).

---

## 3) Test Coverage Quantification

### Assessment

PIE v4.0 strongly mandates testing breadth in practice, including real data, adversarial probes, progressive scale, and full-suite re-runs, but it never quantifies whether the suite is complete enough ([PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).

That leaves a blind spot: an agent can test intensely inside a narrow slice of reality and still claim compliance.

### SWOT

**Strengths**
- Adds objective visibility into test completeness.
- Helps compare different implementations and track whether new changes expand or shrink protection.
- Forces explicit accounting for scenario classes that PIE already values implicitly.

**Weaknesses**
- Pure numeric thresholds can become shallow compliance targets.
- Coverage measurement varies by artifact type; code coverage alone is insufficient for UI, integrations, pipelines, and schedule-based systems.
- Instrumentation overhead can be non-trivial in some environments.

**Opportunities**
- Define a multidimensional coverage model that better fits PIE’s philosophy than standard line coverage.
- Surface blind spots early: untested failure modes, data shapes, environmental conditions, concurrency modes.
- Improve council/swarm review quality because reviewers can inspect coverage gaps, not just pass counts.

**Threats**
- If reduced to line coverage, teams may hit a number while missing system behavior.
- Coverage dashboards can become bureaucratic if every tiny tool must satisfy enterprise-level instrumentation.
- False precision may hide weak assertions or low-quality tests.

### Systemic Cost Analysis (8 dimensions)

| Dimension | Impact | Analysis |
|---|---|---|
| Tokens/Credits | Medium | More planning and reporting to define the coverage ledger. |
| Time | Medium | Instrumentation and gap-closing increase upfront effort. |
| Compute | Medium | Coverage collection and broader suites add overhead. |
| Lines of Code | Medium | Helpers, matrices, and instrumentation raise supporting code volume. |
| Cognitive Load | Medium-High | Teams must understand several coverage dimensions, not one scalar. |
| Context Window | Medium | Coverage matrices take space unless compressed well. |
| Human Interventions | Low-Medium | Better visibility reduces review churn, but initial framework design needs thought. |
| Technical Debt | Low if multidimensional; Medium if naive | Strong upside if it prevents silent blind spots; downside if it locks PIE into brittle metrics. |

### Recommendation

**ADAPT.** PIE should quantify coverage, but through a **coverage ledger** rather than a single minimum percentage.

Rationale: completeness matters, but a single threshold would distort behavior. PIE’s philosophy is scenario realism and robustness, so the metric model should mirror that.

### Specification Sketch

Add a v4.1 section: **Coverage Ledger and Minimum Sufficiency**.

Proposed model:
1. **Coverage must be reported across at least these dimensions:**
   - input/data-shape coverage
   - path/branch coverage where tooling exists
   - failure-mode coverage
   - scale-tier coverage
   - environment coverage (runtime/platform/browser/server/etc.)
   - state-transition or lifecycle coverage for stateful systems
   - interaction coverage for external dependencies
2. **Minimum ship requirement:** no dimension may be completely unmeasured when it is relevant to the system under test.
3. **Required artifact:** a compact coverage matrix listing tested vs untested scenario classes and explicit rationale for any uncovered class.
4. **Suggested thresholds:**
   - branch/path coverage: target threshold where tooling is available, but not sole gate
   - failure-mode coverage: all known high-severity modes must be exercised
   - scale coverage: at least small, medium, and largest-available tiers
   - environment coverage: every claimed deployment environment must be tested or explicitly excluded
5. **Anti-theater rule:** high code coverage cannot waive missing scenario coverage.

### Implementation Note

This addition should be deliberately lightweight in wording so it creates visibility, not reporting bloat.

---

## 4) Adversarial Testing Protocol

### Assessment

PIE v4.0 already contains adversarial self-probing, including malformed inputs, scale stress, missing dependencies, boundary conditions, race conditions, and environment gaps ([PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md)).

So the question is not whether adversarial testing belongs in PIE; it already does. The gap is that it is described as good practice rather than formal protocol.

### SWOT

**Strengths**
- Already consistent with PIE’s current philosophy, so formalization is low-friction.
- Better matches Paperclip-inspired circuit-breaker thinking by testing failure containment before production incidents ([context brief](file:///home/user/workspace/swarm/context-brief.md)).
- Raises robustness against hostile inputs, integration instability, and pathological workloads.

**Weaknesses**
- Can become expensive if every system must run exhaustive chaos-style campaigns.
- Some adversarial scenarios require sophisticated harnesses or controlled infrastructure to simulate accurately.
- Too much emphasis on breakage can distract from normal-path usability if not balanced.

**Opportunities**
- Standardize adversarial classes so agents know the minimum hostile scenarios to run.
- Connect adversarial outcomes to explicit failure expectations: fail fast, retry, isolate, degrade gracefully, or require manual review.
- Improve incident prevention by surfacing resource exhaustion and concurrency bugs earlier.

**Threats**
- Unbounded chaos testing can waste time on edge cases with low relevance.
- If protocol lacks severity-based prioritization, teams may spend equal effort on trivial and catastrophic scenarios.
- Poorly contained fault injection can damage shared test environments.

### Systemic Cost Analysis (8 dimensions)

| Dimension | Impact | Analysis |
|---|---|---|
| Tokens/Credits | Medium | Extra scenario design and analysis work. |
| Time | Medium-High | Hostile scenarios materially expand suite duration. |
| Compute | Medium-High | Stress, concurrency, and resource tests can be expensive. |
| Lines of Code | Medium | Fault injection and chaos helpers add support code. |
| Cognitive Load | Medium | Teams must think in terms of failure behavior, not just correctness. |
| Context Window | Low-Medium | Can be summarized as attack-class checklists and outcomes. |
| Human Interventions | Low | Strong protocol reduces production firefighting and bug triage. |
| Technical Debt | Low | Good protocol lowers debt by preventing brittle systems from shipping. |

### Recommendation

**ADOPT.** PIE v4.1 should formalize an adversarial testing protocol.

Rationale: PIE already contains the seed of this idea; formalizing it upgrades consistency and auditability without changing PIE’s identity.

### Specification Sketch

Add a v4.1 section: **Adversarial and Failure-Injection Testing**.

Proposed minimum adversarial classes:
1. malformed/invalid inputs
2. boundary-value extremes
3. missing/slow/unavailable dependencies
4. timeout and retry behavior
5. concurrency / duplicate invocation / race behavior
6. resource pressure: large payloads, memory pressure, queue growth, rate-limit pressure
7. environment mismatch / permission limitations
8. partial-state corruption or interrupted execution for stateful systems

Protocol requirements:
- Each relevant class must be either exercised or explicitly marked not applicable.
- Each adversarial test must assert an expected failure mode: graceful degradation, bounded retry, fast fail, rollback, dead-letter/manual review, or safe no-op.
- Resource-exhaustion and timeout tests are mandatory for long-running or externally dependent systems.
- Concurrency/duplicate-trigger tests are mandatory for stateful, scheduled, or multi-agent systems.
- Fault injection must run in isolated test conditions.

### Boundary Note

PIE should test against circuit-breaker expectations but should not own the suite-wide circuit-breaker architecture itself; that belongs upstream.

---

## 5) Cross-Agent Integration Testing

### Assessment

The swarm context explicitly notes that Paperclip’s org-chart delegation means agents interact, while current PIE mainly focuses on the implementation loop itself rather than explicit multi-agent chain validation ([context brief](file:///home/user/workspace/swarm/context-brief.md)).

This is the biggest structural gap because single-agent correctness does not guarantee pipeline correctness.

### SWOT

**Strengths**
- Protects against interface drift, handoff mismatches, duplicated work, dropped state, and orchestration dead zones.
- Complements Brain/ExecDev by validating the actual interaction chain, not just the theoretical contract design.
- Brings PIE in line with real swarm behavior, where failure often lives between agents rather than inside any one agent.

**Weaknesses**
- Multi-agent integration suites are harder to build, slower to run, and more brittle than local unit tests.
- Ownership can become ambiguous: who maintains the end-to-end harness?
- Failures are harder to localize because several agents may contribute.

**Opportunities**
- Define contract-chain tests, replay tests, and degraded-node tests for pipelines.
- Reduce downstream rework by catching schema/semantic mismatches before merge.
- Create reusable patterns for handoff assertions: schema, semantics, state continuity, retry behavior, and escalation signals.

**Threats**
- If PIE overreaches, it may start redefining orchestration architecture instead of testing it.
- End-to-end suites can become flaky if underlying fixtures are unstable.
- Heavyweight integration testing on every change can slow iteration sharply.

### Systemic Cost Analysis (8 dimensions)

| Dimension | Impact | Analysis |
|---|---|---|
| Tokens/Credits | High | Richer harnesses and broader analysis across interfaces. |
| Time | High | End-to-end and replay tests increase cycle time materially. |
| Compute | Medium-High | Multiple agents or simulated nodes increase runtime cost. |
| Lines of Code | High | Mock agents, orchestration fixtures, and chain assertions add substantial support code. |
| Cognitive Load | High | Engineers must reason across contracts, sequencing, failure ownership, and semantics. |
| Context Window | High | Multi-agent test plans require more context unless carefully modularized. |
| Human Interventions | Medium | Better than production debugging, but triage/review of integration failures is inherently harder. |
| Technical Debt | Low if standardized; High if ad hoc | Strong upside when built as reusable patterns; messy debt if each pipeline invents its own scheme. |

### Recommendation

**ADOPT.** PIE v4.1 should include first-class cross-agent integration testing guidance.

Rationale: this is now core to the suite’s real operating model. Without it, the system tests parts but not the organism.

### Specification Sketch

Add a v4.1 section: **Cross-Agent and Pipeline Testing**.

Proposed requirements:
1. **Applicability trigger:** Any workflow where outputs of one agent become inputs, decisions, or state for another agent requires integration testing.
2. **Required test layers:**
   - contract compatibility tests at each boundary
   - end-to-end happy path across the full chain
   - degraded-node tests where one upstream or downstream agent is slow, partial, or unavailable
   - replay/idempotency tests for duplicate handoffs
   - escalation-path tests for failures requiring review or fallback
3. **Required assertions at each handoff:**
   - schema validity
   - semantic validity, not just field presence
   - state continuity / correlation IDs where relevant
   - no silent loss, duplication, or mutation of critical data
4. **Minimum strategy rule:**
   - fast boundary/contract tests run frequently
   - heavier end-to-end suites run at meaningful checkpoints
5. **Failure localization rule:** integration failures must record which boundary failed, what contract was expected, what arrived, and whether the defect is producer-side, consumer-side, or orchestration-side.

### Boundary Note

ExecDev should define contracts and orchestration structure; PIE should define how to test whether those structures actually hold under execution.

---

## Synthesis Across All Five Items

### What v4.1 Should Add

PIE v4.1 should add four major implementation-governance upgrades and one scoped extension:
- formal convergence criteria
- multidimensional coverage quantification
- formal adversarial/failure-injection protocol
- first-class cross-agent integration testing
- schedule-aware testing for periodic agents, scoped to testing rather than runtime governance

### What v4.1 Should Avoid

PIE v4.1 should **not** become the owner of:
- heartbeat runtime architecture
- company/mission ancestry
- budget enforcement and auto-pause policy
- immutable audit-log platform design
- full orchestration topology or organizational hierarchy

Those belong primarily to Brain and ExecDev per the swarm split ([context brief](file:///home/user/workspace/swarm/context-brief.md)).

### Net Effect on PIE Identity

These changes make PIE more complete, not less focused, if the document stays anchored on one question: **how do we test and decide implementation readiness under realistic operating conditions?**

---

## Recommended v4.1 Insertions (Compact Draft Language)

### A. New Section: Convergence and Stop Conditions

“Continue until convergence” becomes “Continue until the last 3 epochs show stable or improving full-suite results, zero regressions, no newly discovered failure class, and no unresolved high-severity defect. Stable failure is not convergence. Time pressure is not convergence.

Track per epoch: pass/fail counts, regressions, new failure classes, runtime/resource trend, and human interventions required.”

### B. New Section: Coverage Ledger

“Testing completeness must be quantified through a coverage ledger, not pass count alone. Relevant dimensions include input shapes, path/branch coverage where available, failure modes, scale tiers, environments, state transitions, and dependency interactions. No relevant dimension may be entirely unmeasured at ship time. High code coverage does not waive missing scenario coverage.”

### C. New Section: Adversarial and Failure-Injection Testing

“For every relevant system, exercise malformed inputs, boundary extremes, dependency failures, timeout/retry paths, concurrency/duplicate-trigger behavior, resource pressure, and environment limitations. Each adversarial test must assert expected failure behavior: graceful degradation, bounded retry, fast fail, rollback, manual-review routing, or safe no-op.”

### D. New Section: Periodic / Scheduled Execution Testing

“If a system executes on schedule, heartbeat, or polling cadence, test across multiple consecutive cycles using controllable time and persisted state. Required checks: idempotency across repeated cycles, safe replay after restart, empty-cycle correctness, delayed-cycle recovery, and bounded backlog catch-up.”

### E. New Section: Cross-Agent and Pipeline Testing

“If one agent’s output becomes another agent’s input, integration testing is mandatory. Validate each handoff for schema, semantics, state continuity, duplication/loss, and escalation behavior. Use both fast boundary tests and slower end-to-end chain tests. Record boundary-localized failure evidence.”

---

## Cross-Facet Flags

### Flags for T1-A (Brain)

1. **Heartbeat governance ownership boundary:** If Brain adopts heartbeat governance or circuit-breaker policy, it should explicitly state that PIE only owns the test protocol for those behaviors, not the runtime control plane.
2. **Convergence vs budget/cost stops:** If Brain introduces budget enforcement or auto-pause patterns, it should reconcile them with PIE convergence criteria so agents do not stop because budget is exhausted while claiming technical convergence.
3. **Failure semantics alignment:** If Brain formalizes circuit breakers, PIE adversarial tests should map to the same failure outcomes vocabulary: fail fast, retry, safe no-op, isolate, manual review, or pause.
4. **Auditability dependency:** If Brain strengthens immutable audit or telemetry, PIE convergence/coverage artifacts could become auditable evidence streams rather than prose summaries.

### Flags for T1-B (ExecDev)

1. **Cross-agent contract-chain dependency:** PIE can require integration testing, but ExecDev must provide authoritative contract, handoff, and orchestration schemas for those tests to target.
2. **State and replay semantics:** Scheduled-agent tests and pipeline replay tests need ExecDev clarity on state ownership, transition authority, and idempotency expectations.
3. **Portable templates opportunity:** If ExecDev adds portable templates, it should consider including reusable test-harness templates for coverage ledgers, boundary tests, replay tests, and scheduled-agent test scaffolds.
4. **Runtime skill injection risk:** If ExecDev formalizes runtime skill injection, PIE will need to treat skill-injection changes as an integration surface that requires compatibility and regression testing.

---

## Final Recommendation Stack

| Item | Recommendation | Why |
|---|---|---|
| Periodic Execution Patterns | ADAPT | Real gap, but testing-only scope in PIE. |
| Convergence Metrics | ADOPT | Existing concept needs operational definition. |
| Test Coverage Quantification | ADAPT | Necessary, but multidimensional rather than scalar. |
| Adversarial Testing Protocol | ADOPT | Already philosophically present; formalize it. |
| Cross-Agent Integration Testing | ADOPT | Critical gap for multi-agent reality. |

## Confidence

Confidence: HIGH.

Rationale: the recommendations preserve PIE’s current identity while closing the most material implementation-governance gaps visible from the v4.0 text and swarm brief ([PIE v4.0](file:///home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md), [context brief](file:///home/user/workspace/swarm/context-brief.md)).
