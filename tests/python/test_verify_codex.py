"""
Comprehensive test suite for the Codex verifier.

Positive test: canonical bytes pass.
Negative tests: 11 specific drift attacks, each must be detected.
"""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CODEX_PATH = REPO_ROOT / "codex" / "codex.txt"
VERIFIER = REPO_ROOT / "tools" / "python" / "verify_codex.py"
CANONICAL_SHA256 = "feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b"


def run_verifier(target: Path) -> tuple[int, str]:
    """Run the verifier and return (exit_code, stdout)."""
    result = subprocess.run(
        [sys.executable, str(VERIFIER), str(target)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout


def write_temp(content: bytes) -> Path:
    """Write content to a temp file and return the path."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


# --- POSITIVE TEST -----------------------------------------------------------

def test_canonical_passes():
    """The canonical codex.txt must produce exit code 0."""
    code, out = run_verifier(CODEX_PATH)
    assert code == 0, f"canonical failed: {out}"
    assert "CONSTITUTIONAL" in out
    assert CANONICAL_SHA256 in out


def test_canonical_hash_matches():
    """Direct hash check against the canonical constant."""
    data = CODEX_PATH.read_bytes()
    assert hashlib.sha256(data).hexdigest() == CANONICAL_SHA256
    assert len(data) == 217


# --- NEGATIVE TESTS ----------------------------------------------------------

def test_bom_rejected():
    """A file with a UTF-8 BOM prepended must fail."""
    data = b"\xef\xbb\xbf" + CODEX_PATH.read_bytes()
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
        # BOM check happens after byte-count check, so we may get 4 or 5
        assert any(s in out for s in ["BOM present", "byte count is"])
    finally:
        tmp.unlink()


def test_crlf_rejected():
    """CRLF line endings must fail."""
    data = CODEX_PATH.read_bytes().replace(b"\n", b"\r\n")
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_paraphrase_rejected():
    """Substituting English for symbols must fail."""
    data = CODEX_PATH.read_bytes().replace("∞0".encode(), b"infzero")
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_intersection_glyph_swap_rejected():
    """Swapping line 5's ⋂ (U+22C2) for ∩ (U+2229) must fail.

    This is the README-master drift attack — the most likely real-world deviation.
    """
    data = CODEX_PATH.read_bytes()
    # Replace the ⋂ on line 5 with ∩
    data2 = data.replace("⋂".encode("utf-8"), "∩".encode("utf-8"), 1)
    assert data != data2  # ensure we actually changed something
    tmp = write_temp(data2)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_corruption_code_superscript_rejected():
    """Swapping ASCII L1 for superscript L¹ on line 9 must fail.

    This is the TypeScript library drift attack.
    """
    data = CODEX_PATH.read_bytes().replace(b"L1 ", "L¹ ".encode("utf-8"), 1)
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_subscript_zero_rejected():
    """Swapping digit zero for subscript ₀ on line 1 must fail."""
    data = CODEX_PATH.read_bytes().replace("∞0".encode("utf-8"), "∞₀".encode("utf-8"), 1)
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_typographic_prime_rejected():
    """Swapping ASCII apostrophe ' for typographic prime ′ must fail."""
    data = CODEX_PATH.read_bytes().replace(b"'", "′".encode("utf-8"))
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_trailing_whitespace_rejected():
    """Adding a trailing space to any line must fail."""
    raw = CODEX_PATH.read_bytes()
    # Add a space before the LF after line 1
    idx = raw.index(b"\n")
    data = raw[:idx] + b" " + raw[idx:]
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_missing_trailing_lf_rejected():
    """File without final LF must fail."""
    data = CODEX_PATH.read_bytes().rstrip(b"\n")
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_double_trailing_lf_rejected():
    """File with two trailing LFs must fail."""
    data = CODEX_PATH.read_bytes() + b"\n"
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_truncation_rejected():
    """File truncated at line 8 (no line 9) must fail."""
    lines = CODEX_PATH.read_bytes().split(b"\n")
    data = b"\n".join(lines[:8]) + b"\n"
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_holographic_line_inserted_rejected():
    """Inserting the README's ten-line variant (XY := X within Y line) must fail."""
    raw = CODEX_PATH.read_bytes()
    lines = raw.decode("utf-8").split("\n")
    # Insert a fake line 8 (README's holographic insertion)
    fake = lines[:7] + ["8.  XY := X within Y, X,Y ∈ {S,G,Q,P,V}"] + lines[7:]
    data = "\n".join(fake).encode("utf-8")
    tmp = write_temp(data)
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


def test_single_bit_flip_rejected():
    """Flipping a single byte must fail (catches the strongest defense — hash collision is infeasible)."""
    data = bytearray(CODEX_PATH.read_bytes())
    data[10] = (data[10] ^ 0x01) & 0xFF  # flip lowest bit of byte 10
    tmp = write_temp(bytes(data))
    try:
        code, out = run_verifier(tmp)
        assert code != 0
    finally:
        tmp.unlink()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
