from pathlib import Path
S=Path("contracts/RobotsPolicyChangeGuard.py").read_text()
def test_genlayer_primitives():
    assert "gl.eq_principle.strict_eq(evaluate)" in S
    assert "gl.nondet.web.get" in S and "gl.nondet.exec_prompt" in S
def test_no_authorization_clone_architecture():
    for term in ["consume_authorization","authorization_digest","propose_sunset","register_service"]:assert term not in S
def test_provenance_layers_present():
    for term in ["/commits/","/git/trees/","_blob_sha1","hashlib.sha256"]:assert term in S
def test_canonical_parent_advances_only_after_verified_assessment():
    append_body=S.split("def append_snapshot",1)[1].split("def _verified_body",1)[0]
    assess_body=S.split("def assess_snapshot",1)[1].split("def deactivate_watch",1)[0]
    assert 'watch["latest_snapshot_id"] = int(snapshot_id)' not in append_body
    assert 'watch["latest_snapshot_id"] = int(snapshot_id)' in assess_body
    assert 'result["provenance_ok"] is True' in assess_body
    assert "CREATOR_ONLY" in append_body and "STALE_PARENT" in assess_body
    assert 'expected_parent_commit not in parent_shas' in S
