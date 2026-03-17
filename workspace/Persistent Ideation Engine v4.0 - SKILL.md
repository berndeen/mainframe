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
  version: '4.0'
---

# Persistent Ideation Engine — Iterative Testing & Refinement Loop

## Purpose

This is a machine-learning-style training loop for code. The agent explores
multiple approaches, tests relentlessly, analyzes results, ideates improvements,
and repeats — burning through hundreds of test runs autonomously until the code
is bulletproof. The user hands over their test files, describes the goal, and
the agent goes to work. The user should only re-enter the loop at meaningful
decision points — never to report a crash, never to babysit, never to chase
the agent's tail.

Like an AI training on a video game: try every path, fail fast, learn from each
failure, adapt strategy, optimize moves, replay the level hundreds of times
until mastery.

## When to Use This Skill

Use this skill whenever you are:

- Building or modifying any code module, engine, or library
- Porting logic between environments (Python → JS, server → browser, etc.)
- Creating browser extensions, PDF generators, or complex tools
- Solving a problem where the best approach is not immediately obvious
- Working on anything the user will deploy, demo, or rely on

## Core Mindset

### The Agent Is the QA Team, the Debugger, and the Optimizer

The user is NOT your tester. When the user gives you sample files and says
"here, go make this work," that means:

- **You** run the tests — hundreds of them
- **You** find the bugs before the user does
- **You** probe your own code like a hostile user would
- **You** iterate until convergence without asking for permission each cycle
- **You** only come back to the user with results, not with errors

### Minimal User Intervention Is the Goal

Every time the user has to intervene, it's a design failure. Aim for:

- **Auto-detection** over manual selection (detect CSV format from headers)
- **Auto-fallback** over error messages (if API fetch fails, fall back to
  local file upload)
- **Single interaction point** over multi-step wizards (one drop zone, not
  three separate uploaders)
- **Zero configuration** over settings pages (sensible defaults that just work)

The ideal UX: the user drops their files and gets their output. Nothing else.

## Resource Acquisition — Get What You Need to Test

Before the training loop can run, the agent needs test inputs: sample files,
reference outputs, source code, specs, API keys, config values. Here is how
to get them:

### Step 1: Inventory What You Have

Before asking the user for anything, check what's already available:

1. **Scan the workspace.** Files from previous sessions, uploads, or prior
   work may already be sitting in the environment. Use `glob`, `read`, `grep`
   to find CSVs, PDFs, config files, source code, notebooks, reference
   outputs, etc.
2. **Check conversation history.** The user may have already provided URLs,
   file contents, sheet IDs, API endpoints, column names, or specs in earlier
   messages.
3. **Check memory.** Previous sessions may have stored relevant project
   details, file locations, credentials, or architectural decisions.
4. **Check connected services.** Google Drive, Notion, Slack, email — the
   files may be accessible through an integration the user has already
   connected.

Often you already have what you need. Don't ask for something you can find
yourself.

### Step 2: Identify Gaps

After the inventory, list what's still missing. Common gaps:

- Sample input files (CSVs, PDFs, images) for testing
- Reference/expected output to compare against
- Source code from the original implementation (e.g. a Colab notebook)
- Config values (sheet IDs, tab names, API endpoints, column mappings)
- Credentials or access tokens for external services
- Edge case files (large inputs, malformed inputs, unusual formats)

### Step 3: Prompt the User ONCE

If you're missing something critical, ask the user — but do it efficiently:

- **Batch your requests.** Don't ask for one file, wait, then ask for another.
  Ask for everything you need in a single prompt.
- **Be specific.** Don't say "I need test files." Say "I need a sample Veeqo
  CSV export and the corresponding shipping label PDF so I can validate the
  waterfall matching engine."
- **Explain why.** The user is more likely to provide what you need if they
  understand how it will be used.
- **Suggest alternatives.** "If you can't upload the file, can you point me
  to a URL, a Google Sheet ID, or describe the format?"

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

After a single prompt, if the user can't upload something or doesn't respond
to a specific request, **do not ask again.** Instead, solve it yourself:

- **Generate synthetic test data** from what you DO have. If you have the CSV
  schema but no sample rows, generate realistic rows. If you have one dataset
  but need edge cases, create variants.
- **Extract from source code.** If the user gave you a Colab notebook, the
  sheet IDs, column names, and format specs are in the code. Read them.
- **Fetch from URLs.** If a sheet ID or API endpoint is referenced in the
  code, try to fetch it directly.
- **Reverse-engineer from output.** If you have a reference output PDF but
  not the input, analyze the output to understand the expected format, layout,
  fonts, and margins.
- **Use public resources.** If you need a library, documentation, or format
  spec, search for it. Don't wait for the user to hand it to you.
- **Build a mock.** If all else fails, build a minimal mock that exercises
  the code path, and note it as a gap to be replaced with real data when
  available.

The rule: **prompt once, then self-solve.** The user should never be nagged
for the same thing twice.

### Throughout the Process: Continuous Resource Awareness

Resource gaps don't only appear at the start. They surface mid-build:

- **Epoch 3 reveals you need a 200-page PDF to test memory limits** — check
  if the workspace has one, or generate a synthetic large file.
- **A test failure suggests the column mapping is wrong** — re-read the
  source code or CSV headers before asking the user.
- **Visual comparison needs the original Colab output** — check if it was
  uploaded earlier, check workspace files, check if you can regenerate it
  from the notebook code.

At any point during the loop, if you discover you need something:

1. **Check workspace first** (files may already exist from earlier steps)
2. **Check conversation/memory** (user may have mentioned it)
3. **Try to acquire it yourself** (fetch, generate, reverse-engineer)
4. **Only if truly stuck:** prompt the user once, clearly and specifically
5. **If user doesn't provide it:** work around it and move on

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

1. **Define the problem.** Inputs, outputs, constraints, edge cases, target
   environments.
2. **Generate 2-4 distinct solution paths.** Don't settle on the first idea.
   - Different algorithms, libraries, architectures
   - Different trade-offs: speed vs memory, simplicity vs flexibility
   - Client-side vs server-side, streaming vs batch, sync vs async
3. **Evaluate each path** against real constraints:
   - Does it work in the target environment?
   - What are its failure modes?
   - How does it handle the largest realistic input?
   - What dependencies does it bring?
4. **Pick the most promising path.** Keep alternatives ranked — if this one
   hits a wall, pivot to the next without starting from zero.

### Epoch 1: Harness First, Then Implement

1. **Build the test harness before production code.**
   - Use the user's REAL sample files — never fabricate test data when real
     data exists
   - Cover every input format/path the code must handle
   - Output PASS/FAIL per run with key metrics (record counts, match rates,
     file sizes, execution time)
   - Designed to run headlessly (Node.js, sandbox — no manual browser clicks)
2. **Implement the chosen solution.**
3. **Run the full suite.** Get a baseline — what passes, what fails, what
   errors appear.

### Epoch 2+: The Persistent Feedback Loop

This is where the real work happens. Each epoch chains into the next.

#### Step 1: Analyze Failures AND Passes

Don't just fix what broke. Analyze everything:

- **Failures:** What assumption was wrong? What edge case was missed? Is the
  fix a band-aid or a root-cause solution?
- **Passes:** Is the code doing unnecessary work? Are there redundant copies,
  wasted allocations, repeated computations? Could the architecture be cleaner?

#### Step 2: Ideate Improvements

For each finding, brainstorm multiple fixes — don't grab the first one:

- Could a different data structure eliminate a bottleneck?
- Could a pre-processing step simplify downstream logic?
- Could a fallback path handle this failure gracefully instead of crashing?
- Could the UX be simplified to eliminate the user interaction that exposed
  this bug?

#### Step 3: Implement and Re-Test the FULL Suite

Not just the thing you changed. Everything. Every format, every dataset,
every edge case. Run it all, minimum 10x per test set.

#### Step 4: Compare to Previous Epoch

- Did pass rate improve? (Must be ≥ previous epoch)
- Did performance improve or hold?
- Did any previously passing test regress?
- **If regression occurred:** revert or rethink. Never ship a regression.

#### Step 5: Chain Into Next Epoch

The output of this epoch's analysis becomes the input to the next epoch's
ideation. This is the persistent feedback loop — each cycle learns from the
last.

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

Don't just test the happy path. Actively try to break your own code:

- **Malformed inputs:** CSVs with BOM encoding, extra whitespace, missing
  columns, empty rows
- **Scale inputs:** What happens with 200 pages instead of 5? 500 ITEMDB rows
  instead of 10?
- **Missing dependencies:** What if the Google Sheets fetch fails? What if a
  column name is slightly different?
- **Boundary conditions:** Zero items, one item, max-length item names, special
  characters, Unicode
- **Race conditions:** Run the same operation 10x in rapid succession — does
  state leak between runs?
- **Environment gaps:** Does it work in Node.js AND the browser? Does it work
  with the extension's content security policy?

For each adversarial probe that reveals a weakness, it goes back into the
ideation loop.

### Progressive Scale Testing

Don't jump to the largest dataset. Scale up gradually:

```
Level 1: Smallest dataset (5 pages, 5 records) × 10 runs
Level 2: Medium dataset (15-20 pages) × 10 runs
Level 3: Largest available dataset × 10 runs
Level 4: Multiple datasets in same run (mixed formats) × 10 runs
```

Each level may reveal issues that didn't appear at smaller scale — memory
growth, performance degradation, index overflow.

### Path Abandonment Protocol

Sometimes an approach is fundamentally broken. Know when to pivot:

- **3 consecutive failed fix attempts** on the same root issue → re-evaluate
  the approach, not just the fix
- **Environmental impossibility** (e.g. CORS blocking API calls from
  extension) → pivot to the next ranked solution path
- **Diminishing returns** (each fix creates a new bug) → the architecture may
  be wrong, not just the implementation

When abandoning a path:

1. Document what was tried and why it failed
2. Carry forward any reusable components (parsers, utilities, test harness)
3. Pivot to the next ranked approach from Epoch 0
4. Do NOT keep retrying the same broken thing

This is like the AI recognizing that a strategy will never clear the level and
switching to a completely different approach.

## Visual Output Verification

For code that produces visual artifacts (PDFs, images, slides):

1. Generate sample output from the test suite
2. Render and inspect — open the PDF, screenshot the page, examine every
   element
3. Compare against the user's reference:
   - Font sizes and weights — check the source code specs, don't eyeball
   - Margins — left AND right, symmetrical if reference is symmetrical
   - Text wrapping — same break points as reference
   - Layout spacing — measure, don't guess
4. If anything is off → back into the ideation loop

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