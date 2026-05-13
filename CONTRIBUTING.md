# Contributing

Thank you for caring about this work. A few things to know.

## What is constitutional vs what is variable

**Constitutional (cannot be changed without ratification):**

- `codex/codex.txt` — the 217 canonical bytes
- `codex/CANONICAL_FORM.md` — the glyph decisions
- The SHA-256 hash referenced in verifiers
- The manifest schema in `manifest/manifest.schema.json`

**Variable (can be improved by PR):**

- All code in `tools/`, `kernel/`, `interrogator/`, `write-gate/`
- All documentation outside the constitutional set above
- All files in `narrative/` (Tier-B records — can be amended through ordinary PR workflow)
- Test fixtures and test suites
- CI/CD configuration

A PR that changes a constitutional file requires the V.L.5(b) tri-condition gate (see [`GOVERNANCE.md`](GOVERNANCE.md)) and is not a normal contribution.

## How to contribute

### Bug reports

Open a GitHub issue. Include:

- The verifier exit code (Python/Rust/Node, whichever you used)
- The byte count of your `codex.txt`
- The SHA-256 you computed
- Steps to reproduce

If you found a verification *false positive* (verifier rejects a file that should pass) or *false negative* (verifier accepts a file that should fail) — this is a high-priority bug. Tag the issue `[verification-defect]`.

### Pull requests

- Run `python3 -m pytest tests/python/` before submitting; all tests must pass
- Sign your commits (`git commit -S`)
- Add a test for any new behavior
- Do not modify constitutional files (above)
- Open as a draft if you want feedback before completion

### New verifier implementations

Welcome. To add a verifier in language X:

1. Create `tools/x/` directory
2. Implement the same 11 checks as the Python/Rust/Node reference (canonical hashes, byte count, BOM, CRLF, trailing whitespace, line count, trailing LF, byte identity, SHA-256, SHA-512, BLAKE2b)
3. Use the same exit codes (0 = constitutional, 1 = SHA-256 mismatch, etc.)
4. Add a test that runs your verifier and confirms it passes on the canonical and fails on each negative fixture
5. Update `manifest/manifest.json` to list your verifier under `verifiers`
6. Update README's "Verify in three ways" section to include yours

The whole point of multi-language verifiers is **independent** implementations. Don't copy the Python reference and translate it; read the spec in [`specs/MASTER_ARCHITECTURE.md`](specs/MASTER_ARCHITECTURE.md) §2.4 and implement from scratch.

## What this project is not

- Not an AI agent framework (though it can host one)
- Not a smart-contract platform (though it has on-chain anchoring)
- Not a constitutional convention (the constitution is already written)
- Not the place to debate 5QLN's philosophy (use the 5qln.com substack)

This is engineering work in service of a constitutional artifact. The constitution comes first.

## Pre-incorporation status

The 5QLN Foundation legal entity does not yet exist. All contributions are made under the operator's personal capacity / Anti Entropy fiscal sponsorship cover. Contributors retain copyright in their contributions, licensed under Apache 2.0 (this repository) and the [5QLN Open Source License](https://www.5qln.com/5qln-open-source-license/) (for any Codex-derived material).

## Conduct

Be specific. Be technical. Be honest about uncertainty. The work is serious; the register should be too.

The membrane between human and AI is structural. Treat the AI as a sensor in PRs (when reviewing AI-generated contributions, the AI's verdict is logged and reviewable; never authoritative). Treat humans as judges. Don't conflate.

## License

Contributions are licensed under Apache 2.0 unless otherwise stated. See [`LICENSE`](LICENSE).

### Narrative contributions

Files in `narrative/` are Tier-B Structured Records. They can be amended through
ordinary PR workflow. Guidelines:

- Load-bearing numerical claims (Codex hash, byte count) must match `codex/codex.txt`
- Epistemic register tags are required on any claim that could be mistaken for authority
- Mirror discipline: if you change narrative prose, the 5qln.com mirror should be
  updated to match (or the drift documented as intentional — pre-incorporation,
  a weekly comparison check is sufficient)
- Prose improvements (clarity, accuracy, corrections) are welcome
- Substantive reinterpretation of the architecture belongs in `specs/`, not narrative
