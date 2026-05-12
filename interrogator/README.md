# Interrogator

This directory will hold the bounded-AI sensor that mediates soft predicates.

**Status:** Empty pending Phase 3. Full specification at [`../phases/PHASE_3_INTERROGATOR.md`](../phases/PHASE_3_INTERROGATOR.md).

## What the Interrogator does

Composes Codex-derived prompts from hashed templates, calls AI as a bounded sensor, logs the verdict to the trail. Verdicts are **evidence, not law**.

## Three soft predicates

| Predicate | Codex line | Question asked of the AI |
|---|---|---|
| `IdentityPreservationPredicate` | 4 (`G = α ≡ {α'}`) | Does α remain structurally identical across all {α'}? |
| `IntersectionLandingPredicate` | 5 (`Q = φ ⋂ Ω`) | Has φ ⋂ Ω landed — does something lock that neither alone contained? |
| `LocalGlobalIntersectionPredicate` | 7 (`V = (L ∩ G → B'') → ∞0'`) | Do L and G genuinely meet at ∩, or is the meeting claimed but not present? |

Each prompt is a hashed template. The AI's answer is parsed into a structured label (IDENTICAL/SHIFTED/UNCERTAIN, LANDED/NOT_LANDED/UNCERTAIN, MEETS/CLAIMED_NOT_MET/UNCERTAIN) plus a one-sentence rationale.

Every verdict is logged with:
- Template SHA-256 (foreign key)
- Codex SHA-256 (anchors to Phase 0)
- Filled-prompt SHA-256 (exactly what AI saw)
- Raw response (exactly what AI returned)
- Parsed label + rationale
- Provider + model identifier
- Timestamp
- Parent verdict ID (chain)
- Conductor signature (on sealed records)

## The bounded-sensor principle

The AI is a sensor. The operator is a judge. The verdict log is the evidence. If you forget which is which, the architecture has failed.

A reference TypeScript implementation (~500 LOC) is provided in [`../specs/MASTER_ARCHITECTURE.md`](../specs/MASTER_ARCHITECTURE.md) §5.4. It will be built out here in Phase 3.
