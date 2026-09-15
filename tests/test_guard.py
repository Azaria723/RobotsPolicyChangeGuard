import hashlib,json
import pytest

pytestmark = pytest.mark.filterwarnings("ignore:Web mock never matched")

OWNER="Azaria723";REPO="RobotsPolicyChangeGuard";PATH="/fixtures/robots.txt"
V1=b"User-agent: GPTBot\nAllow: /docs/\n";V2=b"User-agent: GPTBot\nAllow: /docs/\nDisallow: /docs/private/\n"
C1="1"*40;C2="2"*40
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1((f"blob {len(b)}\0").encode()+b).hexdigest()
def deploy(vm,direct_deploy,actor):
    vm.strict_mocks=True;vm.check_pickling=True
    with vm.prank(actor):return direct_deploy("contracts/RobotsPolicyChangeGuard.py")
def create(vm,c,actor):
    with vm.prank(actor):assert c.create_watch("example.com",PATH,OWNER,REPO,json.dumps(["gptbot"]),json.dumps(["/docs/","/docs/private/"]))==0
def append(vm,c,actor,commit,body):
    with vm.prank(actor):return c.append_snapshot(0,commit,sha(body))
def mock(vm,fixtures,truncated=None,bad_blob=False):
    api=f"https://api.github.com/repos/{OWNER}/{REPO}";raw=f"https://raw.githubusercontent.com/{OWNER}/{REPO}/"
    for i,(commit,body) in enumerate(fixtures):
        tree=str(i+5)*40
        vm.mock_web((api+"/commits/"+commit).replace(".",r"\.")+"$",{"status":200,"body":json.dumps({"sha":commit,"commit":{"tree":{"sha":tree}}}).encode()})
        entry={"path":PATH[1:],"mode":"100644","type":"blob","size":len(body),"sha":"0"*40 if bad_blob else blob(body)}
        vm.mock_web((api+"/git/trees/"+tree+r"\?recursive=1$").replace(".",r"\."),{"status":200,"body":json.dumps({"truncated":commit==truncated,"tree":[entry]}).encode()})
        vm.mock_web((raw+commit+PATH).replace(".",r"\.")+"$",{"status":200,"body":body})
def snap(c,i):return json.loads(c.get_snapshot(i))

def test_baseline_then_restriction_creates_alert(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V1);mock(direct_vm,[(C1,V1)])
    assert c.assess_snapshot(0)=="BASELINE_VERIFIED" and json.loads(c.get_counts())["alert_count"]==0
    append(direct_vm,c,direct_alice,C2,V2);mock(direct_vm,[(C1,V1),(C2,V2)])
    direct_vm.mock_llm(r"Compare two robots.*",json.dumps({"classification":"ACCESS_RESTRICTED","affected":["gptbot|/docs/private/"]}))
    assert c.assess_snapshot(1)=="ACCESS_RESTRICTED";assert json.loads(c.get_counts())["alert_count"]==1
    assert json.loads(c.get_alert(0))["affected"]==["gptbot|/docs/private/"]

def test_expansion_has_no_alert(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V2);append(direct_vm,c,direct_alice,C2,V1);mock(direct_vm,[(C1,V2),(C2,V1)])
    assert c.assess_snapshot(0)=="BASELINE_VERIFIED"
    direct_vm.mock_llm(r"Compare two robots.*",json.dumps({"classification":"ACCESS_EXPANDED","affected":["gptbot|/docs/private/"]}))
    assert c.assess_snapshot(1)=="ACCESS_EXPANDED" and json.loads(c.get_counts())["alert_count"]==0

def test_no_material_change_has_no_alert(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V1);append(direct_vm,c,direct_alice,C2,V1);mock(direct_vm,[(C1,V1),(C2,V1)])
    assert c.assess_snapshot(0)=="BASELINE_VERIFIED"
    direct_vm.mock_llm(r"Compare two robots.*",json.dumps({"classification":"NO_MATERIAL_CHANGE","affected":[]}))
    assert c.assess_snapshot(1)=="NO_MATERIAL_CHANGE" and json.loads(c.get_counts())["alert_count"]==0

@pytest.mark.parametrize("output",[
    {"classification":"ACCESS_RESTRICTED","affected":[]},
    {"classification":"ACCESS_RESTRICTED","affected":["evilbot|/admin"]},
    {"classification":"ALLOW_EVERYTHING","affected":[]},
    {"classification":"NO_MATERIAL_CHANGE","affected":[],"reason":"extra"},
])
def test_malformed_semantics_fail_to_ambiguous(direct_vm,direct_deploy,direct_alice,output):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V1);append(direct_vm,c,direct_alice,C2,V2);mock(direct_vm,[(C1,V1),(C2,V2)]);assert c.assess_snapshot(0)=="BASELINE_VERIFIED"
    direct_vm.mock_llm(r"Compare two robots.*",json.dumps(output));assert c.assess_snapshot(1)=="AMBIGUOUS_POLICY";assert json.loads(c.get_counts())["alert_count"]==1

def test_digest_and_tree_fail_closed(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V1);mock(direct_vm,[(C1,V2)])
    assert c.assess_snapshot(0)=="SOURCE_UNVERIFIED" and snap(c,0)["assessed"]==1

def test_truncated_tree_fails_closed(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V1);mock(direct_vm,[(C1,V1)],truncated=C1)
    assert c.assess_snapshot(0)=="SOURCE_UNVERIFIED"

def test_blob_identity_mismatch_fails_closed(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V1);mock(direct_vm,[(C1,V1)],bad_blob=True)
    assert c.assess_snapshot(0)=="SOURCE_UNVERIFIED"

def test_snapshot_cannot_be_assessed_twice(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice);append(direct_vm,c,direct_alice,C1,V1);mock(direct_vm,[(C1,V1)])
    assert c.assess_snapshot(0)=="BASELINE_VERIFIED" and c.assess_snapshot(0)=="SNAPSHOT_ALREADY_ASSESSED"

def test_append_only_chain_and_duplicate_commit(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice)
    assert append(direct_vm,c,direct_bob,C1,V1)==0;assert append(direct_vm,c,direct_bob,C2,V2)==1
    assert append(direct_vm,c,direct_bob,C1,V1)=="COMMIT_ALREADY_RECORDED"
    assert snap(c,0)["parent_snapshot_id"]==-1 and snap(c,1)["parent_snapshot_id"]==0

def test_creator_only_deactivation(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=deploy(direct_vm,direct_deploy,direct_alice);create(direct_vm,c,direct_alice)
    with direct_vm.prank(direct_bob):assert c.deactivate_watch(0)=="CREATOR_ONLY"
    with direct_vm.prank(direct_alice):assert c.deactivate_watch(0)=="WATCH_DEACTIVATED"
    assert append(direct_vm,c,direct_bob,C1,V1)=="WATCH_INACTIVE"

def test_invalid_config_preserves_counts(direct_vm,direct_deploy,direct_alice):
    c=deploy(direct_vm,direct_deploy,direct_alice)
    with direct_vm.prank(direct_alice):
        assert c.create_watch("Example.COM",PATH,OWNER,REPO,"[]","[]")=="INVALID_DOMAIN"
        assert c.create_watch("example.com","/../robots",OWNER,REPO,json.dumps(["gptbot"]),json.dumps(["/docs/"]))=="INVALID_SOURCE"
    assert json.loads(c.get_counts())=={"alert_count":0,"snapshot_count":0,"watch_count":0}
