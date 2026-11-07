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
  ensure(not remote_map(),"import refs already exist, no overwrite permitted")
  if mode=="audit":
   report["status"]="AUDIT_PASS_NO_IMPORT"
   return 0
  token=os.environ.get("GITHUB_TOKEN","")
  ensure(bool(token),"write token unavailable")
  header="AUTHORIZATION: basic "+base64.b64encode(("x-access-token:"+token).encode()).decode()
  refs=[k+":refs/heads/imported/cwo/"+k[len("refs/heads/"):] for k in sorted(branches)]
  refs += [k+":refs/tags/imported-cwo/"+k[len("refs/tags/"):] for k in sorted(tags)]
  cmd=["git","-c","http.https://github.com/.extraheader="+header,"push",DEST,*refs]
  dry=subprocess.run(cmd[:4]+["--dry-run"]+cmd[4:],cwd=MIRROR,capture_output=True)
  ensure(dry.returncode==0,"dry-run import refused by destination")
  actual=subprocess.run(cmd,cwd=MIRROR,capture_output=True)
  ensure(actual.returncode==0,"Git push failed; review partial refs before retry")
  want={"refs/heads/imported/cwo/"+k[len("refs/heads/"):]:v for k,v in branches.items()}
  want.update({"refs/tags/imported-cwo/"+k[len("refs/tags/"):]:v for k,v in tags.items()})
  ensure(remote_map()==want,"provider readback mismatch after push")
  report["status"]="IMPORTED_47_BRANCHES_4_TAGS__NO_MAIN_CHANGE"
  return 0
 except Exception as exc:
  report["status"]="HOLD";report["error"]=str(exc)
  print("HOLD: "+str(exc),file=sys.stderr)
  return 1
 finally:
  REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
  print("Historical transfer status: "+report["status"])

if __name__=="__main__":sys.exit(main())
