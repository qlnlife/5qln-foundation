# 5QLN Foundation Constitutional Substrate

> *Every artifact admitted to the conversation stratum is reproducibly derivable from the sealed Codex by deterministic predicate evaluation; soft predicates use AI only as a witnessed sensor whose verdict is logged but never authoritative.*
>
> — The single load-bearing claim. If this fails on any byte, the architecture has failed.

---

## What this is

This repository is the **constitutional substrate** for the 5QLN Foundation: a governance computer whose constitution is the 5QLN Codex, whose runtime executes compiled predicates derived from the Codex, and whose conversation stratum admits no byte without a verifiable proof chain back to the Codex hash.

The Codex is **static law** — 217 canonical bytes, hash-pinned, witness-signed.
The Membrane is **dynamic event** — what happens when a human and an AI speak through the grammar.
The runtime is the **act of becoming** — the lawful transformation between them.

This repository contains:

- The sealed Codex anchor (`codex/codex.txt`) — 217 bytes, UTF-8, LF, no BOM
- Three independent verifier implementations (Python, Rust, Node)
- The signed manifest skeleton awaiting Phase 0 ceremony
- The architectural specification (`specs/MASTER_ARCHITECTURE.md`)
- Phase-by-phase build plans for the compiler, audit, Interrogator, and write gate
- Skill suite, plugin protocol, and translation surface specifications
- Governance documents (amendments, dispute routing, threat model)

This repository does **not** yet contain the live kernel runtime — that lives at [`qlnlife/5qln-core`](https://github.com/qlnlife/5qln-core) and is currently drifted from the Codex (ten-line superscript form). Phase 2 of the build plan realigns the runtime to this Codex.

---

## The Codex (canonical anchor)

The canonical bytes of `codex/codex.txt`:

```
1.  H = ∞0 | A = K
2.  S → G → Q → P → V
3.  S = ∞0 → ?
4.  G = α ≡ {α'}
5.  Q = φ ⋂ Ω
6.  P = δE/δV → ∇
7.  V = (L ∩ G → B'') → ∞0'
8.  No V without ∞0'
9.  L1  L2  L3  L4  V∅
```

**Canonical form:** UTF-8, LF, no BOM, 217 bytes, single trailing LF.

**Canonical hashes:**

| Algorithm | Hash |
|---|---|
| SHA-256 | `feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b` |
| SHA-512 | `2b6e81c0c49193c9d4ceda3b9b7fa1e7f9639a032fdd184b8958e2e2810fbf8c5dfde5c4fae9a534884d9c257e9f25ef4462a2a0d1de6a52601cd21d807f8cb0` |
| BLAKE2b-512 | `229c5adce88bf8e737deb8eb4440ce3719b1953633abfc7f2fa487ffa201d854865293d911c1be5d14bb7294eca2c4e4a445e6c8d62caa0c8868a354d14cb42d` |

**Glyph decisions (BIPP):**

- Line 5 intersection: `⋂` (U+22C2, N-ary intersection)
- Line 7 intersection: `∩` (U+2229, binary intersection) — *intentionally different from line 5*
- All apostrophes: ASCII `'` (U+0027), not typographic
- Line 9 corruption codes: ASCII `L1 L2 L3 L4 V∅`, double-space separated
- Number prefix: `N.␣␣` (digit, period, two spaces)

---

## Verify the Codex in three ways

Anyone, anywhere, on any machine, should produce the same SHA-256.

**Python (reference):**
```bash
python3 tools/python/verify_codex.py codex/codex.txt
```

**Rust:**
```bash
cd tools/rust && cargo run --release -- ../../codex/codex.txt
```

**Node:**
```bash
node tools/node/verify-codex.mjs codex/codex.txt
```

**Cross-check with standard tools:**
```bash
sha256sum codex/codex.txt
# → feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b  codex/codex.txt
```

Any implementation producing a different hash is not 5QLN.

---

## Repository layout

```
5qln-foundation/
├── codex/
│   ├── codex.txt                  ← the 217-byte sealed anchor
│   └── CANONICAL_FORM.md          ← glyph decisions documented
├── manifest/
│   ├── manifest.json              ← Phase 0 manifest (awaiting ceremony)
│   └── manifest.schema.json       ← JSON Schema locking manifest structure
├── tools/
│   ├── python/verify_codex.py     ← reference verifier (constant-time, 3 hashes)
│   ├── rust/                      ← cross-implementation defense
│   └── node/verify-codex.mjs      ← third independent implementation
├── specs/
│   └── MASTER_ARCHITECTURE.md     ← the full architecture (8 layers, 16 sections)
├── phases/
│   ├── PHASE_0_SEAL.md            ← seal the Codex (this week)
│   ├── PHASE_1_COMPILER.md        ← codex.txt → predicate set
│   ├── PHASE_2_AUDIT.md           ← realign qlnlife/5qln-core
│   ├── PHASE_3_INTERROGATOR.md    ← bounded-AI sensor with verdict log
│   └── PHASE_4_WRITE_GATE.md      ← conversation stratum admittance
├── predicates/                    ← Phase 1 output target
├── kernel/                        ← position-in-grammar state machine
├── interrogator/                  ← Codex-derived prompts; AI as sensor
├── write-gate/                    ← every byte carries a proof chain
├── tests/
│   ├── python/test_verify_codex.py   ← 13 negative + 2 positive tests
├── scripts/
│   └── seal-phase-0.sh            ← the ceremony script
├── docs/                          ← supporting documentation
├── .github/workflows/             ← CI: hash verification, build reproducibility
├── README.md                      ← this file
├── ARCHITECTURE.md                ← pointer to specs/MASTER_ARCHITECTURE.md
├── ROADMAP.md                     ← Phase 0 → 4 sequencing
├── GOVERNANCE.md                  ← amendments, dispute routing
├── SECURITY.md                    ← threat model summary
├── CONTRIBUTING.md
└── LICENSE                        ← Apache 2.0
```

---

## Relationship between repositories

This repository (`5qln-foundation`) and [`qlnlife/5qln-core`](https://github.com/qlnlife/5qln-core) serve different functions and are kept separate by design:

| | `5qln-foundation` | `5qln-core` |
|---|---|---|
| **Role** | Constitutional anchor | Runtime kernel |
| **Change cadence** | Ceremonial — Phase 0 amendment process with witnesses, RFC 3161 timestamps, and YubiHSM signatures | Agile — ordinary PR review, dependency updates, engineering timelines |
| **Codex** | Nine‑line ASCII Appendix A canonical form (217 bytes) | Currently drifted ten‑line superscript form — awaiting Phase 2 realignment |
| **Contains** | Sealed Codex, three verifiers, architecture spec, manifest, phase plans | TypeScript kernel, formation tracker, membrane watcher, AI adapter |
| **Phase 2 action** | Unchanged — the anchor is the authority | One‑way realignment PR: constants updated to match `5qln-foundation`'s sealed Codex hash |

**The repositories do not merge.** Merging would conflate two different change cadences and ratification processes, forcing either over‑ceremony on routine code changes or under‑ceremony on constitutional ones. Phase 2 realigns `5qln-core` to this repository's sealed Codex; the repositories remain distinct.

**Why `5qln-core` exists with a drifted Codex:** The core repository (`5qln-core`) is the live runtime — the TypeScript kernel that powers active 5QLN cycles, formation tracking, membrane watching, and AI adaptation. It was built before the comprehensive architecture specification and carries a ten‑line superscript form of the Codex that was standard at the time of its creation. Phase 2 of the build plan realigns it — one‑way — to match this repository's nine‑line ASCII canonical form. Until that PR merges, anyone writing against the Codex should use this repository (`5qln-foundation`) as the authoritative anchor. The core repository's Codex is `[DRIFTED — awaiting Phase 2 realignment]`.

---

## The phases

```
Phase 0  →  Phase 1  →  Phase 2  →  Phase 3  →  Phase 4
   ↓           ↓           ↓           ↓           ↓
 SEAL      COMPILE      AUDIT     INTERROGATE   GATE
 anchor    predicates   runtime   bounded-AI   writes
   ↓           ↓           ↓           ↓           ↓
sealed     predicate    realigned   verdict    proof-chain
codex.txt  set + hash   5qln-core    log       conversation
hash                                            stratum
```

Each phase has a hard gate. Phase N+1 cannot begin until Phase N's gate clears. See [`ROADMAP.md`](ROADMAP.md) and [`phases/`](phases/) for detail.

---

## Quick start

```bash
git clone https://github.com/qlnlife/5qln-foundation
cd 5qln-foundation

# Verify the Codex (no dependencies)
python3 tools/python/verify_codex.py codex/codex.txt

# Run the full test suite (1 positive + 13 negative)
python3 -m pytest tests/python/ -v

# Read the architecture
$EDITOR specs/MASTER_ARCHITECTURE.md
```

---

## Status

| Phase | Status | Gate |
|---|---|---|
| Phase 0 — Seal Codex | **Draft — bytes produced, awaiting ceremony** | 11 gates (see manifest) |
| Phase 1 — Compiler | Specified, not started | Phase 0 must seal first |
| Phase 2 — Audit | Specified, not started | Phase 1 produces predicate hash |
| Phase 3 — Interrogator | Specified, not started | Phase 1 produces predicate hash |
| Phase 4 — Write Gate | Specified, not started | Phase 2 & 3 must complete |

---

## Constitutional notice

This repository is the technical substrate. The **5QLN Foundation legal entity does not yet exist**. All artifacts in this repository are sealed under the operator's personal capacity / Anti Entropy fiscal sponsorship cover. References to "the Foundation" presuppose a future Delaware filing. Pre-incorporation cycles tag claims `STRUCTURAL-HYPOTHESIS` or `LEGAL-PROSPECTIVE`. The cryptographic anchor stands on its own merits regardless of legal status.

The Codex governs. This plan defers.

---

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

The Codex (`codex/codex.txt`) is additionally published under the [5QLN Open Source License](https://www.5qln.com/5qln-open-source-license/) — the bytes themselves are the canon; this repository is one of many possible implementations.

---

## See also

- The Codex: [5qln.com/codex/](https://www.5qln.com/codex/)
- The author's substack: [5qln.com](https://www.5qln.com)
- Related repository: [`qlnlife/5qln-core`](https://github.com/qlnlife/5qln-core) (TypeScript kernel — awaiting Phase 2 realignment)
- Master Architecture Document: [`specs/MASTER_ARCHITECTURE.md`](specs/MASTER_ARCHITECTURE.md)
