# Architecture (overview)

> The full specification is in [`specs/MASTER_ARCHITECTURE.md`](specs/MASTER_ARCHITECTURE.md) (16 sections, ~32k words). This file is the orientation.

## The eight layers

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ L8  GOVERNANCE / FOUNDATION LAYER                                            │
│     V.L.5(b) amendment gate · Schedule C paired editions                     │
│     Resonance Court → Chancery V.L.7(f) · CIO indicators · CBRP              │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (constitutional acts, sealed gliffs)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L7  TRANSLATION SURFACES (downstream projections — never feed back)          │
│     5qln-legal · 5qln-medical · 5qln-education projectors                    │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (regenerable from cycle residue)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L6  PLUGIN / EXTENSION PROTOCOL                                              │
│     Manifest-declared predicate touches · sandbox · install attestation      │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (signed, quota-bounded)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L5  SKILL SUITE                                                              │
│     Layer A kernel skills · Layer B attestation · Layer C topology           │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (operator-facing protocols)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L4  RUNTIME INFRASTRUCTURE                                                   │
│     AOSRAP wrapper · Sigstore Rekor · breach response · BreachDetector       │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (every byte witnessed)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L3  KERNEL + 6 RING FUNCTIONS              [position-in-grammar only]        │
│     Loader │ Witness │ Watcher │ Sealer │ Attestor │ Interrogator            │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (predicate calls)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L2  COMPILER + PREDICATE SET                                                 │
│     codex.txt → predicate-set.ts + predicate-set.json + predicate-set-hash   │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (compile, hash, sign)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L1  SUBSTRATE / CODEX ANCHOR                                                 │
│     codex.txt (217 B UTF-8 LF no BOM) · manifest.json · 3 witness sigs       │
│     Ed25519 (Conductor) · RFC 3161 timestamp · Rekor entry · IPFS CID        │
└──────────────────────────────────────────────────────────────────────────────┘
```

## The two strata

**Dry stratum** — frozen, small, byte-identical worldwide. The Codex, the compiled predicate set, the kernel, the ring functions, the manifest. Verifiable against published hash forever.

**Conversation stratum** — grows without bound. Append-only, hash-chained. Every artifact carries a proof chain `{predicate-id, predicate-hash, codex-hash, ai-verdict-log-id?, parent-hash}` back to the Codex hash.

The boundary between the two strata is enforced by a single write-path API (Phase 4). Nothing enters the conversation stratum except through a dry-stratum predicate.

## The single load-bearing claim

> **Every artifact admitted to the conversation stratum is reproducibly derivable from the sealed Codex by deterministic predicate evaluation; soft predicates use AI only as a witnessed sensor whose verdict is logged but never authoritative.**

If this fails on any byte, the architecture has failed. Every later property (Chancery defensibility, substrate independence, drift detection, federation) is downstream consequence.

## Hard vs soft predicates

| Type | What it is | Drift surface |
|---|---|---|
| **Hard** | Pure runtime, no AI in loop. Type checks, state-machine edges, hash comparisons, phase-gated patterns, trail measures | Zero — only the compilation step from Codex to predicates |
| **Soft** | Runtime + bounded AI sensor (the Interrogator) + operator confirmation. Identity preservation across {α'}, ⋂ landing, L ∩ G genuineness | The AI's calibration, recorded and reviewable. Verdicts logged, replayable on different AI |

**Default to hard.** Soft predicates require written justification per Phase 2 audit. The architecture's verifiability rests on hard predicates carrying the structural load.

## The Membrane

```
H = ∞0 | A = K
```

The pipe `|` is the membrane. The human side holds ∞0 (the not-yet-known, the authentic question). The AI side works K (the known, the recombinable). The runtime enforces this as a **type system**, not a discipline: inputs tagged `speaker: ai` cannot seed X at S phase; the runtime refuses the assignment.

The Membrane is not a layer in the diagram. It is the *event the architecture exists to honor*. The architecture is the negative space around it.

## Further reading

- [`specs/MASTER_ARCHITECTURE.md`](specs/MASTER_ARCHITECTURE.md) — full specification
- [`phases/`](phases/) — phase-by-phase build plans
- [`SECURITY.md`](SECURITY.md) — threat model
- [`GOVERNANCE.md`](GOVERNANCE.md) — amendment process, dispute routing
- [Codex](https://www.5qln.com/codex/) — the canonical text on the operator's site
