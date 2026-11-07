#!/usr/bin/env python3
"""Guarded, manual A9 historical Git ref import. Never writes either main."""
import base64, json, os, re, subprocess, sys
from pathlib import Path

SOURCE="https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub.git"
DEST="https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library.git"
PIN_SRC="4eb68c004fbe8d19b83bf3b17327c853debef58a"
PIN_DST="336a274c2660998041aad506a32b76d03e194e3f"
PIN_STAGE="018dd5903afcfad0e00a5cc37cefbbe2d399ea10"
MIRROR=Path("source-a9-mirror.git")
REPORT=Path("migration/audit/history-import-run.json")
PATTERNS={
 "private_key":rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
 "github_token":rb"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})",
 "google_api_key":rb"AIza[0-9A-Za-z_-]{30,}",
 "aws_key":rb"(?:AKIA|ASIA)[0-9A-Z]{16}",
 "openai_token":rb"sk-(?:proj-)?[A-Za-z0-9_-]{24,}",
 "slack_token":rb"xox[baprs]-[A-Za-z0-9-]{20,}",
 "database_password_uri":rb"postgres(?:ql)?://[^\s:/]+:[^\s@]+@[^\s]+",
}
NAME_RISK=re.compile(r"(?:^|/)(?:\.env(?:\.[^/]*)?|id_rsa|id_ed25519|\.npmrc|credentials?(?:\.[^/]*)?|private[_-]?key(?:\.[^/]*)?|[^/]+\.pem)$",re.I)

def run(*args,cwd=None):
 p=subprocess.run(args,cwd=cwd,capture_output=True,check=False,text=True,env={**os.environ,"GIT_TERMINAL_PROMPT":"0"})
 if p.returncode: raise RuntimeError("command failed (exit "+str(p.returncode)+"): "+" ".join(args[:3]))
 return p.stdout.strip()

def ensure(value,msg):
 if not value:raise RuntimeError("HOLD: "+msg)

def refmap(prefix):
 return dict(line.split(" ",1) for line in run("git","for-each-ref","--format=%(refname) %(objectname)",prefix,cwd=MIRROR).splitlines() if line)

def remote_map():
 out={}
 for line in run("git","ls-remote","--heads","--tags",DEST,"refs/heads/imported/cwo/*","refs/tags/imported-cwo/*").splitlines():
  sha,ref=line.split("\t",1)
  if not ref.endswith("^{}"):out[ref]=sha
 return out

def build_import_plan(manifest, branches, tags, existing):
 """Validate the entire import namespace before producing missing-only refspecs."""
 expected = {}
 refspecs = {}
 for r in manifest["branches"]:
  src = r["source_ref"]
  dst = r["target_ref"]
  ensure(src.startswith("refs/heads/") and dst == "refs/heads/imported/cwo/" + src[len("refs/heads/"):], "unsafe branch mapping")
  ensure(branches.get(src) == r["source_sha"], "source branch SHA changed")
  ensure(dst not in expected, "duplicate target ref")
  expected[dst] = branches[src]
  refspecs[dst] = src + ":" + dst
 for r in manifest["tags"]:
  src = r["source_ref"]
  dst = r["target_ref"]
  ensure(src.startswith("refs/tags/") and dst == "refs/tags/imported-cwo/" + src[len("refs/tags/"):], "unsafe tag mapping")
  ensure(tags.get(src) == r["source_object_sha"], "source tag object SHA changed")
  ensure(dst not in expected, "duplicate target ref")
  expected[dst] = tags[src]
  refspecs[dst] = src + ":" + dst
 ensure(len(expected) == 51 and len(refspecs) == 51, "unexpected manifest import cardinality")
 unexpected = sorted(set(existing) - set(expected))
 mismatched = sorted(ref for ref in existing if ref in expected and existing[ref] != expected[ref])
 ensure(not unexpected, "unrecognized imported ref(s): " + ", ".join(unexpected[:5]))
 ensure(not mismatched, "imported ref SHA mismatch: " + ", ".join(mismatched[:5]))
 return expected, refspecs, sorted(set(expected) - set(existing))

def sanitized_push_error(proc, token):
 """Keep actionable Git transport rejection text without echoing credentials."""
 raw = proc.stderr.decode("utf-8","replace") if isinstance(proc.stderr, bytes) else (proc.stderr or "")
 if token: raw = raw.replace(token, "[REDACTED_TOKEN]")
 raw = re.sub(r"(?i)(authorization:\\s*basic)\\s+[^\\s]+", r"\\1 [REDACTED]", raw)
 raw = re.sub(r"(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{12,}", "[REDACTED_GITHUB_TOKEN]", raw)
 raw = re.sub(r"(?:xox[baprs]-)[A-Za-z0-9-]{12,}", "[REDACTED_SLACK_TOKEN]", raw)
 return " | ".join(raw.splitlines()).strip()[-1400:] or "no Git transport message provided"

def scan():
 objectlines=run("git","rev-list","--objects","--all",cwd=MIRROR).splitlines()
 objects=sorted(set(line.split(" ",1)[0] for line in objectlines))
 names={}
 for line in objectlines:
  oid,_,path=line.partition(" ")
  if path:names.setdefault(oid,set()).add(path)
 findings=[]; count=0
 for oid in objects:
  if run("git","cat-file","-t",oid,cwd=MIRROR)!="blob":continue
  count+=1
  paths=sorted(names.get(oid,[]))
  reason=[]
  size=int(run("git","cat-file","-s",oid,cwd=MIRROR))
  if size>20000000:reason.append("large_blob_not_fully_scanned")
  if any(NAME_RISK.search(p) for p in paths):reason.append("sensitive_path")
  if size<=20000000:
   raw=subprocess.run(["git","cat-file","blob",oid],cwd=MIRROR,capture_output=True,check=True).stdout
   reason += [label for label,regex in PATTERNS.items() if re.search(regex,raw)]
  if reason:findings.append({"blob_sha":oid,"paths":paths[:8],"reason_codes":sorted(set(reason))})
 return {"unique_blobs_checked":count,"findings":findings,"scope":"Pattern-based only; no independent privacy certification"}

def main():
 mode=os.getenv("HISTORY_MODE","audit")
 report={"schema_version":"1.0.0","mode":mode,"status":"UNVERIFIED","source_main_pin":PIN_SRC,"destination_initial_main":PIN_DST}
 REPORT.parent.mkdir(parents=True,exist_ok=True)
 try:
  ensure(mode in ("audit","import"),"invalid action")
  if mode=="import":ensure(os.getenv("IMPORT_CONFIRMATION")=="IMPORT_47_BRANCHES_4_TAGS","missing explicit import confirmation")
  anc=subprocess.run(["git","merge-base","--is-ancestor",PIN_DST,"HEAD"],capture_output=True).returncode==0
  ensure(anc,"destination original commit no longer an ancestor")
  run("git","fetch","--no-tags","origin","refs/heads/migration/phase1_communication_source_20261107")
  ensure(run("git","rev-parse","FETCH_HEAD")==PIN_STAGE,"staging source-manifest SHA changed")
  manifest=json.loads(run("git","show",PIN_STAGE+":migration/audit/phase1-source-snapshot.v1.json"))
  ensure(manifest["source"]["pinned_main_commit"]==PIN_SRC,"manifest source pin mismatch")
  ensure(manifest["file_QA"]["sha_mode_size_match"]==448,"448-file QA missing")
  run("git","clone","--mirror","--quiet",SOURCE,str(MIRROR))
  branches=refmap("refs/heads");tags=refmap("refs/tags")
  wantb={r["source_ref"]:r["source_sha"] for r in manifest["branches"]}
  wantt={r["source_ref"]:r["source_object_sha"] for r in manifest["tags"]}
  ensure(branches==wantb and tags==wantt,"source branch/tag mapping changed")
  ensure(len(branches)==47 and len(tags)==4 and branches.get("refs/heads/main")==PIN_SRC,"expected source ref counts/head mismatch")
  run("git","fsck","--full","--no-reflogs",cwd=MIRROR)
  report.update(branches=47,tags=4)
  report["scan"]=scan()
  ensure(not report["scan"]["findings"],"potential credentials in history; inspect sanitized audit")
  existing=remote_map()
  expected, refspecs, missing=build_import_plan(manifest,branches,tags,existing)
  report.update(
   matched_existing_refs=len(existing),
   missing_refs_before_run=len(missing),
   refs_created_this_run=[],
   import_namespace_validated=True,
  )
  if mode=="audit":
   report["status"]="AUDIT_PASS_PARTIAL_IMPORT_PRESENT__NO_WRITE" if existing else "AUDIT_PASS_NO_IMPORT"
   return 0
  token=os.environ.get("GITHUB_TOKEN","")
  ensure(bool(token),"write token unavailable")
  header="AUTHORIZATION: basic "+base64.b64encode(("x-access-token:"+token).encode()).decode()
  # Single-ref pushes make each rejected ref identifiable. Already-correct refs are never overwritten.
  for target in missing:
   refspec=refspecs[target]
   cmd=["git","-c","http.https://github.com/.extraheader="+header,"push",DEST,refspec]
   dry=subprocess.run(cmd[:4]+["--dry-run"]+cmd[4:],cwd=MIRROR,capture_output=True)
   ensure(dry.returncode==0, "dry-run rejected "+target+": "+sanitized_push_error(dry,token))
   actual=subprocess.run(cmd,cwd=MIRROR,capture_output=True)
   ensure(actual.returncode==0, "push rejected "+target+": "+sanitized_push_error(actual,token))
   latest=remote_map()
   ensure(latest.get(target)==expected[target], "provider readback mismatch for "+target)
   ensure(not (set(latest)-set(expected)), "unexpected imported ref created")
   report["refs_created_this_run"].append(target)
  actual=remote_map()
  ensure(actual==expected,"final provider ref readback mismatch")
  report["status"]="IMPORTED_47_BRANCHES_4_TAGS__NO_MAIN_CHANGE"
  return 0
 except Exception as exc:
  report["status"]="HOLD";report["error"]=str(exc)
  try:
   observed=remote_map()
   report["imported_refs_observed_after_failure"]=len(observed)
   report["imported_ref_names_after_failure"]=sorted(observed)
  except Exception:
   report["imported_refs_observed_after_failure"]="UNKNOWN_PROVIDER_READBACK_FAILED"
  print("HOLD: "+str(exc),file=sys.stderr)
  return 1
 finally:
  REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
  print("Historical transfer status: "+report["status"])

if __name__=="__main__":sys.exit(main())
