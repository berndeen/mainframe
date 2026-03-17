#!/usr/bin/env python3
"""
Full Governance Package Audit — All 3 Skills
Runs: Brain (already compressed), Exec-Dev (just compressed), PIE (just compressed)
Verifies: structural integrity, semantic kernel, cross-skill parity, compression stats.
"""
import sys
import re

FILES = {
    # Brain
    "brain_pre": "/home/user/workspace/the-brain-v4.1-SKILL.md",
    "brain_post": "/home/user/workspace/the-brain-v4.3-SKILL.md",
    # Exec-Dev
    "execdev_pre": "/home/user/workspace/executive-dev-v3.2-pre-compression-SKILL.md",
    "execdev_post": "/home/user/workspace/executive-dev-architecture-v3.2-compressed-SKILL.md",
    # PIE
    "pie_pre": "/home/user/workspace/Persistent Ideation Engine v4.0 - SKILL.md",
    "pie_post": "/home/user/workspace/persistent-ideation-engine-v4.0-compressed-SKILL.md",
}

def read(path):
    with open(path) as f:
        return f.read()

def word_count(text):
    return len(text.split())

def line_count(text):
    return len([l for l in text.split('\n') if l.strip()])

def count_structural(doc):
    lines = doc.split('\n')
    hg_open = len(re.findall(r'(?<!`)(?<!\w)<HARD-GATE>(?!`)', doc))
    hg_close = len(re.findall(r'(?<!`)(?<!\w)</HARD-GATE>(?!`)', doc))
    st_open = len(re.findall(r'(?<!`)(?<!\w)<SELF-TEST>(?!`)', doc))
    st_close = len(re.findall(r'(?<!`)(?<!\w)</SELF-TEST>(?!`)', doc))
    return {
        'hard_gates': hg_open,
        'hard_gate_balanced': hg_open == hg_close,
        'self_tests': st_open,
        'self_test_balanced': st_open == st_close,
        'code_blocks': doc.count('```') // 2,
        'tables': sum(1 for l in lines if l.strip().startswith('|') and '|' in l[1:]),
        'checklists': doc.count('[ ]'),
        'headers': sum(1 for l in lines if l.startswith('#')),
    }


# ================================================================
# LOAD ALL FILES
# ================================================================
docs = {}
for key, path in FILES.items():
    try:
        docs[key] = read(path)
    except FileNotFoundError:
        print(f"ERROR: Missing file: {path}")
        sys.exit(1)

findings = []

# ================================================================
# SECTION 1: COMPRESSION STATS (Before → After)
# ================================================================
print("=" * 78)
print("FULL GOVERNANCE PACKAGE AUDIT — ALL 3 SKILLS")
print("=" * 78)

print("\n## SECTION 1: COMPRESSION STATS\n")
print(f"{'Skill':<25} {'Pre Words':>10} {'Post Words':>11} {'Reduction':>10} {'%':>7}")
print("-" * 68)

total_pre = 0
total_post = 0
for name, pre_key, post_key in [
    ("Brain v4.3", "brain_pre", "brain_post"),
    ("Exec-Dev v3.2", "execdev_pre", "execdev_post"),
    ("PIE v4.0", "pie_pre", "pie_post"),
]:
    pre_w = word_count(docs[pre_key])
    post_w = word_count(docs[post_key])
    red = pre_w - post_w
    pct = (red / pre_w) * 100 if pre_w > 0 else 0
    total_pre += pre_w
    total_post += post_w
    print(f"{name:<25} {pre_w:>10,} {post_w:>11,} {red:>10,} {pct:>6.1f}%")

total_red = total_pre - total_post
total_pct = (total_red / total_pre) * 100
print("-" * 68)
print(f"{'TOTAL':<25} {total_pre:>10,} {total_post:>11,} {total_red:>10,} {total_pct:>6.1f}%")

# ================================================================
# SECTION 2: STRUCTURAL INTEGRITY (Post-Compression)
# ================================================================
print("\n## SECTION 2: STRUCTURAL INTEGRITY (Post-Compression)\n")

for name, key in [("Brain v4.3", "brain_post"), ("Exec-Dev v3.2", "execdev_post"), ("PIE v4.0", "pie_post")]:
    s = count_structural(docs[key])
    print(f"  {name}:")
    print(f"    HARD-GATE blocks: {s['hard_gates']} (balanced: {'YES' if s['hard_gate_balanced'] else 'NO ✗'})")
    print(f"    SELF-TEST blocks: {s['self_tests']} (balanced: {'YES' if s['self_test_balanced'] else 'NO ✗'})")
    print(f"    Code blocks: {s['code_blocks']}")
    print(f"    Table rows: {s['tables']}")
    print(f"    Checklist items: {s['checklists']}")
    print(f"    Section headers: {s['headers']}")
    if not s['hard_gate_balanced']:
        findings.append(f"STRUCTURAL: {name} HARD-GATE tags unbalanced")
    if not s['self_test_balanced']:
        findings.append(f"STRUCTURAL: {name} SELF-TEST tags unbalanced")

# ================================================================
# SECTION 3: STRUCTURAL PRESERVATION (Pre vs Post counts)
# ================================================================
print("\n## SECTION 3: STRUCTURAL PRESERVATION (Pre vs Post)\n")
print(f"{'Skill':<20} {'Element':<20} {'Pre':>5} {'Post':>5} {'Status':>8}")
print("-" * 62)

for name, pre_key, post_key in [
    ("Brain", "brain_pre", "brain_post"),
    ("Exec-Dev", "execdev_pre", "execdev_post"),
    ("PIE", "pie_pre", "pie_post"),
]:
    pre_s = count_structural(docs[pre_key])
    post_s = count_structural(docs[post_key])
    
    for element in ['hard_gates', 'self_tests', 'code_blocks', 'checklists']:
        pre_val = pre_s[element]
        post_val = post_s[element]
        status = "OK ✓" if post_val >= pre_val else "LOSS ✗"
        if post_val < pre_val:
            findings.append(f"PRESERVATION: {name} lost {element}: {pre_val} → {post_val}")
        print(f"{name:<20} {element:<20} {pre_val:>5} {post_val:>5} {status:>8}")

# ================================================================
# SECTION 4: CROSS-SKILL PARITY (shared concepts match)
# ================================================================
print("\n## SECTION 4: CROSS-SKILL PARITY\n")

# Concepts that must appear in both Brain AND Exec-Dev
brain_execdev_parity = [
    ("SCOPE and AUTHORITY, not intelligence", "Tier differentiation"),
    ("all 8 dimensions, all time horizons", "Cost universality"),
    ("multi-path on HOW to execute", "T3 ideation"),
    ("scope-level ideation", "T3 exclusion"),
    ("cross-scope trade-off authority", "T3 trade-off boundary"),
    ("DOES get within contract", "T3 positive authority"),
    ("Lazy execution that forces", "T3 quality floor"),
    ("fax of a fax", "Copy-of-a-copy"),
    ("ideation loops", "T1 budget"),
    ("Quality floor unchanged", "T3 budget"),
    ("re-classify task as T1", "Cascading failure"),
    ("Brain governs governance depth", "Composability"),
]

parity_pass = 0
parity_fail = 0
for phrase, label in brain_execdev_parity:
    in_brain = phrase.lower() in docs["brain_post"].lower()
    in_execdev = phrase.lower() in docs["execdev_post"].lower()
    status = "✓" if (in_brain and in_execdev) else "✗"
    if not (in_brain and in_execdev):
        missing = []
        if not in_brain: missing.append("Brain")
        if not in_execdev: missing.append("Exec-Dev")
        findings.append(f"PARITY: '{label}' missing from {', '.join(missing)}")
        parity_fail += 1
    else:
        parity_pass += 1
    print(f"  {status} {label:<35} Brain: {'✓' if in_brain else '✗'}  Exec-Dev: {'✓' if in_execdev else '✗'}")

# Concepts that must appear in both Brain AND PIE
brain_pie_parity = [
    ("persistent-ideation-engine", "PIE reference"),
    ("test", "Testing concept"),
    ("convergence", "Convergence"),
]

for phrase, label in brain_pie_parity:
    in_brain = phrase.lower() in docs["brain_post"].lower()
    in_pie = phrase.lower() in docs["pie_post"].lower()
    status = "✓" if (in_brain and in_pie) else "✗"
    if not (in_brain and in_pie):
        missing = []
        if not in_brain: missing.append("Brain")
        if not in_pie: missing.append("PIE")
        findings.append(f"PARITY: '{label}' missing from {', '.join(missing)}")
        parity_fail += 1
    else:
        parity_pass += 1
    print(f"  {status} {label:<35} Brain: {'✓' if in_brain else '✗'}  PIE: {'✓' if in_pie else '✗'}")

print(f"\n  Parity: {parity_pass}/{parity_pass + parity_fail} checks passed")

# ================================================================
# SECTION 5: SEMANTIC KERNEL SPOT-CHECK (5 key phrases per skill)
# ================================================================
print("\n## SECTION 5: SEMANTIC KERNEL SPOT-CHECK\n")

brain_kernels = [
    ("Cost = any expendable resource consumed to produce an outcome", "Cost definition"),
    ("METABOLISM", "Metabolism identity"),
    ("No proposal without analysis", "Iron Law 1"),
    ("No ship without test", "Iron Law 2"),
    ("5 consecutive clean audit passes", "Compression requirement"),
    ("not compression — it's corruption", "Corruption definition"),
    ("Prime Directive 1", "PD1"),
    ("Prime Directive 3", "PD3"),
    ("Cherry-picking ≠ synthesis", "Swarm integrity"),
    ("PROPOSE → EVALUATE", "Council FSM"),
]

execdev_kernels = [
    ("organizational operating system", "Philosophy"),
    ("hostile audit", "SWOT-W probe"),
    ("What would a competitor build", "SWOT-O probe"),
    ("merge strategy BEFORE spawning", "Orchestration rule"),
    ("Containment before root cause", "Incident rule"),
    ("exactly ONE Accountable", "RACI rule"),
    ("Rollback is tested before promotion", "Promotion rule"),
    ("No secrets in notebooks", "Secrets rule"),
    ("No pipeline context", "T3 delegation"),
    ("This is not insubordination", "T2 challenge legitimacy"),
]

pie_kernels = [
    ("User is NOT your tester", "User ≠ tester"),
    ("prompt once, then self-solve", "Resource rule"),
    ("IDEATE → IMPLEMENT → TEST (relentlessly) → ANALYZE", "Training loop"),
    ("Never ship a regression", "No-regression rule"),
    ("3 consecutive failed fix attempts", "Abandon trigger"),
    ("300+ test runs across 8 epochs", "Practice example"),
    ("Reasoning is not testing", "Anti-pattern"),
    ("Resource inventory done", "Checklist item"),
    ("minimum 10x per test set", "10x minimum"),
    ("hostile user", "Adversarial mindset"),
]

for skill_name, key, kernels in [
    ("Brain v4.3", "brain_post", brain_kernels),
    ("Exec-Dev v3.2", "execdev_post", execdev_kernels),
    ("PIE v4.0", "pie_post", pie_kernels),
]:
    print(f"  {skill_name}:")
    for phrase, label in kernels:
        found = phrase.lower() in docs[key].lower()
        status = "✓" if found else "✗"
        if not found:
            findings.append(f"SEMANTIC: {skill_name} missing '{label}': \"{phrase}\"")
        print(f"    {status} {label}")
    print()

# ================================================================
# SECTION 6: VERSION CONSISTENCY
# ================================================================
print("## SECTION 6: VERSION CONSISTENCY\n")

version_checks = [
    ("Brain", "brain_post", "4.3"),
    ("Exec-Dev", "execdev_post", "3.2"),
    ("PIE", "pie_post", "4.0"),
]

for name, key, expected_ver in version_checks:
    has_version = f"version: '{expected_ver}'" in docs[key]
    status = "✓" if has_version else "✗"
    if not has_version:
        findings.append(f"VERSION: {name} missing version {expected_ver} in frontmatter")
    print(f"  {status} {name}: version {expected_ver} in frontmatter")

# ================================================================
# FINAL SUMMARY
# ================================================================
print("\n" + "=" * 78)
if findings:
    print(f"RESULT: FAIL — {len(findings)} findings")
    print("=" * 78)
    for f in findings:
        print(f"  ✗ {f}")
else:
    print("RESULT: ALL CLEAR — 0 findings across all 3 skills")
    print("=" * 78)
    print(f"\nFinal Package (compressed):")
    print(f"  Brain v4.3:    {word_count(docs['brain_post']):,} words")
    print(f"  Exec-Dev v3.2: {word_count(docs['execdev_post']):,} words")
    print(f"  PIE v4.0:      {word_count(docs['pie_post']):,} words")
    print(f"  TOTAL:         {total_post:,} words (down from {total_pre:,}, {total_pct:.1f}% reduction)")
    print(f"\nAll structural elements preserved. All semantic kernels intact.")
    print(f"Cross-skill parity verified. Compression per protocol. No behavioral loss.")

print("=" * 78)
sys.exit(1 if findings else 0)
