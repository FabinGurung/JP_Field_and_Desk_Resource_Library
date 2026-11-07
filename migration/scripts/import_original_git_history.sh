#!/usr/bin/env bash
# A9/A7 Phase 1 history-transfer gate. Nothing executes automatically.
# Run from Git Bash or a POSIX shell with networked authenticated git.
set -euo pipefail
SOURCE='https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub.git'
DEST='https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library.git'
PIN_SOURCE='4eb68c004fbe8d19b83bf3b17327c853debef58a'
PIN_DEST='336a274c2660998041aad506a32b76d03e194e3f'
WORKDIR='./A9_CWO_GIT_MIRROR_20261107.git'
if [[ -e "$WORKDIR" ]]; then echo 'HOLD: local mirror path already exists; do not overwrite' >&2; exit 2; fi
git clone --mirror "$SOURCE" "$WORKDIR"
ACTUAL_SOURCE="$(git -C "$WORKDIR" rev-parse refs/heads/main)"
if [[ "$ACTUAL_SOURCE" != "$PIN_SOURCE" ]]; then echo 'HOLD: source main changed; re-audit before import' >&2; exit 3; fi
COUNT_B="$(git -C "$WORKDIR" for-each-ref refs/heads --format='%(refname)' | wc -l | tr -d ' ')"
COUNT_T="$(git -C "$WORKDIR" for-each-ref refs/tags --format='%(refname)' | wc -l | tr -d ' ')"
if [[ "$COUNT_B" != 47 || "$COUNT_T" != 4 ]]; then echo 'HOLD: source branch/tag inventory changed' >&2; exit 4; fi
git -C "$WORKDIR" remote add destination "$DEST"
ACTUAL_DEST="$(git -C "$WORKDIR" ls-remote destination refs/heads/main | awk '$2=="refs/heads/main"{print $1}')"
if [[ "$ACTUAL_DEST" != "$PIN_DEST" ]]; then echo 'HOLD: destination main changed; re-audit before import' >&2; exit 5; fi
if [[ -n "$(git -C "$WORKDIR" ls-remote destination 'refs/heads/imported/cwo/*' 'refs/tags/imported-cwo/*')" ]]; then echo 'HOLD: imported refs already exist; reconcile rather than overwrite' >&2; exit 6; fi
git -C "$WORKDIR" push --dry-run destination 'refs/heads/*:refs/heads/imported/cwo/*'
git -C "$WORKDIR" push --dry-run destination 'refs/tags/*:refs/tags/imported-cwo/*'
if [[ "$(printenv CONFIRM_HISTORY_IMPORT || true)" != YES ]]; then
  echo 'DRY RUN ONLY. After source-history security review, set CONFIRM_HISTORY_IMPORT=YES and run again.'
  exit 0
fi
# Never force push. Imported refs are under their own namespace.
git -C "$WORKDIR" push destination 'refs/heads/*:refs/heads/imported/cwo/*'
git -C "$WORKDIR" push destination 'refs/tags/*:refs/tags/imported-cwo/*'
git -C "$WORKDIR" for-each-ref refs/heads --format='%(refname:strip=2) %(objectname)' | while read -r name sha; do
  ref="refs/heads/imported/cwo/$name"
  actual="$(git -C "$WORKDIR" ls-remote destination "$ref" | awk -v r="$ref" '$2==r{print $1}')"
  if [[ "$sha" != "$actual" ]]; then echo "HOLD: branch mismatch $name" >&2; exit 7; fi
done
git -C "$WORKDIR" for-each-ref refs/tags --format='%(refname:strip=2) %(objectname)' | while read -r name sha; do
  ref="refs/tags/imported-cwo/$name"
  actual="$(git -C "$WORKDIR" ls-remote destination "$ref" | awk -v r="$ref" '$2==r{print $1}')"
  if [[ "$sha" != "$actual" ]]; then echo "HOLD: tag mismatch $name" >&2; exit 8; fi
done
echo 'ALL 47 BRANCH REFS AND FOUR TAG REFS TRANSFERRED WITH IDENTICAL OBJECT HASHES.'
echo 'NEXT: audit reachable commit graph, integrate histories on another staging branch; do not touch main.'
