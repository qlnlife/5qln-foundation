//! verify-codex — 5QLN Codex anchor verifier (Rust reference).
//!
//! Deterministic. AI-free. Network-free.
//! Cross-implementation defense against single-language bugs.
//!
//! Exit codes mirror the Python reference verifier:
//!   0  constitutional       4  byte count mismatch
//!   1  sha256 mismatch      5  BOM detected
//!   2  sha512 mismatch      6  non-LF line ending
//!   3  blake2b mismatch     7  trailing whitespace
//!   8  wrong line count     9  no trailing LF / extra trailing LF
//!  10  file not readable   64  internal error

use std::{env, fs, path::PathBuf, process::ExitCode};

use blake2::{Blake2b512, Digest as Blake2Digest};
use ring::{constant_time, digest};

/// Canonical SHA-256 of the codex.txt shipped in /codex/
const CANONICAL_SHA256: &str =
    "feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b";

/// Canonical SHA-512
const CANONICAL_SHA512: &str = concat!(
    "2b6e81c0c49193c9d4ceda3b9b7fa1e7f9639a032fdd184b8958e2e2810fbf8c",
    "5dfde5c4fae9a534884d9c257e9f25ef4462a2a0d1de6a52601cd21d807f8cb0"
);

/// Canonical BLAKE2b-512
const CANONICAL_BLAKE2B: &str = concat!(
    "229c5adce88bf8e737deb8eb4440ce3719b1953633abfc7f2fa487ffa201d854",
    "865293d911c1be5d14bb7294eca2c4e4a445e6c8d62caa0c8868a354d14cb42d"
);

const EXPECTED_BYTES: usize = 217;
const EXPECTED_LINES: usize = 9;

/// Canonical line content — Codex Appendix A, exact glyph decisions.
const CANONICAL_LINES: &[&str] = &[
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
    let mut s = CANONICAL_LINES.join("\n");
    s.push('\n');
    s.into_bytes()
}

fn hex(bytes: &[u8]) -> String {
    let mut s = String::with_capacity(bytes.len() * 2);
    for b in bytes {
        s.push_str(&format!("{:02x}", b));
    }
    s
}

fn ct_eq(a: &[u8], b: &[u8]) -> bool {
    a.len() == b.len() && constant_time::verify_slices_are_equal(a, b).is_ok()
}

fn verify(raw: &[u8]) -> (u8, Vec<String>) {
    let mut findings = Vec::new();

    // 1. Byte count
    if raw.len() != EXPECTED_BYTES {
        findings.push(format!(
            "FAIL: byte count is {}, expected {}",
            raw.len(),
            EXPECTED_BYTES
        ));
        return (4, findings);
    }
    findings.push(format!("PASS: byte count = {}", EXPECTED_BYTES));

    // 2. BOM
    if raw.starts_with(&[0xEF, 0xBB, 0xBF]) {
        findings.push("FAIL: BOM present".into());
        return (5, findings);
    }
    findings.push("PASS: no BOM".into());

    // 3. Line endings
    if raw.windows(2).any(|w| w == b"\r\n") || raw.contains(&b'\r') {
        findings.push("FAIL: CR/CRLF detected".into());
        return (6, findings);
    }
    findings.push("PASS: LF only".into());

    // 4. Trailing whitespace per line
    let bad: Vec<usize> = raw
        .split(|&b| b == b'\n')
        .enumerate()
        .filter(|(_, ln)| ln.last().is_some_and(|&b| b == b' ' || b == b'\t'))
        .map(|(i, _)| i)
        .collect();
    if !bad.is_empty() {
        findings.push(format!("FAIL: trailing whitespace on lines {:?}", bad));
        return (7, findings);
    }
    findings.push("PASS: no trailing whitespace".into());

    // 5. Line count
    let lines: Vec<&[u8]> = raw.split(|&b| b == b'\n').filter(|l| !l.is_empty()).collect();
    if lines.len() != EXPECTED_LINES {
        findings.push(format!(
            "FAIL: line count is {}, expected {}",
            lines.len(),
            EXPECTED_LINES
        ));
        return (8, findings);
    }
    findings.push(format!("PASS: {} invariant lines", EXPECTED_LINES));

    // 6. Trailing LF
    if !raw.ends_with(b"\n") || raw.ends_with(b"\n\n") {
        findings.push("FAIL: must end with exactly one LF".into());
        return (9, findings);
    }
    findings.push("PASS: exactly one trailing LF".into());

    // 7. Byte identity
    let expected = canonical_bytes();
    if !ct_eq(raw, &expected) {
        findings.push("FAIL: bytes do not match canonical".into());
        return (1, findings);
    }
    findings.push("PASS: byte-identical to canonical".into());

    // 8. SHA-256
    let sha256 = digest::digest(&digest::SHA256, raw);
    let sha256_hex = hex(sha256.as_ref());
    if !ct_eq(sha256_hex.as_bytes(), CANONICAL_SHA256.as_bytes()) {
        findings.push(format!("FAIL: SHA-256 mismatch (got {})", sha256_hex));
        return (1, findings);
    }
    findings.push(format!("PASS: SHA-256 = {}", sha256_hex));

    // 9. SHA-512
    let sha512 = digest::digest(&digest::SHA512, raw);
    let sha512_hex = hex(sha512.as_ref());
    if !ct_eq(sha512_hex.as_bytes(), CANONICAL_SHA512.as_bytes()) {
        findings.push("FAIL: SHA-512 mismatch".into());
        return (2, findings);
    }
    findings.push("PASS: SHA-512 verified".into());

    // 10. BLAKE2b
    let mut hasher = Blake2b512::new();
    hasher.update(raw);
    let blake = hex(&hasher.finalize());
    if !ct_eq(blake.as_bytes(), CANONICAL_BLAKE2B.as_bytes()) {
        findings.push("FAIL: BLAKE2b mismatch".into());
        return (3, findings);
    }
    findings.push("PASS: BLAKE2b verified".into());

    (0, findings)
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    let path = if args.len() > 1 {
        PathBuf::from(&args[1])
    } else {
        PathBuf::from("codex/codex.txt")
    };

    println!("=== 5QLN Codex Verifier (Rust reference) ===");
    println!("Target: {}", path.display());
    println!();

    let raw = match fs::read(&path) {
        Ok(b) => b,
        Err(e) => {
            eprintln!("FAIL: cannot read {}: {}", path.display(), e);
            return ExitCode::from(10);
        }
    };

    let (code, findings) = verify(&raw);
    for f in &findings {
        println!("  {}", f);
    }
    println!();
    if code == 0 {
        println!("RESULT: CONSTITUTIONAL — canonical form verified.");
    } else {
        println!("RESULT: NON-CONSTITUTIONAL — failure code {}", code);
    }
    ExitCode::from(code)
}
