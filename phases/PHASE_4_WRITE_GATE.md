# Phase 4 — The Write Gate

**Goal:** make the dry-stratum / conversation-stratum boundary structural, not voluntary. Nothing enters the conversation stratum without a proof chain back to the Codex hash.

**Time:** 5 engineer-weeks.

**Predecessors:** Phase 2 (predicates available) and Phase 3 (verdict-log schema signed).

## The write-path API

```typescript
export interface ArtifactProof {
  predicate_id: string;            // which predicate gated this write
  predicate_hash: string;          // foreign key to predicate-set hash
  codex_hash: string;              // anchors to Phase 0
  ai_verdict_log_id: string | null; // present iff a soft predicate was involved
  parent_hash: string;             // hash of the prior artifact in this stream
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

The gate **refuses** any request where:

- `proof.codex_hash` differs from the loaded Codex hash
- `proof.predicate_hash` is not in the pinned predicate set
- `proof.parent_hash` does not resolve in storage
- `proof.ai_verdict_log_id`, if present, does not match a valid verdict record

No bypass. No exception list. No "trusted writer" mode.

## Storage layer

- **Content-addressed:** keys are SHA-256 of canonicalised content
- **Append-only:** no UPDATE, no DELETE; only INSERT
- **Hash-chained per stream:** every artifact's `parent_hash` resolves to a prior artifact's `stored_hash`
- **Implementations:**
  - PostgreSQL with `INSERT ONLY` enforced by trigger (primary working store)
  - Sigstore Rekor (public anchor; selected artifacts)
  - IPFS mirror (content-addressed external)

## Lineage walker

From any node hash, walk `parent_hash` links until a Codex anchor is reached.

```typescript
export interface LineageNode {
  hash: string;
  predicate_id: string;
  predicate_hash: string;
  phase: Phase;
  timestamp_iso: string;
  speaker: 'human' | 'ai';
}

export interface LineageWalker {
  walk(from_hash: string): Promise<LineageNode[]>;
}
```

Output: ordered list of nodes from the queried artifact back to the Codex anchor. Each step verifiable independently. The walk is a deterministic Tier-A audit primitive.

## Graph edge admittance

New context-graph edges enter the conversation stratum only if:

1. Both endpoints exist (both `parent_hash` values resolve)
2. Both endpoints' proofs verify
3. The connecting predicate (typically `PhaseTransitionPredicate` or an adaptive-context predicate) admits the transition

The graph can grow unboundedly across operators, decades, domains — and remain fully verifiable because every edge carries its own proof.

## Cycle lineage chain

```
Cycle N's ∞0'  ──hashes──→  Cycle N+1's seed X
              \                          /
               parent_hash chain
               carrying:
                 - hash of N's ∞0'
                 - hash of N's B''
                 - hash of N's full trail
```

The Loader of cycle N+1 verifies these are valid Tier-A artifacts (Phase 0 signed) before accepting them as seed.

## Bypass attempts leave no record

A write that fails predicate evaluation does not create a "failed-write log" entry in the conversation stratum — failed writes are visible only in operational metrics. This is by design: the conversation stratum's integrity claim is *every entry was lawful*. If failed writes were stored alongside successful ones, the stratum would be polluted with non-constitutional entries that future readers would have to manually filter.

Failed writes are reported back to the caller and logged separately for operational monitoring.

## Gate criteria for Phase 4 done

- [ ] Write-gate API implemented and tested
- [ ] Storage layer rejects UPDATE/DELETE at the database level
- [ ] Lineage walker traces a sample cycle from V back to S to Codex hash
- [ ] One end-to-end verifier-passing cycle produced (operator-led, sealed, walked)
- [ ] Bypass attempts (writes without proof, writes with bad codex_hash) verified to fail
- [ ] PostgreSQL working store deployed
- [ ] Sigstore Rekor anchor producing public attestations for selected artifacts
- [ ] CI runs the lineage walker on every PR's new artifacts

## What Phase 4 unlocks

- **First verifier-passing cycle** — the architecture is no longer specified-only; it has an existence proof
- Skill suite (Layer A) can integrate with the gate
- Plugin protocol can register against the gate
- Translation surfaces can read from sealed residue
- BIPP federation work (multi-jurisdiction) becomes legal to start after ≥30 verifier-passing cycles

This is where the architecture stops being a plan and starts being a system.
