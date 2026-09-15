# RobotsPolicyChangeGuard

RobotsPolicyChangeGuard is a narrow GenLayer Intelligent Contract that detects material access changes between consecutive `robots.txt` or AI-crawler policy snapshots.

It is intentionally not an authorization gate. The contract maintains an append-only snapshot chain, independently verifies each GitHub artifact, compares the current policy with its immediate parent through validator consensus, and emits an on-chain alert journal for restrictions or ambiguous rules.

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
- Snapshots are append-only, commits cannot repeat within a watch, and each snapshot is assessed once.
- Anyone may append a correctly bound snapshot; only the watch creator may deactivate monitoring.
- The deployer receives no special role.

## Development

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

See [architecture](docs/ARCHITECTURE.md), [threat model](docs/THREAT_MODEL.md), [deployment checklist](docs/DEPLOYMENT.md), and [local verification](verification/local-verification.md).
