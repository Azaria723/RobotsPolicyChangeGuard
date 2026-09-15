# Architecture

## State model

`Watch -> Snapshot 0 -> Snapshot 1 -> ...`

Each watch binds one represented domain, one GitHub repository, one policy path, and finite normalized sets of crawlers and protected paths. Every appended snapshot stores its immediate parent, sequence number, immutable commit and expected digest. Assessment never rewrites history; it annotates one snapshot and may append one alert.

## Assessment pipeline

1. Fetch the GitHub commit object and require the requested full SHA.
2. Fetch its recursive tree and reject truncated trees.
3. Locate exactly one regular `100644` blob at the bound path.
4. Fetch raw bytes and verify size, Git blob SHA-1 and caller-supplied SHA-256.
5. For a non-baseline snapshot, repeat verification for its immediate parent.
6. Ask validators to compare only the configured crawler/path matrix.
7. Validate the exact response schema and allowlist every affected pair.
8. Commit the identical consensus result and append an alert when appropriate.

This is an observation journal, not a registry-classification or consumable-authorization workflow.
