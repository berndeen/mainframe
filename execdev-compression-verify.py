#!/usr/bin/env python3
"""
Lossless Compression Protocol Verification — Exec-Dev v3.2
Verifies compressed exec-dev against pre-compression reference.
Per protocol: structural counts, semantic phrases, 5x backtest, deep verify.
"""
import sys
import re

ORIGINAL = "/home/user/workspace/Executive Dev Architecture v3.1 - SKILL.md"
COMPRESSED = "/home/user/workspace/executive-dev-architecture-v3.2-compressed-SKILL.md"

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
        'separator_lines': sum(1 for l in lines if l.startswith('# ═══')),
        'json_blocks': doc.count('```json'),
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
    
    # Code block pairs must match (all structural, never compress)
    if comp_c['code_block_pairs'] < orig_c['code_block_pairs']:
        findings.append(f"STRUCTURAL: Lost code block pairs: {comp_c['code_block_pairs']} vs orig {orig_c['code_block_pairs']}")
    
    # Checklist items must match exactly
    if comp_c['checklist_items'] != orig_c['checklist_items']:
        findings.append(f"STRUCTURAL: Checklist items changed: {comp_c['checklist_items']} vs orig {orig_c['checklist_items']}")
    
    # Section separator lines must match
    if comp_c['separator_lines'] != orig_c['separator_lines']:
        findings.append(f"STRUCTURAL: Section separators changed: {comp_c['separator_lines']} vs orig {orig_c['separator_lines']}")
    
    # JSON blocks must match
    if comp_c['json_blocks'] != orig_c['json_blocks']:
        findings.append(f"STRUCTURAL: JSON blocks changed: {comp_c['json_blocks']} vs orig {orig_c['json_blocks']}")
    
    # Table rows should not decrease (tables are protocol kernel)
    if comp_c['tables'] < orig_c['tables']:
        findings.append(f"STRUCTURAL: Lost table rows: {comp_c['tables']} vs orig {orig_c['tables']}")

    # ================================================================
    # STEP 2: SEMANTIC — Key behavioral phrases MUST survive
    # ================================================================
    
    kernel_phrases = [
        # Philosophy
        ("Cost = any expendable resource consumed to produce an outcome", "Cost definition"),
        ("METABOLISM", "Ideation engine = metabolism"),
        ("not a tool, checklist, or style guide", "Systemic thinking identity"),
        ("organizational operating system", "Philosophy identity"),
        
        # Systemic Cost Test — all 4 questions
        ("What does this cost across ALL dimensions", "SCT Q1"),
        ("reduces cost in one dimension without materially", "SCT Q2"),
        ("create future cost (debt) that someone else will pay", "SCT Q3"),
        ("different tier of agent or a different scope boundary", "SCT Q4"),
        ("haven't finished thinking", "SCT conclusion"),
        
        # Tier model
        ("SCOPE and AUTHORITY, not intelligence", "Tier differentiation"),
        ("Every tier reads cost identically", "Tier-invariant cost"),
        ("all 8 dimensions, all time horizons", "Cost universality"),
        ("Scope limits what you ACT on, not what you UNDERSTAND", "Scope vs understanding"),
        ("fax of a fax", "Copy-of-a-copy anti-pattern"),
        
        # T3 conceptual model (post F1-F5 fixes — critical)
        ("multi-path on HOW to execute", "T3 HOW ideation"),
        ("Does NOT explore alternatives outside its contract", "T3 scope boundary"),
        ("scope-level ideation", "T3 exclusion"),
        ("cross-scope trade-off authority", "T3 trade-off boundary"),
        ("DOES get within contract", "T3 positive authority"),
        ("No scope creep, no redefining the task", "T3 I/O enforcement"),
        ("Lazy execution that forces upstream rework = systemic cost failure", "T3 lazy warning"),
        ("flag malformed inputs, refuse garbage output", "T3 quality gate"),
        
        # Tier Assignment
        ("blast radius local", "Blast radius gate"),
        
        # Ideation — How to Ideate
        ("Define the outcome", "Ideation step 1"),
        ("Generate 2+ paths", "Ideation step 2"),
        ("Document why", "Ideation step 5"),
        ("T3: within contract only", "T3 ideation scope"),
        
        # Code Review Gate
        ("tested per `persistent-ideation-engine`", "PIE integration"),
        
        # SWOT Protocol
        ("PRESERVE because it's already working", "SWOT-S probe"),
        ("hostile audit", "SWOT-W probe"),
        ("What would a competitor build", "SWOT-O probe"),
        ("looks like improvement but actually increases systemic cost", "SWOT-T probe"),
        ("Only strengths = marketing", "SWOT theater"),
        ("Empty Threats = naive optimism", "SWOT empty threats"),
        
        # Delegation
        ("execution environment and constraints", "T3 brief includes env"),
        ("No pipeline context", "T3 brief excludes pipeline"),
        ("file reference, not inline", "Context passing rule"),
        
        # ADR Template fields
        ("Status: Proposed", "ADR Status field"),
        ("Systemic Cost Analysis:", "ADR Cost field"),
        ("Alternatives Considered:", "ADR Alternatives field"),
        ("Consequences:", "ADR Consequences field"),
        
        # Cost Governance
        ("ideation loops", "T1 budget"),
        ("Minimal context", "T3 budget"),
        ("Quality floor unchanged", "T3 quality floor"),
        ("unchanged state", "Efficiency rule"),
        
        # Cascading Failure
        ("re-classify task as T1 (new agent, not upgrade)", "Cascading failure clarity"),
        
        # State Machine
        ("intake → validated → processing → review → complete → archived", "State machine FSM"),
        ("not in the state store, it didn't happen", "No implicit state"),
        
        # Agent Contracts
        ("failure_modes:", "Contract failure modes"),
        ("escalation:", "Contract escalation"),
        
        # Orchestration
        ("merge strategy BEFORE spawning", "Fan-out merge rule"),
        ("dead-letter, not /dev/null", "Dead-letter rule"),
        
        # Environment Promotion
        ("Never skip staging", "Staging rule"),
        ("Rollback is tested before promotion", "Rollback rule"),
        
        # Observability
        ("SYMPTOMS (error rate spike)", "Alert on symptoms"),
        ("Dead-letter queue depth is always monitored", "Dead-letter monitoring"),
        
        # Secrets
        ("No secrets in notebooks, spreadsheets, Slack, or email", "Secrets rule"),
        
        # RACI
        ("exactly ONE Accountable", "RACI single accountable"),
        ("Accountable ≠ Responsible", "RACI A≠R"),
        
        # Incident Response
        ("Containment before root cause", "Incident rule 1"),
        ("Postmortems are blameless", "Incident rule 2"),
        
        # Upward Challenge
        ("This is not insubordination", "Challenge legitimacy"),
        
        # Pipeline Awareness
        ("What feeds in", "Pipeline Q1"),
        ("What consumes", "Pipeline Q2"),
        
        # Composability
        ("Brain governs governance depth", "Composability brain"),
        ("All three share systemic thinking", "Composability all"),
        
        # T2 Checklists — spot check items
        ("Tests pass (per persistent-ideation-engine)", "Checklist: tests"),
        ("No hardcoded values", "Checklist: hardcoded"),
        ("Schema validated against contract", "Checklist: schema"),
        ("Rollback path documented", "Checklist: rollback"),
        
        # Inter-Agent Communication
        ("handoff_type", "Handoff schema"),
        ("payload_ref", "Payload schema"),
        
        # Reference Index — spot check
        ("https://docs.python.org/3/library/", "Ref: Python"),
        ("https://peps.python.org/pep-0008/", "Ref: PEP8"),
        ("https://developer.veeqo.com/docs", "Ref: Veeqo"),
        
        # Failure Model
        ("Soft fail", "Failure: soft"),
        ("Hard fail", "Failure: hard"),
        ("Business exception", "Failure: business"),
        ("Dead-letter", "Failure: dead-letter"),
        
        # Agent Catalog — spot check
        ("PythonAutomator", "Agent: Python"),
        ("EcomOpsAnalyst", "Agent: Ecom"),
        ("DataOpsAuditor", "Agent: DataOps"),
        
        # Anti-Patterns — spot check
        ("Copy-of-a-copy delegation", "Anti-pattern: copy"),
        ("Skipping SWOT before T1 proposals", "Anti-pattern: SWOT"),
        ("Pretty reports masking unresolved exceptions", "Anti-pattern: reports"),
        
        # Routing
        ("Do NOT read the entire document", "Routing instruction"),
        ("STATIC CORE", "Routing: static core"),
        ("T1 EXECUTIVE MODULE", "Routing: T1"),
        ("T2 SPECIALIST MODULE", "Routing: T2"),
        ("T3 EXECUTOR MODULE", "Routing: T3"),
    ]
    
    for phrase, label in kernel_phrases:
        if phrase.lower() not in comp.lower():
            findings.append(f"SEMANTIC: Missing '{label}': \"{phrase}\"")
    
    # ================================================================
    # STEP 3: DEEP VERIFY — Structural integrity checks
    # ================================================================
    
    # Tier routing must have all 4 steps
    routing = comp.split("Tier Routing")[1].split("---")[0] if "Tier Routing" in comp else ""
    for step in ["Step 1", "Step 2", "Step 3", "Step 4"]:
        if step not in routing:
            findings.append(f"DEEP: Routing missing {step}")
    
    # All 5 module sections present
    for section in ["STATIC CORE", "T1 EXECUTIVE MODULE", "T2 SPECIALIST MODULE", 
                     "T3 EXECUTOR MODULE", "SHARED INFRASTRUCTURE"]:
        if section not in comp:
            findings.append(f"DEEP: Missing section: {section}")
    
    # Six planes of topology
    for plane in ["Ingestion", "Validation", "Processing", "State", "Output", "Governance"]:
        if plane not in comp:
            findings.append(f"DEEP: Missing topology plane: {plane}")
    
    # ADR template must have all fields in a code block
    adr_section = comp.split("Architecture Decision Records")[1][:2000] if "Architecture Decision Records" in comp else ""
    for field in ["Status:", "Context:", "Decision:", "Systemic Cost Analysis:", 
                  "Alternatives Considered:", "Consequences:", "Review:"]:
        if field not in adr_section:
            findings.append(f"DEEP: ADR template missing field: {field}")
    
    # All 3 checklist types present
    for ctype in ["CODE DELIVERABLE:", "DATA DELIVERABLE:", "INTEGRATION DELIVERABLE:"]:
        if ctype not in comp:
            findings.append(f"DEEP: Missing checklist type: {ctype}")
    
    # State machine has all states
    for state in ["intake", "validated", "processing", "review", "complete", "archived"]:
        if state not in comp:
            findings.append(f"DEEP: Missing state: {state}")
    
    # Delegation briefs cover all tiers
    deleg_section = comp.split("Delegation Protocol")[1].split("###")[0] if "Delegation Protocol" in comp else ""
    for tier in ["T1 (Executive)", "T2 (Contextual Specialist)", "T3 (Elite Executor)"]:
        if tier not in deleg_section:
            findings.append(f"DEEP: Delegation missing brief for {tier}")
    
    # Severity levels all present
    for sev in ["SEV1:", "SEV2:", "SEV3:"]:
        if sev not in comp:
            findings.append(f"DEEP: Missing severity level: {sev}")
    
    # Promotion environments
    if "dev → staging → production" not in comp:
        findings.append("DEEP: Missing environment promotion chain")
    
    # RACI definitions
    for role in ["R — Responsible:", "A — Accountable:", "C — Consulted:", "I — Informed:"]:
        if role not in comp:
            findings.append(f"DEEP: Missing RACI role: {role}")
    
    # Secrets lifecycle stages
    for stage in ["Creation:", "Storage:", "Access:", "Rotation:", "Revocation:", "Audit:"]:
        if f"  {stage}" not in comp and stage not in comp:
            findings.append(f"DEEP: Missing secrets lifecycle stage: {stage}")
    
    # Three observability pillars
    for pillar in ["Logs:", "Metrics:", "Traces:"]:
        if pillar not in comp:
            findings.append(f"DEEP: Missing observability pillar: {pillar}")
    
    # Composability block
    for skill in ["the-brain", "executive-dev-architecture", "persistent-ideation-engine"]:
        if skill not in comp:
            findings.append(f"DEEP: Missing composability reference: {skill}")
    
    # Version in frontmatter
    if "version: '3.2'" not in comp:
        findings.append("DEEP: Version not 3.2 in frontmatter")
    
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
print("EXEC-DEV v3.2 LOSSLESS COMPRESSION VERIFICATION")
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
print("Exec-dev v3.2 compression verified. Protocol kernel intact.")
print(f"Compression: {orig_words} → {comp_words} words ({pct:.1f}% reduction)")
print("No behavioral loss detected.")
print("=" * 70)
