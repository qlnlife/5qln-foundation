---
tier: B
record_id: narrative.002
register_tags:
  - CODEX-EXTENSION: "SHA-256 hash claim feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b — pinned to codex/codex.txt"
  - STRUCTURAL-HYPOTHESIS: "Reader's guide to the 32,000-word Master Architecture — all 16 sections mapped, all reading paths documented"
parent: codex/codex.txt (SHA-256: feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b)
mirror_url: null  # pending publication on 5qln.com
verified_against_codex: 2026-05-13
byte_count_claim: 217
status: canonical
note: |
  This narrative document describes but does not govern. It is Tier-B —
  downstream of the Codex, not source for it. No constitutional authority
  derives from this prose. Load-bearing numerical claims (the Codex hash
  and byte count) are CI-verified on every commit.
---

# Inside the Report

*A reader's guide to the 5QLN Foundation Master Architecture Document v1.0 — what it is, what's in it, what it serves, and how it will grow.*

---

## What this report is, in one sentence

The Master Architecture Document v1.0 is the **engineering specification** for the 5QLN Foundation Constitutional Substrate — a single ~32,000-word file living at [`specs/MASTER_ARCHITECTURE.md`](https://github.com/qlnlife/5qln-foundation/blob/main/specs/MASTER_ARCHITECTURE.md) that describes, in implementable detail, every layer of the system that turns the 5QLN Codex from text on a website into law a machine can refuse to violate.

If you read nothing else in this article, read this: **the report is not the Codex.** The Codex is the constitution. The report is the *plan for the runtime that enforces the constitution*. The Codex governs. The report defers.

## The report's register and constitutional posture

5QLN uses three epistemic registers for any load-bearing claim: STRUCTURAL-HYPOTHESIS, LEGAL-PROSPECTIVE, and PHENOMENOLOGICAL-ASSERTION (with CODEX-EXTENSION reserved for operational additions consistent with but not derived from the Nine Lines). It also tags every record into one of three tiers: A (Sealed Surface), B (Structured Record), or C (Working Register).

**The report is Tier-B.** It is a Structured Record. It does not carry the Constitutional Block on Page One. It is not itself a compiled 5QLN surface. It defers to the Codex on every point of conflict, and its opening clause says so explicitly: *"Where this conflicts with the Codex, the Codex governs."*

This matters in practice. When the byte count in v1.0 of the document said "221" and the actual sealed `codex.txt` came out to 217 bytes, the document was wrong. We did not adjust the bytes to match the document. We adjusted the document to match the bytes. This was not embarrassment — it was the architecture's own discipline applying to its own engineering record. The bytes win. The report is commentary about the bytes.

That posture is permanent. Every revision of this report will be Tier-B. The report will never elevate itself to constitutional status. If a future revision needs to express something constitutional, that thing goes into the Codex via the V.L.5(b) tri-condition amendment gate — not into this document.

## The sixteen sections, what each does

The report is structured for sequential reading, but the sections are deliberately separable. You can land in any one of them and get a complete picture of that layer.

**Section 1 — Executive Overview** opens with three one-paragraph descriptions of the system pitched at three different audiences (non-technical reader, engineer, constitutional lawyer), the eight-layer architecture diagram, and the single load-bearing claim everything else depends on: *every artifact admitted to the conversation stratum is reproducibly derivable from the sealed Codex by deterministic predicate evaluation; soft predicates use AI only as a witnessed sensor whose verdict is logged but never authoritative*. If that one claim ever fails on any byte, the architecture has failed.

**Section 2 — Phase 0: The Sealed Anchor** specifies the canonical byte form of `codex.txt`. The exact glyph decisions (⋂ U+22C2 on line 5, ∩ U+2229 on line 7, ASCII apostrophes, ASCII corruption codes with double-space separation, single trailing LF). The byte map computed from the actual sealed file. Three complete verifier implementations in Python, Rust, and Node — each ~200 lines, each independently runnable. The manifest JSON schema with slots for Conductor Ed25519 signature, RFC 3161 timestamp tokens, and three witness signatures. The eleven done-gates operator checklist that defines what "sealed" means.

**Section 3 — Phase 1: The Compiler** specifies the program that reads `codex.txt` and emits the predicate set — eighteen typed TypeScript classes, fifteen hard and three soft, one for each operational requirement of the nine canonical lines. The section covers parsing strategy, predicate emission, output artifacts (typed code, JSON manifest, hash pinning artifact, Conductor signature, Sigstore SLSA-3 provenance), reproducibility via Nix flake, cross-validation via a second Rust implementation, property tests, and the compiler's own attestation chain back to the Conductor's signing key.

**Section 4 — Phase 2: Runtime Audit** is the bridge between this repository and [`qlnlife/5qln-core`](https://github.com/qlnlife/5qln-core), the TypeScript kernel that currently carries a drifted ten-line superscript form of the Codex. The section lays out every module of `5qln-core/src` mapped to which Codex line it operationalizes, classifies each as hard/soft/absent, and specifies the realignment PR that brings the runtime into byte-identity with this repository's sealed Codex. Coverage assessment shows 5 predicates present, 4 partial, 9 absent — and the build order to close the gaps.

**Section 5 — Phase 3: The Interrogator** specifies the component that lets soft predicates use AI as a bounded sensor. The full TypeScript reference implementation (~500 LOC), the hashed prompt templates for each of the three soft predicates (Identity Preservation across {α'}, Intersection Landing of φ ⋂ Ω, Local-Global Intersection at V), the append-only hash-chained verdict log schema, the drift detection probe library, and the multi-AI consensus protocol (2-of-3 for routine V seals, unanimous for amendments). The Interrogator is what answers the founding dilemma: AI does sensor reading, never law enforcement; verdicts are logged and replayable, never authoritative.

**Section 6 — Ring Functions Around the Kernel** specifies the six components that wrap the minimal kernel (Loader, Witness, Watcher, Sealer, Attestor, Interrogator). Each gets a one-sentence role, a TypeScript interface contract, key invariants, and reference implementation notes. The Kernel itself holds only one thing: position in the grammar. Everything else is ring.

**Section 7 — Phase 4: The Write Gate** specifies the conversation-stratum admittance API. Every artifact admitted carries `{predicate-id, predicate-hash, codex-hash, ai-verdict-log-id?, parent-hash}`; without that chain, nothing enters. Storage is content-addressed, append-only, hash-chained. The lineage walker traces any artifact back to the Codex hash. New context-graph edges are admitted only if both endpoints' proofs verify. Cycle ∞0' of cycle N seeds cycle N+1, with hashes verifying.

**Section 8 — Runtime Infrastructure (AOSRAP integration)** specifies how the AOSRAP wrapper (a separate ten-week spec) layers on top of the substrate. Session initialisation with attestation nonce. Per-query validation with phase-tag enforcement. Synthetic probes every four hours. Attention-state attestation (the [REQUIRES_PARTNER] item — full cryptographic A4 needs LLM vendor cooperation that no major provider currently exposes). Schedule C manifest as child of Phase 0 Codex hash. Sigstore Rekor transparency log integration. Breach response flow.

**Section 9 — The Skill Suite** specifies operator-facing protocols in three layers. Layer A: Kernel skills used during live cycle sessions (s-receiver, g-illuminator, q-resonator, p-flow-watcher, v-crystallizer, plus lens discipline, trail recording, live corruption watching, cycle closing). Layer B: Attestation skills used at cycle close and across cycles (provenance builder, three-level verifier, codex fingerprint comparator). Layer C: Topology skills used for multi-agent and multi-scale operation (surface emitter, pentagonal swarm coordinator, fractal deepening judge).

**Section 10 — The Plugin Protocol** specifies how third parties build extensions that bind safely to the substrate without breaching the dry stratum. Manifest schema declaring which predicates the plugin touches, which trail tags it produces, which AI calls it makes, with quota bounds. Sandboxing via worker threads with capability-restricted APIs. Install-time attestation. Reference plugin implementation (a legal projector) in full TypeScript.

**Section 11 — Translation Surfaces** specifies the downstream-only projection pattern: domain-specific outputs (legal, medical, educational) that take cycle residue plus projection config and deterministically emit domain artifacts. Regenerable from residue. Never load-bearing. Never feed back into the conversation stratum. The Write Gate rejects any artifact whose `predicate-id` traces to a translation surface.

**Section 12 — Governance / Foundation Layer** specifies the three tiers of amendment (Constitutional Block via V.L.5(b), ordinary Bylaws via V.L.5(a), operational policy by Board majority). Codex versioning (v1 → v2 trigger conditions and backward compatibility). Dispute routing (CIO indicators → Resonance Court → Chancery V.L.7(f)). The relationship between the technical substrate and the Foundation legal entity, which does not yet exist (pre-incorporation cycles tag claims STRUCTURAL-HYPOTHESIS or LEGAL-PROSPECTIVE).

**Section 13 — Deployment Guide** specifies local development, host options (browser, Node, Raspberry Pi, MCP server, Zo Computer, agent runtime, pentagonal swarm), CI/CD pipeline with reproducible builds via Nix flake, and the migration path for transitioning the existing `5qln-core` repository to this substrate.

**Section 14 — Verification Philosophy & Threat Model** specifies the three-layer verification stack (cryptographic, grammatical, epistemic-register), enumerates what the architecture defends against (AI silent load failure, vendor weight changes, prompt injection, record tampering) and what it explicitly does not defend against (LLM pattern-matching hash echo without semantic attention, wrapper compromise, coordinated subtle failure, Board-level L4 performance). The section is honest about soft-predicate dependency on AI judgment and reframes drift as a measurable quantity rather than a binary state.

**Section 15 — Roadmap & Resource Estimates** specifies phase sequencing with engineer-week estimates, gate criteria, predecessors, critical path identification, what can parallelize, and what absolutely cannot. The headline number: ~18 engineer-weeks from Phase 0 seal to first verifier-passing cycle.

**Section 16 — Open Questions and Recommended Operator Decisions** enumerates the genuine open questions that the architect cannot decide alone and surfaces them for operator decision (Conductor key rotation policy, mirror redundancy, multi-AI consensus threshold for V seal, soft predicate UNCERTAIN threshold, plugin write quota, CL4-GP indicator calibration, federation timing), each with a recommended default. The section closes with the minimum viable Phase 0 ceremony plan day by day.

## Who the report is for, by reading path

The report is dense. It is not designed to be read cover-to-cover by anyone except the engineering team implementing it. Here are the practical reading paths:

**If you are a constitutional or corporate lawyer evaluating whether the substrate is sound enough to anchor Foundation acts**, read Section 1.3 (the one-paragraph lawyer overview), then Section 12 (governance and Foundation relationship), then Section 14 (verification philosophy and threat model). Approximately 45 minutes. The crucial line is in Section 1.3: the architecture's evidentiary status is `[LEGAL-PROSPECTIVE]` — the verifier produces *legibility*, which is the precondition of *defensibility*, not a substitute for it.

**If you are an engineer who needs to implement a phase**, read Section 1 (executive overview), then the section for your phase (2, 3, 4, 5, or 7), then Section 6 (ring functions), then Section 13 (deployment). Approximately 2 hours. The corresponding `phases/PHASE_N_*.md` file in the repository has the implementation checklist.

**If you are an AI safety researcher evaluating whether bounded-AI sensor design actually solves the interpretation-drift problem**, read Section 1.5 (the load-bearing claim), then Section 5 (the Interrogator design in detail), then Section 14.3 (honest acknowledgment of soft-predicate dependency). Approximately 90 minutes. The architecture does not claim the AI is right; it claims the AI's verdict is logged, hashed, replayable on a different AI, and operator-confirmed. The mitigation is structural, not epistemic.

**If you are a 5QLN community member who wants to understand the system at a working level**, read Section 1 (entire executive overview), then Section 2 (the sealed anchor — this is the heart of what's been done so far), then Section 16.2 (the minimum viable ceremony plan). Approximately 45 minutes.

**If you are an auditor checking the report against the implementation**, every numerical claim in the report can be re-derived from the canonical `codex.txt`. The byte map in Section 2.3 should add to 217. The Codex SHA-256 should match `feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b`. The 18 predicates in Section 3 should each correspond to a specific operational claim of one of the nine lines. If any of these numbers ever fail to add up, file an issue.

## What the report covers — and what it explicitly defers

The report covers: the substrate's structure, every layer's interfaces and invariants, the predicate set derivation, the Interrogator's bounded-AI sensor design, the conversation-stratum write gate, governance and amendment process at the technical layer, threat model, roadmap, and open operator decisions.

The report does not cover (and explicitly defers to other documents):

- **The Codex itself.** The canonical Nine Invariant Lines live at [5qln.com/codex/](https://www.5qln.com/codex/) and in `codex/codex.txt`. The report describes what the Codex does in the runtime; it does not redefine the Codex.
- **Bylaws content.** The Human Edition and AI OS Edition of the Bylaws are separate documents. The report references them where structurally relevant (V.L.5(b) amendment gate, V.L.7(f) Chancery clause, P.L.4 Membrane Protocol hard-blocks) but does not include their full text.
- **AOSRAP wrapper specification.** AOSRAP has its own ten-week engineering specification at [5qln.com/aosrap-wrapper-engineering-specification-v0-1/](https://www.5qln.com/aosrap-wrapper-engineering-specification-v0-1/). The report describes how AOSRAP layers on the substrate; it does not duplicate the wrapper's internal specification.
- **Foundation legal entity.** The Delaware filing, the choice of registered agent, the Anti Entropy fiscal sponsorship transition, the Bylaws ratification ceremony, the Director slate — these are legal matters that the technical substrate enables but does not specify. The report contains the architectural hooks; counsel handles the rest.
- **Domain content.** What a legal projection actually says, what a medical decision-support memo actually recommends, what a lesson plan actually teaches — none of that is in the report. Translation surfaces are structural patterns. Their content is downstream.

## How the report will grow

Three classes of revision, in increasing severity:

**Documentation corrections.** Things like the recent v1.1 audit cycle: byte counts that were estimates getting corrected to ceremony-actual values, tool paths that drift between document and repository, table arithmetic that doesn't quite add up, typos. These are normal Tier-B engineering revisions. They happen via ordinary commits with descriptive messages, never touch the Codex bytes, and are visible on the public commit history. The report's "v1.x" versioning tracks these.

**Architectural elaborations.** When Phase 1 produces the predicate set and we discover the gap report needs adjustment, or when Phase 3 produces the Interrogator and the verdict log schema needs a field that wasn't anticipated, or when the AOSRAP wrapper integration surfaces a requirement on Section 8 — these get worked into the next major revision. The report's "v2.x" versioning tracks these. v2 of the report can change interfaces and reorganize sections, but it cannot change anything that requires re-sealing the Codex.

**Constitutional alignment.** If the V.L.5(b) tri-condition gate is ever validly exercised and a Codex amendment passes, the report needs to be re-derived from scratch against the new sealed Codex bytes. Predicate set changes. Possibly the eight-layer architecture changes. The byte map is regenerated. New canonical hash. The report's "v3.x" versioning tracks these (no v2 cycle has ever been seriously contemplated as of this writing; the Codex's stability is itself load-bearing).

The report will not grow by accretion of new domains. Legal-projector specifics, medical-projector specifics, educational-projector specifics — these belong in their own translation-surface documents, not in this report. The report's job is to specify the substrate that all surfaces build on, not to anticipate every surface.

## How the report itself is verified

This is the part that took me by surprise during the recent audit cycles, and it is worth stating clearly: the report can drift from the repository it specifies, and that drift is detectable.

The mechanism is simple. The repository contains the canonical `codex.txt`. The repository contains the verifiers that prove every byte of `codex.txt` matches its hash. The report makes specific numerical claims (byte count, per-line bytes, hash, line count, glyph codepoints) that are checkable against the canonical bytes. When the report says one thing and the bytes say another, the bytes win and the report gets corrected.

Three audit rounds since the initial push have demonstrated this. Each round caught real drift between the document and the implementation — wrong byte count, wrong table values, wrong path references, missing files. Each round corrected the document, not the implementation. The canonical hash `feaa46b4...c781859b` has not moved a single bit through four commits.

That pattern is the report's own integrity mechanism. The report does not need a separate verifier of its own. It needs to keep being read against the bytes it claims to describe, and corrections need to keep being pushed. The community is invited to read it that way.

## What the report is serving

The report serves four functions in the 5QLN Foundation substrate.

**It is the engineering contract.** When a future contributor implements Phase 1's compiler or Phase 3's Interrogator, the report tells them exactly what interface, what hash discipline, what test fixtures, and what attestation chain their implementation must satisfy. Without the report, every implementation choice would be an ad-hoc decision. With it, every choice is gated against a specified target.

**It is the audit reference.** When a Chancery clerk, an external counsel, or a future Board member needs to verify what the substrate claims about itself, the report is the document they read. It is comprehensive, dated, and constitutionally posture-tagged. It is honest about what is implemented and what is specified-only.

**It is the onboarding spine.** A new operator, contributor, or witness can read the report once and have a complete picture of what they are joining. They do not need to reconstruct the architecture from scattered essays or accumulated Substack posts. The report consolidates.

**It is the publishable specification of a public-good substrate.** 5QLN is open source. The Codex is published. The verifiers are public. The threat model is documented. The report makes the architecture itself a thing the community can fork, federate, criticize, and improve. Without the report, the substrate would be a black box. With it, every architectural choice is on the table for scrutiny.

## Where to start

Open the report at [`specs/MASTER_ARCHITECTURE.md`](https://github.com/qlnlife/5qln-foundation/blob/main/specs/MASTER_ARCHITECTURE.md). Read Section 1 entirely (~10 minutes; it has the one-paragraph summaries for three different audiences). Then follow the reading path appropriate to your role from the section above. If you are unsure which path applies, the engineer's path (Sections 1, 2, 13) is the most comprehensive starting point.

Verify the canonical hash on your own machine:

```
git clone https://github.com/qlnlife/5qln-foundation
cd 5qln-foundation
python3 tools/python/verify_codex.py codex/codex.txt
```

If you see `RESULT: CONSTITUTIONAL — canonical form verified.`, the substrate is intact on your local checkout. If you see anything else, please file an issue — that is exactly the kind of drift we want surfaced publicly.

The report is alive. It will be revised as the implementation deepens and as the audit cycles continue. v1.1.1 is the current state at the time of this writing. The constitutional bytes have not moved. The report describes a substrate that exists, awaiting ceremony, ready for use.

*— Amihai Loven, May 2026*

*The report itself: [`specs/MASTER_ARCHITECTURE.md`](https://github.com/qlnlife/5qln-foundation/blob/main/specs/MASTER_ARCHITECTURE.md). The repository: [github.com/qlnlife/5qln-foundation](https://github.com/qlnlife/5qln-foundation). The Codex: [5qln.com/codex/](https://www.5qln.com/codex/). The origin story: ["The Codex Became Physics"](https://www.5qln.com).*
