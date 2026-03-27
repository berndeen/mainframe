#!/usr/bin/env python3
"""
T1-T3 Conceptual Logic Audit + Full Parity Check
Covers: F1-F5 conceptual fixes + all prior parity fixes from v4.3 sessions.
Runs 5 consecutive passes per Lossless Compression Protocol.
"""
import sys

BRAIN = "/home/user/workspace/the-brain-v4.3-SKILL.md"
EXECDEV = "/home/user/workspace/Executive Dev Architecture v3.1 - SKILL.md"
PIE = "/home/user/workspace/Persistent Ideation Engine v4.0 - SKILL.md"

def read(path):
    with open(path) as f:
        return f.read()

def run_audit(pass_num):
    brain = read(BRAIN)
    ed = read(EXECDEV)
    pie = read(PIE)
    findings = []

    # ====================================================================
    # F1: Tier Assignment — blast radius check before T3
    # ====================================================================
    if "Blast radius local?" not in brain:
        findings.append("F1: Brain Tier Assignment missing blast radius check")
    if "blast radius local" not in ed.lower():
        findings.append("F1: Exec-dev Tier Assignment missing blast radius check")
    # Task Classification flow should also have blast radius
    if "Blast radius local?" not in brain.split("Task Classification")[1].split("Highest triggered")[0]:
        findings.append("F1: Brain Task Classification flow missing blast radius gate")
    # Stale: "NO → T3" without blast check should be gone
    if "NO  → T3 (Elite Executor)" in brain:
        findings.append("F1: Brain still has direct NO→T3 without blast check")
    if "NO  → Tier 3 (Elite Executor)" in ed:
        findings.append("F1: Exec-dev still has direct NO→T3 without blast check")

    # ====================================================================
    # F2: I/O Contract — no "no exploration, alternatives"
    # ====================================================================
    if "no exploration, alternatives" in brain:
        findings.append("F2: Brain I/O Contract still says 'no exploration, alternatives'")
    if "No exploration, no alternatives" in ed:
        findings.append("F2: Exec-dev I/O Contract still says 'no exploration, no alternatives'")
    # Should have: "no scope creep, no redefining the task"
    if "no scope creep, no redefining the task" not in brain:
        findings.append("F2: Brain missing 'no scope creep, no redefining the task'")
    if "No scope creep, no redefining the task" not in ed:
        findings.append("F2: Exec-dev missing 'No scope creep, no redefining the task'")

    # ====================================================================
    # F3: T3 delegation brief — execution environment, not "Nothing else"
    # ====================================================================
    if "Nothing else" in brain.split("Delegation Protocol")[1].split("Context Passing")[0]:
        findings.append("F3: Brain T3 brief still says 'Nothing else'")
    if "execution environment" not in brain.lower():
        findings.append("F3: Brain T3 brief missing execution environment")
    if "Execution environment" not in ed:
        findings.append("F3: Exec-dev T3 brief missing execution environment")
    if "Nothing else" in ed.split("For T3")[1].split("Context Passing")[0] if "For T3" in ed else True:
        findings.append("F3: Exec-dev T3 brief still says 'Nothing else'")

    # ====================================================================
    # F4: Cascading failure — "re-classify task as T1" not "promote to T1"
    # ====================================================================
    if "re-classify task as T1" not in brain:
        findings.append("F4: Brain cascading failure missing 're-classify task as T1'")
    if "re-classify task as T1" not in ed:
        findings.append("F4: Exec-dev cascading failure missing 're-classify task as T1'")
    if "promote to T1" in brain:
        findings.append("F4: Brain still has ambiguous 'promote to T1'")
    if "promote to T1" in ed:
        findings.append("F4: Exec-dev still has ambiguous 'promote to T1'")

    # ====================================================================
    # F5: T3 "Does NOT get" — cross-scope trade-off, not blanket trade-off
    # ====================================================================
    if "cross-scope trade-off authority" not in brain:
        findings.append("F5: Brain T3 missing 'cross-scope trade-off authority'")
    if "cross-scope trade-off authority" not in ed:
        findings.append("F5: Exec-dev T3 missing 'cross-scope trade-off authority'")
    # T3 DOES get within-contract
    if "DOES get within contract" not in brain:
        findings.append("F5: Brain missing 'DOES get within contract' block")
    if "DOES get within contract" not in ed:
        findings.append("F5: Exec-dev missing 'DOES get within contract' block")
    # Stale blanket exclusions should be gone
    quick_brain = brain.split("QUICK MODE MODULE")[1].split("STANDARD MODE MODULE")[0] if "QUICK MODE MODULE" in brain else ""
    if "trade-off authority" in quick_brain and "cross-scope" not in quick_brain.split("trade-off authority")[0][-30:]:
        findings.append("F5: Brain Quick module has unscoped 'trade-off authority'")
    # Check "multi-path ideation" is NOT in exclusion (it's now allowed)
    if "multi-path ideation" in quick_brain:
        findings.append("F5: Brain still excludes 'multi-path ideation' from T3")

    # ====================================================================
    # PRIOR PARITY CHECKS (from v4.3 session)
    # ====================================================================
    
    # Tier-invariant cost statement
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "Every tier reads cost identically" not in doc:
            findings.append(f"PARITY: {name} missing tier-invariant cost statement")
    
    # T3 budget "Minimal context" + quality floor
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "Minimal context" not in doc:
            findings.append(f"PARITY: {name} T3 budget missing 'Minimal context'")
        if "Quality floor unchanged" not in doc:
            findings.append(f"PARITY: {name} T3 budget missing 'Quality floor unchanged'")
    
    # "Don't re-derive unchanged state"
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "unchanged state" not in doc:
            findings.append(f"PARITY: {name} missing 'unchanged state'")
    
    # "lowest systemic cost" in operational checklist
    if "lowest systemic cost quality gate" not in ed:
        findings.append("PARITY: Exec-dev missing 'lowest systemic cost quality gate'")
    
    # T3 ideation scope — multi-path on HOW
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "multi-path on HOW to execute" not in doc:
            findings.append(f"PARITY: {name} missing 'multi-path on HOW to execute'")
    
    # T3 boundaries — "outside your contract"
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "outside your contract" not in doc:
            findings.append(f"PARITY: {name} missing 'outside your contract' in T3 boundaries")
    
    # "scope-level ideation" in T3 exclusion
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "scope-level ideation" not in doc:
            findings.append(f"PARITY: {name} missing 'scope-level ideation'")
    
    # T3 lazy execution warning
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "Lazy execution" not in doc or "systemic cost failure" not in doc:
            findings.append(f"PARITY: {name} missing lazy execution warning")
    
    # Ideation loops in T1 budget
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "ideation loops" not in doc:
            findings.append(f"PARITY: {name} missing 'ideation loops' in T1 budget")
    
    # Composability — three-skill model
    # Use '## Composability' to find the actual section, not the references list
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        comp_marker = "## Composability"
        if comp_marker in doc:
            comp_section = doc.split(comp_marker)[1][:500]
            if "the-brain" not in comp_section:
                findings.append(f"PARITY: {name} composability missing 'the-brain'")
        else:
            findings.append(f"PARITY: {name} missing composability section")
    
    # "T3: within contract only" in How to Ideate
    for name, doc in [("Brain", brain), ("Exec-dev", ed)]:
        if "T3: within contract only" not in doc:
            findings.append(f"PARITY: {name} missing 'T3: within contract only' in How to Ideate")
    
    # No stale terms
    stale_checks = [
        ("cheapest quality gate", "exec-dev", ed),
        ("T3: skip", "Brain", brain),
        ("T3: skip this", "exec-dev", ed),
        ("No alternative exploration", "Brain", brain),
        ("Philosophy, design, delegate, decide", "exec-dev", ed),
    ]
    for term, name, doc in stale_checks:
        if term in doc:
            findings.append(f"STALE: {name} still contains '{term}'")
    
    # PIE clean check
    for term in ["cheapest", "cost governance", "ideation loops", "promote to T1"]:
        if term in pie:
            findings.append(f"PIE: contains stale term '{term}'")

    return findings


print("=" * 60)
print("T1-T3 CONCEPTUAL + PARITY AUDIT: 5 CONSECUTIVE PASSES")
print("=" * 60)

for i in range(1, 6):
    findings = run_audit(i)
    if findings:
        print(f"\nPass {i}/5: FAIL ({len(findings)} findings)")
        for f in findings:
            print(f"  ✗ {f}")
        print("\nSTOPPING — fix findings before restarting count.")
        sys.exit(1)
    else:
        print(f"Pass {i}/5: CLEAN ✓")

print("\n" + "=" * 60)
print("RESULT: 5/5 CLEAN — All conceptual + parity checks pass.")
print("=" * 60)
