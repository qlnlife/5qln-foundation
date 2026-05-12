# Canonical Form — Glyph Decisions

This document records every editorial decision behind the 217 canonical bytes of `codex.txt`. Each decision is traced to its source. The decisions cannot be changed without amending the Codex itself (Bylaws V.L.5(b) tri-condition gate).

## File-level form

| Property | Value | Rationale |
|---|---|---|
| Encoding | UTF-8 | Codex Appendix A canonical encoding |
| Line ending | LF only (0x0A) | POSIX convention; BIPP from Codex-as-Verifier §III.1 |
| Byte-order mark | absent | UTF-8 BOM is optional and creates parser inconsistency |
| Trailing newline | exactly one LF | POSIX text-file convention |
| Total byte count | 217 | Ceremony-produced, derived from glyph decisions below |
| Line count | 9 | Codex Appendix A "Nine Invariant Lines" |

## Per-line content

```
Line 1:  1.  H = ∞0 | A = K
Line 2:  2.  S → G → Q → P → V
Line 3:  3.  S = ∞0 → ?
Line 4:  4.  G = α ≡ {α'}
Line 5:  5.  Q = φ ⋂ Ω
Line 6:  6.  P = δE/δV → ∇
Line 7:  7.  V = (L ∩ G → B'') → ∞0'
Line 8:  8.  No V without ∞0'
Line 9:  9.  L1  L2  L3  L4  V∅
```

Each line begins with `N.␣␣` (digit, period, two spaces) and terminates with LF.

## Symbol-level decisions

| Symbol | Codepoint | Where used | Rationale |
|---|---|---|---|
| `∞` | U+221E | Lines 1, 3, 7, 8 | Codex Appendix A canonical |
| `0` (digit zero) | U+0030 | `∞0` and `∞0'` | All Codex equation renderings use digit zero, not subscript ₀ (U+2080) |
| `→` (rightward arrow) | U+2192 | Lines 2, 3, 6, 7 | All Codex equations |
| `α` (alpha) | U+03B1 | Line 4 (twice) | All Codex equations |
| `≡` (identity) | U+2261 | Line 4 | All Codex equations |
| `'` (ASCII apostrophe) | U+0027 | Lines 4, 7, 8 (prime marks) | All Codex equation renderings use ASCII apostrophe, not typographic prime ′ (U+2032) |
| `φ` (phi) | U+03C6 | Line 5 | All Codex equations |
| `⋂` (N-ary intersection) | U+22C2 | **Line 5 only** | Codex Appendix A line 5 explicitly uses N-ary form (operator/concept) |
| `Ω` (omega) | U+03A9 | Line 5 | All Codex equations |
| `δ` (delta) | U+03B4 | Line 6 (twice) | All Codex equations |
| `∇` (nabla / gradient) | U+2207 | Line 6 | All Codex equations |
| `∩` (binary intersection) | U+2229 | **Line 7 only** | Codex Appendix A line 7 explicitly uses binary form (operation between two named operands L and G) |
| `''` (two ASCII apostrophes) | U+0027 × 2 | Line 7 (B'' artifact) | All Codex equation renderings; not double-prime ″ (U+2033) |
| `∅` (empty set) | U+2205 | Line 9 (V∅) | Standard Codex notation |

## Two intentional within-document features

These look like inconsistencies but are intentional and load-bearing:

1. **Line 5 uses ⋂ (U+22C2) while line 7 uses ∩ (U+2229).** This is preserved from Codex Appendix A. Line 5 names the *operation* (Natural Intersection as an N-ary type — `Q = φ ⋂ Ω` describes how perception meets potential); line 7 invokes the *binary meet* between two specific named operands (L and G). The visual difference is meaningful and reflects the Codex's deliberate distinction. Do not unify.

2. **Line 9 uses ASCII corruption codes** (`L1 L2 L3 L4 V∅`), not Unicode superscripts (`L¹ L² L³ L⁴`). The published Codex Appendix A is ASCII-canonical. The qlnlife/5qln-core TypeScript library currently uses superscripts and is in **declared drift** from this canon. Phase 2 of the build plan realigns the library; in the interim, the library's runtime watcher includes a one-line aliasing map so its 34 detection patterns continue to function (`L¹ ↔ L1`, etc.).

## Drifts to detect

The test suite at `tests/python/test_verify_codex.py` includes negative tests for every plausible drift. Drifts that must be rejected:

- BOM prepended
- CRLF line endings
- Paraphrase (English substituted for symbols)
- Line 5 ⋂ swapped for ∩ (or vice versa)
- ASCII corruption codes swapped for superscripts
- Digit zero swapped for subscript ₀
- ASCII apostrophe swapped for typographic prime ′
- Trailing whitespace
- Missing trailing LF
- Multiple trailing LFs
- Truncation (missing line 9)
- Insertion (README's holographic "Ten Invariant Lines" form)
- Single bit flip

All thirteen drift vectors are tested and rejected with distinct exit codes.

## Modification protocol

This canonical form may not be modified except by the Bylaws V.L.5(b) tri-condition gate (unanimous Director vote + contemporaneously documented finding under one of three enumerated grounds + Board-adopted procedures). Routine documentation edits to surrounding files do not require ratification. Any change to a single byte of `codex.txt` requires:

1. Constitutional amendment per V.L.5(b)
2. Fresh manifest with new hashes
3. New Phase 0 ceremony (witness signatures, RFC 3161 timestamps, Sigstore Rekor entry)
4. Version bump (v1 → v2)
5. New publication at canonical URL with old version preserved for backward compatibility

A cycle sealed against `codex.txt` v1 remains verifiable against v1 forever; v2 cycles verify against v2. The verifier accepts a `--codex-version` flag and refuses cross-version verdicts silently.

— *End of canonical form documentation. The bytes are the truth.*
