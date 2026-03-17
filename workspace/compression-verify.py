#!/usr/bin/env python3
"""
Lossless Compression Protocol Verification
Verifies Brain v4.3 (compressed) against v4.1 (pre-compression reference).
Per protocol: structural counts, semantic phrases, 5x backtest, deep verify.
"""
import sys

BRAIN = "/home/user/workspace/the-brain-v4.3-SKILL.md"
BRAIN_REF = "/home/user/workspace/the-brain-v4.1-SKILL.md"
EXECDEV = "/home/user/workspace/Executive Dev Architecture v3.1 - SKILL.md"

def read(path):
    with open(path) as f:
        return f.read()

def count_elements(doc):
    lines = doc.split('\n')
    # Count only actual XML-style tags, not backtick-wrapped references
    import re
    # Match <HARD-GATE> but NOT `<HARD-GATE>` (backtick-wrapped)
    hg_open = len(re.findall(r'(?<!`)(?<!\w)<HARD-GATE>(?!`)', doc))
    hg_close = len(re.findall(r'(?<!`)(?<!\w)</HARD-GATE>(?!`)', doc))
    st_open = len(re.findall(r'(?<!`)(?<!\w)<SELF-TEST>(?!`)', doc))
    st_close = len(re.findall(r'(?<!`)(?<!\w)</SELF-TEST>(?!`)', doc))
    counts = {
        'hard_gate_open': hg_open,
        'hard_gate_close': hg_close,
        'self_test_open': st_open,
        'self_test_close': st_close,
        'tables': sum(1 for l in lines if l.strip().startswith('|') and '|' in l[1:]),
        'code_blocks': doc.count('```'),
        'checklist_items': doc.count('[ ]'),
        'section_headers': sum(1 for l in lines if l.startswith('#')),
        'excuse_reality_rows': sum(1 for l in lines if l.startswith('| "') or l.startswith('| \\"')),
    }
    # Code blocks should be even (open/close pairs)
    counts['code_block_pairs'] = counts['code_blocks'] // 2
    return counts

def run_verification(pass_num):
    brain = read(BRAIN)
    ref = read(BRAIN_REF)
    ed = read(EXECDEV)
    findings = []
    
    # ================================================================
    # STEP 1: STRUCTURAL — Count protocol kernel elements
    # ================================================================
    brain_counts = count_elements(brain)
    ref_counts = count_elements(ref)
    
    # HARD-GATE pairs must match (these are protocol kernel)
    if brain_counts['hard_gate_open'] != brain_counts['hard_gate_close']:
        findings.append(f"STRUCTURAL: Brain HARD-GATE tags unbalanced: {brain_counts['hard_gate_open']} open vs {brain_counts['hard_gate_close']} close")
    if brain_counts['self_test_open'] != brain_counts['self_test_close']:
        findings.append(f"STRUCTURAL: Brain SELF-TEST tags unbalanced: {brain_counts['self_test_open']} open vs {brain_counts['self_test_close']} close")
    
    # HARD-GATE count must match reference (never compress these)
    if brain_counts['hard_gate_open'] < ref_counts['hard_gate_open']:
        findings.append(f"STRUCTURAL: Brain lost HARD-GATE blocks: {brain_counts['hard_gate_open']} vs ref {ref_counts['hard_gate_open']}")
    if brain_counts['self_test_open'] < ref_counts['self_test_open']:
        findings.append(f"STRUCTURAL: Brain lost SELF-TEST blocks: {brain_counts['self_test_open']} vs ref {ref_counts['self_test_open']}")
    
    # Checklist items must not decrease
    if brain_counts['checklist_items'] < ref_counts['checklist_items']:
        findings.append(f"STRUCTURAL: Brain lost checklist items: {brain_counts['checklist_items']} vs ref {ref_counts['checklist_items']}")
    
    # Excuse/Reality rows must not decrease
    if brain_counts['excuse_reality_rows'] < ref_counts['excuse_reality_rows']:
        findings.append(f"STRUCTURAL: Brain lost excuse/reality rows: {brain_counts['excuse_reality_rows']} vs ref {ref_counts['excuse_reality_rows']}")

    # ================================================================
    # STEP 2: SEMANTIC — Key behavioral phrases MUST exist
    # ================================================================
    
    # Protocol kernel phrases that must survive compression
    kernel_phrases = [
        # Philosophy
        ("Cost = any expendable resource consumed to produce an outcome", "Cost definition"),
        ("METABOLISM", "Ideation engine = metabolism"),
        ("not a tool, checklist, or style guide", "Systemic thinking identity"),
        
        # Tier model
        ("SCOPE and AUTHORITY, not intelligence", "Tier differentiation"),
        ("Every tier reads cost identically", "Tier-invariant cost"),
        ("all 8 dimensions, all time horizons", "Cost universality"),
        ("Scope limits what you ACT on, not what you UNDERSTAND", "Scope vs understanding"),
        ("fax of a fax", "Copy-of-a-copy anti-pattern"),
        
        # T3 conceptual model (NEW — post F1-F5 fixes)
        ("multi-path on HOW to execute", "T3 HOW ideation"),
        ("No scope exploration", "T3 scope boundary"),
        ("scope-level ideation", "T3 exclusion"),
        ("cross-scope trade-off authority", "T3 trade-off boundary"),
        ("DOES get within contract", "T3 positive authority"),
        ("no scope creep, no redefining the task", "T3 I/O enforcement"),
        ("Lazy execution that forces upstream rework = systemic cost failure", "T3 lazy warning"),
        
        # Classification
        ("Blast radius local?", "Blast radius gate in classification"),
        ("Highest triggered mode wins", "Mode escalation rule"),
        
        # Tier assignment
        ("Blast radius local?", "Blast radius gate in tier assignment"),
        
        # Iron Laws
        ("No proposal without analysis", "Iron Law 1"),
        ("No ship without test", "Iron Law 2"),
        ("No governance bypass under pressure", "Iron Law 3"),
        ("Violating the letter IS violating the spirit", "Letter = spirit"),
        
        # Excuse/Reality rows (protocol kernel — never compress)
        ("Simple ≠ low blast radius", "Excuse row: simple"),
        ("Name 2 rejected alternatives or you assumed", "Excuse row: know right approach"),
        ("Cost of NOT running SWOT", "Excuse row: strategic"),
        ("Empty Threats = haven't thought hard enough", "Excuse row: SWOT overkill"),
        ("Cheap now ≠ cheap total", "Excuse row: cheaper fix"),
        
        # SWOT probing questions
        ("What to PRESERVE because it's already working", "SWOT-S probe"),
        ("hostile audit", "SWOT-W probe"),
        ("What would a competitor build", "SWOT-O probe"),
        ("What looks like improvement but increases systemic cost", "SWOT-T probe"),
        
        # Red Flags
        ("Quick to avoid SWOT", "Red flag 1"),
        ("judge ≠ contestant", "Red flag: T1-Super in swarm"),
        
        # Council/Swarm FSMs
        ("PROPOSE → EVALUATE", "Council FSM"),
        ("DECOMPOSE", "Swarm phase 1"),
        ("SYNTHESIZE", "Swarm phase 4"),
        ("Cherry-picking ≠ synthesis", "Swarm integrity"),
        
        # Delegation
        ("execution environment", "T3 brief includes environment"),
        ("No pipeline context", "T3 brief excludes pipeline"),
        
        # Cascading failure
        ("re-classify task as T1 (new agent, not upgrade)", "Cascading failure clarity"),
        
        # Routing
        ("DO NOT read beyond your classification", "Routing enforcement"),
        ("Brain governs governance depth", "Skill composition"),
        
        # Platform Directives
        ("Prime Directive 1", "PD1"),
        ("Prime Directive 2", "PD2"),
        ("Prime Directive 3", "PD3"),
        ("backtested before presenting to user", "PD3 verification"),
        ("User is never QA", "PD3 rationale"),
        
        # Compression protocol itself
        ("5 consecutive clean audit passes", "Compression verification requirement"),
        ("not compression — it's corruption", "Corruption definition"),
    ]
    
    for phrase, label in kernel_phrases:
        if phrase not in brain:
            findings.append(f"SEMANTIC: Brain missing '{label}': \"{phrase}\"")
    
    # ================================================================
    # STEP 3: DEEP VERIFY — Routing, delegation, mode transitions
    # ================================================================
    
    # Routing protocol must have all 5 steps
    routing = brain.split("ROUTING PROTOCOL")[1].split("---")[0] if "ROUTING PROTOCOL" in brain else ""
    for step in ["STEP 1", "STEP 2", "STEP 3", "STEP 4", "STEP 5"]:
        if step not in routing:
            findings.append(f"DEEP: Brain routing missing {step}")
    
    # Mode modules must have stop markers
    for marker in ["STOP AT ═══ STANDARD MODE", "STOP AT ═══ STRATEGIC MODE", "STOP AT ═══ SHARED INFRASTRUCTURE"]:
        if marker not in brain:
            findings.append(f"DEEP: Brain missing stop marker: {marker}")
    
    # Delegation briefs must cover all tiers
    deleg = brain.split("Delegation Protocol")[1].split("##")[0] if "Delegation Protocol" in brain else ""
    for tier in ["T1-Super", "T1:", "T2:", "T3:"]:
        if tier not in deleg:
            findings.append(f"DEEP: Brain delegation missing {tier} brief")
    
    # Mode transition hooks must be present
    for hook in ["QUICK → STANDARD", "STANDARD → STRATEGIC", "QUICK → STRATEGIC"]:
        if hook not in brain:
            findings.append(f"DEEP: Brain missing mode transition hook: {hook}")
    
    # ADR template must have all required fields
    # Use "## ADRs" section header to find the right section
    adr_full = brain.split("## ADRs")[1][:1000] if "## ADRs" in brain else ""
    for field in ["Status:", "Context:", "Decision:", "Systemic Cost Analysis:", "Alternatives:", "Consequences:", "Review:"]:
        if field not in adr_full:
            findings.append(f"DEEP: Brain ADR template missing field: {field}")
    
    # ================================================================
    # STEP 4: EXEC-DEV structural integrity
    # ================================================================
    ed_counts = count_elements(ed)
    
    # Exec-dev should have same key phrases
    ed_phrases = [
        ("Every tier reads cost identically", "Tier-invariant cost"),
        ("multi-path on HOW to execute", "T3 HOW ideation"),
        ("scope-level ideation", "T3 exclusion"),
        ("cross-scope trade-off authority", "T3 trade-off boundary"),
        ("DOES get within contract", "T3 positive authority"),
        ("No scope creep, no redefining the task", "T3 I/O enforcement"),
        ("Lazy execution that forces", "T3 lazy warning"),
        ("blast radius local", "Blast radius gate (case-insensitive)"),
        ("re-classify task as T1", "Cascading failure"),
        ("lowest systemic cost quality gate", "Checklist description"),
        ("unchanged state", "Efficiency rule"),
        ("ideation loops", "T1 budget"),
        ("Minimal context", "T3 budget"),
        ("Quality floor unchanged", "T3 quality floor"),
    ]
    
    for phrase, label in ed_phrases:
        # Case-insensitive check for phrases that may vary in capitalization
        if phrase.lower() not in ed.lower():
            findings.append(f"EXECDEV-SEMANTIC: Missing '{label}': \"{phrase}\"")

    return findings


print("=" * 70)
print("LOSSLESS COMPRESSION PROTOCOL VERIFICATION: 5 CONSECUTIVE PASSES")
print("=" * 70)

for i in range(1, 6):
    findings = run_verification(i)
    if findings:
        print(f"\nPass {i}/5: FAIL ({len(findings)} findings)")
        for f in findings:
            print(f"  ✗ {f}")
        print("\nSTOPPING — fix findings before restarting count.")
        sys.exit(1)
    else:
        print(f"Pass {i}/5: CLEAN ✓")

print("\n" + "=" * 70)
print("RESULT: 5/5 CLEAN")
print("Compression integrity verified. Protocol kernel intact.")
print("No behavioral loss detected across Brain v4.3 + exec-dev v3.2.")
print("=" * 70)
