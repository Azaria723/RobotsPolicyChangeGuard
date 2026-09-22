# StudioNet verification — remediated deployment

Verified 2026-09-22.

## Deployment and parity

- Contract: [`0x5ad3db5e6658868dbad1e35538871B2c76a68f10`](https://explorer-studio.genlayer.com/address/0x5ad3db5e6658868dbad1e35538871B2c76a68f10)
- Chain ID: `61999`
- Deployed source SHA-256: `a2f8fb9ecba3b9fb0ff83537cfd57080665fb82ea55422dc971c6b3923dfd642`
- Local source SHA-256: `a2f8fb9ecba3b9fb0ff83537cfd57080665fb82ea55422dc971c6b3923dfd642`
- Exact source parity: `true`
- Initial counters: watches `0`, snapshots `0`, alerts `0`

The deployer receives no watch role. A separate test wallet created the watch; another test wallet exercised unauthorized append.

## Finalized transactions

The SDK returned final status `7` for every transaction.

| Operation | Transaction | Authoritative effect |
|---|---|---|
| Create watch | [`0x3aeb…dc40`](https://explorer-studio.genlayer.com/tx/0x3aeb91fe5923da855da54247c8ad4bef5f03673c81f7f7b44ddb731f0cc0dc40) | Creates watch 0 with creator derived from sender |
| Unauthorized append | [`0x6aac…2b72`](https://explorer-studio.genlayer.com/tx/0x6aac452c377c4381b26ec42c43f3c819b02b2e90470149003d171e22c5212b72) | `CREATOR_ONLY`; snapshot count remains 0 |
| Append bad digest | [`0x8f4f…0ea1`](https://explorer-studio.genlayer.com/tx/0x8f4f7f30809b22a70c4e52869398ab2db795100bb86e68a5cab8bc83c3680ea1) | Creates candidate 0 without advancing canonical pointer |
| Assess bad digest | [`0xe1c9…c64e`](https://explorer-studio.genlayer.com/tx/0xe1c9ff41a622bcfdaeacd34efae14899c2769e91f4f1ab5038eff937059fc64e) | `SOURCE_UNVERIFIED`, `canonical=0` |
| Append corrected digest | [`0x7b20…5c87`](https://explorer-studio.genlayer.com/tx/0x7b208220a8d5700bc28a0fb9d6a067bf61b7bc66920e6adaba6367f5a6bb5c87) | New immutable recovery candidate for the same non-canonical commit |
| Assess corrected baseline | [`0x0d8f…78b7`](https://explorer-studio.genlayer.com/tx/0x0d8f75a87bbc061051ed0a9434c62c0789776fc006afe48438db0996cfec78b7) | `BASELINE_VERIFIED`, promotes snapshot 1 |
| Append restricted commit | [`0x8b61…d1be`](https://explorer-studio.genlayer.com/tx/0x8b6163e8f2137145793fbbfd24403e8b9a347a312d3346932c2326b0f03bd1be) | Candidate 2 binds canonical parent 1 and sequence 1 |
| Assess restricted commit | [`0x7bf2…a7a9`](https://explorer-studio.genlayer.com/tx/0x7bf2117690a3aeae36b8d9d55d792d15ec8c214136f78ae88ea69f1a51eca7a9) | Commit ancestry and bytes verified; `ACCESS_RESTRICTED` promoted |

## Poisoning attempt readback

Immediately after the bad-digest assessment:

- snapshot 0: `SOURCE_UNVERIFIED`, `canonical=0`, `provenance_ok=false`;
- `latest_snapshot_id=-1`;
- `snapshot_sequence=0`;
- alert count `0`.

The invalid candidate therefore never became the parent of a future comparison.

## Recovery and final canonical state

- snapshot 1: `BASELINE_VERIFIED`, `canonical=1`, parent `-1`;
- snapshot 2: `ACCESS_RESTRICTED`, `canonical=1`, parent snapshot `1`, sequence `1`;
- watch: `latest_snapshot_id=2`, `snapshot_sequence=2`;
- alert 0: `ACCESS_RESTRICTED`, affected `gptbot|/docs/private/`;
- final counters: watches `1`, snapshots `3`, alerts `1`.

This live sequence proves both halves of the remediation: an invalid candidate cannot poison canonical history, and a corrected immutable submission can recover without deleting the rejected audit record.
