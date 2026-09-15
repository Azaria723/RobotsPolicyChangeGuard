# Studionet verification

## Deployment and source parity

- Contract: `0x67099434f4e200862238DfdF9065BE8B827F26ef`
- Explorer: https://explorer-studio.genlayer.com/address/0x67099434f4e200862238DfdF9065BE8B827F26ef
- Chain ID: `61999`
- Local and deployed source SHA-256: `ac9a0c860fc2cc84ce75e01b9c5b4969fbcd7608f88d2d7599eed4f2e369799b`
- Exact source parity: `true`
- Initial readback: `watch_count=0`, `snapshot_count=0`, `alert_count=0`

## Verified lifecycle

- Create watch: [`0x671d914e28f4ad02534bc55b91193730a2c6f1a5c47c091a8fe35bef03ca035e`](https://explorer-studio.genlayer.com/tx/0x671d914e28f4ad02534bc55b91193730a2c6f1a5c47c091a8fe35bef03ca035e)
- Append baseline: [`0x6ea8896e201a60f9f274123ebebb5c4ce65977c696f13c7aff2983b7f289c17b`](https://explorer-studio.genlayer.com/tx/0x6ea8896e201a60f9f274123ebebb5c4ce65977c696f13c7aff2983b7f289c17b)
- Assess baseline: [`0x634ced1af00d05866681341189999064a50acc94200c62effb195e0602dd4e7c`](https://explorer-studio.genlayer.com/tx/0x634ced1af00d05866681341189999064a50acc94200c62effb195e0602dd4e7c)
- Append restricted snapshot: [`0x99e157cf1490fe9a6441071c5df9aaf976798f117d0d4497d1ec58bddaf25758`](https://explorer-studio.genlayer.com/tx/0x99e157cf1490fe9a6441071c5df9aaf976798f117d0d4497d1ec58bddaf25758)
- Assess restricted snapshot: [`0x51c8aa99af263e02a564c03d7f3a70f7efe950995bb079ffdae109716018ae8b`](https://explorer-studio.genlayer.com/tx/0x51c8aa99af263e02a564c03d7f3a70f7efe950995bb079ffdae109716018ae8b)

Authoritative readback after the lifecycle:

- Baseline: `BASELINE_VERIFIED`, `provenance_ok=true`, parent `-1`.
- Restricted snapshot: `ACCESS_RESTRICTED`, `provenance_ok=true`, parent snapshot `0`.
- Alert: `ACCESS_RESTRICTED`, affected pair `gptbot|/docs/private/`.
- Counts: one watch, two snapshots, one alert.

Validators fetched both immutable GitHub commits from the source bound in the watch, checked complete commit trees and blob identity, fetched raw policy bytes, recomputed their digests, and compared the scoped access semantics.

## Adversarial state-preservation checks

- Duplicate commit: [`0x40d3a2930f2d1d219a7666fd64ce318c39f54320d472c1e04e7c1c31fc6ddee2`](https://explorer-studio.genlayer.com/tx/0x40d3a2930f2d1d219a7666fd64ce318c39f54320d472c1e04e7c1c31fc6ddee2)
- Reassess completed snapshot: [`0x09c4e27179516a039a40841d47fff74c01caaa2b9480b7c5e677835d211f1533`](https://explorer-studio.genlayer.com/tx/0x09c4e27179516a039a40841d47fff74c01caaa2b9480b7c5e677835d211f1533)
- Unauthorized deactivation: [`0x87705752248992d0e5ca738fd5bf41738f9983be6df7ae5421e7988ad20f9e8b`](https://explorer-studio.genlayer.com/tx/0x87705752248992d0e5ca738fd5bf41738f9983be6df7ae5421e7988ad20f9e8b)

For each adversarial call, the complete watch, snapshot, alert and counter state was captured before and after finalization and remained byte-for-byte unchanged. The watch remained active. No private credential or account-orchestration procedure is included in this public report.
