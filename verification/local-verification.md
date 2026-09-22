# Local verification

- Result: `17 passed`.
- Contract source SHA-256: `ac9a0c860fc2cc84ce75e01b9c5b4969fbcd7608f88d2d7599eed4f2e369799b`.
- Direct Mode uses strict web mocks and serialization checks.
- Happy paths cover baseline verification, restriction alert, expansion and no material change.
- Provenance failures cover incorrect SHA-256, truncated trees and Git blob identity mismatch.
- Semantic adversarial cases cover unknown classifications, extra fields, empty affected sets, out-of-scope pairs and ambiguous fallback.
- State tests cover creator-only append, promotion-only canonical links, duplicate commits, assess-once behavior, creator-only deactivation and invalid configuration preserving counters.
- Steward remediation tests prove invalid digests cannot advance the canonical parent, rejected commits have a corrected-digest recovery path, out-of-order commits fail provenance, and racing candidates cannot overwrite ordering.

Latest remediation run on 2026-09-22: **21/21 passed** with `gltest==0.2.16`.
- Static tests prove the contract contains GenLayer web/LLM/consensus primitives and does not contain the previous authorization lifecycle.

Studionet source parity and live transaction evidence are recorded in `studionet-verification.md`.
