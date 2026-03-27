# T1-T3 Conceptual Logic Audit — Brain v4.3
## Methodology: Read every line that mentions T1, T2, or T3. Check for contradictions, ambiguity, or logic that would cause a tier to misunderstand its role.

---

### CHECK 1: Tier Assignment Flow
```
Multiple valid approaches?
  YES → Cross-domain/pipeline? → YES → T1 (Executive)
                                → NO  → T2 (Contextual Specialist)
  NO  → T3 (Elite Executor)
```
**Question:** If there's only ONE valid approach but it's cross-domain... does T3 handle it?
- The flow says: "Multiple valid approaches? NO → T3"
- But what if the task is cross-domain with one obvious path? A T3 shouldn't handle cross-domain work regardless of ambiguity.
- **FINDING 1: Tier Assignment doesn't account for cross-domain single-path tasks.**

---

### CHECK 2: T3 I/O Contract Enforcement vs. T3 Ideation
Line 293-298 (I/O Contract Enforcement):
```
3. Execute precisely — no exploration, alternatives, scope creep
```
Line 167 (Ideation Engine):
```
T3: Within I/O contract — multi-path on HOW to execute, flag broken inputs, propose better output formats. No scope exploration.
```
**Question:** "no exploration, alternatives" in I/O Contract vs "multi-path on HOW to execute" in Ideation.
- These contradict. Line 297 says "no alternatives." Line 167 says "multi-path on HOW."
- **FINDING 2: I/O Contract Enforcement step 3 contradicts T3 multi-path ideation.**

---

### CHECK 3: T3 Delegation Brief
Line 536:
```
T3: Input spec, output spec, success criteria. Nothing else.
```
**Question:** If T3 gets multi-path ideation on HOW to execute, does "Nothing else" in the delegation brief starve it of the context needed to ideate on HOW?
- T3 needs to know what tools/approaches are available to ideate on HOW.
- "Nothing else" means: no pipeline context, no upstream info, no domain references. But to think of 3 ways to parse a CSV, you need to know the environment (Python? JS? What libraries available?).
- **FINDING 3: T3 delegation brief "Nothing else" may be too restrictive if T3 ideates on HOW.** Need to include execution environment context.

---

### CHECK 4: T2 "Does NOT get: SWOT (request from T1)"
Line 347:
```
Does NOT get: ... SWOT (request from T1)
```
**Question:** T2 can REQUEST a SWOT from T1. That's good. But can T2 do a lightweight SWOT-like analysis within its domain? The ideation engine says T2 generates 2+ approaches within scope. Evaluating approaches IS a form of strengths/weaknesses/opportunities/threats analysis.
- This seems fine actually — T2 ideation covers this without needing the formal SWOT protocol. The SWOT exclusion means T2 doesn't produce a formal SWOT deliverable, not that T2 can't analyze trade-offs.
- **NO FINDING — logic is sound.**

---

### CHECK 5: Mode-to-Tier Mapping
Routing says:
- QUICK → T3 Executor
- STANDARD → T2 Specialist  
- STRATEGIC → T1 Executive

**Question:** What if a QUICK task needs T2-level pipeline awareness? E.g., "add a column to this CSV" is one path (QUICK), but the CSV feeds a downstream pipeline (needs pipeline awareness).
- The classification flow handles this: "Blast Radius: If wrong, who else affected? Anyone → not Quick."
- So if it affects the pipeline, it's not QUICK — it escalates to STANDARD.
- **NO FINDING — classification catches this.**

---

### CHECK 6: Cascading Failure Chain
Lines 573-576:
```
T3 fails → retry once, reroute
T2 fails → review context, may promote to T1
T1 fails → T1-Super reviews, re-briefs or absorbs
T1-Super fails → human with full context
```
**Question:** "may promote to T1" — what does this mean? Promote the TASK to T1 scope? Or promote the T2 AGENT to T1 authority?
- Should mean: re-classify the task at T1 scope and assign a T1 agent. The T2 agent doesn't get promoted — a new T1 takes over.
- The text is ambiguous. "May promote to T1" could be read as giving the T2 expanded authority.
- **FINDING 4: "may promote to T1" is ambiguous — should clarify: re-classify task as T1, not upgrade the T2 agent.**

---

### CHECK 7: T3 Quality Gate "output a T1 would approve on first review"
Line 308:
```
Floor: output a T1 would approve on first review.
```
**Question:** How does a T3 know what a T1 would approve if T3 has no pipeline context or organizational awareness?
- T3 has the I/O contract with success criteria. "T1 would approve" means: meets the contract perfectly, handles edge cases, no garbage. It's aspirational quality language, not requiring T1 knowledge.
- **NO FINDING — metaphor is sound within context.**

---

### CHECK 8: T2 Challenge → T1 Override → Execute Original
Lines 377-379:
```
How: 1) State requested 2) State recommended 3) Cost analysis for BOTH 4) T1 decides.
Override: Execute original. Log challenge. ADR is T1's responsibility.
```
**Question:** If T1 overrides and the T2 executes the original, but the T2 KNOWS it's suboptimal — does the T2 execute at full quality or does the disagreement cause subtle quality loss?
- This is actually addressed by the anti-pattern "Copy of a Copy" and the tier-invariant statement "Every tier at full capacity." T2 executes at full quality regardless of disagreement.
- **NO FINDING — existing anti-patterns cover this.**

---

### CHECK 9: Ideation "propose multiple upward" for T3
Line 174:
```
4. Pick best or propose multiple upward
```
**Question:** T3 can "propose multiple upward"? That's a form of challenging — presenting options to the parent. But T3 "Does NOT get: challenge rights" (line 291).
- Proposing HOW options upward (within contract) ≠ challenging WHAT to do. T3 could say "I can do this with pandas or csv module — pandas is cheaper, want me to proceed?" That's proposing implementation options, not challenging the brief.
- But line 291 also says "Does NOT get: trade-off authority" — choosing between implementation approaches IS a trade-off.
- **FINDING 5: Tension between T3 "propose multiple upward" and "Does NOT get: trade-off authority." If T3 can ideate multi-path on HOW, it needs authority to pick the best path, not just propose.**

---

### SUMMARY OF FINDINGS

| # | Severity | Finding |
|---|----------|---------|
| F1 | MEDIUM | Tier Assignment doesn't account for cross-domain single-path tasks |
| F2 | HIGH | I/O Contract Enforcement "no exploration, alternatives" contradicts T3 multi-path ideation |
| F3 | MEDIUM | T3 delegation brief "Nothing else" too restrictive for T3 that ideates on HOW |
| F4 | LOW | "may promote to T1" is ambiguous |
| F5 | HIGH | T3 "Does NOT get: trade-off authority" contradicts T3 multi-path ideation on HOW |
