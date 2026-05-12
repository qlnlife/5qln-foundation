# Documentation Index

## Start here

| You are... | Read |
|---|---|
| First-time visitor | [`../README.md`](../README.md) |
| Reviewing the architecture | [`../ARCHITECTURE.md`](../ARCHITECTURE.md) then [`../specs/MASTER_ARCHITECTURE.md`](../specs/MASTER_ARCHITECTURE.md) |
| Operator planning Phase 0 seal | [`../phases/PHASE_0_SEAL.md`](../phases/PHASE_0_SEAL.md) |
| Engineer building Phase 1 compiler | [`../phases/PHASE_1_COMPILER.md`](../phases/PHASE_1_COMPILER.md) |
| Counsel reviewing the substrate | [`../specs/MASTER_ARCHITECTURE.md`](../specs/MASTER_ARCHITECTURE.md) §1.3, then [`../GOVERNANCE.md`](../GOVERNANCE.md) |
| Security researcher | [`../SECURITY.md`](../SECURITY.md) |
| Auditor verifying the hash | Run `./scripts/seal-phase-0.sh --verify-only` |
| Contributor | [`../CONTRIBUTING.md`](../CONTRIBUTING.md) |

## Core constitutional documents

- [`../codex/codex.txt`](../codex/codex.txt) — the 217 canonical bytes (the constitution itself)
- [`../codex/CANONICAL_FORM.md`](../codex/CANONICAL_FORM.md) — glyph decisions and rationale
- [`../manifest/manifest.json`](../manifest/manifest.json) — the Phase 0 manifest (awaiting ceremony)
- [`../manifest/manifest.schema.json`](../manifest/manifest.schema.json) — JSON Schema locking manifest structure

## Verifiers

- [`../tools/python/verify_codex.py`](../tools/python/verify_codex.py) — Python reference (constant-time, 3 hashes)
- [`../tools/rust/`](../tools/rust/) — Rust implementation (cross-language defense)
- [`../tools/node/verify-codex.mjs`](../tools/node/verify-codex.mjs) — Node implementation
- [`../scripts/seal-phase-0.sh`](../scripts/seal-phase-0.sh) — ceremony helper

## Phase plans

- [`../phases/PHASE_0_SEAL.md`](../phases/PHASE_0_SEAL.md) — seal the Codex (11 gates)
- [`../phases/PHASE_1_COMPILER.md`](../phases/PHASE_1_COMPILER.md) — Codex → predicates
- [`../phases/PHASE_2_AUDIT.md`](../phases/PHASE_2_AUDIT.md) — realign `qlnlife/5qln-core`
- [`../phases/PHASE_3_INTERROGATOR.md`](../phases/PHASE_3_INTERROGATOR.md) — bounded-AI sensor
- [`../phases/PHASE_4_WRITE_GATE.md`](../phases/PHASE_4_WRITE_GATE.md) — conversation-stratum admittance

## Reference materials

External (operator's authoritative site):

- The Codex: https://www.5qln.com/codex/
- Foundation Build Plan: https://www.5qln.com/5qln-foundation-legal-constitutional-governance-system-engineering-build-plan/
- AOSRAP wrapper spec: https://www.5qln.com/aosrap-wrapper-engineering-specification-v0-1/
- Codex as Verifier: https://www.5qln.com/the-codex-as-complete-verifier-of-a-5qln-harness-run/
- Reverse Walk: https://www.5qln.com/exhibit-06-the-reverse-walk/
- AI OS Edition synthesis: https://www.5qln.com/ai-os-edition-legal-governance-operational-synthesis/

Related repository:

- [`qlnlife/5qln-core`](https://github.com/qlnlife/5qln-core) — TypeScript kernel runtime (awaiting Phase 2 realignment)

## File layout

```
5qln-foundation/
├── codex/                 ← THE CONSTITUTION (217 canonical bytes)
├── manifest/              ← Phase 0 manifest + JSON Schema
├── tools/                 ← Three independent verifiers
├── tests/                 ← Verifier test suite (15 tests)
├── specs/                 ← Master Architecture Document v1.0
├── phases/                ← Phase-by-phase build plans
├── predicates/            ← Phase 1 output target (currently empty)
├── kernel/                ← Phase 2 output target (currently empty)
├── interrogator/          ← Phase 3 output target (currently empty)
├── write-gate/            ← Phase 4 output target (currently empty)
├── scripts/               ← Ceremony helper scripts
├── docs/                  ← This index
├── .github/workflows/     ← CI (verify Codex hash on every push)
├── README.md              ← Front door
├── ARCHITECTURE.md        ← 8-layer overview
├── ROADMAP.md             ← Phase sequencing
├── GOVERNANCE.md          ← Amendment process, dispute routing
├── SECURITY.md            ← Threat model
├── CONTRIBUTING.md        ← How to contribute
├── LICENSE                ← Apache 2.0 + Codex addendum
├── flake.nix              ← Reproducible builds
└── .gitignore
```
