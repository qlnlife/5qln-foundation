# Governance

## Three tiers of amendment

| Tier | Scope | Gate |
|---|---|---|
| **Tier 1** | The Constitutional Block (`codex.txt`) — the 217 canonical bytes | **V.L.5(b) tri-condition gate**: (1) unanimous vote of all Directors then in office; (2) contemporaneously documented finding under (A) compliance with applicable law, (B) correction of demonstrable transcription error, or (C) refinement validated by 5QLN open-source community and accepted by consensus at the canonical source of record; (3) compliance with Board-adopted additional procedures. Any failure renders the amendment invalid. |
| **Tier 2** | Ordinary Bylaws | Two-thirds (2/3) of Directors then in office, ≥30 days written notice, per Bylaws V.L.5(a) |
| **Tier 3** | Operational policy | Board majority by resolution |

## Codex versioning

| Event | Trigger | Effect |
|---|---|---|
| v1 → v2 | V.L.5(b) gate passes; new manifest sealed per Phase 0 ceremony | New hash; new manifest; new publication; v1 preserved |
| Backward compatibility | A cycle sealed against v1 remains verifiable against v1 forever; v2 cycles verify against v2 | Verifier accepts `--codex-version` flag; refuses cross-version verdicts silently |
| Documentation edits | Not the canonical bytes | No version bump; no ratification required |

A change to a single byte of `codex.txt` requires the full V.L.5(b) tri-condition gate and a new Phase 0 ceremony.

## Dispute routing

```
                            Dispute arises
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  CIO indicators fire?         │
                  └──────────────┬───────────────┘
                          yes    │    no
                  ┌──────────────┘
                  ▼
        ┌──────────────────────┐         ┌────────────────────────┐
        │ Operational review   │   ───→  │ Routine handling       │
        │ Tier-B record        │         │ (no formal escalation) │
        └──────────────┬───────┘         └────────────────────────┘
                       │ unresolved or contested
                       ▼
        ┌──────────────────────────────────────────┐
        │ Resonance Court convened                 │
        │ Protocol: Z → ? → ∇ → α → Z'             │
        │ 3-5 facilitators external to Board       │
        │ 5QLN-certified                            │
        │ DTBP tracks default_max & hard_max times │
        └──────────────┬───────────────────────────┘
                       │ resolution or hard_max exceeded
                       ▼
        ┌──────────────────────────────────────────┐
        │ Chancery V.L.7(f)                         │
        │ Sole and exclusive external forum for:    │
        │  - derivative actions                      │
        │  - fiduciary-duty claims                   │
        │  - DGCL-arising claims                     │
        │  - internal-affairs-doctrine claims        │
        │ Chancery bypass:                           │
        │  - 2+ Phase Circle Representatives qualify │
        │  - DTBP hard_max exceeded                  │
        └──────────────────────────────────────────┘
```

## CIO indicators

The Final Blueprint lists 12 indicators currently labeled **[SPECULATIVE]** pending Phase-2 calibration:

1. Excessive AI verdict UNCERTAIN rate
2. Soft-predicate drift variance >5% over 30 days
3. Membrane breach pattern frequency
4. Cycle close failure rate
5. Witness signature delay
6. Plugin write-quota saturation
7. Translation-surface regeneration mismatch
8. Adaptive context chain inconsistency
9. Cross-substrate hash divergence (Schedule C heartbeat)
10. AOSRAP probe failure rate
11. Rekor entry latency
12. Lineage walk depth exceeding threshold

Recommended default: instrument all 12 with logging but do not gate any decisions on them until 6 months of operational data exists.

## The Foundation legal entity vs the substrate

**Important:** as of repository creation, the 5QLN Foundation as a legal entity does not exist. The substrate **predates** the entity.

| Aspect | Status |
|---|---|
| Technical substrate (this repo) | Real, sealed (after Phase 0 ceremony), cryptographically verifiable |
| Foundation legal entity | Does not exist; future Delaware filing |
| Counsel of record | Not yet engaged; Anti Entropy fiscal sponsorship for now |
| Bylaws (Human Edition + AI OS Edition) | Drafted, awaiting ratification |

Pre-incorporation cycles tag claims **`STRUCTURAL-HYPOTHESIS`** (philosophical/architectural) or **`LEGAL-PROSPECTIVE`** (what counsel would likely conclude given the substrate). The verifier records `pre_incorporation: true` until the Delaware Certificate is filed.

Asset transfer from personal/Anti Entropy fiscal sponsorship to the Foundation is a standard pre-formation operational practice and does not require ratification under any current authority.

## Open operator decisions

Documented in [`specs/MASTER_ARCHITECTURE.md`](specs/MASTER_ARCHITECTURE.md) §16:

1. Conductor key rotation policy — *recommended*: cycles verify against key state at seal time; revocation does not retroactively un-seal
2. Public Codex mirror redundancy — *recommended*: monthly Bitcoin OP_RETURN anchor + weekly Internet Archive snapshot
3. Multi-AI consensus threshold — *recommended*: 2-of-3 routine, unanimous for amendments
4. Soft predicate UNCERTAIN threshold — *recommended*: halt and require operator decision after 3 UNCERTAINs on same predicate in one cycle
5. Plugin write quota — *recommended*: 1 write per cycle per plugin
6. CL4-GP indicator calibration — *recommended*: log all 12, gate nothing for 6 months
7. Federation timing — *recommended*: wait until Phase 4 produces ≥30 verifier-passing cycles

## Constitutional notice on this document

This file is engineering-register, Tier-B. It does not carry the Constitutional Block on Page One; it is not itself a compiled 5QLN surface. The Codex governs; this document defers.

Where this conflicts with the Codex, the Codex governs.
