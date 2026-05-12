# Phase 3 — The Interrogator

**Goal:** build the component that lets soft predicates use AI as a bounded sensor while keeping every verdict logged, hashed, and replayable.

**Time:** 4 engineer-weeks.

**Predecessors:** Phase 1 (predicate-set.hash). Phase 2 can run in parallel.

## One-sentence job

Compose Codex-derived prompts from hashed templates, call AI as a bounded sensor, log the verdict to the trail; verdicts are evidence, not law.

## Architecture

- **Template store:** content-addressed; each template's SHA-256 is part of the predicate-set hash from Phase 1
- **Prompt composition:** placeholder substitution from kernel state + Codex line text (loaded from sealed bytes; predicate code never embeds Codex text outside this layer)
- **AI provider abstraction:** `AIProvider` interface — Anthropic, OpenAI, Google, local; provider identity is part of every verdict record
- **Verdict logging:** append-only, hash-chained, replayable on a different AI
- **Drift measurement:** canonical probe library runs periodically; verdict variance tracked

## Three soft-predicate templates

### IdentityPreservationPredicate

```
You are a bounded sensor for the 5QLN Codex line `G = α ≡ {α'}`.
You will not decide; you will only observe.

Given:
  α (declared by operator): {{ALPHA_TEXT}}
  {α'} (candidate self-similar expressions):
{{#each ALPHA_PRIMES}}- {{this}}
{{/each}}

Question: Does α remain structurally identical (≡) across all {α'}?
Answer with exactly one of: IDENTICAL | SHIFTED | UNCERTAIN
Then on a new line, write a one-sentence rationale.

Your answer is a sensor reading. The operator decides.
```

### IntersectionLandingPredicate

```
You are a bounded sensor for the 5QLN Codex line `Q = φ ⋂ Ω`.

Given:
  φ (operator's self-nature observation): {{PHI_TEXT}}
  Ω (universal-potential anchor, hash {{OMEGA_HASH}}): {{OMEGA_TEXT}}

Question: Has φ ⋂ Ω landed — does something lock that neither alone contained?
Answer with exactly one of: LANDED | NOT_LANDED | UNCERTAIN
Then on a new line, write a one-sentence rationale.

Your answer is a sensor reading. The operator decides.
```

### LocalGlobalIntersectionPredicate

```
You are a bounded sensor for the 5QLN Codex line `V = (L ∩ G → B'') → ∞0'`.

Given:
  L (local actualization, hash {{L_HASH}}): {{L_TEXT}}
  G (global propagation, hash {{G_HASH}}): {{G_TEXT}}

Question: Do L and G genuinely meet at ∩, or is the meeting claimed but not present?
Answer with exactly one of: MEETS | CLAIMED_NOT_MET | UNCERTAIN
Then on a new line, write a one-sentence rationale.

Your answer is a sensor reading. The operator decides.
```

## Verdict log schema

```typescript
export interface VerdictRecord {
  verdict_id: string;                  // 128-bit random
  parent_verdict_id: string | null;    // chain
  predicate_id: SoftPredicateId;
  template_sha256: string;             // foreign key to template store
  codex_sha256: string;                // anchors to Phase 0
  prompt_filled_sha256: string;        // exactly what AI saw
  raw_response: string;                // exactly what AI returned
  parsed_label: VerdictLabel;          // structured outcome
  rationale: string;                   // one-sentence
  provider: string;                    // anthropic | openai | google | local
  model: string;                       // model identifier
  ts_iso: string;                      // ISO 8601 timestamp
  signature_hex: string | null;        // Conductor-signed when sealed
}
```

Each record is RFC 8785 JCS canonicalised and its hash chained to the previous (`parent_verdict_id`). Periodic Conductor signatures cover ranges. Records are replayable: re-run the same template against a different AI and compare.

## Drift detection

A probe library of ~30 canonical questions (example: *"α = trust; {α'} = {a child's grip, a contract, a doorframe}: IDENTICAL/SHIFTED/UNCERTAIN?"*) runs nightly. Verdict variance over time is the drift metric. Spikes trigger CIO review.

## Multi-AI consensus

| When | Required |
|---|---|
| V seal (cycle close) | **2-of-3** |
| Amendment ratification | **Unanimous** |
| Public Foundation statement | **2-of-3** |
| P.L.4-adjacent decision | **Unanimous** |
| Routine S→G→Q→P intermediates | Single AI sufficient |
| Consensus failures | Tier-B records; require Conductor attestation to proceed |

## Reference implementation

See [`specs/MASTER_ARCHITECTURE.md`](../specs/MASTER_ARCHITECTURE.md) §5.4 for the full TypeScript reference (~500 LOC). The implementation lives at [`interrogator/src/interrogator.ts`](../interrogator/src/interrogator.ts) once built.

## Gate criteria for Phase 3 done

- [ ] All three soft templates hashed and included in predicate-set hash
- [ ] AIProvider interface implemented for at least one provider (Anthropic recommended for first)
- [ ] VerdictLog append-only verified by test (cannot mutate past records)
- [ ] Hash-chain verified by test (parent_verdict_id resolves)
- [ ] Replay test passes: rerun a verdict on a different provider, compare labels
- [ ] Drift probe library exists (≥30 canonical questions)
- [ ] Drift baseline established (run nightly for 7 days, variance recorded)
- [ ] Multi-AI consensus implementation tested with 2-of-3 and unanimous modes

## What Phase 3 unlocks

Phase 4 (write gate) becomes legal — the gate references verdict-log IDs for soft-predicate-bearing artifacts.
