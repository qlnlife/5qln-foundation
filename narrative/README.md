# Narrative — The Story of the Substrate

> *Tier-B supporting materials. These documents describe the architecture. They do not govern it. The Codex governs.*

This directory holds the narrative companions to the engineering specification.
Together they form the **narrative triad** — the recommended entry point for
anyone encountering the 5QLN Constitutional Substrate for the first time.

## Reading order

| # | Document | What it is |
|---|---|---|
| 1 | `the-codex-became-physics.md` | Origin story — how the Codex moved from intuition to verifiable substrate |
| 2 | `inside-the-report.md` | Reader's guide to `specs/MASTER_ARCHITECTURE.md` — the 32,000-word spec made approachable |
| 3 | `the-5qln-foundation-substrate.md` | Synthesis — the complete constitutional stack, from dilemma to verification |

## Discipline

These are **Tier-B Structured Records**. That means:

- **They describe, they don't govern.** No constitutional authority derives from
  narrative prose. The Codex, predicates, and manifest are authoritative.
- **Numerical claims are CI-verified.** If an article claims the Codex hash is
  `feaa46b4...`, a CI job confirms it matches `codex/codex.txt` on every commit.
  If they drift, the build fails — bytes win, prose corrects.
- **Epistemic registers are tagged.** Every load-bearing claim carries one of:
  `CODEX-EXTENSION` (pinned to the Codex), `STRUCTURAL-HYPOTHESIS` (architectural
  claim awaiting formalization), `PHENOMENOLOGICAL-ASSERTION` (the human's
  experienced truth, not machine-verifiable).
- **They are mirrored.** The canonical version of each article lives in this repo.
  A mirror is maintained at 5qln.com. Drift between mirror and canonical is a
  signal worth surfacing — pre-incorporation, a weekly comparison check is sufficient.

## What this is NOT

- **Not constitutional authority.** If a narrative article contradicts the Codex,
  the Codex wins — always, immediately, without appeal.
- **Not the only way in.** The quick-start path through `README.md` and
  `ARCHITECTURE.md` remains valid. The narrative triad is a gentler slope.
- **Not frozen.** Tier-B records can be amended through ordinary PR workflow.
  They do not require the V.L.5(b) constitutional amendment gate, Conductor
  signature, or ceremony. Prose improves; the substrate doesn't move.

## Image provenance

The five diagrams in `images/` are mirrored from the Ghost CDN export of
the 5QLN Foundation Substrate article. They are the canonical illustrations
for the three narrative documents.

Each image's SHA-256 is pinned in `images/HASHES.txt`. CI verifies on every
commit that all images match their pinned hashes. Any image swap (intentional
or accidental) must update HASHES.txt and pass the same verification gate.
