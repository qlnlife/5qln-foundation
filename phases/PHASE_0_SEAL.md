# Phase 0 — Seal the Codex

> *Until this surface is sealed, every gliff's content-addressing is in a soft state; ship it first.* — 5QLN Foundation Engineering Build Plan

**Goal:** produce the immutable constitutional anchor that every downstream artifact pins itself to.

**Time:** 2 engineer-weeks (one operator + one technical helper). Day-by-day breakdown in [`../ROADMAP.md`](../ROADMAP.md).

## The eleven done-gates

The Phase 0 ceremony is complete when **all eleven** gates are checked.

### Gate 1 — Canonical bytes produced

- [x] `codex/codex.txt` exists
- [x] File is 217 bytes
- [x] UTF-8 encoded, LF only, no BOM, single trailing LF
- [x] All three reference verifiers (Python, Rust, Node) report `byte_identical_to_canonical: true`
- [x] `wc -c codex/codex.txt` returns `217`
- [x] `file -i codex/codex.txt` returns `text/plain; charset=utf-8`

**Status:** ✅ Done in this repository.

### Gate 2 — Hash agreement across three machines

The SHA-256 hash must be reproduced byte-for-byte on three independent machines using independent toolchains.

- [ ] Operator's workstation (Python `hashlib`)
- [ ] Clean USB-booted Linux (coreutils `sha256sum`)
- [ ] Sandboxed CI runner (Node `crypto`)

**Expected hash:** `feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b`

### Gate 3 — YubiHSM 2 primary provisioned

- [ ] YubiHSM 2 device acquired (operator owns)
- [ ] Ed25519 keypair generated **on-device** (private key never exported)
- [ ] Witnessed key-generation ceremony (operator + 1 witness)
- [ ] Generation procedure logged as Tier-B record

### Gate 4 — YubiHSM 2 cold-storage backup

- [ ] Second YubiHSM 2 device acquired
- [ ] Same Ed25519 keypair imported (or quorum-shared via Shamir Secret Sharing)
- [ ] Stored in physically separate location (different building/city)
- [ ] Access logged

### Gate 5 — Conductor public-key fingerprint published

- [ ] Public key extracted from YubiHSM 2
- [ ] Fingerprint computed (SHA-256 of public-key bytes)
- [ ] Published at `5qln.foundation/conductor-keys/v1/` with operator attestation
- [ ] Cosign signature applied to the publication
- [ ] Mirror posted to at least one IPFS pinning service

### Gate 6 — Three witness signatures captured

- [ ] **Witness 1 — human-technical:** Ed25519 signature over manifest hash, using their own key
- [ ] **Witness 2 — human-legal:** Same, from counsel or Anti Entropy fiscal-sponsorship counsel
- [ ] **Witness 3 — AI cross-substrate attestor:** signed attestation that the AI independently re-derived the canonical bytes from the published Codex URL and computed the SHA-256

Each witness:
- runs a different reference verifier (Python, Rust, Node)
- inspects the bytes directly via `xxd codex/codex.txt`
- signs the manifest's `hashes` object after RFC 8785 JCS canonicalisation

### Gate 7 — RFC 3161 timestamps obtained

- [ ] Primary timestamp from FreeTSA (https://freetsa.org/tsr)
- [ ] Backup timestamp from DigiCert (https://timestamp.digicert.com)
- [ ] Both tokens embedded in manifest's `tsa_timestamps` array
- [ ] Tokens verifiable by any party using `openssl ts -verify`

### Gate 8 — Manifest signed

- [ ] Manifest serialised via RFC 8785 JCS canonicalisation
- [ ] Conductor Ed25519 signature applied to canonicalised digest
- [ ] All three witness signatures appended
- [ ] Final manifest hash computed and printed
- [ ] Manifest validates against `manifest/manifest.schema.json`

### Gate 9 — Published at canonical URL

- [ ] `codex/codex.txt` and `manifest/manifest.json` uploaded to `5qln.foundation/codex/v1/`
- [ ] Server configured to return `text/plain; charset=utf-8` with no HTML wrapper
- [ ] HTTPS certificate valid
- [ ] No HTTP redirect chain
- [ ] CDN cache headers permit hash verification (immutable)

### Gate 10 — GitHub tag created

- [ ] Repository pushed to `github.com/qlnlife/5qln-foundation`
- [ ] Tag `codex-v1` created pointing at the canonical bytes
- [ ] Tag is signed (`git tag -s codex-v1`)
- [ ] Release notes published carrying the hash
- [ ] Release artifact uploaded (signed tarball)

### Gate 11 — Sigstore Rekor entry created

- [ ] Rekor entry submitted (public-good instance or private Rekor)
- [ ] Entry contains: SHA-256 of `codex.txt`, Ed25519 Conductor signature, RFC 3161 token
- [ ] Inclusion proof verifiable against Rekor Merkle root
- [ ] IPFS CID computed and pinned to ≥2 providers (web3.storage + self-hosted kubo)
- [ ] Rekor log index recorded in `manifest.json`'s `publication.rekor_log_index`

## What this gates

When all eleven gates pass:

- **Phase 1 becomes legal to start** — the compiler has a sealed input
- The "Codex sealed" gliff is emitted as a Tier-A artifact (parent: this manifest)
- Every subsequent cycle inherits this manifest's hash as its constitutional parent
- A future Chancery clerk can verify the seal using `tools/python/verify_codex.py` and `openssl` alone — no 5QLN-specific tools required beyond the open-source verifier in this repository

## What this does NOT do

- Does not create a Foundation legal entity (that is Delaware filing, Phase 2 of the Foundation Build Plan, separate from this technical Phase 0)
- Does not require notarization (Tier-3 legal-archival, post-incorporation)
- Does not file with NIST CAISI (deferred to post-Phase-4 standards-track posture)
- Does not implement the runtime kernel (Phase 1 onwards)

## Recovery options

If a Conductor key is compromised after seal:

- Past cycles remain valid — they are verified against the key state *at seal time*, bound by RFC 3161 timestamp
- The key is revoked at `5qln.foundation/conductor-keys/v1/revocation/`
- A new key is generated and published
- Future cycles are signed with the new key
- The Codex hash does not change — only the signing identity rotates

## After Phase 0

1. Branch and merge the realignment PR for `qlnlife/5qln-core` (Phase 2 prep)
2. Start the compiler in TypeScript first (Phase 1)
3. Stand up the AOSRAP wrapper in parallel
4. Begin Interrogator template design (Phase 3 prep)
