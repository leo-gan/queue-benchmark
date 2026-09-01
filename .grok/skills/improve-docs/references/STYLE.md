# Style guide — docs improvements (README + Dashboard)

Keep it simple. Prefer delete and clarify over decorate.

## Terminology (binding)

| Say | Never say |
|-----|-----------|
| **payload size** (256 B, 4 KiB) for the published size filter | fixture; five leftover type names as if they were different shapes |
| **pattern** as **1P1C**, **4P4C**, **1P4C**, **4P1C** | SPSC, MPMC on the published filter |
| **data type** only as the catalog id (`size_256`, `size_4096`) | fixture, fixtures, fixtureKey, `dataset.fixtures` |

The published axis is how many bytes each queued item is. Experiment 13 showed that 256 B and 4 KiB tell different stories; 512 B / 1 KiB / 2 KiB do not. Use **payload size** in README, Dashboard copy, and findings. Catalog ids stay `type_id` values (`size_256`, `size_4096`). Older folders may still say `message` / `document` (same lengths). Do not keep `fixture*` as an internal alias. Old `configs.json` may still contain `fixtures`; read it as a fallback, write `data_types`.

Do not rank a library on payload size. Every queue in a cell moves the same bytes. Size is the sample, not a score.

---

## Scope of “docs” in this skill

| In scope | Out of scope (unless user expands) |
|----------|-------------------------------------|
| Root `README.md` | Full theory 101–401 rewrite |
| `docs/index.md` storefront (if it drifts from README) | Language runner internals |
| `dashboard/` UI copy, layout, light refactors | New chart libraries, redesign from scratch |
| Short Method/Learn *links* and honesty lines | Re-running full multi-lang benches for prose |

---

## Content style

- **One idea per paragraph.** Prefer tables for role/path matrices **on the site / Dashboard**, not by fattening the root README.
- **User terms:** payload size (256 B, 4 KiB), pattern (1P1C, 4P4C), ops/s, latency, Pareto, baseline. Do not say SPSC or MPMC on the dashboard filter.
- **Never say “fixture”.** The published sample is a **payload size**. The catalog id is a **data type** (`size_256`, `size_4096`). Say that in docs, Dashboard copy, skills, comments, identifiers, and JSON keys. Do not keep `fixture*` as an internal alias “until later.”
- **Avoid in user copy:** fixture, median size (we do not measure payload size as a result), harness (prefer benchmark runner), unexplained IQR/P95.
- **Honesty line** when ranks appear: within one language; cross-lang directional — prefer **one** place (e.g. Statistics / Method), not a second essay block on README.
- **Links:** prefer site paths that match MkDocs nav labels (Dashboard, Learn, Method). Avoid “storefront” / “CTA” wording in user-facing labels.
- **No emoji spam** in product UI; README badges OK.

### Voice

- **Textbook quality for a high-school student.** Complete sentences. One idea, then the reason. Define a term the first time it is not everyday English.
- This Voice section applies to **replies to the user** as well as published copy. A chat explanation is reader-facing.
- No slang (“at 3 a.m.”, “chatty ping”, “get user”).
- No telegraphic fragments (“Keep YAML on disk. Convert once.”). Write the sentence out.
- No unexplained jargon (stream, socket, pickle, gzip) unless the next sentence says what it is.
- **No clipped systems metaphors.** Do not write “pass a handle”, “pointer-bound”, “copy-bound”, “pack collapse”, “size barely moves them”, or “the knee” as if those were ordinary English. First say what the computer does, then what the clocks did. Example: the queue either copies every byte of the message, or it stores a short reference to a message that is already in memory. A larger message then either takes longer (because every byte is copied) or it does not (because only the reference is moved).
- Direct, calm. Not marketing hype (“blazing”, “crush”).
- “We measure …” not “We revolutionize …”.
- **No slogan stacks** under the title (“Same A. Same B. Same C.”).
- **No lede hedges** that argue with imaginary critics (“not marketing microbenchmarks”).

This rule applies to **every** reader-facing surface: replies to the user, Dashboard story cards (Why / Example / Trade-off), experiment YAML, `results.md`, `experiments/PLAN.md`, `docs/experiments/`, Learn pages, README. The Dashboard reads Example and Trade-off from `experiments/*/experiment.yaml` via `sync-experiments.py`.

### README-specific (authoritative)

See **[README_EDITING.md](README_EDITING.md)** — maintainer rejections and preferred section order from live edit prompts. Summary:

| Prefer | Avoid |
|--------|--------|
| Short factual lede | Expanded role “know/want/tasks” on README |
| Compact Who-it-is-for table | Second “How to read the numbers” section without ask |
| Try it → then Quick start | “Full quick start” naming |
| Surgical user-driven edits | Big-bang README rewrites in a cycle without buy-in |

---

## Visual design (Dashboard)

- Stay on existing Material/Google-ish tokens in `index.css` (`--color-blue`, glass panels).
- New UI: reuse `.glass-panel`, `.section-help`, `.tab-btn`, `.badge-*`.
- Help / orientation: one compact strip; dismissible; not a modal maze.
- Do not introduce second font stacks or heavy animation.
- Mobile: respect existing breakpoints (~720px); don’t break sticky header.

---

## Internal implementation

| Rule | Detail |
|------|--------|
| Prefer small diffs | Touch the fewest files that deliver the ranked items |
| No framework churn | Stay on vanilla JS + Chart.js + Vite as today |
| Refactor only if it shrinks | Extract string constants / help HTML when duplicating; don’t rename half of `main.js` |
| localStorage keys | Version suffix if schema changes (`…-v2`); migrate or ignore old |
| Build | `dashboard` Vite build if assets ship via `docs/dashboard`; keep `index.html` source of truth in `dashboard/` |
| Tests | No dashboard unit suite today — smoke-check in browser or `npm run build` if available |

### Complexity budget

- Cycle implements **≤3** ranked items.
- Avoid net +200 LOC unless removing more elsewhere.
- If `main.js` must grow, put new copy in one `ORIENTATION` / `HELP` constant block at top of the UI section.

---

## Cycle discipline (summary)

1. Read `ROLES.md`, `RESEARCH.md`, `README_EDITING.md`, this file — **do not recreate** if present; only amend.
2. Analysis → Plan → Critique plan → Implement ≤3 → Critique implementation → Fix.
3. Stop when wall time for the whole workflow &lt; 1 hour **or** no high-importance items remain.
4. Update the skill + references from what you learned.
5. `/prepare-pr` (docs-only: empty changed langs is OK).

---

## File layout for this skill

```text
.grok/skills/improve-docs/
  SKILL.md
  references/
    ROLES.md
    RESEARCH.md
    STYLE.md
    README_EDITING.md
    CYCLE_LOG.md
```
