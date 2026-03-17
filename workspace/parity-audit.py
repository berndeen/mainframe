#!/usr/bin/env python3
"""
Cross-Module Parity Audit: exec-dev v3.2 vs Brain v4.3
Verifies all 7 findings are fixed. Runs 5 consecutive passes (per Lossless Compression Protocol).
"""

import sys

BRAIN_PATH = "/home/user/workspace/the-brain-v4.3-SKILL.md"
EXECDEV_PATH = "/home/user/workspace/Executive Dev Architecture v3.1 - SKILL.md"
PIE_PATH = "/home/user/workspace/Persistent Ideation Engine v4.0 - SKILL.md"

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def run_audit(pass_num):
    brain = read_file(BRAIN_PATH)
    execdev = read_file(EXECDEV_PATH)
    pie = read_file(PIE_PATH)
    
    findings = []
    
    # === EXEC-DEV CHECKS ===
    
    # E1: Tier-invariant cost statement present
    if "Every tier reads cost identically" not in execdev:
        findings.append("E1-FAIL: Missing tier-invariant cost statement in exec-dev")
    if "all 8 dimensions, all time horizons" not in execdev:
        findings.append("E1-FAIL: Missing '8 dimensions, all time horizons' in exec-dev")
    if "Scope limits what you ACT on, not what you UNDERSTAND" not in execdev:
        findings.append("E1-FAIL: Missing 'ACT on / UNDERSTAND' in exec-dev")
    
    # E2: T3 budget "Minimal context" + quality floor
    if "Minimal context" not in execdev:
        findings.append("E2-FAIL: T3 budget still says 'Minimal' without 'context' qualifier")
    if "Quality floor unchanged" not in execdev:
        findings.append("E2-FAIL: Missing 'Quality floor unchanged' in T3 budget row")
    
    # E3: "Don't re-derive unchanged state"
    if "Don't re-derive unchanged state" not in execdev:
        findings.append("E3-FAIL: Missing 'Don't re-derive unchanged state' in exec-dev")
    # Verify stale version is gone
    if "Don't re-derive what's been derived" in execdev:
        findings.append("E3-FAIL: Stale 'what's been derived' still present in exec-dev")
    
    # E4: "lowest systemic cost" not "cheapest"
    if "lowest systemic cost quality gate" not in execdev:
        findings.append("E4-FAIL: Missing 'lowest systemic cost quality gate' in exec-dev")
    if "cheapest quality gate" in execdev:
        findings.append("E4-FAIL: Stale 'cheapest quality gate' still present")
    
    # E5: T3 "Does NOT get" list — scope-level ideation, cost trade-off authority
    if "scope-level ideation" not in execdev:
        findings.append("E5-FAIL: Missing 'scope-level ideation' in exec-dev T3 Does NOT get")
    if "scope-level ideation" not in brain:
        findings.append("E5-FAIL: Missing 'scope-level ideation' in Brain T3 Does NOT get")
    if "cost trade-off authority" not in execdev:
        findings.append("E5-FAIL: Missing 'cost trade-off authority' in T3 Does NOT get")
    # Verify stale "multi-path ideation" is gone from T3 exclusion lists
    # (multi-path is now ALLOWED for T3 within contract)
    t3_section_marker_ed = "# T3 EXECUTOR MODULE \u2014 T3 AGENTS ONLY"
    if t3_section_marker_ed in execdev:
        t3_content_ed = execdev.split(t3_section_marker_ed)[1]
        if "multi-path ideation" in t3_content_ed:
            findings.append("E5-FAIL: Stale 'multi-path ideation' in exec-dev T3 exclusion")
    # Same check in Brain Quick Module
    brain_quick_marker = "QUICK MODE MODULE"
    if brain_quick_marker in brain:
        brain_quick = brain.split(brain_quick_marker)[1].split("STANDARD MODE MODULE")[0]
        if "multi-path ideation" in brain_quick:
            findings.append("E5-FAIL: Stale 'multi-path ideation' in Brain T3 exclusion")
    
    # E5b: T3 ideation scope — multi-path on HOW
    if "multi-path on HOW to execute" not in brain:
        findings.append("E5b-FAIL: Missing 'multi-path on HOW to execute' in Brain T3 ideation scope")
    if "multi-path on HOW to execute" not in execdev:
        findings.append("E5b-FAIL: Missing 'multi-path on HOW to execute' in exec-dev T3 ideation scope")
    
    # E5c: T3 boundaries — "outside your contract" qualifier
    if "outside your contract" not in brain:
        findings.append("E5c-FAIL: Missing 'outside your contract' in Brain T3 boundaries")
    if "outside your contract" not in execdev:
        findings.append("E5c-FAIL: Missing 'outside your contract' in exec-dev T3 boundaries")
    
    # E5d: How to Ideate — T3 within contract (not skip)
    if "T3: within contract only" not in brain:
        findings.append("E5d-FAIL: Missing 'T3: within contract only' in Brain How to Ideate")
    if "T3: within contract only" not in execdev:
        findings.append("E5d-FAIL: Missing 'T3: within contract only' in exec-dev How to Ideate")
    # Stale "T3: skip" should be gone
    if "T3: skip" in brain:
        findings.append("E5d-FAIL: Stale 'T3: skip' in Brain How to Ideate")
    if "T3: skip" in execdev:
        findings.append("E5d-FAIL: Stale 'T3: skip' in exec-dev How to Ideate")
    
    # E6: T3 lazy execution warning
    if "Lazy execution that forces" in execdev and "upstream rework = systemic cost failure" in execdev:
        pass  # GOOD
    else:
        findings.append("E6-FAIL: Missing lazy execution warning in T3 quality floor")
    
    # E7: Composability section — three-skill model
    if "the-brain" not in execdev.split("Composability")[1] if "Composability" in execdev else True:
        findings.append("E7-FAIL: Missing 'the-brain' in composability section")
    if "Governance: think, classify, decide, delegate" not in execdev:
        findings.append("E7-FAIL: Missing Brain governance description")
    if "Organization: topology, agents, platforms, contracts" not in execdev:
        findings.append("E7-FAIL: Missing exec-dev organization description")
    if "Implementation: build, test, iterate, ship" not in execdev:
        findings.append("E7-FAIL: Missing PIE implementation description")
    # Stale role descriptions gone
    if "Philosophy, design, delegate, decide" in execdev:
        findings.append("E7-FAIL: Stale 'Philosophy, design, delegate, decide' still present")
    
    # "ideation loops" is CORRECT in T1 budget (looping = iterate, not one-shot)
    # It should ONLY appear in T1 budget context, NOT in T3 "Does NOT get" list
    # T3 exclusion uses "multi-path ideation" (capability denied), not "ideation loops" (mechanism)
    if "ideation loops" not in execdev:
        findings.append("E5-T1: Missing 'ideation loops' in T1 budget row")
    if "ideation loops" not in brain:
        findings.append("BRAIN-E5: Missing 'ideation loops' in Brain T1 budget row")
    
    # Version bump check
    if "version: '3.2'" not in execdev:
        findings.append("VERSION-FAIL: exec-dev not bumped to 3.2")
    if "v3.2" not in execdev:
        findings.append("VERSION-FAIL: Title not updated to v3.2")
    
    # === BRAIN PARITY CROSS-CHECK ===
    # Verify Brain v4.3 still has the canonical versions of all terms
    brain_checks = [
        ("Every tier reads cost identically", "tier-invariant cost statement"),
        ("Minimal context", "T3 minimal context"),
        ("Quality floor unchanged", "T3 quality floor"),
        ("Don't re-derive unchanged state", "unchanged state efficiency"),
        ("Lowest systemic cost first", "OD-2 lowest systemic cost"),
        ("scope-level ideation", "scope-level ideation in T3 exclusions"),
        ("cost trade-off authority", "cost trade-off authority"),
        ("Lazy execution that forces upstream rework = systemic cost failure", "lazy execution warning"),
    ]
    for phrase, label in brain_checks:
        if phrase not in brain:
            findings.append(f"BRAIN-DRIFT: Brain v4.3 missing '{label}' — check for regression")
    
    # === PIE CLEAN CHECK ===
    # PIE should NOT have any of the stale terms (confirming it's clean)
    stale_terms_pie = ["cheapest", "cost governance", "ideation loops"]
    for term in stale_terms_pie:
        if term in pie:
            findings.append(f"PIE-STALE: persistent-ideation-engine contains '{term}'")
    
    return findings

# Run 5 consecutive passes
print("=" * 60)
print("CROSS-MODULE PARITY AUDIT: 5 CONSECUTIVE PASSES")
print("=" * 60)

all_clean = True
for i in range(1, 6):
    findings = run_audit(i)
    if findings:
        all_clean = False
        print(f"\nPass {i}/5: FAIL ({len(findings)} findings)")
        for f in findings:
            print(f"  ✗ {f}")
        print("\nSTOPPING — fix findings before restarting count.")
        sys.exit(1)
    else:
        print(f"Pass {i}/5: CLEAN ✓")

print("\n" + "=" * 60)
if all_clean:
    print("RESULT: 5/5 CLEAN — All parity checks pass.")
    print("exec-dev v3.2 is aligned with Brain v4.3")
    print("persistent-ideation-engine v4.0 is CLEAN (no changes needed)")
else:
    print("RESULT: FINDINGS REMAIN — do not ship.")
print("=" * 60)
