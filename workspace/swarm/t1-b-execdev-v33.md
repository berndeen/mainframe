# T1-B Swarm Vector: ExecDev v3.3 — Organizational Gaps

**Objective:** Analyze 5 potential additions to Executive Dev Architecture (inspired by Paperclip AI) and provide SWOT, systemic cost analysis, recommendations, and concrete specification sketches for adopted/adapted items.

---

## 1. Portable Skill/Template Protocol
*Idea: Formal export/import protocol for skill packages with secret scrubbing and collision handling.*

### SWOT Analysis
- **Strengths:** Enables sharing, marketplace economies, and fast "one-click" environment instantiations. Encourages strict modularity.
- **Weaknesses:** Increases schema complexity. Secret scrubbing is notoriously difficult to guarantee 100%. Version collisions can break existing swarms.
- **Opportunities:** Community templates, standardization of agentic tools across organizations.
- **Threats:** Fragmentation if standards diverge. Bloat if templates package unneeded dependencies. Security risks from importing third-party templates.

### Systemic Cost Analysis
- **Tokens/Compute:** Negligible impact on execution.
- **Time:** Increases initial architectural dev time; drastically reduces setup time for new deployments.
- **Lines of Code:** High increase (packaging, validation, scrubbing logic).
- **Cognitive Load:** Medium increase (developers must learn the packaging standard).
- **Context Window:** Low impact (templates are parsed, not kept in active memory).
- **Human Interventions:** Reduces manual setup error; requires human audit on imported templates.
- **Technical Debt:** High risk if versioning semantics are poorly designed.

### Recommendation: ADAPT
**Rationale:** Full "company" templates are out of scope for ExecDev (which is an architecture, not a platform), but a standardized, portable format for *Skills* is highly valuable. We should adapt this into a **Skill Package Manifest** that declares dependencies and environment requirements without containing runtime secrets.

### Specification Sketch
Add to **Shared Infrastructure**:
```yaml
## Portable Skill Manifest (skill.json)
Every skill MUST export a manifest defining its boundary, dependencies, and requirements. No hardcoded secrets.

{
  "name": "sales-pipeline",
  "version": "1.2.0",
  "tier_compatibility": ["T1", "T2"],
  "dependencies": ["the-brain@^4.0"],
  "env_requirements": [
    { "key": "CRM_API_KEY", "description": "Read/write access to CRM", "secret": true }
  ],
  "entrypoint": "README.md",
  "collision_strategy": "namespace_prefix"
}
```

---

## 2. Multi-Context Isolation
*Idea: Model how agents maintain isolation across different projects/companies/contexts within a single deployment.*

### SWOT Analysis
- **Strengths:** Highly efficient resource utilization. Centralized infrastructure and governance.
- **Weaknesses:** Catastrophic blast radius if isolation fails (cross-tenant data leakage).
- **Opportunities:** Enables multi-tenant B2B architectures and agency models (one swarm managing multiple clients).
- **Threats:** Context window poisoning if isolation metadata leaks into execution prompts.

### Systemic Cost Analysis
- **Tokens/Compute:** Low.
- **Time:** Significant upfront engineering time to enforce isolation at the file and state level.
- **Lines of Code:** High (RBAC and tenant-scoping throughout the codebase).
- **Cognitive Load:** High (developers must always maintain tenant awareness).
- **Context Window:** Low (assuming scoped contexts).
- **Human Interventions:** Reduces ops overhead (one deploy for many contexts).
- **Technical Debt:** Massive if bolted on later; must be native to the architecture.

### Recommendation: ADAPT
**Rationale:** Paperclip relies on this because it's a runtime platform. ExecDev is a methodology. We shouldn't build a multitenant database, but we MUST define the architectural pattern for *Context Isolation* so developers building on ExecDev know how to isolate data safely.

### Specification Sketch
Add to **Shared Infrastructure**:
```markdown
## Context Isolation Pattern
When a swarm operates across multiple contexts (e.g., clients, projects):
1. **Workspace Partitioning:** `workspace/{context_id}/...` — Agents MUST be jailed to the context's directory.
2. **State Jailing:** State stores MUST require `context_id` as the primary partition key.
3. **Secret Scoping:** Secrets are namespaced `context_{id}_crm_key`, never globally shared.
4. **Context Injection:** Delegation briefs must explicitly declare the `context_id`. Cross-context reasoning is strictly prohibited unless explicitly authorized by a T1-Super agent.
```

---

## 3. Runtime Skill Injection Lifecycle
*Idea: Formalize when skills are loaded, how they compose, versioning during runtime, and graceful degradation.*

### SWOT Analysis
- **Strengths:** Drastically reduces context window bloat (load on demand). Defines clear failure modes for missing skills.
- **Weaknesses:** Adds latency during execution. Potential race conditions if skills update mid-flight.
- **Opportunities:** Dynamic, highly-adaptive agents that fetch knowledge just-in-time.
- **Threats:** Cascading failures if a core dependency cannot be injected.

### Systemic Cost Analysis
- **Tokens/Compute:** Major reduction in tokens (smaller context windows).
- **Time:** Slight latency on injection.
- **Lines of Code:** Medium (lifecycle management).
- **Cognitive Load:** Medium (understanding transient skill states).
- **Context Window:** Massive savings (primary benefit).
- **Human Interventions:** None at runtime.
- **Technical Debt:** Low.

### Recommendation: ADOPT
**Rationale:** We currently load skills ad-hoc. Formalizing the injection, ejection, and degradation lifecycle is essential for scaling complex swarms without hitting context limits.

### Specification Sketch
Add to **T1 Executive Module**:
```markdown
### Runtime Skill Injection Lifecycle
Skills are transient context, not permanent identity.
1. **Discovery:** Agent identifies a capability gap.
2. **Resolution & Injection:** Agent requests skill load. If version conflict exists, newest compatible version wins.
3. **Execution:** Skill active in context window.
4. **Ejection:** Upon task completion, skill is dropped from active context to free tokens.
5. **Graceful Degradation:** If injection fails (missing/offline), agent executes `<SELF-TEST>`: Can outcome be achieved via base tools? 
   - YES → Proceed with base tools.
   - NO → Halt and escalate (T2/T3) or re-plan (T1).
```

---

## 4. Agent Communication Protocol Enhancement
*Idea: Enhance JSON handoff with message routing, priority queuing, acknowledgment, and dead-letter for failed handoffs.*

### SWOT Analysis
- **Strengths:** Robust asynchronous execution. Spikes in workload are handled gracefully. Zero lost messages.
- **Weaknesses:** Overkill for simple, synchronous tasks. Requires queue infrastructure.
- **Opportunities:** Decoupled micro-agents. Seamless human-in-the-loop (human acts as just another node in the queue).
- **Threats:** Queue deadlocks. Complex asynchronous debugging.

### Systemic Cost Analysis
- **Tokens/Compute:** Slight increase (envelope parsing, acks).
- **Time:** Async introduces wait states but improves overall swarm throughput.
- **Lines of Code:** High (message brokers, retry logic).
- **Cognitive Load:** High (async programming model).
- **Context Window:** N/A.
- **Human Interventions:** Requires ops monitoring of queue depths.
- **Technical Debt:** Medium.

### Recommendation: ADAPT
**Rationale:** We do not want to mandate a specific ticket/queue system (like Paperclip does), as that locks users into a specific tech stack. However, we DO need to enhance our current JSON handoff schema to *support* asynchronous envelopes, acks, and dead-letters.

### Specification Sketch
Update **T2: Inter-Agent Communication**:
```json
{
  "envelope": {
    "msg_id": "uuid",
    "reply_to": "msg_id_or_null",
    "priority": "high | standard | low",
    "ttl": "timestamp",
    "status": "dispatch | ack | nack | dead-letter"
  },
  "payload": {
    "from_agent": "AgentName",
    "to_agent": "AgentName_or_Role",
    "handoff_type": "output_review | dependency_request | challenge | escalation",
    "payload_ref": "workspace_file_path",
    "context": "what was done",
    "expectations": "what to do"
  }
}
```
*Rule:* Every `dispatch` requires an `ack` or `nack`. If `ttl` expires, the message is routed to the Dead-Letter Queue.

---

## 5. Goal Ancestry in Agent Contracts
*Idea: Every agent contract includes mission/goal tracing so agents know WHY they're executing, not just WHAT.*

### SWOT Analysis
- **Strengths:** Prevents semantic drift ("doing the thing right, but doing the wrong thing"). Aligns swarm with human intent.
- **Weaknesses:** Takes up valuable context window. Might confuse strict executor agents.
- **Opportunities:** Dynamic reprioritization. Better autonomous trade-off decisions by T2 agents.
- **Threats:** Over-contextualizing T3 agents leading to hallucinated scope creep.

### Systemic Cost Analysis
- **Tokens/Compute:** Low to Moderate increase (ancestry strings).
- **Time:** Negligible.
- **Lines of Code:** Low.
- **Cognitive Load:** Low.
- **Context Window:** Moderate increase.
- **Human Interventions:** Reduces need for manual realignment.
- **Technical Debt:** Low.

### Recommendation: ADAPT
**Rationale:** Goal ancestry is brilliant, but it must be strictly tiered. T1 needs the full company mission. T3 only needs to know the immediate objective. Passing the entire corporate mission to a T3 CSV parser is a waste of context and invites hallucination.

### Specification Sketch
Add to **Delegation Protocol**:
```markdown
### Tiered Goal Ancestry
Every delegation brief MUST include an ancestry trace, scoped by tier to prevent context waste:
- **T1:** `[Mission] -> [Initiative] -> [Objective]` (Requires full strategic alignment)
- **T2:** `[Initiative] -> [Objective] -> [Task]` (Requires pipeline alignment)
- **T3:** `[Objective] -> [Task]` (Requires strictly local alignment)

This ensures every agent knows the immediate "WHY" without suffering from scope-creep or context bloat.
```

---

## Cross-Facet Flags for Swarm Synchronization

**For T1-A (Brain / Governance):**
- **Budgeting vs. Goal Ancestry:** If Brain implements atomic budget enforcement, it should map directly to the *Goal Ancestry* tree (e.g., budgets are allocated at the `Initiative` level and cascade down, rather than just per-agent).
- **Queue Governance:** If ExecDev formalizes async communication (`ack/nack` and dead-letter), Brain must define the governance rules for queue health (e.g., at what dead-letter depth is a SEV2 incident triggered?).

**For T1-C (PIE / Implementation):**
- **Injection Degradation Testing:** PIE must build test patterns to simulate network/registry failures during *Runtime Skill Injection* to verify that agents degrade gracefully rather than crash.
- **Async Communication Testing:** PIE needs to introduce mock message brokers to test how agents handle `nack` responses, timeouts (`ttl`), and dead-letter scenarios.
