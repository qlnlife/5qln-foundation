#!/usr/bin/env bash
#
# seal-phase-0.sh — 5QLN Foundation Phase 0 ceremony helper
#
# This script walks the operator through the Phase 0 sealing ceremony.
# It does NOT sign anything; signing is on the YubiHSM 2 device by the Conductor.
# It DOES verify, report, and prepare the ceremony record.
#
# Usage:
#   ./scripts/seal-phase-0.sh                  # interactive walkthrough
#   ./scripts/seal-phase-0.sh --verify-only    # just run verifiers, no ceremony
#   ./scripts/seal-phase-0.sh --gate N         # check status of specific gate
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX="$REPO_ROOT/codex/codex.txt"
MANIFEST="$REPO_ROOT/manifest/manifest.json"

CANONICAL_SHA256="feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b"
CANONICAL_BYTES=217

# Colors
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
BOLD=$'\033[1m'
RESET=$'\033[0m'

print_header() {
  echo
  echo "${BOLD}$1${RESET}"
  echo "${BOLD}$(printf '═%.0s' $(seq 1 ${#1}))${RESET}"
}

pass() { echo "  ${GREEN}✓${RESET}  $1"; }
fail() { echo "  ${RED}✗${RESET}  $1"; }
warn() { echo "  ${YELLOW}!${RESET}  $1"; }
info() { echo "  ${BLUE}i${RESET}  $1"; }

print_banner() {
  cat <<'EOF'

    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         5QLN Foundation — Phase 0 Sealing Ceremony           ║
    ║                                                              ║
    ║    The Codex is static law.                                  ║
    ║    The Membrane is dynamic event.                            ║
    ║    The runtime is the act of becoming.                       ║
    ║                                                              ║
    ║    Sealing is the moment law becomes physics.                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

EOF
}

check_gate_01() {
  print_header "Gate 1 — Canonical bytes produced"
  if [ ! -f "$CODEX" ]; then
    fail "codex.txt not found at $CODEX"
    return 1
  fi
  pass "codex.txt exists at $CODEX"

  local bytes
  bytes=$(wc -c < "$CODEX" | tr -d ' ')
  if [ "$bytes" = "$CANONICAL_BYTES" ]; then
    pass "byte count = $bytes"
  else
    fail "byte count = $bytes (expected $CANONICAL_BYTES)"
    return 1
  fi

  if file "$CODEX" | grep -q 'UTF-8'; then
    pass "UTF-8 encoded"
  else
    warn "file(1) does not report UTF-8 — check manually"
  fi

  return 0
}

check_gate_02() {
  print_header "Gate 2 — Hash agreement across implementations"

  # Implementation 1: Python verifier
  if command -v python3 > /dev/null; then
    if python3 "$REPO_ROOT/tools/python/verify_codex.py" "$CODEX" > /dev/null 2>&1; then
      pass "Python reference verifier (hashlib)"
    else
      fail "Python verifier disagrees"
      return 1
    fi
  else
    warn "python3 not installed; skipping Python verifier"
  fi

  # Implementation 2: Node verifier
  if command -v node > /dev/null; then
    if node "$REPO_ROOT/tools/node/verify-codex.mjs" "$CODEX" > /dev/null 2>&1; then
      pass "Node reference verifier (crypto)"
    else
      fail "Node verifier disagrees"
      return 1
    fi
  else
    warn "node not installed; skipping Node verifier"
  fi

  # Implementation 3: coreutils sha256sum
  if command -v sha256sum > /dev/null; then
    local actual
    actual=$(sha256sum "$CODEX" | awk '{print $1}')
    if [ "$actual" = "$CANONICAL_SHA256" ]; then
      pass "coreutils sha256sum"
    else
      fail "sha256sum disagrees: $actual"
      return 1
    fi
  elif command -v shasum > /dev/null; then
    local actual
    actual=$(shasum -a 256 "$CODEX" | awk '{print $1}')
    if [ "$actual" = "$CANONICAL_SHA256" ]; then
      pass "shasum -a 256"
    else
      fail "shasum disagrees: $actual"
      return 1
    fi
  fi

  # Implementation 4: openssl
  if command -v openssl > /dev/null; then
    local actual
    actual=$(openssl dgst -sha256 "$CODEX" | awk '{print $NF}')
    if [ "$actual" = "$CANONICAL_SHA256" ]; then
      pass "openssl dgst -sha256"
    else
      fail "openssl disagrees: $actual"
      return 1
    fi
  fi

  info "Canonical SHA-256: $CANONICAL_SHA256"
  return 0
}

check_gate_03_04() {
  print_header "Gates 3 & 4 — YubiHSM 2 provisioning"
  warn "YubiHSM 2 provisioning is a manual operator step"
  info "Required: primary YubiHSM 2, on-device Ed25519 keypair generation"
  info "Required: cold-storage backup in physically separate location"
  info "Document the ceremony as a Tier-B record before proceeding"

  if command -v yubihsm-shell > /dev/null; then
    pass "yubihsm-shell present"
  else
    warn "yubihsm-shell not installed (acquire from Yubico)"
  fi

  return 0
}

check_gate_05() {
  print_header "Gate 5 — Conductor public-key publication"
  warn "Conductor public-key publication is a manual operator step"
  info "Publish at: https://5qln.foundation/conductor-keys/v1/"
  info "Format: SSH-style fingerprint + PEM + Cosign signature"
  info "Mirror to ≥1 IPFS pinning service"
  return 0
}

check_gate_06() {
  print_header "Gate 6 — Three witness signatures"
  warn "Witness signatures are a manual operator step"
  info "Required: 2 human witnesses + 1 AI cross-substrate attestor"
  info "Each witness uses a DIFFERENT verifier (Python/Rust/Node)"
  info "Each witness inspects bytes via xxd codex/codex.txt"
  info "Each witness signs the manifest's hashes object after JCS canonicalisation"
  return 0
}

check_gate_07() {
  print_header "Gate 7 — RFC 3161 timestamps"
  warn "RFC 3161 timestamp acquisition is a manual operator step"
  info "Primary: https://freetsa.org/tsr"
  info "Backup:  https://timestamp.digicert.com"
  info "Embed tokens in manifest.tsa_timestamps array"

  if command -v openssl > /dev/null; then
    pass "openssl present (can verify tokens with: openssl ts -verify)"
  else
    warn "openssl not installed"
  fi

  return 0
}

check_gate_08() {
  print_header "Gate 8 — Manifest signed"
  if [ ! -f "$MANIFEST" ]; then
    fail "manifest.json not found"
    return 1
  fi
  pass "manifest.json exists"

  if command -v python3 > /dev/null; then
    if python3 -c "
import json
m = json.load(open('$MANIFEST'))
if m.get('conductor_signature', {}).get('signature_hex'):
    print('SIGNED')
else:
    print('UNSIGNED')
" 2>/dev/null | grep -q SIGNED; then
      pass "Conductor signature present"
    else
      warn "Conductor signature slot is null — Phase 0 not yet sealed"
    fi
  fi

  return 0
}

check_gate_09_10_11() {
  print_header "Gates 9, 10, 11 — Publication"
  warn "Publication is a manual operator step"
  info "Gate 9:  upload to 5qln.foundation/codex/v1/"
  info "Gate 10: git tag -s codex-v1 && git push --tags"
  info "Gate 11: submit Sigstore Rekor entry; pin to IPFS (2+ providers)"

  if command -v git > /dev/null && git -C "$REPO_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
    if git -C "$REPO_ROOT" tag -l | grep -q '^codex-v1$'; then
      pass "git tag codex-v1 exists"
    else
      info "git tag codex-v1 not yet created"
    fi
  fi

  if command -v rekor-cli > /dev/null; then
    pass "rekor-cli present"
  else
    warn "rekor-cli not installed (install from sigstore/rekor)"
  fi

  if command -v ipfs > /dev/null; then
    pass "ipfs present"
  else
    warn "ipfs not installed"
  fi

  return 0
}

run_full_walkthrough() {
  print_banner
  echo "Working with:"
  echo "  REPO_ROOT: $REPO_ROOT"
  echo "  CODEX:     $CODEX"
  echo "  MANIFEST:  $MANIFEST"
  echo

  check_gate_01 || true
  check_gate_02 || true
  check_gate_03_04 || true
  check_gate_05 || true
  check_gate_06 || true
  check_gate_07 || true
  check_gate_08 || true
  check_gate_09_10_11 || true

  echo
  print_header "Phase 0 readiness summary"
  info "Gates 1-2 are technical and can be confirmed by this script"
  info "Gates 3-11 require operator action (keys, witnesses, publishing)"
  info "See phases/PHASE_0_SEAL.md for the full checklist"
  echo

  echo "Once all 11 gates pass:"
  echo "  1. Update manifest.json's phase_0_gates booleans to true"
  echo "  2. Set manifest.json's phase_0_status to 'SEALED'"
  echo "  3. Commit and tag: git tag -s codex-v1"
  echo "  4. Push to GitHub and publish to 5qln.foundation/codex/v1/"
  echo "  5. The Codex is now load-bearing for every downstream artifact"
  echo
}

verify_only() {
  print_header "Quick verification (no ceremony)"
  check_gate_01
  check_gate_02
  echo
  echo "${GREEN}${BOLD}Canonical form verified.${RESET}"
}

case "${1:-}" in
  --verify-only)
    verify_only
    ;;
  --gate)
    case "${2:-}" in
      1)  check_gate_01 ;;
      2)  check_gate_02 ;;
      3|4) check_gate_03_04 ;;
      5)  check_gate_05 ;;
      6)  check_gate_06 ;;
      7)  check_gate_07 ;;
      8)  check_gate_08 ;;
      9|10|11) check_gate_09_10_11 ;;
      *)  echo "usage: $0 --gate N  (where N in 1..11)" >&2 ; exit 2 ;;
    esac
    ;;
  --help|-h)
    cat <<EOF
seal-phase-0.sh — 5QLN Foundation Phase 0 ceremony helper

Usage:
  $0                  Interactive walkthrough of all 11 gates
  $0 --verify-only    Just run technical verifiers (gates 1-2)
  $0 --gate N         Check status of specific gate N (1..11)
  $0 --help           This message

This script does not sign or publish anything. Signing happens on the
Conductor's YubiHSM 2 device. Publishing is a manual operator step.

Read phases/PHASE_0_SEAL.md for the full ceremony specification.
EOF
    ;;
  *)
    run_full_walkthrough
    ;;
esac
