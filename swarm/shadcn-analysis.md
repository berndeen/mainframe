# shadcn/ui — Deep Pattern Analysis for Skill Suite v4.4

**Source:** 16 architectural doc pages crawled via wide_browse (2026-03-08)
**Pages:** Namespaces, Authentication, components.json, Skills, Monorepo, Dark Mode, Getting Started, MCP, Registry Index, Open in v0, JavaScript, RTL, Changelog, Examples, MCP Registry, llms.txt

---

## Core Philosophy

shadcn/ui is NOT a component library — it's a **code distribution platform**. Five principles:

1. **Open Code / Copy-Don't-Install** — Users own source code, not npm dependencies. No version lock-in, no abandoned packages.
2. **Composable Interface** — Common, predictable API across all components. Flat-file schema + registry for distribution.
3. **AI-Ready** — Open code means LLMs read, understand, generate against real schemas. Skills + MCP bridge AI agents to registries.
4. **Beautiful Defaults with Override** — Great out-of-box design, fully customizable at every layer.
5. **Decentralized Federation** — No central authority. Teams host their own registries, resolve cross-registry deps.

---

## Architecture: Six Interconnected Systems

### 1. Registry System (Distribution Backbone)

**registry.json** — Top-level manifest:
```json
{
  "$schema": "https://ui.shadcn.com/schema/registry.json",
  "name": "acme",
  "homepage": "https://acme.com",
  "items": [...]
}
```

**registry-item.json** — Atomic unit of distribution:
```json
{
  "name": "unique-id",
  "type": "registry:component | registry:ui | registry:hook | registry:lib | registry:block | registry:page | registry:theme | registry:style | registry:font | registry:file | registry:base | registry:item",
  "dependencies": { "npm-package": "@version" },
  "devDependencies": {},
  "registryDependencies": ["button", "@acme/input-form", "https://example.com/r/item.json"],
  "files": [{ "path": "...", "type": "...", "target": "..." }],
  "cssVars": { "light": {}, "dark": {} },
  "css": "...",
  "envVars": ["API_KEY"],
  "categories": ["..."],
  "author": "...",
  "docs": "Custom CLI install message",
  "meta": {}
}
```

**Key design decisions:**
- Items are data-only JSON — no arbitrary code execution (trust model)
- `registryDependencies` enable recursive resolution across registries
- `target` field maps abstract paths to concrete project locations
- `meta` field = extensible metadata without breaking core schema
- `extends: none` option bypasses default behaviors

### 2. Namespaced Registries (Federation)

- Prefix: `@namespace/resource` — prevents collisions, clear provenance
- Configured in `components.json` under `registries` key
- **Simple format:** URL string with `{name}` placeholder
- **Advanced format:** Object with `url`, `headers`, `query` fields
- **Resolution overrides:** Later-resolved resources overwrite files + deep-merge configs (Tailwind, CSS vars)
- **Cross-registry dependency resolution:** Topological sorting, deduplication, recursive fetching

### 3. Authentication (Access Control)

Three auth patterns:
- **Bearer tokens:** `"Authorization": "Bearer ${REGISTRY_TOKEN}"`
- **API keys:** `"X-API-Key": "${API_KEY}"` + `"X-Workspace-Id": "${WORKSPACE_ID}"`
- **Query parameters:** `"token": "${ACCESS_TOKEN}"`

Advanced patterns:
- Team-based access control (different registries per team)
- User-personalized registries (content varies by identity)
- Temporary expiring tokens (`{ token, expiresAt, scope }`)
- Environment variable expansion (`${VAR_NAME}`) — no secrets in config
- HTTPS enforcement, rate limiting, access logging
- Custom error responses from server → CLI displays human-readable messages

### 4. Skills System (AI Context Injection)

The killer pattern for our suite:
- **Activation:** Detects `components.json` presence
- **Context gathering:** Runs `shadcn info --json` → exports framework, Tailwind version, aliases, installed components
- **Injection:** Project state fed into AI assistant's system prompt
- **Pattern enforcement:** Assistant follows composition rules (e.g., "always use FieldGroup for forms") based on detected state
- **Result:** AI generates code that's architecturally compliant, not generic

### 5. MCP Server (AI Agent Bridge)

Model Context Protocol server enables:
- AI assistants search, browse, install from registries via natural language
- Maps user intent → CLI commands
- Configured via `.mcp.json` in project root
- Works with any MCP-compatible client (Claude Code, etc.)
- Bridges the gap between documentation and implementation

### 6. Monorepo Support (Workspace Awareness)

- `init --monorepo` sets up Turborepo structure
- Per-workspace `components.json` with different alias configurations
- CLI detects monorepo boundaries automatically
- Shared UI in `packages/ui`, app-specific in `apps/web`
- Alias-based composability (`@workspace/ui`) decouples usage from paths

---

## Changelog Signals (Evolution Direction)

- **Presets:** Encapsulated design system configs distributed as short codes
- **registry:base:** Entire design system as single payload
- **Agent-First CLI:** `--dry-run`, `--view`, `docs` command designed for coding agents
- **Unified packages:** Moving from granular `@radix-ui/react-*` to single `radix-ui` 
- **Logical styling (RTL):** Physical → logical CSS class transformation at install time

---

## Pattern Mapping: shadcn → Our Skill Suite

### HIGH PRIORITY — Direct Implementation

| shadcn Pattern | Our Equivalent | Gap | v4.4 Action |
|---------------|---------------|-----|-------------|
| `registry-item.json` schema | No formal skill manifest | **Critical** | ExecDev v3.3: Skill Registry Schema |
| Namespaced registries | Single-origin skills | **Medium** | ExecDev v3.3: Namespace-aware skill resolution |
| `registryDependencies` | Informal "load Brain + PIE" | **Critical** | ExecDev v3.3: `skillDependencies` field with version constraints |
| Skill types (`registry:ui`, etc.) | No skill type taxonomy | **Medium** | ExecDev v3.3: `skill:governance`, `skill:architecture`, `skill:implementation`, `skill:reference`, `skill:audit` |
| `target` file placement | Ad-hoc workspace paths | **Low** | ExecDev v3.3: Standard paths in skill manifest |
| `meta` extensibility | No extensible metadata | **Low** | ExecDev v3.3: `meta` field in skill manifest |

### MEDIUM PRIORITY — Architectural Adaptation

| shadcn Pattern | Adaptation | v4.4 Location |
|---------------|-----------|--------------|
| Skills (context injection) | Skill self-describes its context requirements; loader injects project state | Brain v4.4: Context Injection Protocol |
| MCP bridge | Skills expose discovery tools to agents | ExecDev v3.3: Agent discovery protocol |
| `--dry-run` / `--view` | Pre-load inspection of skill impact | Brain v4.4: Skill impact preview |
| Pattern enforcement | Skills declare composition rules agents must follow | Already exists (routing protocol) — validate it's explicit enough |
| Resolution overrides | Local skill can extend/override vendor skill | ExecDev v3.3: Override protocol in namespace system |

### ALREADY IMPLEMENTED (Validation)

| shadcn Pattern | Our Implementation | Status |
|---------------|-------------------|--------|
| Copy-don't-install | Skills are markdown files loaded + modified | VALIDATED |
| AI-ready design | Modular routing, compression protocol, clear boundaries | VALIDATED |
| Beautiful defaults | Brain defaults to T1-Super, PIE defaults to full convergence | VALIDATED |
| Composability | Brain → classify, ExecDev → organize, PIE → build | VALIDATED |
| Data-only trust model | Skills are text/markdown, not executable code | VALIDATED |

### LOW PRIORITY / FUTURE

| shadcn Pattern | Future Possibility |
|---------------|-------------------|
| Presets | "Governance presets" — pre-configured skill bundles for common archetypes (startup, enterprise, compliance-heavy) |
| registry:base | Single-payload "full governance suite" install |
| Monorepo awareness | Multi-project skill scoping (same org, different governance tiers) |
| Team-based auth | Access control for proprietary governance skills |
| Temporary tokens | Time-boxed skill access for consultants/contractors |

---

## Key Insight: What shadcn Gets Right That We Should Steal

1. **Schema-first distribution.** Their entire system runs on two JSON schemas. Everything flows from those schemas — CLI, MCP, skills, namespaces. Our skills lack this structural backbone.

2. **Dependency resolution is first-class.** Not an afterthought. `registryDependencies` + topological sorting + deduplication. Our "load Brain + PIE" is informal.

3. **AI is a first-class consumer.** Skills, MCP, `--dry-run`, `info --json` — the entire system assumes AI agents are primary users. We should formalize how agents discover, load, and compose skills.

4. **Federation without centralization.** Anyone can host a registry. Namespaces prevent collision. Overrides allow local customization. Our skills are currently single-origin only.

5. **The meta field pattern.** Arbitrary extensibility without schema changes. Critical for governance metadata (compliance-level, security-tier, stability-rating).

---

## Synthesis Implications for v4.4

The deep crawl **reinforces and deepens** the existing synthesis proposals:

- **Skill Registry Schema** (ExecDev v3.3): Now informed by full `registry-item.json` spec — should include `type`, `dependencies`, `skillDependencies`, `files`, `routing`, `meta`, `envVars`
- **Context Injection** (Brain v4.4): Skills system shows how to formalize self-description for agent consumption
- **Agent Discovery** (ExecDev v3.3): MCP pattern shows bridge between agent natural language and skill operations
- **Override Protocol** (ExecDev v3.3): Namespace system shows layered override with deep-merge semantics

**New additions from deep crawl (not in initial synthesis):**
1. **Skill Impact Preview** — pre-load inspection (from `--dry-run` pattern)
2. **Universal Items** — framework-agnostic file distribution (from Examples page)
3. **Preset Bundles** — encapsulated governance configs (from Changelog)
4. **Custom Error Responses** — human-readable governance enforcement messages (from Auth page)
