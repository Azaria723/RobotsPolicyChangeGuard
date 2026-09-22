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

Direct Mode: **20/20 passed**.

New adversarial sequences cover unauthorized append, invalid-digest poisoning, corrected resubmission recovery, out-of-order commit ancestry, and competing pending candidates. Assertions compare canonical watch state before and after rejected assessments.

## Deployment status

The prior deployment predates this fix and must not be submitted as matching evidence. A new StudioNet deployment and live poisoning/recovery lifecycle are required before resubmission.
