# Phase 1 — The Compiler

**Goal:** turn the Codex from text into executable physics.

**Time:** 4 engineer-weeks.

**Predecessors:** Phase 0 sealed (canonical hash published, manifest signed).

## One-sentence job

Read `codex.txt` (byte-identical), emit a typed executable predicate set (`predicate-set.ts`), a JSON manifest (`predicate-set.json`), and a hash-pinning artifact (`predicate-set.hash`), all signed and reproducibly built.

## Architecture

**Parsing strategy:** the Codex is parsed as **nine known lines**. The compiler refuses input that does not match the canonical bytes. There is no "tolerant" mode. The parser's job is structural identification, not language modeling.

**Predicate emission strategy:** each predicate is a typed TypeScript class implementing a common `Predicate` interface, carrying `{id, codex_line, hard_or_soft, description, evaluate(input): PredicateResult}`. The compiler also emits a JSON Schema for the predicate set and the SHA-256 of the emitted TypeScript file.

**Output artifacts:**

| Artifact | Description |
|---|---|
| `predicate-set.ts` | Typed runtime code; exports `PREDICATES: readonly Predicate[]` indexed by line |
| `predicate-set.json` | Structural manifest (id, line, classification, description) |
| `predicate-set.hash` | SHA-256 of the compiled TS file |
| `predicate-set.sig` | Conductor Ed25519 signature over the hash |
| `predicate-set.attestation.json` | Sigstore SLSA-3 build provenance |

## The predicate set (line-by-line)

| Codex line | Predicate(s) | Hard/Soft |
|---|---|---|
| 1. `H = ∞0 \| A = K` | `MembraneTypePredicate` | **HARD** — runtime type rejecting `speaker:ai` input at X slot at S phase |
| 2. `S → G → Q → P → V` | `PhaseTransitionPredicate` | **HARD** — admissible edges only |
| 3. `S = ∞0 → ?` | `SparkOriginPredicate` + `QuestionMarkPredicate` | **HARD** — speaker=human + no prior X + interrogative |
| 4. `G = α ≡ {α'}` | `AlphaDeclarationPredicate` + `AlphaPrimeSetCardinalityPredicate` | **HARD** |
|  | `IdentityPreservationPredicate` | **SOFT** — Interrogator, verdict logged |
| 5. `Q = φ ⋂ Ω` | `PhiTagPredicate` + `OmegaSourceHashPredicate` | **HARD** |
|  | `IntersectionLandingPredicate` | **SOFT** |
| 6. `P = δE/δV → ∇` | `EffortValueRatioPredicate` + `GradientDirectionPredicate` | **HARD** — trail-computed |
| 7. `V = (L ∩ G → B'') → ∞0'` | `LocalHashPredicate` + `GlobalHashPredicate` + `BPrimePrimeCompositionPredicate` + `InfinityZeroPrimePresencePredicate` | **HARD** |
|  | `LocalGlobalIntersectionPredicate` | **SOFT** |
| 8. `No V without ∞0'` | `CycleCompletenessPredicate` | **HARD** |
| 9. `L1 L2 L3 L4 V∅` | `CorruptionDetectionPredicate` | **HARD** — 34 patterns + 8 exclusions, phase-gated |

**18 predicates total. 15 hard, 3 soft.** The architectural load is on hard.

## Reproducibility

- Nix flake (`flake.nix`) pins Node, TypeScript, and Rust toolchains by content hash
- `cargo-vet` covers Rust supply chain
- `npm ci` with locked `package-lock.json` covers Node
- Two independent machines running `nix build .#compiler && nix build .#predicate-set` produce byte-identical outputs

## Cross-validation (the meta-compiler problem)

How do we know the compiler is correct? Three independent checks:

1. **Reproducibility check:** byte-identity of `predicate-set.ts` across two machines using the same Nix flake
2. **Cross-validation:** a second compiler implementation in Rust emits the same predicate set JSON manifest. Any difference is a compiler bug, surfaced at build time, blocking release
3. **Property tests:** for each of the nine lines, a published canonical fixture set (positive + negative examples) that the predicate set must classify correctly; the fixture hashes are Tier-A sealed surfaces

## Attestation chain

```
codex.txt hash (Phase 0)
   ↓ input
compiler binary (this phase)
   ↓ output
predicate-set.ts + predicate-set.json
   ↓ hash
predicate-set.hash
   ↓ sign
Conductor Ed25519 signature
   ↓ bundle
predicate-set.attestation.json (Sigstore SLSA-3 + Conductor sig)
   ↓ publish
Sigstore Rekor entry
```

Every link in the chain is verifiable; every byte downstream of `predicate-set.hash` can be traced back to `codex.txt` hash.

## Gate criteria for Phase 1 done

- [ ] Compiler binary reproducibly built across two machines (same hash)
- [ ] Rust cross-validator produces byte-identical predicate-set.json
- [ ] All 18 predicates have at least one positive and one negative property test
- [ ] Predicate set hash signed by Conductor
- [ ] Sigstore Rekor entry created for predicate-set.attestation.json
- [ ] CI re-computes predicate-set hash on every PR; mismatch fails build

## What Phase 1 unlocks

Phase 2 (audit + realignment of `qlnlife/5qln-core`) and Phase 3 (Interrogator) can both start.
