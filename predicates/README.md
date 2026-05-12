# Predicates

This directory will hold the compiled predicate set after Phase 1.

**Status:** Empty pending Phase 0 seal and Phase 1 compiler build.

## What will live here

After Phase 1 runs (see [`../phases/PHASE_1_COMPILER.md`](../phases/PHASE_1_COMPILER.md)), this directory will contain:

| File | Description |
|---|---|
| `predicate-set.ts` | The 18 predicates as typed TypeScript |
| `predicate-set.json` | Structural manifest of predicates |
| `predicate-set.hash` | SHA-256 of `predicate-set.ts`, signed by Conductor |
| `predicate-set.sig` | Conductor Ed25519 signature |
| `predicate-set.attestation.json` | Sigstore SLSA-3 build provenance |

## The 18 predicates

| Codex line | Predicates produced |
|---|---|
| 1 | MembraneTypePredicate (hard) |
| 2 | PhaseTransitionPredicate (hard) |
| 3 | SparkOriginPredicate, QuestionMarkPredicate (both hard) |
| 4 | AlphaDeclarationPredicate, AlphaPrimeSetCardinalityPredicate (hard); IdentityPreservationPredicate (soft) |
| 5 | PhiTagPredicate, OmegaSourceHashPredicate (hard); IntersectionLandingPredicate (soft) |
| 6 | EffortValueRatioPredicate, GradientDirectionPredicate (both hard) |
| 7 | LocalHashPredicate, GlobalHashPredicate, BPrimePrimeCompositionPredicate, InfinityZeroPrimePresencePredicate (hard); LocalGlobalIntersectionPredicate (soft) |
| 8 | CycleCompletenessPredicate (hard) |
| 9 | CorruptionDetectionPredicate (hard) |

**15 hard + 3 soft.** The architectural load is on hard.

See the master architecture (§3) for full specifications.
