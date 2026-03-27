# T1 Swarm Context Brief — v4.4 Suite Ideation

## Current State

### Active Package (v4.3 compressed, 11,943 words total)
- **The Brain v4.3** (4,798 words) — Governance: classify, decide, delegate. SWOT, council, swarm, lossless compression, Prime/Operational Directives for Perplexity Computer.
- **Executive Dev Architecture v3.2** (4,447 words) — Organization: tier routing, agent catalog, contracts, orchestration, state machines, RACI, observability.
- **Persistent Ideation Engine v4.0** (2,698 words) — Implementation: build, test, iterate, ship. ML-like training loop for code.

### All 3 Skills Verified
- Full-package audit: 0 findings
- Cross-skill parity: 15/15
- All structural/semantic kernels intact

## External Reference: Paperclip AI (github.com/paperclipai/paperclip)

Open-source orchestration for "zero-human companies." Relevant patterns:

### What Paperclip Does Well (That We Should Evaluate)
1. **Heartbeat system** — Agents wake on schedule, check work, act. Not always-on. Energy-efficient execution model.
2. **Goal ancestry** — Every task traces back through project goals to company mission. Agents always know the "why."
3. **Atomic budget enforcement** — Task checkout + budget check in single operation. Auto-pause at 100%, soft warning at 80%.
4. **Immutable audit log** — Append-only history for all decisions and tool calls.
5. **Runtime skill injection** — Agents learn workflows/context at runtime without retraining.
6. **Portable company templates** — Export/import orgs, agents, skills with secret scrubbing.
7. **Multi-company isolation** — One deployment, many companies, complete data isolation.
8. **Org chart as delegation structure** — reports_to relationships, hierarchical delegation.

### Where Paperclip Differs From Our Architecture
- Paperclip is a runtime platform (Node.js server + Postgres + React UI). We're a governance/methodology skill suite.
- Paperclip uses heartbeat-based execution; we use classification-driven governance.
- Paperclip has explicit monthly budgets per agent; we have cost governance by tier but no formal budget mechanism.
- Paperclip has immutable audit logs as a system feature; we have ADRs and telemetry as process artifacts.
- Paperclip models companies; we model decision-making and execution quality.

### Potential Gaps in Our Suite (Informed by Paperclip)
1. No formal "heartbeat" or periodic execution governance pattern
2. No explicit budget/quota enforcement mechanism (we have cost awareness but no hard limits)
3. No immutable audit log specification (ADRs are mutable, telemetry is schema-only)
4. Goal ancestry / mission alignment not explicit (we have task classification but not mission tracing)
5. No portable template / export-import protocol for skill packages
6. No multi-context isolation model (equivalent to multi-company)
7. Runtime skill injection not formalized (we load skills but don't govern the injection lifecycle)
8. No circuit breaker / auto-pause pattern in failure model

## Swarm Assignment

Each T1 agent attacks ONE vector. Produce: analysis, SWOT, proposals with systemic cost analysis, cross-facet flags.

### Vector Assignments
- **T1-A: Brain v4.4** — Governance gaps: budget enforcement, circuit breakers, immutable audit, goal ancestry, heartbeat governance
- **T1-B: ExecDev v3.3** — Organizational gaps: portable templates, multi-context isolation, runtime skill injection lifecycle, agent communication protocols
- **T1-C: PIE v4.1** — Implementation gaps: periodic execution patterns, convergence metrics, test coverage quantification, adversarial testing against Paperclip-style patterns
