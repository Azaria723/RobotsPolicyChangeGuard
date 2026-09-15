# Deployment and live verification

1. Run all Direct Mode tests and record the contract SHA-256.
2. Create a public repository and push the baseline `fixtures/robots.txt`.
3. Record its full commit and exact raw SHA-256.
4. Modify the same path with a restriction, commit it, and record the second commit/digest.
5. Deploy the contract without constructor arguments. Confirm deployed/local source parity and zero counts before writes.
6. Create one watch bound to the repository, `/fixtures/robots.txt`, selected crawlers and protected paths.
7. Append and assess the baseline; require `BASELINE_VERIFIED` and zero alerts.
8. Append and assess the changed snapshot; require `ACCESS_RESTRICTED` and read back its exact affected pair.
9. Exercise duplicate commit, unauthorized deactivation, invalid digest and malformed semantic-output branches.
10. Publish transaction links and authoritative state readbacks without private credentials or descriptions of account orchestration.
