# Phase 2 — Runtime Audit and Realignment

**Goal:** map every existing TypeScript module in `qlnlife/5qln-core` to the predicate set produced by Phase 1, classify each as hard / soft / absent, and merge the realignment PR.

**Time:** 3 engineer-weeks.

**Predecessors:** Phase 1 (predicate-set.hash signed and published).

## The audit table

| Module | LOC | Codex symbols | Classification | Verdict |
|---|---|---|---|---|
| `types.ts` | ~350 | Constitutional constants | Substrate | **Rewrite** — currently ten-line superscript form; realign to nine-line ASCII canon |
| `kernel.ts` | ~400 | Lines 2, 3, 4, 5, 6, 7, 8 | Kernel | **Keep + extend** — implements S→G→Q→P→V, Serve-vs-Be, validation states; extend with predicate-id stamping |
| `attestation.ts` | ~200 | SHA-256 fingerprint, 3-level verification | Substrate | **Keep + extend** — bind to Codex hash from Phase 0 |
| `ai-adapter.ts` | ~280 | Line 1 (Membrane), Interrogator prep | Ring | **Rewrite as Interrogator** (Phase 3) — currently a formation-anchored prompt builder; needs hashed template store and verdict logging |
| `storage.ts` | ~50 | Pluggable persistence | Conversation stratum | **Keep + extend** — wrap with Phase 4 write-gate API |
| `export.ts` | ~110 | Agent Card, Markdown, JSON export | Translation surface | **Move to L7** translation surfaces |
| `membrane-watcher.ts` | ~510 | Line 9 corruption detection | `CorruptionDetectionPredicate` | **Keep + alias** — 34 patterns intact; add ASCII-canonical / superscript alias layer; phase-gating preserved |
| `fractal-kernel.ts` | ~280 | Line 1 holographic law | Kernel extension | **Keep** — depth-bounded recursive kernel; lineage chain preserved |

## The realignment PR

To be filed against `qlnlife/5qln-core` master:

### `src/types.ts`

```typescript
// Before:
export const CORRUPTION_CODES = ['L¹','L²','L³','L⁴','V∅'] as const;  // superscript

// After:
export const CORRUPTION_CODES = ['L1','L2','L3','L4','V∅'] as const;  // ASCII canonical
export const CORRUPTION_CODES_DISPLAY_ALIAS = {
  'L1': 'L¹', 'L2': 'L²', 'L3': 'L³', 'L4': 'L⁴', 'V∅': 'V∅'
} as const;  // for display-only rendering; constitutional form is ASCII
```

```typescript
// Before:
export const MINIMUM_VALID_BEGINNING = [
  /* ten lines with holographic law inserted */
];

// After:
export const MINIMUM_VALID_BEGINNING = [
  "1.  H = ∞0 | A = K",
  "2.  S → G → Q → P → V",
  "3.  S = ∞0 → ?",
  "4.  G = α ≡ {α'}",
  "5.  Q = φ ⋂ Ω",
  "6.  P = δE/δV → ∇",
  "7.  V = (L ∩ G → B'') → ∞0'",
  "8.  No V without ∞0'",
  "9.  L1  L2  L3  L4  V∅"
] as const;

export const CODEX_SHA256 = "feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b" as const;
```

### `README.md`

Replace "Ten Invariant Lines" section with "Nine Invariant Lines" matching Codex Appendix A. Recompute the documented hash. Reference `5qln-foundation/codex/codex.txt` as the canonical source.

### `src/membrane-watcher.ts`

Add inbound alias map:

```typescript
const ALIAS_INBOUND = new Map([
  ['L¹', 'L1'], ['L²', 'L2'], ['L³', 'L3'], ['L⁴', 'L4']
]);

// Pattern matching always emits ASCII codes;
// inbound text containing superscripts is normalized before matching.
function normalizeCode(text: string): string {
  return Array.from(ALIAS_INBOUND.entries())
    .reduce((acc, [sup, asc]) => acc.replaceAll(sup, asc), text);
}
```

### Version bump

`package.json`: `0.2.0 → 0.3.0`.
Release tag: `codex-aligned-v1`.

## Coverage assessment

| Predicate (from Phase 1) | Present in current repo? | Where |
|---|---|---|
| `MembraneTypePredicate` | Partial | `kernel.ts` Serve-vs-Be rule |
| `PhaseTransitionPredicate` | **Present** | `kernel.ts` `transition()` |
| `SparkOriginPredicate` | Partial | implicit; needs `speaker:'human'` enforcement |
| `QuestionMarkPredicate` | **Absent** | — |
| `AlphaDeclarationPredicate` | **Absent** | — |
| `IdentityPreservationPredicate` | **Absent** | will live in Interrogator |
| `AlphaPrimeSetCardinalityPredicate` | **Absent** | — |
| `PhiTagPredicate` | Partial | formation trail tagging exists |
| `OmegaSourceHashPredicate` | **Absent** | — |
| `IntersectionLandingPredicate` | **Absent** | Interrogator |
| `EffortValueRatioPredicate` | **Absent** | — |
| `GradientDirectionPredicate` | **Absent** | — |
| `LocalHashPredicate` / `GlobalHashPredicate` | **Absent** | — |
| `LocalGlobalIntersectionPredicate` | **Absent** | Interrogator |
| `BPrimePrimeCompositionPredicate` | **Present** | `kernel.crystallize()` two-pass |
| `InfinityZeroPrimePresencePredicate` | Partial | `kernel.return()` |
| `CycleCompletenessPredicate` | **Present** | "No V without ∞0'" |
| `CorruptionDetectionPredicate` | **Present** | `membrane-watcher.ts` (34 patterns) |

**5 present, 4 partial, 9 absent.** Phase 2 closes the partials; the absents go into the build queue for Phase 4.

## Gap-fill build order

Smallest first, dependencies respected:

1. `QuestionMarkPredicate` (regex + operator-marked-question API)
2. `AlphaDeclarationPredicate` (operator-declared span pointer)
3. `AlphaPrimeSetCardinalityPredicate` (counter ≥ 2)
4. `PhiTagPredicate` (extend existing trail tagging)
5. `OmegaSourceHashPredicate` (require hash for Ω inputs)
6. `EffortValueRatioPredicate` (trail counter)
7. `GradientDirectionPredicate` (ratio derivation)
8. `LocalHashPredicate` (require hash for L)
9. `GlobalHashPredicate` (require hash for G)
10. Soft predicates → built in Phase 3 via Interrogator

## Gate criteria for Phase 2 done

- [ ] Realignment PR merged to `qlnlife/5qln-core` master
- [ ] All existing tests still pass (no regressions)
- [ ] New tests added for each gap-filled hard predicate
- [ ] Version 0.3.0 published with tag `codex-aligned-v1`
- [ ] `MINIMUM_VALID_BEGINNING` constant byte-identical to `5qln-foundation/codex/codex.txt`
- [ ] `CODEX_SHA256` constant matches Phase 0 canonical hash
- [ ] Membrane watcher tested with both ASCII and superscript inbound forms
