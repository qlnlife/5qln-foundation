# Roadmap

Five phases. Each gated. Phase N+1 cannot start until Phase N's gate clears.

## Phase sequencing

| Phase | Engineer-weeks | Predecessors | Gate criteria |
|---|---|---|---|
| **Phase 0** — Seal Codex | 2 | — | All 11 done-gates pass (see [`phases/PHASE_0_SEAL.md`](phases/PHASE_0_SEAL.md)) |
| **Phase 1** — Compiler | 4 | Phase 0 sealed | Reproducible build; cross-validation (TS vs Rust manifests match); property tests green |
| **Phase 2** — Audit + Realignment | 3 | Phase 1 predicate hash | `qlnlife/5qln-core` PR merged; hashes recomputed; all tests green |
| **Phase 3** — Interrogator | 4 | Phase 1 predicate hash | Three soft templates hashed and pinned; verdict log append-only verified; drift baseline established |
| **Phase 4** — Write Gate | 5 | Phase 2 & 3 complete | Write-gate API live; lineage walker traces sample cycles; one verifier-passing cycle end-to-end |
| **Total to first verifier-passing cycle** | **~18 weeks** | | |

## Critical path

```
Phase 0 → Phase 1 → Phase 4
```

Phase 2 and Phase 3 parallelise after Phase 1.

## Parallelisation

- Phase 2 (audit) and Phase 3 (Interrogator) run concurrently after Phase 1
- AOSRAP wrapper (10-week separate spec) parallelises with Phase 3
- Skill suite (Layer A) parallelises with Phase 4
- Plugin protocol and translation surfaces wait for Phase 4 completion

## Hard sequencing (cannot be parallelised)

- Phase 1 cannot start until Phase 0's Codex hash is published — the compiler's input must be sealed
- Phase 4 cannot start until Phase 3's verdict log schema is signed — the write-gate references it
- Federation work (BIPP, multi-jurisdiction) cannot start until Phase 4 is producing verifier-passing cycles

## Minimum viable Phase 0 ceremony (this week)

- **Day 1:** Produce `codex.txt`; run all three verifiers locally; confirm byte identity ← *done in this repo*
- **Day 2:** Provision YubiHSM 2 primary and cold-storage; generate Ed25519 keypair; publish public-key fingerprint
- **Day 3:** Cross-verify hash on a clean USB-booted Linux and a sandboxed CI runner
- **Day 4:** Convene witnesses (2 human + 1 AI cross-substrate attestor); each signs the manifest
- **Day 5:** Obtain RFC 3161 timestamps from FreeTSA + DigiCert; finalise manifest; Conductor signs
- **Day 6:** Publish to canonical URL, push GitHub tag `codex-v1`, pin to IPFS (2+ providers), submit Sigstore Rekor entry
- **Day 7:** Publish Phase 0 done-gates checklist with all green; emit Tier-A "Codex sealed" gliff

## Benchmarks that change recommendations

- **Phase 0 cannot seal within 14 days:** the gate is operator availability, not engineering. Restructure the ceremony around the operator's calendar
- **Phase 1 cannot produce reproducibly-built predicate sets across two machines within 8 weeks:** toolchain pinning is the bottleneck — drop Rust, ship TypeScript-only v1
- **Phase 4 cannot produce a verifier-passing cycle within 90 days of Phase 1 completion:** the architecture is over-scoped — apply the Subtraction Principle
- **AOSRAP vendor RFIs return null after 12 months:** freeze Phase 2 entry of Foundation Build Plan; extend manual attestation fallback indefinitely
