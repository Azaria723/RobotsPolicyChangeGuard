# Architecture

## State model

`Watch -> Snapshot 0 -> Snapshot 1 -> ...`

Each watch binds one represented domain, one GitHub repository, one policy path, and finite normalized sets of crawlers and protected paths. Only its creator may append a candidate. Every candidate binds the current canonical parent, canonical sequence, immutable commit and expected digest. Append does not update the watch pointer.

Assessment first rejects a stale parent deterministically. Validators then verify the candidate source. For every non-baseline candidate, the GitHub commit object must list the canonical commit as a parent. Only a provenance-valid consensus result promotes the candidate, advances `latest_snapshot_id`, and increments `snapshot_sequence`. Invalid sources remain non-canonical; a corrected digest may be submitted as a new record without deleting the rejected audit record.

## Assessment pipeline

1. Fetch the GitHub commit object and require the requested full SHA.
2. Fetch its recursive tree and reject truncated trees.
3. Locate exactly one regular `100644` blob at the bound path.
4. Fetch raw bytes and verify size, Git blob SHA-1 and caller-supplied SHA-256.
5. For a non-baseline snapshot, require the candidate commit to directly descend from the canonical commit and repeat byte verification for that canonical parent.
6. Ask validators to compare only the configured crawler/path matrix.
7. Validate the exact response schema and allowlist every affected pair.
8. Atomically promote the verified candidate, commit the identical consensus result, and append an alert when appropriate.

This is an observation journal, not a registry-classification or consumable-authorization workflow.
