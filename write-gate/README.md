# Write Gate

This directory will hold the conversation-stratum admittance API.

**Status:** Empty pending Phase 4. Full specification at [`../phases/PHASE_4_WRITE_GATE.md`](../phases/PHASE_4_WRITE_GATE.md).

## What the Write Gate does

Makes the dry-stratum / conversation-stratum boundary **structural, not voluntary**. Nothing enters the conversation stratum without a proof chain back to the Codex hash.

```typescript
export interface ArtifactProof {
  predicate_id: string;
  predicate_hash: string;
  codex_hash: string;
  ai_verdict_log_id: string | null;
  parent_hash: string;
}

export interface WriteGate {
  admit(req: ArtifactRequest): Promise<{ stored_hash: string }>;
}
```

The gate **refuses** any request where:
- `codex_hash` differs from the loaded Codex hash
- `predicate_hash` is not in the pinned predicate set
- `parent_hash` does not resolve in storage
- `ai_verdict_log_id`, if present, does not match a valid verdict record

No bypass. No exception list. No "trusted writer" mode.

## What lives here once built

| File | Description |
|---|---|
| `src/write-gate.ts` | The `admit()` implementation |
| `src/lineage-walker.ts` | From any node hash, walk back to Codex anchor |
| `src/storage-pg.ts` | PostgreSQL append-only working store |
| `src/storage-rekor.ts` | Sigstore Rekor public anchor |
| `src/storage-ipfs.ts` | Optional IPFS content-addressed mirror |
| `tests/` | End-to-end cycle verification tests |

## The cycle lineage chain

```
Cycle N's ∞0'  ──hashes──→  Cycle N+1's seed X
              \                          /
               parent_hash chain
```

The Loader of cycle N+1 verifies cycle N's `∞0'` is a valid Tier-A artifact (Phase 0 signed) before accepting it as seed. The chain walks all the way back to the Codex hash, every step independently verifiable.
