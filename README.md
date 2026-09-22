# RobotsPolicyChangeGuard

RobotsPolicyChangeGuard is a narrow GenLayer Intelligent Contract that detects material access changes between consecutive `robots.txt` or AI-crawler policy snapshots.

It is intentionally not an authorization gate. The contract maintains a verified canonical snapshot chain, independently verifies each GitHub artifact and commit ordering, compares the current policy with its canonical parent through validator consensus, and emits an on-chain alert journal for restrictions or ambiguous rules.

## Outcomes

- `BASELINE_VERIFIED` — first canonical snapshot established.
- `NO_MATERIAL_CHANGE` — scoped crawler/path access is unchanged.
- `ACCESS_EXPANDED` — at least one scoped pair gained access.
- `ACCESS_RESTRICTED` — at least one scoped pair lost access; an alert is recorded.
- `AMBIGUOUS_POLICY` — rules cannot be compared safely; an alert is recorded.
- `SOURCE_UNVERIFIED` — immutable source provenance or content integrity failed.

## Why GenLayer

Robots policies contain precedence, wildcard and user-agent semantics that are awkward to reduce to simple byte equality. GenLayer validators fetch both canonical versions, verify their provenance and integrity, and independently compare their meaning for an explicitly bounded crawler/path matrix. `strict_eq` commits only an identical structured classification.

## Security model

- Repository coordinates and policy path are fixed when a watch is created.
- Every snapshot uses a full 40-character immutable commit and SHA-256 digest.
- The contract verifies GitHub Commit API identity, a complete non-truncated tree, blob path/type/mode/size/Git SHA-1, raw bytes and SHA-256.
- Model output is constrained to four classifications and an allowlisted crawler/path Cartesian product.
- Only the watch creator may append candidates or deactivate monitoring.
- Appending creates a pending candidate and never advances the canonical parent.
- A candidate is promoted only after validators verify its exact bytes and, after the baseline, prove its commit directly descends from the current canonical commit.
- Rejected-source records remain immutable but do not poison future comparisons. The creator may submit a corrected digest as a new record for the same non-canonical commit.
- Concurrent candidates bind the same canonical parent; after one is promoted, the other becomes `STALE_PARENT` and cannot rewrite ordering.
- The deployer receives no special role.

## Development

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

See [architecture](docs/ARCHITECTURE.md), [threat model](docs/THREAT_MODEL.md), [deployment checklist](docs/DEPLOYMENT.md), and [local verification](verification/local-verification.md).
