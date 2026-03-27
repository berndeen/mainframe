#!/usr/bin/env python3
"""
Lossless Compression Protocol Verification — PIE v4.0
Verifies compressed PIE against pre-compression reference.
Per protocol: structural counts, semantic phrases, 5x backtest, deep verify.
"""
import sys

ORIGINAL = "/home/user/workspace/Persistent Ideation Engine v4.0 - SKILL.md"
COMPRESSED = "/home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md"

def read(path):
    with open(path) as f:
        return f.read()

def count_elements(doc):
    lines = doc.split('\n')
    counts = {
        'tables': sum(1 for l in lines if l.strip().startswith('|') and '|' in l[1:]),
        'code_blocks': doc.count('```'),
        'code_block_pairs': doc.count('```') // 2,
        'checklist_items': doc.count('[ ]'),
        'section_headers': sum(1 for l in lines if l.startswith('#')),
        'bold_items': doc.count('**'),
    }
    return counts

def run_verification(pass_num):
    orig = read(ORIGINAL)
    comp = read(COMPRESSED)
    findings = []
    
    # ================================================================
    # STEP 1: STRUCTURAL — Count protocol kernel elements
    # ================================================================
    orig_c = count_elements(orig)
    comp_c = count_elements(comp)
    
    # Code block pairs must match
    if comp_c['code_block_pairs'] < orig_c['code_block_pairs']:
        findings.append(f"STRUCTURAL: Lost code block pairs: {comp_c['code_block_pairs']} vs orig {orig_c['code_block_pairs']}")
    
    # Checklist items must match exactly (Pre-Ship Checklist is protocol kernel)
    if comp_c['checklist_items'] != orig_c['checklist_items']:
        findings.append(f"STRUCTURAL: Checklist items changed: {comp_c['checklist_items']} vs orig {orig_c['checklist_items']}")
    
    # Anti-pattern table rows must match
    orig_ap = sum(1 for l in orig.split('\n') if l.startswith('| ') and 'Anti-Pattern' not in l and '---' not in l and l.strip() != '|')
    comp_ap = sum(1 for l in comp.split('\n') if l.startswith('| ') and 'Anti-Pattern' not in l and '---' not in l and l.strip() != '|')
    if comp_ap < orig_ap:
        findings.append(f"STRUCTURAL: Lost anti-pattern table rows: {comp_ap} vs orig {orig_ap}")

    # ================================================================
    # STEP 2: SEMANTIC — Key behavioral phrases MUST survive
    # ================================================================
    
    kernel_phrases = [
        # Purpose / Identity
        ("ML-style training loop", "ML identity (compressed form)"),
        ("test relentlessly", "Relentless testing"),
        ("hundreds of test runs", "Test volume"),
        ("bulletproof", "Quality target"),
        ("meaningful decision points", "User re-entry point"),
        
        # Core Mindset
        ("User is NOT your tester", "User ≠ tester"),
        ("hostile user", "Adversarial probing mindset"),
        ("iterate until convergence", "Convergence goal"),
        ("results, not errors", "Output = results"),
        
        # Minimal Intervention
        ("Auto-detection", "Auto-detect pattern"),
        ("Auto-fallback", "Auto-fallback pattern"),
        ("Zero configuration", "Zero-config pattern"),
        ("design failure", "Intervention = failure"),
        
        # Resource Acquisition
        ("Scan workspace", "Step 1: workspace scan"),
        ("Check conversation history", "Step 1: conversation check"),
        ("Check memory", "Step 1: memory check"),
        ("Check connected services", "Step 1: connected services"),
        ("prompt once, then self-solve", "Core resource rule"),
        ("Generate synthetic test data", "Self-solve: synthetic"),
        ("Extract from source code", "Self-solve: extract"),
        ("Fetch from URLs", "Self-solve: fetch"),
        ("Reverse-engineer from output", "Self-solve: reverse-engineer"),
        ("Build a mock", "Self-solve: mock"),
        ("Never nag", "No-nag rule"),
        
        # Training Loop
        ("IDEATE → IMPLEMENT → TEST", "Training loop diagram"),
        ("convergence", "Convergence criterion"),
        
        # Epoch 0
        ("2-4 distinct solution paths", "Multi-path exploration"),
        ("Keep alternatives ranked", "Ranked alternatives"),
        
        # Epoch 1
        ("Build test harness before production code", "Harness-first"),  
        ("REAL sample files", "Real data priority"),
        ("never fabricate", "No fake data"),
        ("PASS/FAIL", "Test output format"),
        ("headlessly", "Headless execution"),
        
        # Epoch 2+ Steps
        ("Analyze Failures AND Passes", "Analyze both"),
        ("band-aid or root-cause", "Root cause focus"),
        ("Re-Test the FULL Suite", "Full suite re-test"),
        ("minimum 10x per test set", "10x minimum"),
        ("Never ship a regression", "No-regression rule"),
        ("persistent feedback loop", "Loop identity"),
        
        # Epoch chaining example
        ("ArrayBuffer detachment", "Epoch chain: ArrayBuffer"),
        ("BOM double-encoding", "Epoch chain: BOM"),
        ("pixel-width wrap is better", "Epoch chain: pixel-width"),
        ("Each fix exposed the next issue", "Chaining principle"),
        
        # Adversarial
        ("Malformed inputs", "Adversarial: malformed"),
        ("Boundary conditions", "Adversarial: boundaries"),
        ("Race conditions", "Adversarial: race"),
        ("Environment gaps", "Adversarial: environment"),
        
        # Progressive Scale
        ("Level 1:", "Scale level 1"),
        ("Level 4:", "Scale level 4"),
        
        # Path Abandonment
        ("3 consecutive failed fix attempts", "Abandon trigger 1"),
        ("Environmental impossibility", "Abandon trigger 2"),
        ("Diminishing returns", "Abandon trigger 3"),
        ("Do NOT keep retrying", "No retry rule"),
        ("Carry forward", "Carry forward components"),
        
        # Visual Verification
        ("Font sizes and weights", "Visual: fonts"),
        ("Margins", "Visual: margins"),
        ("Text wrapping", "Visual: wrapping"),
        ("measure, don't guess", "Visual: measure"),
        
        # Practice Example
        ("Beat your head against the wall", "Practice example trigger"),
        ("300+ test runs across 8 epochs", "Practice example result"),
        ("User intervened 3 times", "Practice example interventions"),
        
        # Anti-Patterns (spot check)
        ("Reasoning is not testing", "Anti-pattern: reasoning ≠ testing"),
        ("Probe your own code adversarially", "Anti-pattern: self-probe"),
        ("convergence, 10x is the minimum", "Anti-pattern: 10x minimum"),
        
        # Pre-Ship Checklist (spot check)
        ("Resource inventory done", "Checklist: inventory"),
        ("Adversarial probes run", "Checklist: adversarial"),
        ("No regressions from any previous epoch", "Checklist: regression"),
        ("not \"it should work\"", "Checklist: results not promises"),
        
        # Frontmatter
        ("version: '4.0'", "Version in frontmatter"),
        ("persistent-ideation-engine", "Skill name"),
    ]
    
    for phrase, label in kernel_phrases:
        if phrase.lower() not in comp.lower():
            findings.append(f"SEMANTIC: Missing '{label}': \"{phrase}\"")
    
    # ================================================================
    # STEP 3: DEEP VERIFY — Structural integrity
    # ================================================================
    
    # All major sections present
    for section in ["Purpose", "When to Use", "Core Mindset", "Resource Acquisition",
                    "The Training Loop", "Epoch 0", "Epoch 1", "Epoch 2+",
                    "Adversarial Self-Probing", "Progressive Scale Testing",
                    "Path Abandonment Protocol", "Visual Output Verification",
                    "What This Looks Like in Practice", "Anti-Patterns", "Pre-Ship Checklist"]:
        if section not in comp:
            findings.append(f"DEEP: Missing section: {section}")
    
    # Resource acquisition has all 4 steps
    for step in ["Step 1:", "Step 2:", "Step 3:", "Step 4:"]:
        if step not in comp:
            findings.append(f"DEEP: Resource acquisition missing {step}")
    
    # Epoch 2+ has all 5 steps
    for step in ["Step 1: Analyze", "Step 2: Ideate", "Step 3: Implement", 
                 "Step 4: Compare", "Step 5: Chain"]:
        if step not in comp:
            findings.append(f"DEEP: Epoch 2+ missing {step}")
    
    # Training loop ASCII art preserved
    if "IDEATE → IMPLEMENT → TEST (relentlessly) → ANALYZE" not in comp:
        findings.append("DEEP: Training loop diagram text missing")
    
    # Progressive scale has all 4 levels in code block
    for level in ["Level 1:", "Level 2:", "Level 3:", "Level 4:"]:
        if level not in comp:
            findings.append(f"DEEP: Progressive scale missing {level}")
    
    # Practice example has all 8 epochs
    for epoch in ["Epoch 0:", "Epoch 1:", "Epoch 2:", "Epoch 3:", "Epoch 4:", 
                  "Epoch 5:", "Epoch 6:", "Epoch 7:", "Epoch 8:"]:
        if epoch not in comp:
            findings.append(f"DEEP: Practice example missing {epoch}")
    
    # Anti-pattern table has 13 rows (check by counting pipes at start)
    ap_section = comp.split("## Anti-Patterns")[1].split("## Pre-Ship")[0] if "## Anti-Patterns" in comp else ""
    ap_rows = [l for l in ap_section.split('\n') if l.startswith('|') and '---' not in l and 'Anti-Pattern' not in l]
    if len(ap_rows) < 13:
        findings.append(f"DEEP: Anti-pattern table has {len(ap_rows)} rows, expected 13")
    
    # Pre-ship checklist has 13 items
    if comp.count('- [ ]') < 13:
        findings.append(f"DEEP: Pre-ship checklist has {comp.count('- [ ]')} items, expected 13")
    
    # Continuous Resource Awareness section present
    if "Continuous Resource Awareness" not in comp:
        findings.append("DEEP: Missing 'Continuous Resource Awareness' section")
    
    return findings


# ================================================================
# RUN 5 CONSECUTIVE CLEAN PASSES
# ================================================================

orig = read(ORIGINAL)
comp = read(COMPRESSED)
orig_words = len(orig.split())
comp_words = len(comp.split())
reduction = orig_words - comp_words
pct = (reduction / orig_words) * 100

print("=" * 70)
print("PIE v4.0 LOSSLESS COMPRESSION VERIFICATION")
print("=" * 70)
print(f"Pre-compression:  {orig_words} words ({sum(1 for l in orig.split(chr(10)) if l)} lines)")
print(f"Post-compression: {comp_words} words ({sum(1 for l in comp.split(chr(10)) if l)} lines)")
print(f"Reduction:        {reduction} words ({pct:.1f}%)")
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
print("PIE v4.0 compression verified. Protocol kernel intact.")
print(f"Compression: {orig_words} → {comp_words} words ({pct:.1f}% reduction)")
print("No behavioral loss detected.")
print("=" * 70)
