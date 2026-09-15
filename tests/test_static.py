from pathlib import Path
S=Path("contracts/RobotsPolicyChangeGuard.py").read_text()
def test_genlayer_primitives():
    assert "gl.eq_principle.strict_eq(evaluate)" in S
    assert "gl.nondet.web.get" in S and "gl.nondet.exec_prompt" in S
def test_no_authorization_clone_architecture():
    for term in ["consume_authorization","authorization_digest","propose_sunset","register_service"]:assert term not in S
def test_provenance_layers_present():
    for term in ["/commits/","/git/trees/","_blob_sha1","hashlib.sha256"]:assert term in S
