---
name: persistent-ideation-engine
description: >-
  Iterative ideation-testing-refinement engine for building code. Works like ML
  training: explore multiple solution paths, pick the best, test relentlessly,
  analyze results, ideate improvements, test again, repeat until convergence.
  Use when building, testing, or refining any code deliverable. Prevents
  shipping untested code.
license: MIT
metadata:
  author: CJ
  version: '4.1'
---

# Persistent Ideation Engine — Iterative Testing & Refinement Loop

## Purpose

ML-style training loop for code. Explore multiple approaches, test relentlessly, analyze results, ideate improvements, repeat — burning through hundreds of test runs autonomously until bulletproof. User hands over test files, describes the goal, agent goes to work. User re-enters only at meaningful decision points — never to report crashes, babysit, or chase the agent's tail.

Like AI training on a video game: try every path, fail fast, learn from each failure, adapt strategy, optimize moves, replay hundreds of times until mastery.

## When to Use This Skill

- Building or modifying any code module, engine, or library
- Porting logic between environments (Python → JS, server → browser, etc.)
- Creating browser extensions, PDF generators, or complex tools
- Solving problems where best approach is not immediately obvious
- Working on anything the user will deploy, demo, or rely on

## Core Mindset

### The Agent Is the QA Team, the Debugger, and the Optimizer

User is NOT your tester. When given sample files and told "make this work":

- **You** run tests — hundreds of them
- **You** find bugs before the user does
- **You** probe your own code like a hostile user would
- **You** iterate until convergence without asking permission each cycle
- **You** only return to user with results, not errors

### Minimal User Intervention Is the Goal

Every user intervention = design failure. Aim for:

- **Auto-detection** over manual selection (detect CSV format from headers)
- **Auto-fallback** over error messages (API fetch fails → fall back to local upload)
- **Single interaction point** over multi-step wizards (one drop zone, not three uploaders)
- **Zero configuration** over settings pages (sensible defaults that just work)

Ideal UX: user drops files, gets output. Nothing else.

## Resource Acquisition — Get What You Need to Test

Before the training loop runs, agent needs test inputs: sample files, reference outputs, source code, specs, API keys, config values.

### Step 1: Inventory What You Have

Before asking the user, check what's available:

1. **Scan workspace.** Files from previous sessions, uploads, prior work. Use `glob`, `read`, `grep` for CSVs, PDFs, config files, source code, notebooks, reference outputs.
2. **Check conversation history.** URLs, file contents, sheet IDs, API endpoints, column names, specs from earlier messages.
3. **Check memory.** Previous sessions: project details, file locations, credentials, architectural decisions.
4. **Check connected services.** Google Drive, Notion, Slack, email — files may be accessible through existing integrations.

Often you already have what you need. Don't ask for what you can find.

### Step 2: Identify Gaps

After inventory, list what's missing. Common gaps: sample input files, reference/expected output, source code from original implementation, config values (sheet IDs, tab names, API endpoints, column mappings), credentials, edge case files.

### Step 3: Prompt the User ONCE

Missing something critical → ask efficiently:

- **Batch requests.** Everything needed in a single prompt.
- **Be specific.** Not "I need test files" — "I need a sample Veeqo CSV export and the corresponding shipping label PDF to validate the waterfall matching engine."
- **Explain why.** User provides more readily when they understand the purpose.
- **Suggest alternatives.** "If you can't upload, point me to a URL, Google Sheet ID, or describe the format."

Example prompt:
```
To build and test the dock tab engine, I need:
1. A sample CSV export from each shipping platform you use (Veeqo, Label
   Express, etc.)
2. The corresponding label PDFs for each CSV
3. A reference output PDF from the Colab notebook so I can match the layout
4. The ITEMDB spreadsheet (or a CSV export of the MATCH/REPLACE columns)

If any of these are already in a Google Sheet or Drive folder, I can pull
them directly — just share the link.
```

### Step 4: If the User Can't Provide It — Figure It Out

After a single prompt, if user can't upload or doesn't respond, **do not ask again.** Self-solve:

- **Generate synthetic test data** from what you DO have. Have schema but no rows → generate realistic rows. Have one dataset → create edge case variants.
- **Extract from source code.** Colab notebook contains sheet IDs, column names, format specs. Read them.
- **Fetch from URLs.** Sheet ID or API endpoint referenced in code → try fetching directly.
- **Reverse-engineer from output.** Have reference output but not input → analyze for format, layout, fonts, margins.
- **Use public resources.** Need a library or format spec → search. Don't wait for the user.
- **Build a mock.** Last resort: minimal mock exercising the code path, noted as gap to replace with real data.

Rule: **prompt once, then self-solve.** Never nag for the same thing twice.

### Throughout: Continuous Resource Awareness

Gaps surface mid-build:

- Epoch 3 reveals need for 200-page PDF for memory testing → check workspace or generate synthetic.
- Test failure suggests wrong column mapping → re-read source code or CSV headers before asking user.
- Visual comparison needs original output → check workspace, check if regenerable from notebook code.

At any point needing something: 1) Check workspace 2) Check conversation/memory 3) Try self-acquisition 4) Only if truly stuck: prompt user once 5) If not provided: work around and move on.

## The Training Loop

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   IDEATE → IMPLEMENT → TEST (relentlessly) → ANALYZE    │
│      ↑                                          │       │
│      └──────────────────────────────────────────┘       │
│                                                          │
│   Each epoch's failures feed the next epoch's ideation   │
│   Keep going until convergence — not until "10 passes"   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Epoch 0: Exploration — Multiple Solution Paths

Before writing production code:

1. **Define the problem.** Inputs, outputs, constraints, edge cases, target environments.
2. **Generate 2-4 distinct solution paths.** Don't settle on the first idea.
   - Different algorithms, libraries, architectures
   - Different trade-offs: speed vs memory, simplicity vs flexibility
   - Client-side vs server-side, streaming vs batch, sync vs async
3. **Evaluate each path** against real constraints:
   - Does it work in the target environment?
   - What are its failure modes?
   - How does it handle the largest realistic input?
   - What dependencies does it bring?
4. **Pick the most promising path.** Keep alternatives ranked — if this one hits a wall, pivot to next without starting from zero.

### Epoch 1: Harness First, Then Implement

1. **Build test harness before production code.**
   - Use the user's REAL sample files — never fabricate when real data exists
   - Cover every input format/path the code must handle
   - Output PASS/FAIL per run with key metrics (record counts, match rates, file sizes, execution time)
   - Designed to run headlessly (Node.js, sandbox — no manual browser clicks)
2. **Implement the chosen solution.**
3. **Run full suite.** Baseline: what passes, what fails, what errors appear.

### Epoch 2+: The Persistent Feedback Loop

Each epoch chains into the next.

#### Step 1: Analyze Failures AND Passes

Don't just fix what broke. Analyze everything:

- **Failures:** What assumption was wrong? Edge case missed? Is the fix a band-aid or root-cause?
- **Passes:** Unnecessary work? Redundant copies, wasted allocations, repeated computations? Cleaner architecture possible?

#### Step 2: Ideate Improvements

For each finding, brainstorm multiple fixes — don't grab the first:

- Different data structure to eliminate bottleneck?
- Pre-processing step to simplify downstream logic?
- Fallback path for graceful failure instead of crash?
- UX simplification to eliminate the interaction that exposed the bug?

#### Step 3: Implement and Re-Test the FULL Suite

Not just the thing you changed. Everything. Every format, every dataset, every edge case. Run it all, minimum 10x per test set.

#### Step 4: Compare to Previous Epoch

- Did pass rate improve? (Must be ≥ previous epoch)
- Did performance improve or hold?
- Did any previously passing test regress?
- **If regression occurred:** revert or rethink. Never ship a regression.

#### Step 5: Chain Into Next Epoch

Output of this epoch's analysis → input to next epoch's ideation. Persistent feedback loop — each cycle learns from last.

```
Epoch 2: Fix ArrayBuffer detachment → .slice(0) copy
  → Unlocks: tests that previously crashed now run
  → Reveals: BOM double-encoding in Label Express CSVs (was hidden by crash)

Epoch 3: Fix BOM detection → strip double-encoded BOM
  → Unlocks: all Label Express tests pass
  → Reveals: word wrap at 25 chars makes text look too large vs reference

Epoch 4: Analyze reference PDF specs → wrap should be 30 chars
  → Fix wrap, re-run full suite
  → Reveals: character-count wrap is imprecise, pixel-width wrap is better

Epoch 5: Switch to font.widthOfTextAtSize() measurement
  → More accurate wrapping, symmetrical margins
  → 30/30 tests pass, visual match confirmed → SHIP
```

Each fix exposed the next issue. That's the chaining.

### Adversarial Self-Probing

Don't just test happy path. Actively break your own code:

- **Malformed inputs:** CSVs with BOM encoding, extra whitespace, missing columns, empty rows
- **Scale inputs:** 200 pages instead of 5? 500 ITEMDB rows instead of 10?
- **Missing dependencies:** Google Sheets fetch fails? Column name slightly different?
- **Boundary conditions:** Zero items, one item, max-length names, special characters, Unicode
- **Race conditions:** Same operation 10x rapid succession — state leak between runs?
- **Environment gaps:** Works in Node.js AND browser? Works with extension's CSP?

Each adversarial probe revealing weakness → back into ideation loop.

### Progressive Scale Testing

Scale up gradually:

```
Level 1: Smallest dataset (5 pages, 5 records) × 10 runs
Level 2: Medium dataset (15-20 pages) × 10 runs
Level 3: Largest available dataset × 10 runs
Level 4: Multiple datasets in same run (mixed formats) × 10 runs
```

Each level may reveal issues invisible at smaller scale — memory growth, performance degradation, index overflow.

### Path Abandonment Protocol

Sometimes an approach is fundamentally broken. Know when to pivot:

- **3 consecutive failed fix attempts** on same root issue → re-evaluate approach, not just fix
- **Environmental impossibility** (e.g. CORS blocking API calls from extension) → pivot to next ranked path
- **Diminishing returns** (each fix creates new bug) → architecture may be wrong, not implementation

When abandoning:

1. Document what was tried and why it failed
2. Carry forward reusable components (parsers, utilities, test harness)
3. Pivot to next ranked approach from Epoch 0
4. Do NOT keep retrying the same broken thing

Like AI recognizing a strategy will never clear the level and switching to a completely different approach.

## Visual Output Verification

For code producing visual artifacts (PDFs, images, slides):

1. Generate sample output from test suite
2. Render and inspect — open PDF, screenshot page, examine every element
3. Compare against user's reference:
   - Font sizes and weights — check source code specs, don't eyeball
   - Margins — left AND right, symmetrical if reference is symmetrical
   - Text wrapping — same break points as reference
   - Layout spacing — measure, don't guess
4. Anything off → back into ideation loop

## What This Looks Like in Practice

```
User: "Here are my test files. Beat your head against the wall testing
       this thing over and over and over again."

Resource check: User uploaded 3 CSVs, 3 PDFs, 1 reference output PDF,
  1 ITEMDB CSV. Colab notebook code already in workspace from prior
  session. Sheet ID found in notebook code: 1cb1iz...hzc. Tab name
  found in code: "ITEMDB" — but will verify against actual data.
  → Have everything needed. No user prompt required.

Epoch 0: Explore paths for porting Python PDF generator to browser JS
  Path A: pdf-lib + pdf.js (client-side, no server needed)
  Path B: jsPDF (simpler but less capable)
  Path C: Server endpoint (powerful but adds infrastructure)
  → Pick A: best fit for Chrome extension environment

Epoch 1: Build harness with 3 real datasets, implement engine
  → 12/20 tests pass, 8 fail on various errors
  → Baseline established

Epoch 2: Fix DockTabEngine undefined → window.DockTabEngine IIFE
  → 16/20 pass now → chained reveal: Sheets fetch failing

Epoch 3: Fix Sheets tab name → "ITEM NAME DATABASE"
  → Need: correct tab name. Check notebook code — says "ITEMDB".
    Check the actual CSV headers user uploaded — columns are MATCH
    and REPLACE. Tab name unclear.
  → Prompt user ONCE: "What's the exact tab name in Google Sheets?"
  → User: "ITEM NAME DATABASE"
  → 18/20 pass → chained reveal: gviz fetch unreliable from extension

Epoch 4: PIVOT — gviz fetch path abandoned after 3 failed approaches
  → Need: ITEMDB data for testing. Already have the CSV the user
    uploaded earlier — use it as local fallback. No prompt needed.
  → Add local CSV upload as fallback → 19/20 pass
  → chained reveal: ArrayBuffer detachment on large PDFs

Epoch 5: Fix ArrayBuffer → .slice(0) before pdf.js consumes it
  → 20/20 pass → chained reveal: BOM double-encoding in Label Express

Epoch 6: Fix BOM detection → strip ï»¿ prefix
  → 20/20 pass, run 10x each → stable
  → chained reveal: word wrap too tight, font visually oversized

Epoch 7: Analyze Colab source → wrap should be 30 chars, not 25
  → Need: exact font specs from Colab. Already have notebook_code_cells.py
    in workspace from prior session — read it directly. No prompt needed.
  → Fix → 30/30 pass (3 datasets × 10 runs)

Epoch 8: User requests 15pt font + symmetrical margins
  → Switch to pixel-width measurement instead of char count
  → More accurate, adapts to actual glyph widths
  → 30/30 pass, visual match confirmed → SHIP

Total: ~300+ test runs across 8 epochs. User intervened 3 times
(tab name correction, font feedback, margin request). Every other
issue — including resource gaps — was resolved by the agent checking
existing files, reading source code, or building fallbacks.
```

## Anti-Patterns

| Anti-Pattern | What to Do Instead |
|---|---|
| Asking the user for files without checking workspace first | Scan workspace, memory, and conversation history before prompting |
| Asking for the same thing twice | Prompt once, then self-solve (generate, fetch, reverse-engineer) |
| Settling on the first approach | Generate 2-4 paths, evaluate, pick the best |
| "I updated the code, try it now" | Run hundreds of tests, then ship results |
| Fixing one bug without re-running everything | Full suite, every format, every time |
| Stopping at 10 passes | Keep going until convergence, 10x is the minimum |
| Waiting for user to find bugs | Probe your own code adversarially |
| Retrying a broken approach 5+ times | Abandon the path, pivot to the next one |
| "The logic looks correct" | Reasoning is not testing — execute and verify |
| Fabricating test data when real data exists | Use the user's real sample files |
| Asking the user what to do at every step | Make decisions, test them, report results |
| Designing UX that requires user configuration | Auto-detect, auto-fallback, zero-config |
| Blocking on a missing file without trying alternatives | Generate synthetic data, reverse-engineer from output, build a mock |



## Convergence and Stop Conditions

Convergence is multi-signal, not a fixed run count.

<HARD-GATE>
No ship without convergence criteria met. Stable failure is not convergence. Time pressure is not convergence.
</HARD-GATE>

**ALL must be true to ship:**
- Stable pass rate over 3 consecutive epochs (no regression)
- Zero regressions from any previous epoch
- No new failure class introduced in last 2 epochs
- No unresolved high-severity defect
- Budget sufficient for at least 1 more epoch (if not, report "budget-stopped" per Brain's Budget Protocol)

**Per-epoch tracking ledger:**
```
Epoch {n}: pass/fail counts | regressions: {count} | new_failures: {count} | 
           runtime_trend: {improving|stable|degrading} | human_interventions: {count}
```

**Stop conditions (any = stop):**

| Condition | Governs |
|-----------|---------|
| Convergence achieved (all criteria met) | Ship |
| Budget exhausted | Brain's Budget Protocol |
| Max epochs reached (default ceiling: 10, configurable) | Report partial results |
| Human override (explicit stop signal) | Respect immediately |
| Circuit breaker tripped | Brain's Circuit Breaker governs |

## Coverage Ledger

High code coverage ≠ coverage. Scenario coverage is the actual risk. Ledger forces explicit tracking — "untested" is valid but must be justified.

| Dimension | Measures | Minimum |
|-----------|---------|---------|
| Input shapes | Types, sizes, encodings, empty, malformed | Every declared input type |
| Path/branch | Code paths exercised | All non-dead paths |
| Failure modes | Expected error handling | Every declared failure_mode |
| Scale tiers | Load levels tested | At least 1x and 10x expected |
| Environments | Platform/config variants | Dev + prod-shaped |
| State transitions | FSM edge coverage | Every valid transition |
| Dependency interactions | External service behavior | Normal + degraded + absent |

No dimension unmeasured at ship. Required artifact: compact coverage matrix — tested vs. untested scenario classes, rationale for any uncovered class. High code coverage cannot waive missing scenario coverage.

## Adversarial and Failure-Injection Testing

Not "can it handle bad input" — "does it fail THE WAY WE EXPECT?" Uncontrolled failure = untested.

8 required adversarial classes — each must have at least 1 test asserting EXPECTED failure behavior:

1. **Malformed inputs** — wrong types, truncated, encoded incorrectly
2. **Boundary extremes** — empty, max-size, off-by-one, overflow
3. **Dependency failures** — service down, timeout, wrong version
4. **Timeouts** — slow responses, hung connections, deadline exceeded
5. **Concurrency** — race conditions, deadlocks, out-of-order delivery
6. **Resource pressure** — memory limits, disk full, rate limits
7. **Environment mismatches** — wrong config, missing env vars, version skew
8. **Partial-state corruption** — half-written files, interrupted transactions, stale cache

Each test must assert expected outcome: graceful degradation, bounded retry, fast fail, rollback, dead-letter/manual-review routing, or safe no-op. Each class exercised or explicitly marked not applicable with rationale. Fault injection runs in isolated conditions only. PIE tests against circuit-breaker expectations; Brain's Circuit Breaker governs suite-wide response.

## Periodic / Scheduled Execution Testing

For agents/tasks on schedules (heartbeat, cron, polling). PIE owns test protocol — not runtime scheduling architecture (Brain and ExecDev govern that).

**Harness requirements:**
- Controllable time — inject artificial timestamps, no real-clock dependency
- Persisted-state snapshots — verify state survives between executions
- 3+ consecutive heartbeat replay — simulate multiple cycles, verify no state drift

**Required assertions:**

| Assertion | What it verifies |
|-----------|-----------------|
| Idempotency | Same input → same output across repeated cycles |
| Replay safety | Re-running produces no duplicate side effects |
| Empty-cycle | Nothing to do → clean skip, no errors, no mutations |
| Delayed-cycle | Late execution → correct catch-up behavior |
| Backlog handling | Multiple missed cycles → correct bounded recovery |

**Ship gate:** No scheduled agent ships without evidence that state persistence, replay safety, and multi-heartbeat regression tests pass.

## Cross-Agent and Pipeline Testing

For multi-agent workflows (swarms, councils, delegation chains). Single-agent correctness does not guarantee pipeline correctness.

**Required test layers:**
- **Contract compatibility** — verify producer output matches consumer input schema
- **E2E happy path** — full pipeline produces correct final output
- **Degraded-node** — one agent fails → pipeline handles gracefully (retry, reroute, partial result)
- **Replay/idempotency** — re-running pipeline segment = no duplicate side effects
- **Escalation-path** — failure at each tier triggers correct escalation chain

**At each handoff point, assert:**

| Assertion | What it verifies |
|-----------|-----------------|
| Schema compliance | Structural validity — fields present, types correct |
| Semantic correctness | Meaningful values, not just valid types |
| State continuity | No lost context or correlation IDs between agents |

Integration failures must record: which boundary failed, what was expected, what arrived, whether defect is producer-side, consumer-side, or orchestration-side. Run fast boundary tests frequently; heavy E2E suites at meaningful checkpoints. ExecDev defines contracts and orchestration; PIE defines how to test whether those structures hold.

## Pre-Ship Checklist

- [ ] Resource inventory done (workspace, memory, conversation, connected services)
- [ ] Missing resources acquired: user prompted once OR self-solved
- [ ] Multiple solution paths explored, best one selected with rationale
- [ ] Test harness built with real user data, all input formats covered
- [ ] Adversarial probes run (malformed inputs, scale, missing deps, boundaries)
- [ ] Progressive scale testing: small → medium → large datasets
- [ ] Full suite passes with 0 failures across all runs
- [ ] Each test set run 10x minimum (more if convergence not yet reached)
- [ ] No regressions from any previous epoch
- [ ] Visual outputs rendered, inspected, and matched against reference
- [ ] Path abandonment used where appropriate (not stuck retrying broken paths)
- [ ] UX minimizes user touchpoints (auto-detect, fallbacks, single drop zone)
- [ ] User receives results + sample output, not "it should work"
