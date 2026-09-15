# Immutable fixture manifest

Use the same canonical path for both consecutive snapshots: `/fixtures/robots.txt`.

## Snapshot 0 — baseline

- Commit: `1a9ae31c6baaf1a4e22243fb38a2d947bbe73edc`
- SHA-256 of exact Git blob bytes: `411326193a527d1599feb47710bf9d432334abb16fcb704046dd85e03022cd6e`
- Raw URL: https://raw.githubusercontent.com/Azaria723/RobotsPolicyChangeGuard/1a9ae31c6baaf1a4e22243fb38a2d947bbe73edc/fixtures/robots.txt

## Snapshot 1 — restricted

- Commit: `504247c8689976bbb2a03fe76155b87c933cb338`
- SHA-256 of exact Git blob bytes: `08a68f7955d33187c5c138d0b89db38f6db91e66fd79fb15ff4f66b9ac72b492`
- Raw URL: https://raw.githubusercontent.com/Azaria723/RobotsPolicyChangeGuard/504247c8689976bbb2a03fe76155b87c933cb338/fixtures/robots.txt

Expected semantic comparison for the configured scope is `ACCESS_RESTRICTED`, with `gptbot|/docs/private/` affected. The manifest contains public evidence only and no account credentials.
