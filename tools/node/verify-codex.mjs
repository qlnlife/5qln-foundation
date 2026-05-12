#!/usr/bin/env node
/**
 * verify-codex.mjs — 5QLN Codex anchor verifier (Node 20+ reference).
 *
 * Deterministic. AI-free. Network-free.
 * Third independent implementation alongside Python and Rust references.
 *
 * Exit codes mirror the Python and Rust verifiers:
 *   0  constitutional        4  byte count mismatch
 *   1  sha256 mismatch       5  BOM detected
 *   2  sha512 mismatch       6  non-LF line ending
 *   3  blake2b mismatch      7  trailing whitespace
 *   8  wrong line count      9  trailing LF problem
 *  10  file not readable    64  internal error
 */
import { readFile } from "node:fs/promises";
import { createHash, timingSafeEqual } from "node:crypto";
import { resolve } from "node:path";
import process from "node:process";

const CANONICAL_SHA256 =
  "feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b";
const CANONICAL_SHA512 =
  "2b6e81c0c49193c9d4ceda3b9b7fa1e7f9639a032fdd184b8958e2e2810fbf8c" +
  "5dfde5c4fae9a534884d9c257e9f25ef4462a2a0d1de6a52601cd21d807f8cb0";
const CANONICAL_BLAKE2B =
  "229c5adce88bf8e737deb8eb4440ce3719b1953633abfc7f2fa487ffa201d854" +
  "865293d911c1be5d14bb7294eca2c4e4a445e6c8d62caa0c8868a354d14cb42d";

const EXPECTED_BYTES = 217;
const EXPECTED_LINES = 9;

const CANONICAL_LINES = [
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

function canonicalBytes() {
  return Buffer.from(CANONICAL_LINES.join("\n") + "\n", "utf8");
}

function ctEq(a, b) {
  if (a.length !== b.length) return false;
  return timingSafeEqual(Buffer.from(a), Buffer.from(b));
}

function verify(raw) {
  const findings = [];

  // 1. Byte count
  if (raw.length !== EXPECTED_BYTES) {
    findings.push(`FAIL: byte count is ${raw.length}, expected ${EXPECTED_BYTES}`);
    return { code: 4, findings };
  }
  findings.push(`PASS: byte count = ${EXPECTED_BYTES}`);

  // 2. BOM
  if (raw[0] === 0xef && raw[1] === 0xbb && raw[2] === 0xbf) {
    findings.push("FAIL: BOM present");
    return { code: 5, findings };
  }
  findings.push("PASS: no BOM");

  // 3. Line endings
  if (raw.includes(Buffer.from("\r\n")) || raw.includes(0x0d)) {
    findings.push("FAIL: CR/CRLF detected");
    return { code: 6, findings };
  }
  findings.push("PASS: LF only");

  // 4. Trailing whitespace
  const lines = raw.toString("utf8").split("\n");
  const bad = lines
    .map((ln, i) => ({ ln, i }))
    .filter(({ ln }) => ln.endsWith(" ") || ln.endsWith("\t"))
    .map(({ i }) => i);
  if (bad.length > 0) {
    findings.push(`FAIL: trailing whitespace on line(s) ${JSON.stringify(bad)}`);
    return { code: 7, findings };
  }
  findings.push("PASS: no trailing whitespace");

  // 5. Line count
  const contentLines = lines.filter((l) => l.length > 0);
  if (contentLines.length !== EXPECTED_LINES) {
    findings.push(
      `FAIL: line count is ${contentLines.length}, expected ${EXPECTED_LINES}`,
    );
    return { code: 8, findings };
  }
  findings.push(`PASS: ${EXPECTED_LINES} invariant lines`);

  // 6. Trailing LF
  if (raw[raw.length - 1] !== 0x0a) {
    findings.push("FAIL: must end with LF");
    return { code: 9, findings };
  }
  if (raw[raw.length - 2] === 0x0a) {
    findings.push("FAIL: multiple trailing LFs");
    return { code: 9, findings };
  }
  findings.push("PASS: exactly one trailing LF");

  // 7. Byte identity
  const expected = canonicalBytes();
  if (!ctEq(raw, expected)) {
    findings.push("FAIL: bytes do not match canonical");
    return { code: 1, findings };
  }
  findings.push("PASS: byte-identical to canonical");

  // 8. SHA-256
  const sha256 = createHash("sha256").update(raw).digest("hex");
  if (!ctEq(sha256, CANONICAL_SHA256)) {
    findings.push(`FAIL: SHA-256 mismatch (got ${sha256})`);
    return { code: 1, findings };
  }
  findings.push(`PASS: SHA-256 = ${sha256}`);

  // 9. SHA-512
  const sha512 = createHash("sha512").update(raw).digest("hex");
  if (!ctEq(sha512, CANONICAL_SHA512)) {
    findings.push("FAIL: SHA-512 mismatch");
    return { code: 2, findings };
  }
  findings.push("PASS: SHA-512 verified");

  // 10. BLAKE2b-512
  const blake = createHash("blake2b512").update(raw).digest("hex");
  if (!ctEq(blake, CANONICAL_BLAKE2B)) {
    findings.push("FAIL: BLAKE2b mismatch");
    return { code: 3, findings };
  }
  findings.push("PASS: BLAKE2b verified");

  return { code: 0, findings };
}

async function main() {
  const path = process.argv[2] ?? "codex/codex.txt";
  console.log("=== 5QLN Codex Verifier (Node reference) ===");
  console.log(`Target: ${resolve(path)}`);
  console.log();

  let raw;
  try {
    raw = await readFile(path);
  } catch (err) {
    console.error(`FAIL: cannot read ${path}: ${err.message}`);
    process.exit(10);
  }

  const { code, findings } = verify(raw);
  for (const f of findings) console.log(`  ${f}`);
  console.log();
  if (code === 0) {
    console.log("RESULT: CONSTITUTIONAL — canonical form verified.");
  } else {
    console.log(`RESULT: NON-CONSTITUTIONAL — failure code ${code}`);
  }
  process.exit(code);
}

main().catch((err) => {
  console.error(`INTERNAL ERROR: ${err.message}`);
  process.exit(64);
});
