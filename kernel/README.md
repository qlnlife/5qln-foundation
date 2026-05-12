# Kernel

This directory will hold the position-in-grammar state machine.

**Status:** Empty pending Phase 2. The existing kernel implementation lives at [`qlnlife/5qln-core`](https://github.com/qlnlife/5qln-core) and will be realigned + extended in Phase 2.

## What the Kernel holds

```typescript
export interface KernelState {
  phase: 'S' | 'G' | 'Q' | 'P' | 'V';
  lens: Lens | null;
  outputs: Record<'X'|'Y'|'Z'|'A'|'B', OutputState>;
  adaptiveContext: ReadonlyArray<string>;
  sparkSource: 'human' | 'residue';
}
```

That is the *entire* kernel state. Everything else is ring function (Loader, Witness, Watcher, Sealer, Attestor, Interrogator).

## What the Kernel does NOT hold

- The Codex itself (Loader reads it at startup; predicates encode it)
- The conversation history (Witness writes it to trail; storage holds it)
- AI verdicts (Interrogator writes them to verdict log)
- Audit records (Attestor builds them at V seal)
- Pattern matchers (Watcher owns them)

The Kernel is small on purpose. The Codex is small on purpose. The architecture is small at the center and grows only outward through ring functions.

See [`../specs/MASTER_ARCHITECTURE.md`](../specs/MASTER_ARCHITECTURE.md) §6 for the full Ring function specification.
