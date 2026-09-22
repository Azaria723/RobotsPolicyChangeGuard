# More Information Submission — Snapshot-Chain Integrity Remediation

Contribution: **RobotsPolicyChangeGuard — Verifiable AI Crawler Policy Change Alerts**

Date: 2026-09-22

## Steward request addressed

The previous version advanced `latest_snapshot_id` immediately when any caller appended a commit and digest. Because provenance verification happened only during the later assessment, an invalid digest or out-of-order commit could become the parent of future comparisons.

This issue has been corrected in contract logic, tested adversarially, redeployed, and verified through a live StudioNet poisoning-and-recovery sequence.

## Contract changes

The corrected contract now enforces all of the following:

1. **Append authorization:** only the authenticated watch creator may append a snapshot candidate.
2. **Candidate isolation:** appending creates a non-canonical candidate and does not change `latest_snapshot_id` or `snapshot_sequence`.
3. **Provenance before promotion:** validators verify the exact GitHub commit, complete tree, unique blob entry, file mode, byte length, Git blob SHA-1, and caller-bound SHA-256 digest.
4. **Commit ordering:** every non-baseline candidate commit must directly descend from the current canonical commit.
5. **Atomic promotion:** the canonical pointer and sequence advance only after consensus returns `provenance_ok=true`.
6. **Race protection:** candidates bind the current canonical parent and sequence. After another candidate is promoted, an older competing candidate becomes `STALE_PARENT` and cannot rewrite history.
7. **Recovery:** a `SOURCE_UNVERIFIED` record remains immutable and non-canonical. The creator may submit the same commit again as a new record with a corrected digest, preserving both recovery and the rejected audit trail.

Corrected source commit: [`8291600`](https://github.com/Azaria723/RobotsPolicyChangeGuard/commit/8291600)

## Matching deployment

- Contract: [`0x5ad3db5e6658868dbad1e35538871B2c76a68f10`](https://explorer-studio.genlayer.com/address/0x5ad3db5e6658868dbad1e35538871B2c76a68f10)
- Network: GenLayer StudioNet, chain ID `61999`
- Deployed source SHA-256: `a2f8fb9ecba3b9fb0ff83537cfd57080665fb82ea55422dc971c6b3923dfd642`
- Repository source SHA-256: `a2f8fb9ecba3b9fb0ff83537cfd57080665fb82ea55422dc971c6b3923dfd642`
- Exact source parity: `true`

The deployment wallet received no watch authority. A separate test wallet created the watch, and another independent test wallet exercised the unauthorized path.

## Live StudioNet remediation proof

| Step | Transaction | Verified result |
|---|---|---|
| Create watch | [`0x3aeb…dc40`](https://explorer-studio.genlayer.com/tx/0x3aeb91fe5923da855da54247c8ad4bef5f03673c81f7f7b44ddb731f0cc0dc40) | Watch creator derived from transaction sender |
| Unauthorized append | [`0x6aac…2b72`](https://explorer-studio.genlayer.com/tx/0x6aac452c377c4381b26ec42c43f3c819b02b2e90470149003d171e22c5212b72) | Rejected with `CREATOR_ONLY`; snapshot count remains zero |
| Append deliberately wrong digest | [`0x8f4f…0ea1`](https://explorer-studio.genlayer.com/tx/0x8f4f7f30809b22a70c4e52869398ab2db795100bb86e68a5cab8bc83c3680ea1) | Creates candidate 0 without advancing canonical state |
| Assess wrong digest | [`0xe1c9…c64e`](https://explorer-studio.genlayer.com/tx/0xe1c9ff41a622bcfdaeacd34efae14899c2769e91f4f1ab5038eff937059fc64e) | `SOURCE_UNVERIFIED`, `provenance_ok=false`, `canonical=0` |
| Submit corrected digest | [`0x7b20…5c87`](https://explorer-studio.genlayer.com/tx/0x7b208220a8d5700bc28a0fb9d6a067bf61b7bc66920e6adaba6367f5a6bb5c87) | Creates a new recovery candidate for the same rejected commit |
| Assess corrected baseline | [`0x0d8f…78b7`](https://explorer-studio.genlayer.com/tx/0x0d8f75a87bbc061051ed0a9434c62c0789776fc006afe48438db0996cfec78b7) | `BASELINE_VERIFIED`, `canonical=1` |
| Append ordered restriction | [`0x8b61…d1be`](https://explorer-studio.genlayer.com/tx/0x8b6163e8f2137145793fbbfd24403e8b9a347a312d3346932c2326b0f03bd1be) | Candidate binds canonical parent 1 and sequence 1 |
| Assess ordered restriction | [`0x7bf2…a7a9`](https://explorer-studio.genlayer.com/tx/0x7bf2117690a3aeae36b8d9d55d792d15ec8c214136f78ae88ea69f1a51eca7a9) | Ancestry and bytes verified; `ACCESS_RESTRICTED` promoted |

All listed transactions reached final SDK status `7`.

## State proof after the poisoning attempt

Immediately after assessing the deliberately incorrect digest:

- candidate 0 was `SOURCE_UNVERIFIED`;
- `canonical=0` and `provenance_ok=false`;
- `latest_snapshot_id=-1`;
- `snapshot_sequence=0`;
- alert count remained `0`.

Therefore, the invalid record did not become the parent of any subsequent comparison.

## Recovery and final authoritative state

- Snapshot 0: rejected audit record, `SOURCE_UNVERIFIED`, `canonical=0`.
- Snapshot 1: corrected recovery record, `BASELINE_VERIFIED`, `canonical=1`.
- Snapshot 2: `ACCESS_RESTRICTED`, `canonical=1`, parent snapshot `1`, sequence `1`.
- Watch: `latest_snapshot_id=2`, `snapshot_sequence=2`.
- Alert 0: `ACCESS_RESTRICTED`, affected pair `gptbot|/docs/private/`.
- Final counts: one watch, three snapshot records, one alert.

The rejected record remains visible for auditability but has no authority over canonical history.

## Local and adversarial verification

Direct Mode result: **21/21 tests passed** with `gltest==0.2.16`.

Coverage includes:

- unauthorized append;
- append without canonical advancement;
- invalid-digest poisoning attempt;
- corrected-digest recovery using a new immutable record;
- invalid commit ancestry;
- competing pending candidates and `STALE_PARENT`;
- complete source verification failures;
- semantic classification and alert creation;
- duplicate commit, reassessment, inactive watch, and invalid configuration guards;
- a static invariant proving the canonical pointer is absent from the append path and only advances behind `provenance_ok=true`.

## Supporting links

- [Repository](https://github.com/Azaria723/RobotsPolicyChangeGuard)
- [Corrected contract](https://github.com/Azaria723/RobotsPolicyChangeGuard/blob/master/contracts/RobotsPolicyChangeGuard.py)
- [StudioNet verification](https://github.com/Azaria723/RobotsPolicyChangeGuard/blob/master/verification/studionet-verification.md)
- [Steward remediation analysis](https://github.com/Azaria723/RobotsPolicyChangeGuard/blob/master/verification/steward-remediation.md)
- [Local verification](https://github.com/Azaria723/RobotsPolicyChangeGuard/blob/master/verification/local-verification.md)
- [Adversarial tests](https://github.com/Azaria723/RobotsPolicyChangeGuard/blob/master/tests/test_guard.py)
- [Threat model](https://github.com/Azaria723/RobotsPolicyChangeGuard/blob/master/docs/THREAT_MODEL.md)
- [Historical deployment marked superseded](https://github.com/Azaria723/RobotsPolicyChangeGuard/blob/master/verification/superseded-deployment.md)

## Resubmission statement

The reported snapshot-chain integrity issue is resolved. Unverified records cannot advance or influence canonical history; ordered provenance is checked before promotion; append authority is authenticated; stale candidates cannot overwrite ordering; and invalid submissions retain a tested recovery path. The repository source and new StudioNet deployment match exactly.
