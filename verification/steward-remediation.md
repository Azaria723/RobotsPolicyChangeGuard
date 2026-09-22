# Steward remediation — canonical snapshot-chain integrity

Date: 2026-09-22

## Reported issue

The original deployment advanced `latest_snapshot_id` during `append_snapshot`. Because any caller could append and source verification occurred later, an invalid digest or out-of-order commit could become the parent of future assessments.

## Corrected invariant

`latest_snapshot_id` and `snapshot_sequence` identify only the last provenance-verified canonical snapshot. `append_snapshot` cannot mutate either field.

The revision implements:

1. creator-only candidate append authorization;
2. immutable pending records bound to canonical parent ID and sequence;
3. full commit/tree/blob/digest verification before promotion;
4. direct Git commit-parent verification for non-baseline ordering;
5. atomic pointer advancement only when `provenance_ok=true`;
6. deterministic `STALE_PARENT` handling for racing candidates;
7. corrected-digest resubmission after a `SOURCE_UNVERIFIED` record, without deleting history.

## Regression evidence

Direct Mode: **21/21 passed**.

New adversarial sequences cover unauthorized append, invalid-digest poisoning, corrected resubmission recovery, out-of-order commit ancestry, and competing pending candidates. Assertions compare canonical watch state before and after rejected assessments.

## Live remediation proof

The matching revision is deployed at [`0x5ad3db5e6658868dbad1e35538871B2c76a68f10`](https://explorer-studio.genlayer.com/address/0x5ad3db5e6658868dbad1e35538871B2c76a68f10). Deployed/local source parity is exact.

The live sequence demonstrates unauthorized append rejection, bad-digest isolation with the canonical pointer still `-1`, corrected-digest resubmission for the same commit, baseline promotion, commit-ordered restriction promotion, and the expected alert. See [StudioNet verification](studionet-verification.md).
