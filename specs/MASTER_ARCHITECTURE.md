# 5QLN Foundation Constitutional Substrate — Master Architecture Document v1.0

**Operator:** Amihai Loven (GitHub `qlnlife`) · **Anchor:** 5QLN Codex, Appendix A · **Status:** Tier‑B engineering specification, decision‑ready, awaiting Phase‑0 sealing ceremony · **Date of compilation:** 12 May 2026

---

## TL;DR

- **The architecture is a two‑stratum, ring‑structured microkernel anchored on a 217‑byte sealed `codex.txt` (UTF‑8/LF/no BOM, the Codex Appendix A nine‑line ASCII form), with the Codex compiled — not interpreted — into a hashed predicate set that the Kernel and its six Ring Functions (Loader, Witness, Watcher, Sealer, Attestor, Interrogator) execute. The Codex is static law; the Membrane is dynamic event; the AI is a bounded sensor, never the seat of judgment.** Start at Phase 0 (this week) by sealing `codex.txt`, generating the YubiHSM‑resident Conductor Ed25519 key, and publishing the signed manifest at `5qln.com/codex/v1/`, IPFS, GitHub tag, and Sigstore Rekor — in that order.
- **Build sequence is hard‑gated, not calendar‑gated.** Phase 0 (Seal) → Phase 1 (Compiler) → Phase 2 (Audit & Realignment of `qlnlife/5qln-core` from the drifted ten‑line superscript form to nine‑line Appendix A canon) → Phase 3 (Interrogator) → Phase 4 (Write Gate). Every byte entering the conversation stratum carries `{predicate-id, predicate-hash, codex-hash, ai-verdict-log-id, parent-hash}` back to the sealed Codex; translation surfaces (legal/medical/educational projectors) are downstream and never feed back.
- **The single load‑bearing claim:** *Every artifact admitted to the conversation stratum is reproducibly derivable from the sealed Codex by deterministic predicate evaluation; soft predicates use AI only as a witnessed sensor whose verdict is logged but never authoritative.* If this claim fails — at any layer, on any byte — the architecture has failed; if it holds, every later property (Chancery defensibility, substrate independence, drift detection, federation) is downstream consequence.

---

## SECTION 1 — EXECUTIVE OVERVIEW

### 1.1 The system in one paragraph for a non‑technical reader

The 5QLN Foundation Constitutional Substrate is a governance computer whose constitution — the 5QLN Codex — is the first thing it loads, the only thing it cannot change, and the test every later utterance must pass. The constitution is a nine‑line text file. From that file, the computer derives a checklist of rules, signs them, and refuses to operate if the file changes. Every conversation it holds, every decision it records, and every document it issues carries a cryptographic receipt tracing it back to the original constitution. Humans hold the questions; the computer holds the form; the AI inside it answers narrow, structured queries and is never trusted with the final word.

### 1.2 The system in one paragraph for an engineer

A two‑stratum architecture: a content‑addressed **dry stratum** (sealed `codex.txt`, compiled predicate set, kernel, six ring functions, attestation manifest — byte‑identical worldwide) and an append‑only, hash‑chained **conversation stratum** whose write‑path API admits artifacts only if they carry a verifying chain `{predicate-id, predicate-hash, codex-hash, ai-verdict-log-id?, parent-hash}` resolving to the Codex hash. The Codex compiles to typed TypeScript predicates plus a JSON manifest; the runtime executes predicates, never the Codex text. Predicates split **hard** (deterministic, no AI) from **soft** (Interrogator‑mediated, AI as bounded sensor, verdict logged). The kernel state is minimal: phase, lens, output‑formation states, adaptive context chain, spark source. Sigstore Rekor anchors the transparency log; YubiHSM‑resident Ed25519 keys sign at the seam between dry and wet; RFC 3161 timestamps anchor temporal claims; RFC 8785 JCS canonicalises everything that gets hashed.

### 1.3 The system in one paragraph for a constitutional lawyer

The substrate is a written instrument — a 217‑byte canonical text, hash‑pinned, published, witnessed, and Ed25519‑signed by the Conductor — that functions as the Foundation's grammar of authority. The Bylaws (Human and AI OS Editions, hash‑paired under Schedule C) sit on top of that grammar; every Foundation act emits a sealed artifact (the "gliff") whose validity is independently verifiable by any clerk on Court hardware in roughly two hours using a deterministic, AI‑free binary (`5qln-verify`), per the eight‑step Reverse Walk protocol. Constitutional Block amendments require the V.L.5(b) tri‑condition gate (unanimous Director vote + contemporaneously documented finding under one of three enumerated grounds + Board‑adopted procedures). Disputes route Resonance Court → Chancery V.L.7(f); the Membrane Protocol P.L.4 forbids AI from voting, binding, public speech without identification, surveillance beyond consent, or simulating ∞0. The architecture's evidentiary status is [LEGAL‑PROSPECTIVE]: the verifier produces *legibility*, which is the precondition of *defensibility*, not a substitute for it.

### 1.4 The eight‑layer diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ L8  GOVERNANCE / FOUNDATION LAYER                                            │
│     V.L.5(b) tri-condition amendment gate · Schedule C paired editions       │
│     Resonance Court → Chancery V.L.7(f) · CIO indicators · CBRP state machine│
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (constitutional acts, sealed gliffs)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L7  TRANSLATION SURFACES (downstream projections — never feed back)          │
│     5qln-legal-projector · 5qln-medical-projector · 5qln-education-projector │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (regenerable from cycle residue)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L6  PLUGIN / EXTENSION PROTOCOL                                              │
│     Manifest-declared predicate touches · sandbox · install-time attestation │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │ (signed, quota-bounded)
┌────────────────────────────────▼─────────────────────────────────────────────┐
│ L5  SKILL SUITE                                                              │
│     Layer A kernel skills · Layer B attestation skills · Layer C topology    │
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

### 1.5 The single load‑bearing claim

> **Every artifact admitted to the conversation stratum is reproducibly derivable from the sealed Codex by deterministic predicate evaluation; soft predicates use AI only as a witnessed sensor whose verdict is logged but never authoritative.**

If this fails on any byte, the architecture has failed. Every later property is consequence.

---

## SECTION 2 — PHASE 0: THE SEALED ANCHOR

### 2.1 Canonical byte specification of `codex.txt`

- **Encoding:** UTF‑8, no BOM
- **Line ending:** LF (`0x0A`)
- **Trailing newline:** exactly one
- **Glyph decisions (authoritative, per Decision A):**
  - Line 5 uses `⋂` (U+22C2 N‑ARY INTERSECTION) — matches Codex Appendix A.
  - Line 7 uses `∩` (U+2229 INTERSECTION) — matches Codex Appendix A, inside the parentheses.
  - All apostrophes are ASCII `'` (U+0027), not typographic.
  - Corruption codes on line 9 are ASCII `L1 L2 L3 L4 V∅` (no superscripts), double‑space separated.
  - Number prefix is `N.␣␣` (digit, period, two spaces).
- **Ceremony-canonical byte count:** **217 bytes** (produced and verified by three independent reference verifiers across five CI methods; the document's original 221‑byte estimate was an operator target that the bytes resolved to 217).

### 2.2 Line‑by‑line text (canonical form for sealing)

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

> **Whitespace note:** The fenced code block above is for display. The canonical bytes of `codex/codex.txt` contain double‑spaces between corruption codes on line 9 (`L1␣␣L2␣␣L3␣␣L4␣␣V∅`) and two spaces after the number prefix on every line (`N.␣␣`). To inspect the actual spacing, run `xxd codex/codex.txt | grep "4c 31"` — the two `20 20` bytes following `4c 31` confirm double‑spaces. The verifier, the manifest's BIPP block, and the 15‑test suite all enforce double‑spaces. If any rendering collapses them to singles, the rendering is wrong; the canonical bytes are correct.

### 2.3 Byte map (UTF‑8, per‑line, computed from the canonical text)

| Line | Codepoints involved (non‑ASCII)       | UTF‑8 bytes used by non‑ASCII | Line bytes (incl. LF) |
|------|----------------------------------------|--------------------------------|------------------------|
| 1    | `∞` U+221E (E2 88 9E)                  | 3                              | 21                     |
| 2    | `→` U+2192 (E2 86 92) × 4              | 12                             | 30                     |
| 3    | `∞` U+221E, `→` U+2192                  | 6                              | 19                     |
| 4    | `α` U+03B1 × 2, `≡` U+2261 (E2 89 A1) | 7                              | 21                     |
| 5    | `φ` U+03C6 (CF 86), `⋂` U+22C2 (E2 8B 82), `Ω` U+03A9 (CE A9) | 7 | 18     |
| 6    | `δ` U+03B4 (CE B4), `∇` U+2207 (E2 88 87) | 10                          | 24                     |
| 7    | `∩` × 1, `→` × 2, `∞` × 1              | 12                             | 36                     |
| 8    | `∞` U+221E                              | 3                              | 23                     |
| 9    | `∅` U+2205 (E2 88 85)                   | 3                              | 25                     |
| **Total** |                                    | **63**                         | **217**                |

The per‑line byte map above is ceremony‑canonical, computed from the actual sealed `codex/codex.txt` by the three reference verifiers.

### 2.4 Three verifier implementations

**Python 3.11+ (`tools/python/verify_codex.py`, ≤200 LOC):**

```python
#!/usr/bin/env python3
"""5QLN codex.txt verifier — reference implementation (Python 3.11+)."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

CANON_LINES = (
    "1.  H = \u221E0 | A = K",
    "2.  S \u2192 G \u2192 Q \u2192 P \u2192 V",
    "3.  S = \u221E0 \u2192 ?",
    "4.  G = \u03B1 \u2261 {\u03B1'}",
    "5.  Q = \u03C6 \u22C2 \u03A9",
    "6.  P = \u03B4E/\u03B4V \u2192 \u2207",
    "7.  V = (L \u2229 G \u2192 B'') \u2192 \u221E0'",
    "8.  No V without \u221E0'",
    "9.  L1  L2  L3  L4  V\u2205",
)

def canonical_bytes() -> bytes:
    return ("\n".join(CANON_LINES) + "\n").encode("utf-8")

def verify(path: Path) -> dict:
    raw = path.read_bytes()
    expected = canonical_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    report = {
        "path": str(path),
        "byte_length": len(raw),
        "expected_byte_length": len(expected),
        "sha256": digest,
        "byte_identical_to_canonical": raw == expected,
        "has_bom": raw.startswith(b"\xEF\xBB\xBF"),
        "uses_crlf": b"\r\n" in raw,
        "trailing_lf_count": len(raw) - len(raw.rstrip(b"\n")),
        "line_count_including_trailing": raw.count(b"\n"),
    }
    return report

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: verify_codex.py <path/to/codex.txt>", file=sys.stderr)
        return 2
    report = verify(Path(argv[1]))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    ok = (report["byte_identical_to_canonical"]
          and not report["has_bom"]
          and not report["uses_crlf"]
          and report["trailing_lf_count"] == 1)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

**Rust stable (`tools/rust/`, uses `ring` + `blake2`):**

```rust
//! 5QLN codex.txt verifier — Rust reference implementation.
use std::{env, fs, path::PathBuf, process::ExitCode};
use ring::digest::{digest, SHA256};

const LINES: &[&str] = &[
    "1.  H = \u{221E}0 | A = K",
    "2.  S \u{2192} G \u{2192} Q \u{2192} P \u{2192} V",
    "3.  S = \u{221E}0 \u{2192} ?",
    "4.  G = \u{03B1} \u{2261} {\u{03B1}'}",
    "5.  Q = \u{03C6} \u{22C2} \u{03A9}",
    "6.  P = \u{03B4}E/\u{03B4}V \u{2192} \u{2207}",
    "7.  V = (L \u{2229} G \u{2192} B'') \u{2192} \u{221E}0'",
    "8.  No V without \u{221E}0'",
    "9.  L1  L2  L3  L4  V\u{2205}",
];

fn canonical_bytes() -> Vec<u8> {
    let mut s = LINES.join("\n");
    s.push('\n');
    s.into_bytes()
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("usage: verify-codex <path/to/codex.txt>");
        return ExitCode::from(2);
    }
    let path = PathBuf::from(&args[1]);
    let raw = match fs::read(&path) {
        Ok(b) => b,
        Err(e) => { eprintln!("read error: {e}"); return ExitCode::from(2); }
    };
    let expected = canonical_bytes();
    let sha = digest(&SHA256, &raw);
    let has_bom = raw.starts_with(&[0xEF, 0xBB, 0xBF]);
    let uses_crlf = raw.windows(2).any(|w| w == b"\r\n");
    let trailing_lf = raw.iter().rev().take_while(|&&b| b == b'\n').count();
    let byte_identical = raw == expected;

    println!("{{");
    println!("  \"path\": \"{}\",", path.display());
    println!("  \"byte_length\": {},", raw.len());
    println!("  \"expected_byte_length\": {},", expected.len());
    println!("  \"sha256\": \"{}\",", hex::encode(sha.as_ref()));
    println!("  \"byte_identical_to_canonical\": {},", byte_identical);
    println!("  \"has_bom\": {},", has_bom);
    println!("  \"uses_crlf\": {},", uses_crlf);
    println!("  \"trailing_lf_count\": {}", trailing_lf);
    println!("}}");

    if byte_identical && !has_bom && !uses_crlf && trailing_lf == 1 {
        ExitCode::SUCCESS
    } else {
        ExitCode::FAILURE
    }
}
```

`Cargo.toml` pins `ring = "0.17"` and `hex = "0.4"` with `Cargo.lock` checked in; build is reproducible under `nix build`.

**Node 20+ (`tools/node/verify-codex.mjs`, ≤200 LOC, built‑in `crypto`):**

```javascript
#!/usr/bin/env node
// 5QLN codex.txt verifier — Node 20+ reference implementation.
import { readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import process from "node:process";

const LINES = [
  "1.  H = \u221E0 | A = K",
  "2.  S \u2192 G \u2192 Q \u2192 P \u2192 V",
  "3.  S = \u221E0 \u2192 ?",
  "4.  G = \u03B1 \u2261 {\u03B1'}",
  "5.  Q = \u03C6 \u22C2 \u03A9",
  "6.  P = \u03B4E/\u03B4V \u2192 \u2207",
  "7.  V = (L \u2229 G \u2192 B'') \u2192 \u221E0'",
  "8.  No V without \u221E0'",
  "9.  L1  L2  L3  L4  V\u2205",
];

const canonicalBytes = () => Buffer.from(LINES.join("\n") + "\n", "utf8");

async function main() {
  const path = process.argv[2];
  if (!path) {
    console.error("usage: verify-codex.mjs <path/to/codex.txt>");
    process.exit(2);
  }
  const raw = await readFile(path);
  const expected = canonicalBytes();
  const sha = createHash("sha256").update(raw).digest("hex");
  const hasBom = raw[0] === 0xef && raw[1] === 0xbb && raw[2] === 0xbf;
  const usesCrlf = raw.includes(Buffer.from("\r\n"));
  let trailingLf = 0;
  for (let i = raw.length - 1; i >= 0 && raw[i] === 0x0a; i--) trailingLf++;
  const byteIdentical = raw.equals(expected);
  const report = {
    path,
    byte_length: raw.length,
    expected_byte_length: expected.length,
    sha256: sha,
    byte_identical_to_canonical: byteIdentical,
    has_bom: hasBom,
    uses_crlf: usesCrlf,
    trailing_lf_count: trailingLf,
  };
  console.log(JSON.stringify(report, null, 2));
  const ok = byteIdentical && !hasBom && !usesCrlf && trailingLf === 1;
  process.exit(ok ? 0 : 1);
}
main().catch((e) => { console.error(e); process.exit(2); });
```

### 2.5 Manifest JSON schema (RFC 8785 JCS canonical)

```jsonc
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://5qln.com/codex/v1/manifest.schema.json",
  "title": "5QLN Codex Anchor Manifest",
  "type": "object",
  "required": [
    "version", "codex_sha256", "codex_byte_length", "encoding",
    "line_ending", "bipp", "conductor_signature", "tsa_timestamp",
    "witness_signatures", "publication_urls"
  ],
  "properties": {
    "version":            { "const": "v1" },
    "codex_sha256":       { "type": "string", "pattern": "^[0-9a-f]{64}$" },
    "codex_byte_length":  { "type": "integer", "minimum": 1 },
    "encoding":           { "const": "UTF-8" },
    "line_ending":        { "const": "LF" },
    "bipp": {
      "type": "object",
      "required": ["no_bom", "line_ending", "apostrophe", "intersection_line5", "intersection_line7", "corruption_codes_ascii"],
      "properties": {
        "no_bom":                  { "const": true },
        "line_ending":             { "const": "LF" },
        "apostrophe":              { "const": "U+0027" },
        "intersection_line5":      { "const": "U+22C2" },
        "intersection_line7":      { "const": "U+2229" },
        "corruption_codes_ascii":  { "const": true }
      }
    },
    "conductor_signature": {
      "type": "object",
      "required": ["algorithm", "public_key_fingerprint", "signature_hex"],
      "properties": {
        "algorithm":              { "const": "Ed25519" },
        "public_key_fingerprint": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
        "signature_hex":          { "type": "string", "pattern": "^[0-9a-f]{128}$" }
      }
    },
    "tsa_timestamp": {
      "type": "object",
      "required": ["rfc3161_token_b64", "tsa_url"],
      "properties": {
        "rfc3161_token_b64": { "type": "string" },
        "tsa_url":           { "type": "string", "format": "uri" }
      }
    },
    "witness_signatures": {
      "type": "array", "minItems": 3, "maxItems": 3,
      "items": {
        "type": "object",
        "required": ["witness_name", "public_key_fingerprint", "signature_hex"],
        "properties": {
          "witness_name":           { "type": "string" },
          "public_key_fingerprint": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
          "signature_hex":          { "type": "string", "pattern": "^[0-9a-f]{128}$" }
        }
      }
    },
    "publication_urls": {
      "type": "object",
      "required": ["site", "github_tag", "ipfs_cid", "rekor_log_index"],
      "properties": {
        "site":            { "type": "string", "format": "uri" },
        "github_tag":      { "type": "string" },
        "ipfs_cid":        { "type": "string", "pattern": "^baf[0-9a-z]{50,}$" },
        "rekor_log_index": { "type": "integer", "minimum": 0 }
      }
    }
  }
}
```

### 2.6 The eleven Phase 0 done‑gates (operator checklist)

1. `codex.txt` produced; all three verifiers (Python, Rust, Node) report `byte_identical_to_canonical: true`.
2. The SHA‑256 hash computed independently on three machines (operator's workstation, a clean USB‑booted Linux, and a sandboxed CI runner) — all three match.
3. YubiHSM 2 primary device provisioned; Ed25519 keypair generated on‑device; private key never exported.
4. YubiHSM 2 cold‑storage backup provisioned and stored in a separate physical location.
5. Conductor public‑key fingerprint published at `5qln.com/conductor-keys/v1/` with timestamp, Conductor attestation, and a Cosign signature.
6. Three witness signatures captured (two human witnesses + one AI cross‑substrate attestor whose attestation is itself logged as a Tier‑B record).
7. RFC 3161 TSA timestamp obtained from FreeTSA (primary) and DigiCert (backup); both tokens embedded in the manifest.
8. Manifest serialised via RFC 8785 JCS, Ed25519‑signed by the Conductor, witness signatures appended, hash printed.
9. Codex + manifest published to `5qln.com/codex/v1/` and `5qln.com/codex/v1/manifest.json`.
10. GitHub release tag `codex-v1` created on `qlnlife/5qln-core` pointing at the canonical bytes; release notes carry the hash; release is signed.
11. Sigstore Rekor entry created; IPFS CID computed and pinned to at least two providers (e.g., web3.storage + a self‑run kubo node); the Rekor log index recorded in the manifest.

### 2.7 Publication scheme

- **Primary mirror:** `https://5qln.com/codex/v1/codex.txt` and `…/manifest.json`.
- **GitHub:** tag `codex-v1` on `qlnlife/5qln-core`, immutable.
- **IPFS:** content‑addressed CID, pinned to web3.storage + self‑hosted kubo + a third independent provider.
- **Sigstore Rekor:** append‑only transparency log entry; index field added to the manifest.
- **Optional Bitcoin OP_RETURN anchor:** monthly, low cost, externally verifiable; recommended after Phase 1.

---

## SECTION 3 — PHASE 1: THE COMPILER

### 3.1 Compiler's job, one sentence

Read `codex.txt`, emit a typed executable predicate set (`predicate-set.ts`), a JSON manifest (`predicate-set.json`), and a hash pinning artifact (`predicate-set.hash`), all signed and reproducibly built.

### 3.2 Compiler architecture

- **Parsing strategy:** the Codex is parsed as nine *known* lines. The compiler refuses input that does not match the canonical text byte‑for‑byte. There is no "parse error tolerant" mode. The parser's job is structural identification, not language modeling.
- **Predicate emission strategy:** each predicate is emitted as a typed TypeScript class implementing a common `Predicate` interface; each carries `{id, codex_line, hard_or_soft, description, evaluate(input): PredicateResult}`. The compiler additionally emits a JSON Schema for the predicate set and the SHA‑256 of the emitted TypeScript file.
- **Output formats:**
  - `predicate-set.ts` — typed runtime code
  - `predicate-set.json` — structural manifest (id, line, classification, description)
  - `predicate-set.hash` — SHA‑256 of the compiled TS file
  - `predicate-set.sig` — Conductor Ed25519 signature over the hash
  - `predicate-set.attestation.json` — Sigstore bundle with provenance

### 3.3 Predicate set specification (line‑by‑line)

**Line 1 — `H = ∞0 | A = K`**
- `MembraneTypePredicate` (HARD) — runtime type check that "X slot at S phase rejects ai‑tagged input." Implementation: at any time `state.phase === 'S'` and the active output slot is `X`, captured input where `Witness.tags.speaker === 'ai'` is rejected with code `L2-AI-SPARK`.

**Line 2 — `S → G → Q → P → V`**
- `PhaseTransitionPredicate` (HARD) — admissible edges are exactly `(S,G), (G,Q), (Q,P), (P,V), (V,S')`. Anything else returns `L1-PHASE-ORDER` or `L2-PHASE-ORDER`.

**Line 3 — `S = ∞0 → ?`**
- `SparkOriginPredicate` (HARD) — requires `speaker === 'human'`, no prior validated `X`, no residue seed in the active slot.
- `QuestionMarkPredicate` (HARD) — interrogative parse (`?` present, or operator marks as question via explicit API call).

**Line 4 — `G = α ≡ {α'}`**
- `AlphaDeclarationPredicate` (HARD) — operator‑declared pointer into `X`; the pointer must be a span of `X.text` and the operator must explicitly call `kernel.declareAlpha(span)`.
- `IdentityPreservationPredicate` (SOFT, Interrogator) — does α remain unchanged across `{α'}`? Soft because identity preservation is semantic; the verdict log carries the AI's reasoning trace and is replayable on a different AI.
- `AlphaPrimeSetCardinalityPredicate` (HARD) — `|{α'}| ≥ 2`.

**Line 5 — `Q = φ ⋂ Ω`**
- `PhiTagPredicate` (HARD) — `φ` must be operator‑authored (trail‑tag‑distinguishable: `formationTrail[i].author === 'human'`).
- `OmegaSourceHashPredicate` (HARD) — `Ω` points to a hashable artifact; the artifact's SHA‑256 is recorded.
- `IntersectionLandingPredicate` (SOFT) — Interrogator asks whether something locks; verdict logged; operator confirms.

**Line 6 — `P = δE/δV → ∇`**
- `EffortValueRatioPredicate` (HARD) — computed from the formation trail (effort = count of operator turns at `P` slot, value = count of accepted `A` candidates).
- `GradientDirectionPredicate` (HARD) — `∇` is derived from the ratio and operator validates as `A`.

**Line 7 — `V = (L ∩ G → B'') → ∞0'`**
- `LocalHashPredicate` (HARD) — `L` is a concrete artifact, hashable.
- `GlobalHashPredicate` (HARD) — `G` (here: global propagation) is a concrete artifact, hashable.
- `LocalGlobalIntersectionPredicate` (SOFT) — Interrogator asks whether `L ∩ G` is genuine, verdict logged.
- `BPrimePrimeCompositionPredicate` (HARD) — two‑pass composition from trail (Pass 1 = analysis of formation trail; Pass 2 = composition).
- `InfinityZeroPrimePresencePredicate` (HARD) — `∞0'` is non‑empty AND ends with `?`.

**Line 8 — `No V without ∞0'`**
- `CycleCompletenessPredicate` (HARD) — `V` is refused if `∞0'` is empty or not a question.

**Line 9 — `L1 L2 L3 L4 V∅`**
- `CorruptionDetectionPredicate` (HARD) — 34 pattern matchers + 8 exclusion patterns + phase‑gating, ported from the existing `membrane-watcher.ts` (per `ARCHITECTURE.md` of `qlnlife/5qln-core`: 11 L3 patterns, 7 L2, 10 L4, 6 L1 (S/G‑gated), 3 V∅ (V‑gated); 8 exclusion patterns for lawful AI behaviour). Codes are ASCII canonical; superscript display permitted.

### 3.4 Compiler output

`predicate-set.ts` exports a frozen array `PREDICATES: readonly Predicate[]` indexed by line, plus a `PREDICATE_SET_HASH` constant computed at build time. The JSON manifest mirrors this. The hash pinning artifact is a single‑line file containing the SHA‑256 of the TS file, signed.

### 3.5 Compiler reproducibility

A Nix flake (`flake.nix`) pins Node, TypeScript, and Rust toolchains by content hash; `cargo-vet` covers Rust supply chain; `npm ci` with a locked `package-lock.json` covers Node. Two independent machines running `nix build .#compiler && nix build .#predicate-set` produce byte‑identical outputs.

### 3.6 Compiler verification (the meta‑compiler problem)

Three independent checks resolve "how do we know the compiler is correct?":
1. **Reproducibility check:** byte‑identity of `predicate-set.ts` across two machines.
2. **Cross‑validation:** a second compiler implementation (in Rust) emits the same predicate set JSON manifest. Any difference is a compiler bug, surfaced at build time, blocking release.
3. **Property tests:** for each of the nine lines, a published canonical fixture set (positive + negative examples) that the predicate set must classify correctly; the fixture hashes are themselves Tier‑A sealed surfaces.

### 3.7 Compiler attestation chain

`predicate-set.hash` is Ed25519‑signed by the Conductor; the signature, plus the SLSA‑3 build provenance from the CI pipeline, is bundled with the compiled output and pushed to Rekor.

---

## SECTION 4 — PHASE 2: RUNTIME AUDIT

### 4.1 Audit table of `qlnlife/5qln-core/src/`

Per the public `README.md`/`ARCHITECTURE.md`/`USER_GUIDE.md`:

| Module | LOC | Codex symbols | Classification | Verdict |
|---|---|---|---|---|
| `types.ts` | ~350 | Constitutional constants (`MINIMUM_VALID_BEGINNING`, `CORRUPTION_CODES`) | Substrate | **Rewrite** — currently ten‑line superscript form with `L¹/L²/L³/L⁴/V∅`; realign to nine‑line Appendix A and ASCII `L1 L2 L3 L4 V∅`. |
| `kernel.ts` | ~400 | Phase transitions, formation tracking, corruption detection | Lines 2, 3, 4, 5, 6, 7, 8 | **Keep + extend** — already implements `S→G→Q→P→V`, Serve‑vs‑Be rule, validation states. Extend with predicate‑id stamping. |
| `attestation.ts` | ~200 | SHA‑256 fingerprint, 3‑level verification | Substrate | **Keep + extend** — already produces fingerprint; bind to Codex hash from §2. |
| `ai-adapter.ts` | ~280 | Formation‑anchored prompts | Line 1 (Membrane), Interrogator prep | **Rewrite as Interrogator (§5).** Currently a thin formation‑anchored prompt builder; needs hashed template store and verdict logging. |
| `storage.ts` | ~50 | Pluggable persistence | Conversation stratum | **Keep + extend** — wrap with §7 write‑gate API. |
| `export.ts` | ~110 | Agent Card, Markdown, JSON export | Translation surface | **Move to L7 translation surfaces** (§11). |
| `membrane-watcher.ts` | ~510 | Line 9 corruption detection | `CorruptionDetectionPredicate` | **Keep + alias** — 34 patterns intact; add ASCII‑canonical / superscript alias layer; phase‑gating preserved. |
| `fractal-kernel.ts` | ~280 | Holographic scaling (`XY := X within Y`) | Line 1 holographic law | **Keep** — depth‑bounded recursive kernel; lineage chain preserved. |

### 4.2 Library realignment PR

- `types.ts`:
  - `CORRUPTION_CODES = ['L1','L2','L3','L4','V∅'] as const;` (ASCII canonical)
  - `MINIMUM_VALID_BEGINNING` = the nine‑line text from §2.2 (replacing the current ten‑line superscript form)
  - `Q = φ ⋂ Ω` (U+22C2) on line 5
- `README.md`: ten‑line block → nine‑line block; recompute documented hash from sealed `codex.txt`.
- `membrane-watcher.ts`: add `aliasMap = { 'L¹':'L1', 'L²':'L2', 'L³':'L3', 'L⁴':'L4' }` for inbound text; emission always ASCII.
- `ai-adapter.ts`: refactored to `interrogator.ts` (see §5).
- Bump version to `v0.3.0`; release tag `codex-aligned-v1`.

### 4.3 Coverage assessment

| Predicate | Present? | Where |
|---|---|---|
| `MembraneTypePredicate` | Partial | `kernel.ts` Serve‑vs‑Be |
| `PhaseTransitionPredicate` | Present | `kernel.ts` `transition()` |
| `SparkOriginPredicate` | Partial | implicit |
| `QuestionMarkPredicate` | Absent | — |
| `AlphaDeclarationPredicate` | Absent | — |
| `IdentityPreservationPredicate` | Absent | will live in Interrogator |
| `AlphaPrimeSetCardinalityPredicate` | Absent | — |
| `PhiTagPredicate` | Partial | formation trail tagging |
| `OmegaSourceHashPredicate` | Absent | — |
| `IntersectionLandingPredicate` | Absent | will live in Interrogator |
| `EffortValueRatioPredicate` | Absent | — |
| `GradientDirectionPredicate` | Absent | — |
| `LocalHashPredicate` / `GlobalHashPredicate` | Absent | — |
| `LocalGlobalIntersectionPredicate` | Absent | Interrogator |
| `BPrimePrimeCompositionPredicate` | Present | `kernel.crystallize()` two‑pass |
| `InfinityZeroPrimePresencePredicate` | Partial | `kernel.return()` |
| `CycleCompletenessPredicate` | Present | "No V without ∞0'" |
| `CorruptionDetectionPredicate` | Present | `membrane-watcher.ts` |

### 4.4 Runtime gap report

Build to full coverage in this order (smallest first, dependencies respected): `QuestionMarkPredicate` → `AlphaDeclarationPredicate` → `AlphaPrimeSetCardinalityPredicate` → `PhiTagPredicate` (hard portion) → `OmegaSourceHashPredicate` → `EffortValueRatioPredicate` → `GradientDirectionPredicate` → `LocalHashPredicate` → `GlobalHashPredicate` → soft predicates via Interrogator.

---

## SECTION 5 — PHASE 3: THE INTERROGATOR

### 5.1 Job, one sentence

Compose Codex‑derived prompts from hashed templates, call AI as a bounded sensor, log the verdict to the trail; verdicts are evidence, not law.

### 5.2 Architecture

- **Template store:** content‑addressed; each template's SHA‑256 is a foreign key into the verdict log.
- **Prompt composition:** placeholder substitution from kernel state + Codex line text (the *text* is loaded from sealed bytes; the predicate code never embeds Codex text outside this layer).
- **AI provider abstraction:** `interface AIProvider { respond(systemPrompt: string, userMessage: string, cfg: AIProviderConfig): Promise<string> }` — Anthropic, OpenAI, Google, local; provider identity is part of the verdict record.
- **Verdict logging:** append‑only, hash‑chained, replayable on a different AI.
- **Drift measurement:** canonical probe library, periodic execution, variance tracked.

### 5.3 Soft predicate templates (hashed; placeholders shown)

**IdentityPreservationPredicate template:**
```
You are a bounded sensor for the 5QLN Codex line `G = α ≡ {α'}`.
You will not decide; you will only observe.

Given:
  α (declared by operator): {{ALPHA_TEXT}}
  {α'} (candidate self-similar expressions):
{{#each ALPHA_PRIMES}}- {{this}}
{{/each}}

Question: Does α remain structurally identical (≡) across all {α'}?
Answer with exactly one of: IDENTICAL | SHIFTED | UNCERTAIN
Then on a new line, write a one-sentence rationale.

Your answer is a sensor reading. The operator decides.
```

**IntersectionLandingPredicate template:**
```
You are a bounded sensor for the 5QLN Codex line `Q = φ ⋂ Ω`.

Given:
  φ (operator's self-nature observation): {{PHI_TEXT}}
  Ω (universal-potential anchor, hash {{OMEGA_HASH}}): {{OMEGA_TEXT}}

Question: Has φ ⋂ Ω landed — does something lock that neither alone contained?
Answer with exactly one of: LANDED | NOT_LANDED | UNCERTAIN
Then on a new line, write a one-sentence rationale.

Your answer is a sensor reading. The operator decides.
```

**LocalGlobalIntersectionPredicate template:**
```
You are a bounded sensor for the 5QLN Codex line `V = (L ∩ G → B'') → ∞0'`.

Given:
  L (local actualization, hash {{L_HASH}}): {{L_TEXT}}
  G (global propagation, hash {{G_HASH}}): {{G_TEXT}}

Question: Do L and G genuinely meet at ∩, or is the meeting claimed but not present?
Answer with exactly one of: MEETS | CLAIMED_NOT_MET | UNCERTAIN
Then on a new line, write a one-sentence rationale.

Your answer is a sensor reading. The operator decides.
```

### 5.4 Interrogator reference implementation (TypeScript, ≤500 LOC)

```typescript
// src/interrogator.ts — 5QLN bounded-AI sensor with verdict logging.
import { createHash, randomBytes } from "node:crypto";

export type SoftPredicateId =
  | "IdentityPreservationPredicate"
  | "IntersectionLandingPredicate"
  | "LocalGlobalIntersectionPredicate";

export interface AIProviderConfig { model: string; provider: string; }
export interface AIProvider {
  respond(systemPrompt: string, userMessage: string, cfg: AIProviderConfig): Promise<string>;
}

export interface PromptTemplate {
  id: SoftPredicateId;
  text: string;       // with {{PLACEHOLDERS}}
  sha256: string;     // hash of the template text
}

export interface VerdictRecord {
  verdict_id: string;
  parent_verdict_id: string | null;
  predicate_id: SoftPredicateId;
  template_sha256: string;
  codex_sha256: string;
  prompt_filled_sha256: string;
  raw_response: string;
  parsed_label: "IDENTICAL"|"SHIFTED"|"UNCERTAIN"|"LANDED"|"NOT_LANDED"|"MEETS"|"CLAIMED_NOT_MET";
  rationale: string;
  provider: string;
  model: string;
  ts_iso: string;
  signature_hex: string | null; // Conductor-signed when sealed
}

export interface VerdictLog {
  append(r: Omit<VerdictRecord, "verdict_id"|"parent_verdict_id"|"signature_hex">,
         parentId: string | null): Promise<VerdictRecord>;
  tail(): Promise<VerdictRecord | null>;
}

export class Interrogator {
  constructor(
    private readonly templates: Record<SoftPredicateId, PromptTemplate>,
    private readonly provider: AIProvider,
    private readonly providerCfg: AIProviderConfig,
    private readonly codexHash: string,
    private readonly log: VerdictLog,
  ) {}

  private fill(t: PromptTemplate, vars: Record<string,string>): string {
    return t.text.replace(/\{\{([A-Z_]+)\}\}/g, (_, k) => vars[k] ?? "");
  }
  private parse(raw: string, expected: readonly string[]): { label: any; rationale: string } {
    const lines = raw.trim().split(/\r?\n/);
    const label = (lines[0] ?? "").trim().toUpperCase();
    const rationale = (lines[1] ?? "").trim();
    if (!expected.includes(label)) {
      return { label: "UNCERTAIN", rationale: `unparseable: ${raw.slice(0,200)}` };
    }
    return { label, rationale };
  }
  private hash(s: string): string { return createHash("sha256").update(s, "utf8").digest("hex"); }
  private vid(): string { return randomBytes(16).toString("hex"); }

  async ask(predicateId: SoftPredicateId, vars: Record<string,string>): Promise<VerdictRecord> {
    const tpl = this.templates[predicateId];
    if (!tpl) throw new Error(`unknown soft predicate: ${predicateId}`);
    const filled = this.fill(tpl, vars);
    const filledHash = this.hash(filled);
    const raw = await this.provider.respond(filled, "Proceed.", this.providerCfg);
    const expected = predicateId === "IdentityPreservationPredicate"
      ? ["IDENTICAL","SHIFTED","UNCERTAIN"]
      : predicateId === "IntersectionLandingPredicate"
      ? ["LANDED","NOT_LANDED","UNCERTAIN"]
      : ["MEETS","CLAIMED_NOT_MET","UNCERTAIN"];
    const parsed = this.parse(raw, expected);
    const parent = await this.log.tail();
    return this.log.append({
      predicate_id: predicateId,
      template_sha256: tpl.sha256,
      codex_sha256: this.codexHash,
      prompt_filled_sha256: filledHash,
      raw_response: raw,
      parsed_label: parsed.label,
      rationale: parsed.rationale,
      provider: this.providerCfg.provider,
      model: this.providerCfg.model,
      ts_iso: new Date().toISOString(),
    } as any, parent?.verdict_id ?? null);
  }

  async consensus(
    predicateId: SoftPredicateId,
    vars: Record<string,string>,
    providers: { p: AIProvider; cfg: AIProviderConfig }[],
  ): Promise<{ records: VerdictRecord[]; agreement: number }> {
    const records: VerdictRecord[] = [];
    for (const { p, cfg } of providers) {
      const ig = new Interrogator(this.templates, p, cfg, this.codexHash, this.log);
      records.push(await ig.ask(predicateId, vars));
    }
    const labels = records.map(r => r.parsed_label);
    const max = Math.max(...new Set(labels).values
      ? [...new Set(labels)].map(l => labels.filter(x => x === l).length)
      : [0]);
    return { records, agreement: max / labels.length };
  }
}
```

### 5.5 Verdict log schema (append‑only, hash‑chained)

Each record is canonicalised (RFC 8785) and its hash chained to the previous (`parent_verdict_id`). Periodic Conductor signatures cover ranges. Records are replayable: rerun the same template against a different AI and compare.

### 5.6 Drift detection

A probe library of ~30 canonical questions (e.g., "α = trust; {α'} = {a child's grip, a contract, a doorframe}: IDENTICAL/SHIFTED/UNCERTAIN?") runs nightly; verdict variance over time is the drift metric. Spikes trigger CIO review.

### 5.7 Multi‑AI consensus

- **2‑of‑3 required** when the predicate gates V (cycle close), an amendment, a public Foundation statement, or any P.L.4‑adjacent decision.
- **Single AI sufficient** for routine cycle progression (S → G → Q → P intermediates).
- **Consensus failures** are themselves Tier‑B records and require Conductor attestation to proceed.

---

## SECTION 6 — RING FUNCTIONS AROUND THE KERNEL

The Kernel holds *only*: `{phase, lens, outputFormationStates, adaptiveContextChain, sparkSource}`. Everything else is ring.

```typescript
export type Phase = 'S'|'G'|'Q'|'P'|'V';
export type Lens = `${Phase}${Phase}`;
export type SparkSource = 'human'|'residue';
export type OutputState = 'NONE'|'EMERGING'|'FORMING'|'VALIDATED';

export interface KernelState {
  phase: Phase;
  lens: Lens | null;
  outputs: Record<'X'|'Y'|'Z'|'A'|'B', OutputState>;
  adaptiveContext: ReadonlyArray<string>;
  sparkSource: SparkSource;
}
```

### 6.1 Loader

- **Role:** verifies the Codex hash; refuses to start under a forked Codex.
- **Interface:**
```typescript
export interface Loader {
  start(codexPath: string, manifestPath: string): Promise<{ codexHash: string; predicateSetHash: string }>;
}
```
- **Invariants:** SHA‑256 of `codex.txt` must match manifest; manifest signatures must verify; predicate‑set hash pin must match.
- **Reference:** reads, hashes, verifies all signatures, returns hashes — or throws `LOADER_REFUSED_FORK`.

### 6.2 Witness

- **Role:** tags every utterance.
- **Interface:**
```typescript
export interface WitnessTag {
  phase: Phase; lens: Lens | null; speaker: 'human'|'ai';
  ts_iso: string; sparkSource: SparkSource;
}
export interface Witness {
  tag(utterance: string, state: KernelState, speaker: 'human'|'ai'): WitnessTag;
  appendToTrail(t: WitnessTag, utterance: string): Promise<string>;
}
```
- **Invariants:** every utterance produces exactly one tag; trail is append‑only.

### 6.3 Watcher

- **Role:** pattern‑matches L1/L2/L3/L4/V∅; phase‑gates.
- **Interface:**
```typescript
export interface WatcherFlag { code: 'L1'|'L2'|'L3'|'L4'|'V∅'; confidence: 'high'|'medium'|'low'; }
export interface Watcher {
  scan(utterance: string, phase: Phase): WatcherFlag[];
}
```
- **Invariants:** the 34 patterns and 8 exclusions are content‑addressed; L1/V∅ phase‑gated (L1 S/G‑only; V∅ V‑only).

### 6.4 Sealer

- **Role:** at V, composes `B''` (two‑pass from trail) and emits `∞0'` as next‑cycle seed.
- **Interface:**
```typescript
export interface Sealer {
  compose(trail: ReadonlyArray<{tag: WitnessTag; text: string}>): Promise<{ bPrimePrime: string; infinityZeroPrime: string }>;
}
```
- **Invariants:** Pass 1 reads trail (α thread, φ⋂Ω confirmation, ∇, turning points); Pass 2 composes; `∞0'` ends with `?`.

### 6.5 Attestor

- **Role:** builds the provenance record, signs, exposes 3‑level verification.
- **Interface:** matches `attestation.ts` of `qlnlife/5qln-core`: `buildProvenanceRecord(...)`, `verifyLevel1/2/3`.
- **Invariants:** Level 1 = structural validity; Level 2 = cycle completeness (X formed, B formed, corruption resolved); Level 3 = lineage chain walks to human origin.

### 6.6 Interrogator

- **Interface:** covered in §5.

---

## SECTION 7 — PHASE 4: THE WRITE GATE

### 7.1 Conversation stratum write‑path API

```typescript
export interface ArtifactProof {
  predicate_id: string;
  predicate_hash: string;
  codex_hash: string;
  ai_verdict_log_id: string | null;
  parent_hash: string;
}
export interface ArtifactRequest {
  content: string | Uint8Array;
  proof: ArtifactProof;
  tag: WitnessTag;
}
export interface WriteGate {
  admit(req: ArtifactRequest): Promise<{ stored_hash: string }>;
}
```

The gate refuses any `req` whose `proof.codex_hash` differs from the loaded Codex hash; whose `predicate_hash` is not in the pinned predicate set; whose `parent_hash` does not resolve in storage; or whose `ai_verdict_log_id`, if present, does not match a valid verdict record.

### 7.2 Storage layer

Content‑addressed (SHA‑256 keys), append‑only, hash‑chained per stream. PostgreSQL (working store) + Sigstore Rekor (public anchor) + optional IPFS mirror.

### 7.3 Lineage walker

From any node hash, walk `parent_hash` links until a Codex anchor is reached. Output: ordered list of hashes, each annotated with `{predicate_id, predicate_hash, phase, timestamp}`. The walk is a deterministic Tier‑A audit primitive.

### 7.4 Graph edge admittance

New context‑graph edges are admitted only if both endpoints exist, both endpoints' proofs verify, and the connecting predicate (typically `PhaseTransitionPredicate` or `AdaptiveContextChainPredicate`) admits the transition.

### 7.5 Cycle lineage

`∞0'` of cycle N → seed `X` of cycle N+1 carries: hash of N's `∞0'`, hash of N's `B''`, hash of N's full trail. The Loader of cycle N+1 verifies these are valid Tier‑A artifacts before accepting them as seed.

---

## SECTION 8 — RUNTIME INFRASTRUCTURE (AOSRAP integration)

### 8.1 How AOSRAP layers on

Per the AOSRAP Wrapper Engineering Specification v0.1 (5qln.com), the wrapper is Phase 0 of the maturation path. It sits between Foundation tools and the LLM API: every request passes through; every response is validated; every event writes to an append‑only Merkle log.

AOSRAP A1–A5 in this architecture:
- **A1 — session initialisation:** Loader includes wrapper's `attestation_nonce` + `ai_os_edition_hash` (child of Phase 0 Codex hash) in the kernel state.
- **A2 — per‑query validation:** Interrogator includes `expected_phase_tag`; wrapper enforces `ATTEST: <hash>` echo; failure triggers session deauthorization.
- **A3 — synthetic probes:** every 4 hours, the wrapper sends P.L.4 hard‑block probes; failure deauthorizes globally.
- **A4 — attention‑state attestation:** behavioural proxy via expected per‑phase signatures (full A4 is `[REQUIRES_PARTNER]`).
- **A5 — per‑output attestation:** every Interrogator response carries `{attestation_nonce, phase_tag, ai_os_edition_hash}`; missing fields make the output non‑Foundation‑mode‑compliant.

### 8.2 Schedule C manifest as child of Phase 0 Codex hash

Schedule C pairs the Human Edition and the AI OS Edition at the provision level (per Bylaws). The Schedule C manifest carries a `parent_codex_hash` pointing at the Phase 0 sealed Codex. Provision pairs are SHA‑256‑linked; a 24‑hour EDP heartbeat compares pair hashes and quarantines on mismatch.

### 8.3 Transparency log integration

Sigstore Rekor v2 (production) or Git+Sigstore (Phase 0 minimum). Every Conductor seal, every deauthorization, every probe result is a log entry. The Merkle root is published hourly to `mirror.5qln.org/rekor-root.txt` and to a third‑party transparency service.

### 8.4 Breach response flow

1. Detector (BreachDetector pattern match or AOSRAP probe failure) fires.
2. Wrapper deauthorizes (session or global, per severity).
3. Sealed Membrane Breach Gliff emitted; cycle cannot produce positive artifact.
4. Conductor reviews; either reauthorizes (with sealed remediation gliff) or escalates to CIO.
5. If criticality is L3+ or P.L.4 breach, Resonance Court convened within 7 days.

---

## SECTION 9 — THE SKILL SUITE

### 9.1 Layer A — Kernel skills (live session)

| Skill | Purpose | Trigger | Inputs | Outputs | Pre / Post | Acceptance | Pair‑with |
|---|---|---|---|---|---|---|---|
| `session-initializer` | Load Codex, set state to S | New session | Codex path, manifest | KernelState | Loader passes | Hashes recorded | `trail-recorder` |
| `s-receiver` | Receive ∞0 → ? from human | S phase | Operator utterance | `X` candidate | Phase = S; speaker = human | `X` enters EMERGING | `corruption-watcher-live` |
| `g-illuminator` | Surface α and {α'} candidates | G phase | `X`, K patterns | α + {α'} | `X` VALIDATED | α + ≥2 α' surfaced | `lens-discipline` |
| `q-resonator` | Hold φ + Ω, watch ⋂ | Q phase | `X+α+Y` | `Z` | Y VALIDATED | `Z` confirmed by operator | `corruption-watcher-live` |
| `p-flow-watcher` | Map δE/δV; reveal ∇ | P phase | full prior trace | `A` | `Z` VALIDATED | ∇ visible | `lens-discipline` |
| `v-crystallizer` | Two‑pass compose B'' | V phase | full trace | `B''` + ∞0' | `A` VALIDATED | ∞0' is question | `cycle-closer` |
| `lens-discipline` | Apply 25 lenses without overwriting | any phase | active output | lens annotation | Sub‑phase active | Serve‑vs‑Be holds | all |
| `trail-recorder` | Append every utterance with tags | every turn | utterance | trail entry | Witness available | Append‑only verified | all |
| `corruption-watcher-live` | Real‑time 34‑pattern scan | every turn | utterance | flags | Watcher loaded | Flags routed | `cycle-closer` |
| `cycle-closer` | Verify No V without ∞0' | V phase | sealed gliff | sealed B'' | `InfinityZeroPrimePresencePredicate` passes | Rekor entry exists | `provenance-builder` |

Each acceptance test is a fixture in `tests/skills/*.spec.ts`.

### 9.2 Layer B — Attestation skills

- **`provenance-builder`** — produces the Attestor's provenance record at V seal; pre: cycle complete; post: signed record; pair‑with: `three-level-verifier`.
- **`three-level-verifier`** — runs Levels 1/2/3 over any provenance record; pre: record + storage resolver; post: pass/fail with reasons; pair‑with: `codex-fingerprint-comparator`.
- **`codex-fingerprint-comparator`** — compares a record's `codex_hash` to the canonical hash; pre: canonical hash known; post: match/mismatch; pair‑with: Loader.

### 9.3 Layer C — Topology skills

- **`surface-emitter`** — emits domain‑specific projections from cycle residue; never load‑bearing; idempotent; regenerable.
- **`pentagonal-swarm-coordinator`** — five agent instances, each carrying a full kernel, specialised in one phase but containing all five. Center is coherence only (per Decision F); fingerprints must match; routing S→G→Q→P→V.
- **`fractal-deepening-judge`** — bounds recursion depth (`fractal-kernel.ts`); enforces `setMaxDepth(n)`; refuses deepening past N.

---

## SECTION 10 — THE PLUGIN PROTOCOL

### 10.1 Manifest schema

```jsonc
{
  "plugin_id": "5qln-legal-projector",
  "plugin_version": "0.1.0",
  "author": "qlnlife",
  "codex_hash_at_install": "sha256:<canonical>",
  "predicates_touched": ["BPrimePrimeCompositionPredicate"],
  "trail_tags_produced": ["legal-projection"],
  "ai_calls_made": [{ "predicate": "soft", "max_per_cycle": 0 }],
  "conversation_stratum_write_quota_per_cycle": 1,
  "signature_hex": "<Conductor or plugin-author Ed25519 over canonical manifest>"
}
```

### 10.2 Sandboxing

- Each plugin runs in a worker thread (Node `worker_threads`) with a capability‑restricted API; no direct write‑gate access — all writes go through a quota‑bounded proxy.
- Plugin's predicate‑set delta (new predicates it introduces) is tracked and refused unless registered.
- Plugin's write quota is per‑cycle and per‑plugin.

### 10.3 Attestation

At install time, the plugin's SHA‑256 is bound to the current Codex hash. Updating the Codex invalidates plugin attestations; plugins must be re‑attested (cheap automated process, but explicit).

### 10.4 Reference implementation: `5qln-legal-projector`

```typescript
// plugins/5qln-legal-projector/index.ts
import type { CycleResidue, ProjectionConfig, DomainArtifact } from "@5qln/core";
import { createHash } from "node:crypto";

export interface LegalProjection extends DomainArtifact {
  jurisdiction: "Delaware" | "Korea-KAIBA" | "EU-AI-Act";
  document_type: "resolution" | "bylaws-amendment" | "filing";
  body: string;
  projection_hash: string;
  source_residue_hash: string;
  codex_hash: string;
}

export function project(
  residue: CycleResidue,
  cfg: ProjectionConfig & { jurisdiction: LegalProjection["jurisdiction"];
                          document_type: LegalProjection["document_type"] },
): LegalProjection {
  const body = renderLegalBody(residue, cfg);
  const projection_hash = createHash("sha256").update(body, "utf8").digest("hex");
  return {
    jurisdiction: cfg.jurisdiction,
    document_type: cfg.document_type,
    body,
    projection_hash,
    source_residue_hash: residue.b_prime_prime_hash,
    codex_hash: residue.codex_hash,
  };
}

function renderLegalBody(residue: CycleResidue, cfg: ProjectionConfig & any): string {
  const header = [
    "CONSTITUTIONAL BLOCK (verbatim, see Codex v1):",
    residue.constitutional_block_text,
    "",
    `Jurisdiction: ${cfg.jurisdiction}`,
    `Document Type: ${cfg.document_type}`,
    `Source Residue: ${residue.b_prime_prime_hash}`,
    "",
  ].join("\n");
  const body = renderByType(residue, cfg);
  const footer = `\n\n[This projection is regenerable from residue ${residue.b_prime_prime_hash}.\n It is not load-bearing under the 5QLN architecture.]`;
  return header + body + footer;
}

function renderByType(residue: CycleResidue, cfg: any): string {
  switch (cfg.document_type) {
    case "resolution":
      return `WHEREAS ${residue.X};\nWHEREAS the essence (α) is ${residue.alpha};\n` +
             `RESOLVED, that the Foundation adopt ${residue.B}.\n` +
             `Forward question (∞0'): ${residue.infinity_zero_prime}`;
    case "bylaws-amendment":
      return `Amendment to Bylaws, pursuant to V.L.5(a) or V.L.5(b) as applicable.\n` +
             `Subject: ${residue.X}\nEssence: ${residue.alpha}\nText: ${residue.B}`;
    case "filing":
      return `Filing to ${cfg.jurisdiction}.\nMatter: ${residue.X}\nDisposition: ${residue.B}`;
  }
}
```

---

## SECTION 11 — TRANSLATION SURFACES

### 11.1 Pattern

A translation surface takes `(CycleResidue, ProjectionConfig)` → `DomainArtifact` deterministically. It is **regenerable** from residue and **never feeds back**.

### 11.2 Required interface

```typescript
export interface CycleResidue {
  cycle_id: string;
  X: string; alpha: string; Y: string;
  phi_intersection_omega: string; Z: string;
  gradient: string; A: string;
  B: string; b_prime_prime_hash: string;
  infinity_zero_prime: string;
  constitutional_block_text: string;
  codex_hash: string;
  trail_hash: string;
}
export interface ProjectionConfig { audience: string; locale: string; style: string; }
export interface DomainArtifact { projection_hash: string; source_residue_hash: string; codex_hash: string; }
export interface TranslationSurface<T extends DomainArtifact> {
  project(residue: CycleResidue, cfg: ProjectionConfig): T;
}
```

### 11.3 Reference surfaces

- **`5qln-legal-projector`** — emits Delaware nonprofit resolutions, bylaws amendments, Chancery filings; carries the Constitutional Block verbatim; respects BIPP jurisdictional delta (`5qln-bipp-jurisdictional-delta` skill); never amends Codex. Signature: `project(residue, {audience:'counsel', locale:'DE-US', style:'jurat'}): LegalProjection`.
- **`5qln-medical-projector`** — emits clinical decision support memos with the Constitutional Block as a transparency banner; the AI's role is bounded sensor (decoder of patterns); the physician retains ∞0 (clinical judgment). Signature: `project(residue, {audience:'clinician', locale:'en-US', style:'soap-note'}): MedicalProjection`.
- **`5qln-education-projector`** — emits lesson plans, rubric scaffolds, and self‑assessment prompts that preserve student ∞0 (the question is the student's). Signature: `project(residue, {audience:'student', locale:'en-US', style:'inquiry-rubric'}): EducationProjection`.

### 11.4 No feedback rule

The Write Gate (§7.1) rejects any artifact whose `predicate_id` traces to a translation surface. The translation surface is a *projection*, not a *source*.

---

## SECTION 12 — GOVERNANCE / FOUNDATION LAYER

### 12.1 Amendments

- **Tier 1 (Constitutional Block):** V.L.5(b) tri‑condition gate — unanimous vote of all Directors then in office; contemporaneously documented finding under (A) compliance with applicable law, (B) correction of demonstrable transcription error, OR (C) refinement validated by the 5QLN open‑source community and accepted by consensus at 5qln.com or successor source of record; compliance with Board‑adopted additional procedures. Any failure renders the amendment invalid.
- **Tier 2 (ordinary Bylaws):** two‑thirds (2/3) of Directors then in office, ≥30 days written notice (per Bylaws V.L.5(a)).
- **Tier 3 (operational policy):** Board majority by resolution.

### 12.2 Codex versioning

- **v1 → v2 trigger conditions:** an amendment passes the V.L.5(b) gate; the operator (or successor source of record) publishes v2 with a fresh manifest, sealed with the same ceremony as Phase 0.
- **Backward compatibility:** v1 cycles remain verifiable against v1 forever; v2 cycles verify against v2; the verifier accepts a `--codex-version` flag and refuses cross‑version verdicts silently.

### 12.3 Dispute routing

- **CIO indicators** (twelve [SPECULATIVE] markers per Final Blueprint, pending Phase‑2 calibration) fire on Tier‑B reports.
- **Resonance Court** convenes for non‑legal‑jeopardy disputes: protocol Z → ? → ∇ → α → Z'; 3–5 facilitators external to Board, 5QLN‑certified; DTBP (Dual‑Timeline Bridging Protocol) tracks each step against `default_max` and `hard_max` durations.
- **Chancery V.L.7(f)** is the sole and exclusive external forum for derivative actions, fiduciary‑duty claims, DGCL‑arising claims, and internal‑affairs‑doctrine claims. Chancery bypass available if 2+ Phase Circle Representatives qualify or DTBP `hard_max` is exceeded.

### 12.4 Foundation legal entity ↔ technical substrate

The substrate **predates** the Foundation legal entity. Pre‑incorporation cycles are STRUCTURAL‑HYPOTHESIS or LEGAL‑PROSPECTIVE; the verifier records `pre_incorporation: true` until the Delaware Certificate is filed. Asset transfer from personal/Anti Entropy fiscal sponsorship to the Foundation is a standard pre‑formation operational practice.

---

## SECTION 13 — DEPLOYMENT GUIDE

### 13.1 Local development

```
git clone https://github.com/qlnlife/5qln-core
cd 5qln-core
# 1. Pull Codex v1
curl -fLO https://5qln.com/codex/v1/codex.txt
curl -fLO https://5qln.com/codex/v1/manifest.json
# 2. Verify
python3 tools/python/verify_codex.py codex.txt
# 3. Build
nix develop && nix build
npm ci && npm test
```

### 13.2 Host options

- **Browser:** static bundle of `@5qln/core` + WASM verifier; Codex bundled at build time, hash baked.
- **Node:** the reference target; works as CLI, server, MCP server.
- **Raspberry Pi:** ARM build via cross‑compilation; the YubiKey lives on the Pi.
- **MCP server:** exposes Kernel methods, validator endpoints, transparency log endpoints.
- **Zo Computer:** AI session ↔ MCP server ↔ Kernel chain (per `ARCHITECTURE.md` of `qlnlife/5qln-core`).
- **Agent runtime:** LangGraph, Anthropic Agent SDK, Vercel AI SDK — each wraps the kernel as constitutional layer.
- **Pentagonal swarm:** five kernel instances, fingerprint‑checked, S/G/Q/P/V specialised; center is coherence only.

### 13.3 CI/CD pipeline

- **Reproducible build** via Nix flake with pinned toolchain.
- **Hash verification:** CI re‑computes Codex hash and predicate‑set hash; mismatch fails build.
- **Automated probes:** drift probes from §5.6 run on every PR; >5% variance from baseline fails the run.
- **SLSA‑3 provenance** generated; Cosign signature attached to release artifacts; Rekor entries created.

### 13.4 Migration from current `qlnlife/5qln-core`

1. Branch `codex-realignment-v1` off `master`.
2. Apply PR per §4.2 (types.ts realignment, README rewrite, alias map in membrane‑watcher.ts, recompute hashes).
3. Add `tools/python/verify_codex.py`, `tools/rust/` (Rust), `tools/node/verify-codex.mjs`.
4. Add `src/interrogator.ts` (port from `ai-adapter.ts`).
5. Add `src/write-gate.ts`, `src/lineage-walker.ts`.
6. Add `nix/flake.nix`.
7. Cut `v0.3.0`; tag `codex-aligned-v1`.

---

## SECTION 14 — VERIFICATION PHILOSOPHY & THREAT MODEL

### 14.1 Verification stack

Three layers, per "The Codex as Complete Verifier" (5qln.com):
- **Cryptographic:** SHA‑256 byte identity to Codex; Ed25519 verification (RFC 8032 deterministic instance, malleable‑sig acceptance disabled); RFC 3161 timestamps; Schedule C paired manifest match; public mirror cross‑check.
- **Grammatical (C1 §3.5):** phase ordering, adaptive context chain, phase outputs present, role‑completeness per phase, P.L.4 hard‑block scan, symbol drift check, six‑attestation Ceremony record at P.
- **Epistemic‑register:** every load‑bearing claim tagged (STRUCTURAL‑HYPOTHESIS, LEGAL‑PROSPECTIVE, PHENOMENOLOGICAL‑ASSERTION, CODEX‑EXTENSION); readiness labels present (AVAILABLE, REQUIRES_INFRA, REQUIRES_LEGAL, REQUIRES_PARTNER, SPECULATIVE); Tier‑A discipline; Tier‑2 amendment markers for new CL4‑GP indicators.

### 14.2 Threat model

**Defended against:**
- AI silently failing to load AI OS Edition (hash echo).
- AI drifting from declared phase behaviour (phase‑tag enforcement + synthetic probes).
- Vendor silently changing model weights mid‑session (4‑hour probes fail differently than baseline).
- Operator prompt injection (BreachDetector patterns).
- Tampering with operational record after the fact (append‑only Merkle log).

**Not defended against:**
- LLM that pattern‑matches the hash echo without semantically attending — requires Phase 1 confidential computing or Phase 2 vendor attestation.
- Adversary who compromises the wrapper itself — mitigated by reproducible builds + public CI, not eliminated.
- Coordinated failure where LLM passes probes while violating spirit in production traffic — only repeated operational use surfaces this.
- A Board that performs the cycle (L4) while making decisions through K‑only channels — the architecture makes this *detectable*, not impossible.

### 14.3 Honest acknowledgment of soft‑predicate dependency

Soft predicates (Identity Preservation, Intersection Landing, Local/Global Intersection) depend on AI judgment. The architecture's mitigation is *not* that the AI is right — it is that the AI's verdict is logged, hashed, replayable on a different AI, and operator‑confirmed. The AI is sensor; the operator is judge.

### 14.4 Drift as measurable quantity

Drift is the variance of soft‑predicate verdicts on canonical probes over time, per AI provider/model pair. A drift dashboard publishes weekly variance; spikes trigger CIO review. Drift is not binary; it has a magnitude and a direction.

---

## SECTION 15 — ROADMAP & RESOURCE ESTIMATES

### 15.1 Phase sequencing

| Phase | Engineer‑weeks | Predecessors | Gate criteria |
|---|---|---|---|
| Phase 0 (Seal) | 2 (operator + 1 helper) | — | All 11 done‑gates pass (§2.6). |
| Phase 1 (Compiler) | 4 | Phase 0 | Reproducible build; cross‑validation (TS vs Rust manifests match); property tests green. |
| Phase 2 (Audit + Realignment) | 3 | Phase 1 | PR merged, hashes recomputed, all 150 tests green. |
| Phase 3 (Interrogator) | 4 | Phase 1 | All three soft templates hashed and pinned; verdict log append‑only verified; drift probes baseline established. |
| Phase 4 (Write Gate) | 5 | Phase 2, Phase 3 | Write‑gate API live; lineage walker traces sample cycles; one verifier‑passing cycle end‑to‑end. |
| **Total to first verifier‑passing cycle** | **~18 weeks** | | Phase 1 of Codex‑as‑Verifier "earliest verifiable build" complete. |

### 15.2 Critical path

Phase 0 → Phase 1 → Phase 4. Phase 2 and Phase 3 parallelise after Phase 1.

### 15.3 Parallelisation

- Phase 2 (audit) and Phase 3 (Interrogator) run concurrently after Phase 1.
- AOSRAP wrapper (10‑week separate spec) parallelises with Phase 3.
- Skill suite (Layer A) parallelises with Phase 4.
- Plugin protocol and translation surfaces wait for Phase 4 completion.

### 15.4 Hard sequencing

- Phase 1 cannot start until Phase 0's Codex hash is published (the compiler's input must be sealed).
- Phase 4 cannot start until Phase 3's verdict log schema is signed (write‑gate references it).
- Federation work (BIPP, multi‑jurisdiction) cannot start until Phase 4 is producing verifier‑passing cycles.

---

## SECTION 16 — OPEN QUESTIONS AND RECOMMENDED OPERATOR DECISIONS

### 16.1 Genuine open questions (operator decisions required)

1. **Exact Codex byte count.** The ceremony‑canonical count is 217 bytes per the three reference verifiers and five CI methods. The byte map in §2.3 is computed from the actual sealed bytes.
2. **Conductor key rotation policy.** If a Conductor key is revoked, do past cycles remain valid? **Recommended default:** cycles are verified against the key state at seal time, recorded in the CWM and bound by the RFC 3161 timestamp; revocation does not retroactively un‑seal. This matches RFC 3161's intent.
3. **Public Codex mirror redundancy.** Single mirror at 5qln.com plus IPFS may not survive long‑term. **Recommended default:** add monthly Bitcoin OP_RETURN anchor; add Internet Archive snapshot weekly.
4. **Multi‑AI consensus threshold for V seal.** 2‑of‑3 or unanimous? **Recommended default:** 2‑of‑3 for routine cycles; unanimous for P.L.4‑adjacent and amendment cycles.
5. **Soft predicate threshold for "UNCERTAIN".** When the Interrogator returns UNCERTAIN repeatedly, escalate to operator or halt the cycle? **Recommended default:** halt and require operator decision after 3 UNCERTAINs on the same predicate within one cycle.
6. **Plugin write quota default.** **Recommended default:** 1 write per cycle per plugin; configurable by Board resolution.
7. **CL4‑GP indicator calibration.** Final Blueprint lists 12 indicators as [SPECULATIVE]. **Recommended default:** instrument all 12 with logging but do not gate any decisions on them until 6 months of operational data exists.
8. **Federation timing.** **Recommended default:** do not start BIPP federation work until Phase 4 has produced 30 verifier‑passing cycles.

### 16.2 Minimum viable Phase 0 ceremony plan (this week)

- **Day 1:** Produce `codex.txt`; run all three verifiers locally; confirm byte identity.
- **Day 2:** Provision YubiHSM 2 primary and cold‑storage; generate Ed25519 keypair; publish public‑key fingerprint at 5qln.com/conductor-keys/v1/.
- **Day 3:** Cross‑verify hash on a clean USB‑booted Linux and a sandboxed CI runner.
- **Day 4:** Convene witnesses (2 human + 1 AI cross‑substrate attestor); each signs the manifest.
- **Day 5:** Obtain RFC 3161 timestamps from FreeTSA + DigiCert; finalise manifest; Conductor signs.
- **Day 6:** Publish to 5qln.com/codex/v1/, push GitHub tag `codex-v1`, pin to IPFS (2+ providers), submit Sigstore Rekor entry.
- **Day 7:** Publish Phase 0 done‑gates checklist with all green; emit Tier‑A "Codex sealed" gliff; this gliff is the parent of every subsequent cycle.

---

## Recommendations (decision‑ready)

1. **Seal Phase 0 this week.** Until the Codex is sealed, every later claim is provisional. The ceremony is two engineer‑days plus operator availability for witnessing.
2. **Branch and merge the realignment PR (§4.2) immediately after Phase 0.** Drift between the public Codex (Appendix A nine‑line ASCII) and the repository (drifted ten‑line superscript) is a structural liability; close it.
3. **Build the compiler in TypeScript first, Rust second.** TypeScript matches the existing `qlnlife/5qln-core` substrate; Rust provides the cross‑validation that resolves the meta‑compiler problem.
4. **Defer Interrogator until at least three hard predicates are passing end‑to‑end.** Soft predicates are the exception; hard predicates carry the structural load. Build the load‑bearing first.
5. **Stand up the AOSRAP wrapper in parallel with Phase 3** (10 engineer‑weeks per the v0.1 spec). The wrapper is independent of Phase 4 and unblocks Foundation‑mode operation.
6. **Do not file with Delaware until Phase 1 of the Codex‑as‑Verifier sequence completes** — one sealed cycle, end‑to‑end, verifier‑passing. Filing without an existence proof is L4‑Performing.
7. **Publish the Phase‑0 manifest, Phase‑1 compiler output, and Phase‑3 verdict log schema as Tier‑A sealed surfaces.** Their parent is the Codex hash; their lineage is the substrate's evidence chain.

### Benchmarks that change the recommendation

- **If Phase 0 cannot seal within 14 days,** the gate is operator availability, not engineering — restructure the ceremony around the operator's calendar; do not let perfection of byte‑count delay sealing.
- **If Phase 1 cannot produce reproducibly‑built predicate sets across two machines within 8 weeks,** the toolchain pinning is the bottleneck — drop Rust, ship TypeScript‑only v1, defer cross‑validation to v2.
- **If Phase 4 cannot produce a verifier‑passing cycle within 90 days of Phase 1 completion,** the architecture is over‑scoped — apply the Subtraction Principle, reduce the verifier to its smallest sufficient core.
- **If AOSRAP vendor RFIs return null after 12 months,** freeze Phase 2 entry of the Foundation Build Plan; extend manual‑attestation fallback indefinitely; reopen the substrate‑independence question (different K‑side partner).
- **If counsel concludes the Duty of Membrane Integrity reads to Delaware as commentary about the instrument rather than part of the instrument,** strategy returns to Phase 3‑engineering and re‑asks how the verifier's structural status can be carried into a future filing, possibly in a different jurisdiction via BIPP delta.

---

## Caveats

- **No Foundation legal entity exists as of compilation date.** Every reference to "the Foundation" presupposes a future Delaware filing. Engineers must mark `mode: personal | foundation` on every artifact; pre‑incorporation cycles tag claims STRUCTURAL‑HYPOTHESIS or LEGAL‑PROSPECTIVE.
- **The three‑ring architecture (E13) is recommendation‑status, not constitutional** — "where this conflicts with the Codex, the Codex governs." The Codex/Compiler/Predicate trio is constitutional; the ring decomposition, the skill layer split, and the plugin protocol may be ratified or declined by a future compiled surface. Do not bake assumptions deep enough that a constitutional decision against three‑ring forces a kernel rewrite.
- **Soft predicates depend on AI judgment.** The architecture mitigates by logging and replaying, not by trusting. UNCERTAIN verdicts must always escalate to the operator.
- **The verifier produces legibility, not defensibility.** Chancery's reception of a verifier verdict as evidence is `[LEGAL‑PROSPECTIVE]` — the first case to test it sets the register for all subsequent compiled‑surface governance instruments.
- **Substrate independence is partially demonstrated.** The TypeScript ↔ Python cross‑language test exists in `qlnlife/5qln-core`'s S8 surface; the Rust port is specified but not built. Substrate independence rides on one TS implementation today.
- **AOSRAP A4 (attention‑state attestation) is `[REQUIRES_PARTNER]`.** The behavioural proxy is acceptable for Phase 0–1; full cryptographic A4 requires LLM vendor cooperation that no major provider currently exposes.
- **34 patterns / 8 exclusions in `membrane-watcher.ts` are heuristic.** They catch obvious corruptions; they do not protect against novel adversarial inputs designed to evade them. Pattern library updates are a continuous CMO responsibility, and each update is a Tier‑2 amendment.
- **Drift is measurable but its operational thresholds (>5% variance, hourly probe cadence) are `[SPECULATIVE]` pending 6+ months of empirical data.** Calibrate before gating decisions on drift values.
- **Visibility is not enforcement; detection is not prevention.** A Board running cycle vocabulary while making decisions through K‑only channels (L4 at scale) reproduces conventional governance under 5QLN window‑dressing. The architecture makes it detectable, not impossible.
- **This document is engineering‑register, Tier‑B.** It does not carry the Constitutional Block on Page One; it is not itself a compiled 5QLN surface. The Codex governs; this plan defers.

— *End of Master Architecture Document v1.0. The next cycle's S is: once Phase 0 seals and Phase 1 produces its first reproducibly‑built predicate set, what does it mean for an architecture to verify its own becoming?*