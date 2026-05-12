#!/usr/bin/env python3
"""
verify_codex.py — Production verifier for the 5QLN Foundation Codex anchor.

Deterministic. AI-free. Network-free.
Verifies byte-identity of codex.txt against the canonical form.

Exit codes:
    0   constitutional — all checks pass
    1   sha256 mismatch
    2   sha512 mismatch
    3   blake2b mismatch
    4   byte count mismatch
    5   BOM detected
    6   non-LF line ending detected
    7   trailing whitespace detected
    8   wrong line count
    9   no trailing LF / extra trailing LF
   10   file not readable
   64   verifier-internal error
"""
from __future__ import annotations
import hashlib
import hmac
import sys
from pathlib import Path

# --- CANONICAL DEFINITION -----------------------------------------------------
# These hashes are computed against the canonical bytes shipped in codex/codex.txt.
# If the canonical file ever changes, all three of these must be recomputed
# AND a new manifest produced AND the Codex must be re-signed by the Conductor.

CANONICAL_SHA256 = "feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b"
CANONICAL_SHA512 = (
    "2b6e81c0c49193c9d4ceda3b9b7fa1e7f9639a032fdd184b8958e2e2810fbf8c"
    "5dfde5c4fae9a534884d9c257e9f25ef4462a2a0d1de6a52601cd21d807f8cb0"
)
CANONICAL_BLAKE2B = (
    "229c5adce88bf8e737deb8eb4440ce3719b1953633abfc7f2fa487ffa201d854"
    "865293d911c1be5d14bb7294eca2c4e4a445e6c8d62caa0c8868a354d14cb42d"
)
EXPECTED_BYTES = 217
EXPECTED_LINES = 9


# --- CANONICAL BYTES (used for byte-identity test) ---------------------------
# These are the nine invariant lines per Codex Appendix A, with the glyph
# decisions documented in /codex/CANONICAL_FORM.md.
CANONICAL_LINES = (
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
    """Build the canonical byte sequence from the line tuple above."""
    return ("\n".join(CANONICAL_LINES) + "\n").encode("utf-8")


def hexdump_diff(actual: bytes, expected: bytes, max_lines: int = 8) -> str:
    """Produce a short hex-and-ascii diff for the first divergent region."""
    out = []
    n = max(len(actual), len(expected))
    for offset in range(0, n, 16):
        a = actual[offset:offset + 16]
        e = expected[offset:offset + 16]
        if a == e and len(out) >= max_lines:
            break
        marker = " " if a == e else "*"
        out.append(
            f"  {marker} {offset:08x}  "
            f"actual:   {a.hex(' '):<48s}  |{_printable(a):<16s}|\n"
            f"             expected: {e.hex(' '):<48s}  |{_printable(e):<16s}|"
        )
        if len(out) >= max_lines:
            out.append("  ... (truncated)")
            break
    return "\n".join(out)


def _printable(b: bytes) -> str:
    return "".join(chr(c) if 0x20 <= c < 0x7F else "." for c in b)


def verify(path: Path) -> tuple[int, list[str]]:
    """Run all checks. Return (exit_code, list_of_findings)."""
    findings: list[str] = []
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return 10, [f"FAIL: cannot read {path}: {exc}"]

    # 1. Byte count
    if len(raw) != EXPECTED_BYTES:
        findings.append(f"FAIL: byte count is {len(raw)}, expected {EXPECTED_BYTES}")
        return 4, findings + ["  diff:\n" + hexdump_diff(raw, canonical_bytes())]
    findings.append(f"PASS: byte count = {EXPECTED_BYTES}")

    # 2. BOM
    if raw.startswith(b"\xef\xbb\xbf"):
        findings.append("FAIL: BOM present (must be absent)")
        return 5, findings
    findings.append("PASS: no BOM")

    # 3. Line endings
    if b"\r\n" in raw or b"\r" in raw:
        findings.append("FAIL: CR or CRLF detected (must be LF only)")
        return 6, findings
    findings.append("PASS: LF only")

    # 4. Trailing whitespace per line
    bad = [i for i, ln in enumerate(raw.split(b"\n")) if ln.endswith((b" ", b"\t"))]
    if bad:
        findings.append(f"FAIL: trailing whitespace on line(s) {bad}")
        return 7, findings
    findings.append("PASS: no trailing whitespace")

    # 5. Line count
    lines = [ln for ln in raw.split(b"\n") if ln]
    if len(lines) != EXPECTED_LINES:
        findings.append(f"FAIL: content line count is {len(lines)}, expected {EXPECTED_LINES}")
        return 8, findings
    findings.append(f"PASS: {EXPECTED_LINES} invariant lines")

    # 6. Trailing LF
    if not raw.endswith(b"\n"):
        findings.append("FAIL: file must end with LF")
        return 9, findings
    if raw.endswith(b"\n\n"):
        findings.append("FAIL: multiple trailing LFs (must be exactly one)")
        return 9, findings
    findings.append("PASS: exactly one trailing LF")

    # 7. Byte identity to in-source canonical
    expected = canonical_bytes()
    if not hmac.compare_digest(raw, expected):
        findings.append("FAIL: bytes do not match canonical form")
        findings.append("  diff:\n" + hexdump_diff(raw, expected))
        return 1, findings
    findings.append("PASS: byte-identical to canonical")

    # 8. SHA-256 verification (constant-time)
    sha256 = hashlib.sha256(raw).hexdigest()
    if not hmac.compare_digest(sha256, CANONICAL_SHA256):
        findings.append(f"FAIL: SHA-256 mismatch")
        findings.append(f"      expected: {CANONICAL_SHA256}")
        findings.append(f"      actual:   {sha256}")
        return 1, findings
    findings.append(f"PASS: SHA-256 = {sha256}")

    # 9. SHA-512 verification (constant-time)
    sha512 = hashlib.sha512(raw).hexdigest()
    if not hmac.compare_digest(sha512, CANONICAL_SHA512):
        findings.append(f"FAIL: SHA-512 mismatch")
        findings.append(f"      expected: {CANONICAL_SHA512}")
        findings.append(f"      actual:   {sha512}")
        return 2, findings
    findings.append(f"PASS: SHA-512 verified")

    # 10. BLAKE2b verification (constant-time)
    blake = hashlib.blake2b(raw).hexdigest()
    if not hmac.compare_digest(blake, CANONICAL_BLAKE2B):
        findings.append(f"FAIL: BLAKE2b mismatch")
        findings.append(f"      expected: {CANONICAL_BLAKE2B}")
        findings.append(f"      actual:   {blake}")
        return 3, findings
    findings.append(f"PASS: BLAKE2b verified")

    return 0, findings


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("codex/codex.txt")
    print(f"=== 5QLN Codex Verifier (Python reference) ===")
    print(f"Target: {path.resolve()}")
    print()
    try:
        code, findings = verify(path)
        for f in findings:
            print(f"  {f}")
        print()
        if code == 0:
            print("RESULT: CONSTITUTIONAL — canonical form verified.")
        else:
            print(f"RESULT: NON-CONSTITUTIONAL — failure code {code}")
        return code
    except Exception as exc:  # pragma: no cover
        print(f"INTERNAL ERROR: {exc}", file=sys.stderr)
        return 64


if __name__ == "__main__":
    sys.exit(main())
