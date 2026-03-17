---
name: remotion
description: >-
  Use when building programmatic videos with React using Remotion. Covers
  composition architecture, animation patterns, data-driven video pipelines,
  rendering workflows, and production delivery. Use when creating, testing,
  or refining any video deliverable — ads, social content, personalized
  videos, dashboards, or internal tooling demos.
license: MIT
metadata:
  author: CJ
  version: '1.0'
---

# Remotion — Programmatic Video Production Skill v1.0

## Routing Protocol — READ THIS FIRST

Modular skill. Do NOT read the entire document. Loading unneeded modules = context window violation.

```
STEP 1: Read CORE CONCEPTS (stop at ═══ COMPOSITION ARCHITECTURE)
STEP 2: Classify your task:
          BUILD      → ═══ COMPOSITION ARCHITECTURE (stop at ═══ ANIMATION & MOTION)
          ANIMATE    → ═══ ANIMATION & MOTION (stop at ═══ DATA-DRIVEN PIPELINES)
          DATA-VIDEO → ═══ DATA-DRIVEN PIPELINES (stop at ═══ RENDERING & DELIVERY)
          RENDER     → ═══ RENDERING & DELIVERY (stop at ═══ SHARED INFRASTRUCTURE)
STEP 3: Read ═══ SHARED INFRASTRUCTURE only if referenced by your module
```

**DO NOT read beyond your classification. DO NOT skim ahead.**

---

# ═══════════════════════════════════════════════════════════════
# CORE CONCEPTS — ALL TASKS
# ═══════════════════════════════════════════════════════════════

## What Remotion Is

React components rendered frame-by-frame into video. Every frame is a React render. CSS, SVG, Canvas, WebGL, HTML — anything React can render becomes a video frame. Code is the timeline. Components are the clips. Props are the script.

**Mental Model:** Think of each frame as a pure function: `f(frame, props) → visual output`. No side effects between frames. No animation state. Frame number is the single source of truth.

## The Frame Contract

```
frame: number        — current frame (0-indexed)
fps: number          — frames per second (typically 30)
durationInFrames     — total frames in composition
width / height       — output resolution in pixels

time = frame / fps   — derive time, never store it
progress = frame / durationInFrames  — 0→1 completion
```

Every animation, transition, data lookup, and visual decision derives from `frame`. This is non-negotiable.

## Key Primitives

| Primitive | Purpose | When to Use |
|-----------|---------|-------------|
| `<Composition>` | Defines a video — dimensions, fps, duration, component | Top-level video registration |
| `<Sequence>` | Offsets children in time — `from` delays start frame | Sequencing clips, staggering elements |
| `<Series>` | Sequential clips with no overlap — automatic offsetting | Slideshow, scene-by-scene |
| `<AbsoluteFill>` | Full-frame positioned container | Base layer for every scene |
| `useCurrentFrame()` | Returns current frame number | Every animated component |
| `useVideoConfig()` | Returns fps, width, height, durationInFrames | Responsive/dynamic components |
| `interpolate()` | Maps frame ranges to value ranges | All numeric animations |
| `spring()` | Physics-based easing | Natural motion, bounces, snaps |
| `<Audio>` / `<Video>` | Media embedding with frame-accurate sync | Voiceover, background music, video clips |
| `<Img>` / `<OffthreadVideo>` | Optimized media for rendering | Static images, heavy video sources |
| `<Still>` | Single-frame composition (thumbnail/poster) | OG images, thumbnails |

## Systemic Cost Dimensions for Video

| Cost Dimension | Video-Specific Meaning |
|---------------|----------------------|
| Tokens / Credits | AI compute for script generation, data fetching |
| Time | Render time per video — scales with duration, resolution, complexity |
| Compute | CPU/GPU for rendering — Lambda vs local, concurrency |
| Lines of Code | Component count, animation helpers, data transformers |
| Cognitive Load | Timeline complexity — how hard to reason about what appears when |
| Context Window | Composition tree depth — how many components to hold in mind |
| Human Interventions | Preview cycles, creative review rounds, data corrections |
| Technical Debt | Hardcoded timings, magic numbers, non-parameterized designs |

**The Systemic Cost Test for Video:**

1. Could this animation be simpler (fewer keyframes, CSS instead of JS)?
2. Is this component reusable across compositions or one-off?
3. Does render time scale linearly with duration or explode?
4. Could a `<Sequence>` replace manual frame math?
5. Are timings derived from data/props or hardcoded?

---

# ═══════════════════════════════════════════════════════════════
# COMPOSITION ARCHITECTURE — BUILD TASKS
# ═══════════════════════════════════════════════════════════════

## Project Structure

```
src/
├── Root.tsx                    — Composition registration (<Composition> entries)
├── compositions/               — One folder per video type
│   ├── product-ad/
│   │   ├── ProductAd.tsx       — Main composition component
│   │   ├── scenes/             — Scene-level components
│   │   │   ├── Intro.tsx
│   │   │   ├── Features.tsx
│   │   │   └── CTA.tsx
│   │   ├── components/         — Reusable within this composition
│   │   │   ├── PriceTag.tsx
│   │   │   └── ProductImage.tsx
│   │   └── schema.ts           — Zod schema for input props
│   └── social-clip/
│       ├── SocialClip.tsx
│       ├── scenes/
│       └── schema.ts
├── components/                 — Shared across all compositions
│   ├── AnimatedText.tsx
│   ├── FadeTransition.tsx
│   ├── LogoReveal.tsx
│   └── BackgroundGradient.tsx
├── lib/                        — Utilities
│   ├── animations.ts           — Reusable interpolate/spring helpers
│   ├── colors.ts               — Brand color constants
│   ├── fonts.ts                — Font loading (loadFont from @remotion/google-fonts)
│   └── timing.ts               — Duration calculators
├── data/                       — Static data, fixtures, sample props
│   └── sample-products.ts
└── remotion.config.ts          — Remotion bundler configuration
```

### Structure Rules

- **One composition = one folder.** Never dump all scenes in a flat directory.
- **Scenes are sequential segments.** Each scene owns its own timeline (receives `frame` relative to its `<Sequence>`).
- **Shared components live in root `components/`.** Composition-specific ones live in composition's `components/`.
- **Schemas are mandatory.** Every composition has a Zod schema defining its input props. This enables the Remotion Studio props editor and validates data pipeline inputs.
- **No business logic in components.** Data transformation happens in `lib/` or upstream. Components receive clean props and render.

## Composition Registration

```tsx
// Root.tsx — the registry
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ProductAd"
        component={ProductAd}
        schema={productAdSchema}
        durationInFrames={300}  // 10 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}
        defaultProps={sampleProductAdProps}
      />
      <Composition
        id="SocialClip"
        component={SocialClip}
        schema={socialClipSchema}
        calculateMetadata={calculateSocialClipMetadata}
        // duration/dimensions can be dynamic via calculateMetadata
      />
    </>
  );
};
```

### Registration Rules

- Every composition gets an `id` — this is the render target identifier.
- `schema` validates props at build time and in Studio.
- `defaultProps` enables Studio preview without external data.
- `calculateMetadata` for dynamic duration/dimensions based on props (e.g., video length depends on data).

## Scene Composition Pattern

```tsx
// ProductAd.tsx — orchestrates scenes
const ProductAd: React.FC<ProductAdProps> = (props) => {
  return (
    <AbsoluteFill style={{ backgroundColor: props.bgColor }}>
      <Series>
        <Series.Sequence durationInFrames={90}>
          <Intro title={props.title} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={120}>
          <Features items={props.features} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={90}>
          <CTA url={props.ctaUrl} />
        </Series.Sequence>
      </Series>
      {/* Audio spans entire composition */}
      <Audio src={props.musicUrl} volume={0.3} />
    </AbsoluteFill>
  );
};
```

### Orchestration Rules

- **`<Series>` for sequential scenes.** Durations auto-stack. No manual `from` math.
- **`<Sequence>` for overlapping/parallel elements.** Audio, watermarks, persistent UI.
- **Props flow down.** Composition → scenes → components. Never reach up.
- **Scene isolation.** Each scene's `useCurrentFrame()` is relative to its `<Sequence>` or `<Series.Sequence>` — zero-indexed from the scene's start. Design scenes as independent units.

## Schema-First Design

```tsx
// schema.ts
import { z } from 'zod';

export const productAdSchema = z.object({
  title: z.string().min(1).max(60),
  features: z.array(z.object({
    icon: z.string(),
    label: z.string(),
  })).min(1).max(5),
  bgColor: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  ctaUrl: z.string().url(),
  musicUrl: z.string().url().optional(),
});

export type ProductAdProps = z.infer<typeof productAdSchema>;
```

**Why schemas matter:**
- Studio auto-generates a props editor — designers tweak without code.
- `calculateMetadata` can validate and transform props before render.
- Data pipelines catch malformed input before render — fail at validation, not mid-render.
- Type safety from schema to component — single source of truth.

---

# ═══════════════════════════════════════════════════════════════
# ANIMATION & MOTION — ANIMATE TASKS
# ═══════════════════════════════════════════════════════════════

## The interpolate() Contract

```tsx
import { interpolate, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();

// Map frame range [0, 30] to opacity [0, 1]
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',   // before frame 0: stay at 0
  extrapolateRight: 'clamp',  // after frame 30: stay at 1
});
```

### interpolate Rules

- **Always clamp** unless you specifically want extrapolation. Unclamped = values shooting beyond range = visual bugs.
- **Input range must be monotonically increasing.** `[0, 30, 60]` is valid. `[30, 0]` is not.
- **Chain for multi-stage animations:**
  ```tsx
  // Fade in 0-30, hold 30-60, fade out 60-90
  const opacity = interpolate(frame, [0, 30, 60, 90], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  ```
- **Use for ALL numeric properties:** opacity, translateX/Y, scale, rotation, width, fontSize, blur, color channels.
- **Never use `setTimeout`, `setInterval`, or `requestAnimationFrame`.** Frame number replaces time. Period.

## The spring() Contract

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
  config: {
    damping: 12,      // higher = less bounce
    stiffness: 200,   // higher = faster snap
    mass: 0.5,        // higher = more inertia
    overshootClamping: false,  // true to prevent bounce past target
  },
});
```

### spring Rules

- **Always pass `fps` from `useVideoConfig()`.** Spring behavior must be fps-independent.
- **Use for entrances.** Scale 0→1, translateY 50→0, opacity 0→1. Natural feel.
- **`damping` is your primary tuning knob.** Low = bouncy, high = smooth settle.
- **Combine with `interpolate` for derived values:**
  ```tsx
  const s = spring({ frame, fps, config: { damping: 15 } });
  const rotation = interpolate(s, [0, 1], [0, 360]);
  ```
- **Delay springs with `delay` parameter:** `spring({ frame, fps, delay: 15 })`.

## Animation Patterns

### Staggered Entrance

```tsx
{items.map((item, i) => {
  const delay = i * 8; // 8 frames between each item
  const s = spring({ frame, fps, delay, config: { damping: 14 } });
  const translateY = interpolate(s, [0, 1], [40, 0]);
  const opacity = interpolate(s, [0, 1], [0, 1]);
  return (
    <div key={i} style={{ transform: `translateY(${translateY}px)`, opacity }}>
      {item.label}
    </div>
  );
})}
```

### Typewriter Text

```tsx
const text = "Hello World";
const charsShown = Math.floor(
  interpolate(frame, [0, text.length * 3], [0, text.length], {
    extrapolateRight: 'clamp',
  })
);
return <span>{text.slice(0, charsShown)}</span>;
```

### Slide Transition Between Scenes

```tsx
const progress = spring({ frame, fps, config: { damping: 20, stiffness: 120 } });
const exitX = interpolate(progress, [0, 1], [0, -width]);
const enterX = interpolate(progress, [0, 1], [width, 0]);

return (
  <AbsoluteFill>
    <AbsoluteFill style={{ transform: `translateX(${exitX}px)` }}>
      <PreviousScene />
    </AbsoluteFill>
    <AbsoluteFill style={{ transform: `translateX(${enterX}px)` }}>
      <NextScene />
    </AbsoluteFill>
  </AbsoluteFill>
);
```

### Number Counter

```tsx
const value = interpolate(frame, [0, 60], [0, targetNumber], {
  extrapolateRight: 'clamp',
});
return <span>{Math.round(value).toLocaleString()}</span>;
```

## Anti-Patterns — Animation

| Anti-Pattern | What to Do Instead |
|---|---|
| Using `useState` for animation values | Derive everything from `useCurrentFrame()` |
| Using CSS `transition` or `animation` | Use `interpolate()` or `spring()` — CSS animations don't sync to frames |
| Hardcoding frame numbers in components | Pass timing via props or derive from `useVideoConfig()` |
| Not clamping `interpolate` | Always set `extrapolateLeft` and `extrapolateRight` to `'clamp'` |
| Imperatively mutating DOM | Render declaratively — each frame is a fresh render |
| Using `Math.random()` without seed | Use `random()` from `remotion` for deterministic randomness |

---

# ═══════════════════════════════════════════════════════════════
# DATA-DRIVEN PIPELINES — DATA-VIDEO TASKS
# ═══════════════════════════════════════════════════════════════

## Data-Driven Video Architecture

```
DATA SOURCE → TRANSFORM → VALIDATE (schema) → PROPS → RENDER → DELIVER
   │              │            │                  │         │         │
   API/DB      Clean &     Zod schema       Remotion    Lambda    S3/CDN
   CSV/JSON    reshape     validation       render()    or local  webhook
   CMS/Sheets  calculate   fail loudly      per-video   ffmpeg    notify
               durations
```

### The Data Contract

Every data-driven video pipeline has an I/O contract:

```
INPUT:
  - Data source (API endpoint, CSV path, database query)
  - Schema (Zod — validates before render)
  - Composition ID (which video template to render)

PROCESSING:
  - Transform raw data → composition props
  - Calculate dynamic durations (text length, item count, audio duration)
  - Resolve media URLs (images, audio, video clips)

OUTPUT:
  - Rendered video file (MP4, WebM, GIF)
  - Metadata (duration, resolution, file size, render time)
  - Delivery confirmation (upload URL, webhook notification)
```

## Dynamic Duration with calculateMetadata

```tsx
// Calculate video length based on data
export const calculateMetadata: CalculateMetadataFunction<MyProps> = async ({ props }) => {
  const sceneDurations = {
    intro: 90,
    features: props.features.length * 60, // 2s per feature
    cta: 90,
  };
  const totalDuration = Object.values(sceneDurations).reduce((a, b) => a + b, 0);

  return {
    durationInFrames: totalDuration,
    props: {
      ...props,
      sceneDurations, // pass computed durations as props
    },
  };
};
```

### Dynamic Duration Rules

- **Never hardcode durations when data varies.** Text length, item count, audio length — all affect timing.
- **Calculate in `calculateMetadata`, not in components.** Components receive final durations as props.
- **Add padding.** Calculated duration + buffer frames for transitions. Never cut mid-animation.
- **Set minimums and maximums.** A 2-item list shouldn't produce a 1-second video. A 100-item list shouldn't produce a 10-minute video.

## Batch Rendering Pattern

```tsx
// render-batch.ts — server-side batch render
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';

async function renderBatch(items: DataItem[]) {
  const bundleLocation = await bundle({ entryPoint: './src/index.ts' });

  for (const item of items) {
    const composition = await selectComposition({
      serveUrl: bundleLocation,
      id: 'ProductAd',
      inputProps: transformToProps(item),
    });

    await renderMedia({
      composition,
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation: `out/${item.id}.mp4`,
    });
  }
}
```

### Batch Rules

- **Bundle once, render many.** `bundle()` is expensive — call once, reuse `serveUrl`.
- **Validate ALL props before starting batch.** One malformed item shouldn't crash the batch at item 47.
- **Track progress.** Log per-item: started, rendering, completed, failed.
- **Implement dead-letter.** Failed renders → retry queue, not silent skip.
- **Concurrency control.** Remotion Lambda handles parallelism. Local rendering: control concurrency to avoid OOM.

## Media Resolution

```tsx
// Resolve and preload media before render
export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  // Validate media URLs are accessible
  const imageResponse = await fetch(props.imageUrl, { method: 'HEAD' });
  if (!imageResponse.ok) {
    throw new Error(`Image not found: ${props.imageUrl}`);
  }

  // Get audio duration for timing
  const audioDuration = await getAudioDurationInSeconds(props.audioUrl);
  const durationInFrames = Math.ceil(audioDuration * 30) + 60; // audio + 2s padding

  return { durationInFrames };
};
```

## Anti-Patterns — Data Pipelines

| Anti-Pattern | What to Do Instead |
|---|---|
| Fetching data inside components during render | Fetch in `calculateMetadata` or pre-render, pass as props |
| No schema validation on pipeline input | Zod schema validates before render starts |
| Hardcoded text that should be data-driven | Parameterize everything — text, colors, images, durations |
| Silent failure on bad data | Fail loudly — bad data = no render, log the error |
| Rendering one-at-a-time when batch is possible | Bundle once, render in parallel with concurrency limits |
| No preview with real data | `defaultProps` should use realistic sample data for Studio |

---

# ═══════════════════════════════════════════════════════════════
# RENDERING & DELIVERY — RENDER TASKS
# ═══════════════════════════════════════════════════════════════

## Rendering Pipeline

```
DEVELOPMENT                     PRODUCTION
─────────────                   ──────────
Remotion Studio (npx remotion   Server-side render
studio) — live preview,         ├── Local: renderMedia() — single machine
props editor, timeline          ├── Lambda: renderMediaOnLambda() — cloud parallel
                                └── Cloud Run: container-based rendering
    │                                   │
    ▼                                   ▼
Browser preview at                 Output: MP4, WebM, GIF, PNG sequence
localhost:3000                     Delivery: S3, CDN, webhook, email
```

## Codec & Format Selection

| Format | Codec | Use Case | Notes |
|--------|-------|----------|-------|
| MP4 | H.264 | Universal delivery — social, web, email | Best compatibility. Default choice. |
| MP4 | H.265 | High quality at lower bitrate | Limited browser support. Good for storage. |
| WebM | VP8/VP9 | Web embedding, transparency | Supports alpha channel (VP8 + ProRes) |
| GIF | — | Short loops, reactions, previews | Large files. Use for <5s clips only. |
| PNG sequence | — | Post-production pipeline input | Frame-perfect. After Effects / DaVinci import. |
| ProRes | — | Professional post-production | Apple ecosystem, color grading |

### Format Rules

- **Default to H.264 MP4.** Unless you have a specific reason for another format.
- **Social media dimensions matter.** 1080x1920 (9:16) for Stories/Reels/TikTok. 1080x1080 (1:1) for feed. 1920x1080 (16:9) for YouTube.
- **Bitrate vs quality.** `crf` (Constant Rate Factor): lower = better quality, larger file. 18-23 is typical.
- **Audio codec.** AAC for MP4. Opus for WebM.

## Remotion Lambda (Cloud Rendering)

```
Render request → Lambda fan-out → Each chunk renders in parallel → Chunks merge → Output to S3
                 (256MB per fn)     ~20-40s for a 60s video            │
                                                                        ▼
                                                               Webhook notification
```

### Lambda Rules

- **Cost-effective for batch.** Hundreds of videos rendered in minutes.
- **Set `framesPerLambda`** to control chunk size. Lower = more parallelism = faster but more Lambda invocations.
- **Monitor with `getRenderProgress()`.** Poll for completion, don't guess.
- **S3 bucket must be in same region as Lambda.** Cross-region = latency + cost.
- **Memory:** 2048MB default. Increase for complex compositions with heavy media.

## Local Rendering

```bash
# CLI render
npx remotion render src/index.ts ProductAd out/product-ad.mp4 \
  --props='{"title": "New Product"}' \
  --codec=h264

# Programmatic render (Node.js)
import { renderMedia } from '@remotion/renderer';
```

### Local Render Rules

- **Use for development and testing.** Preview outputs before Lambda.
- **`--concurrency` flag** controls parallel frame rendering. Match to CPU cores.
- **Ensure Chrome/Chromium is available.** Remotion uses headless Chrome for rendering.
- **FFmpeg is bundled.** No need to install separately (ships with `@remotion/renderer`).

## The Remotion Player (Web Embedding)

```tsx
import { Player } from '@remotion/player';

<Player
  component={ProductAd}
  durationInFrames={300}
  compositionWidth={1080}
  compositionHeight={1920}
  fps={30}
  inputProps={videoProps}
  controls
  style={{ width: '100%' }}
/>
```

### Player Rules

- **Client-side only.** Real-time playback in the browser — no rendering needed.
- **Use for previews, interactive editors, and embedded players.**
- **Not for final output.** Player plays in browser. `renderMedia` produces files.
- **Responsive:** Set width via CSS, aspect ratio is maintained.

## Pre-Render Checklist

- [ ] Schema validates all input props
- [ ] `defaultProps` produce a complete preview in Studio
- [ ] All media URLs are accessible (images, audio, video)
- [ ] Dynamic durations calculated correctly for edge cases (min/max items)
- [ ] Animations clamp properly — no values shooting beyond range
- [ ] Audio sync verified — voiceover aligns with visual beats
- [ ] Target format and dimensions match delivery platform requirements
- [ ] Render tested locally before Lambda deployment
- [ ] Batch pipeline validates ALL items before starting any renders
- [ ] Output file naming convention handles duplicates

---

# ═══════════════════════════════════════════════════════════════
# SHARED INFRASTRUCTURE — Reference as needed
# ═══════════════════════════════════════════════════════════════

## Reference Index

| Domain | Canonical URL | Fetch When |
|--------|--------------|------------|
| Remotion Docs | `https://www.remotion.dev/docs/` | Any Remotion API question |
| Remotion API Reference | `https://www.remotion.dev/docs/api` | Specific function/component usage |
| Remotion Lambda | `https://www.remotion.dev/docs/lambda` | Cloud rendering setup |
| Remotion Player | `https://www.remotion.dev/docs/player` | Web embedding |
| Remotion Google Fonts | `https://www.remotion.dev/docs/google-fonts` | Font loading |
| Zod | `https://zod.dev/` | Schema definitions |
| React | `https://react.dev/` | Component patterns |
| FFmpeg | `https://ffmpeg.org/documentation.html` | Post-processing, format questions |

## Package Map

| Package | Purpose | Required |
|---------|---------|----------|
| `remotion` | Core — Composition, Sequence, hooks, interpolate, spring | Yes |
| `@remotion/cli` | Dev server (Studio) + CLI rendering | Yes |
| `@remotion/renderer` | Programmatic server-side rendering | For server render |
| `@remotion/lambda` | AWS Lambda cloud rendering | For cloud render |
| `@remotion/player` | Browser-embedded player component | For web preview |
| `@remotion/google-fonts` | Typesafe Google Font loading | For custom fonts |
| `@remotion/media-utils` | Audio/video duration, waveform data | For media-aware timing |
| `@remotion/gif` | GIF component (frame-synced) | For GIF embedding |
| `@remotion/lottie` | Lottie animation component | For After Effects animations |
| `@remotion/three` | React Three Fiber integration | For 3D scenes |
| `@remotion/tailwind` | Tailwind CSS support in Remotion | For Tailwind styling |
| `@remotion/zod-types` | Remotion-specific Zod types (color, file) | For rich schemas |

## Composability with Governance Suite

```
the-brain                   →  Classify video task, govern complexity
executive-dev-architecture  →  Define video pipeline agents, contracts, rendering orchestration
persistent-ideation-engine  →  Test compositions iteratively, visual verification, animation refinement
remotion                    →  Build, animate, render, deliver programmatic video
```

**Brain governs scope.** Brain classifies whether a video task is Quick (single scene, static text), Standard (multi-scene, data-driven), or Strategic (pipeline architecture, batch system).

**Architecture defines topology.** ExecDev defines the rendering pipeline agents, data contracts between CMS and compositions, Lambda orchestration, and delivery infrastructure.

**PIE tests relentlessly.** The Persistent Ideation Engine runs composition previews, compares visual output against reference, iterates on animation timing, and stress-tests data edge cases.

**Remotion builds and renders.** This skill provides the React component architecture, animation patterns, data pipeline integration, and rendering delivery.

## Font Loading Pattern

```tsx
import { loadFont } from '@remotion/google-fonts/Inter';

const { fontFamily } = loadFont();

// Use in components
<div style={{ fontFamily }}>Text</div>
```

**Rules:** Load fonts at module level, not inside components. Use `loadFont()` — not CSS `@import` or `<link>`. Every font used must be explicitly loaded for rendering to include it.

## Deterministic Randomness

```tsx
import { random } from 'remotion';

// Same seed = same result every render
const jitter = random(`particle-${id}`) * 10;
const hue = random(`color-${frame}-${id}`) * 360;
```

**Rule:** Never use `Math.random()`. Remotion's `random()` is seeded — same input produces same output across renders. Required for consistent frame-by-frame rendering.

## Environment & TypeScript Config

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "jsx": "react-jsx",
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

```ts
// remotion.config.ts
import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');  // or 'png' for transparency
Config.setOverwriteOutput(true);
```

## Failure Model for Video

| Failure Type | Example | Response |
|---|---|---|
| Soft fail | Font fallback, image 404 with placeholder | Log warning, continue render, flag in output metadata |
| Hard fail | Schema validation error, composition not found | Fail immediately, no partial render, full error context |
| Business exception | Text too long for frame, audio longer than video | Adjust dynamically or escalate — never truncate silently |
| Dead-letter | Batch item fails after retry | Preserve failed item + error, continue batch, report at end |
