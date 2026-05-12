# Security & Threat Model

## What the architecture defends against

| Attack | Defense |
|---|---|
| AI silently fails to load AI OS Edition | Hash echo on every response (AOSRAP A2) |
| AI drifts from declared phase behavior | Phase-tag enforcement + synthetic probes (AOSRAP A3) |
| Vendor silently changes model weights mid-session | 4-hour synthetic probes fail differently than baseline |
| Operator prompt injection | BreachDetector patterns + Witness scope tagging |
| Tampering with operational record after the fact | Append-only Merkle log; conversation stratum is append-only |
| Substituting a forged Codex | Loader refuses to start under any hash other than canonical (Phase 0) |
| Drift attacks on the canonical bytes | 13 negative tests in `tests/python/test_verify_codex.py` reject every known vector |
| Single-language verifier bug | Three independent implementations (Python, Rust, Node) must agree |
| Single-hash-algorithm break | SHA-256, SHA-512, and BLAKE2b verified together (different families) |
| AI making decisions presented as constitutional | Membrane Protocol P.L.4 hard-blocks: no votes, no binding decisions, no public speech, no surveillance, no ∞0 simulation |
| Conductor key compromise post-seal | RFC 3161 timestamp binds signature to seal-time; revocation does not retroactively un-seal |

## What it explicitly does not defend against

| Attack | Why not | Mitigation |
|---|---|---|
| LLM pattern-matches hash echo without semantically attending | Requires Phase 1 confidential computing or Phase 2 vendor attestation, neither yet available | Use multi-AI consensus; require 2-of-3 for V seal |
| Adversary compromises the wrapper itself | Cannot prove integrity of the thing doing the proving | Reproducible builds + public CI; not eliminated, only mitigated |
| Coordinated failure where LLM passes probes while violating spirit in production | Only repeated operational use surfaces this | Long-term drift monitoring; CIO indicators; Resonance Court for contested cycles |
| Board running cycle vocabulary while making decisions through K-only channels (L4 at scale) | Reproduces conventional governance under 5QLN window-dressing | Architecture makes this *detectable* (CL4-GP indicators), not *impossible* |
| Side-channel attacks on YubiHSM 2 | Hardware-specific; firmware vulnerabilities; physical access | YubiHSM 2 documented threat model; quorum-shared cold backup |
| Long-term cryptographic break | SHA-2 and Ed25519 are state-of-art as of 2026 but not future-proof | BLAKE2b as backup hash family; key rotation policy documented; cycles bound by RFC 3161 timestamp |
| Supply-chain attack on toolchain | Nix-pinned reproducible builds reduce surface; `cargo-vet` audits Rust deps | Multi-implementation defense (Python, Rust, Node — three independent supply chains) |

## Honest acknowledgment: soft-predicate dependency

Soft predicates (Identity Preservation, Intersection Landing, Local/Global Intersection) depend on AI judgment. The architecture's mitigation is **not** that the AI is right — it is that the AI's verdict is logged, hashed, replayable on a different AI, and operator-confirmed.

The AI is sensor. The operator is judge.

If you forget which is which, the architecture has failed.

## Drift as a measurable quantity

Drift is not a binary state ("the AI is broken") but a continuous metric: the variance of soft-predicate verdicts on canonical probes over time, per provider/model pair. A drift dashboard publishes weekly variance; spikes trigger CIO review.

Drift has magnitude and direction. The system can tolerate small drift; it cannot tolerate undetected drift.

## Reporting security issues

For vulnerabilities in this repository:

- **DO NOT** open a public issue
- Email the operator: see GitHub profile for `qlnlife`
- Or use GitHub's private security reporting (Security tab → Report a vulnerability)
- Expect acknowledgment within 7 days

For vulnerabilities in the Codex itself (e.g., a semantic flaw in the Nine Invariant Lines, an undocumented drift attack on the canonical form):

- This is a constitutional matter, not a security bug per se
- Follow the V.L.5(b) amendment process documented in [`GOVERNANCE.md`](GOVERNANCE.md)
- Surface the concern publicly at the canonical source of record

## Disclosure policy

This is a **public-good substrate**. Disclosure is the default. The verifier is open-source; the manifest is published; the Sigstore Rekor entry is public; the witness signatures are public; the hash is on multiple mirrors. There is no part of the architecture's correctness that depends on secrecy.

The only secrets are the Conductor's Ed25519 *private* key (on YubiHSM 2, never exported) and any in-flight cryptographic operations. Everything else is open and auditable.
