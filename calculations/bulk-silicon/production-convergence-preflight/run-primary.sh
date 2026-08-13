#!/bin/bash
# PROPOSED PROTECTED EXECUTION — do not run without the exact human A decision.
set -euo pipefail

# Fail closed unless the parent supplies this token only after recording Option A.
[[ "${KSD_PRODUCTION_CONVERGENCE_AUTHORIZATION:-}" == \
  'A-EXECUTE-COMMITTED-PRIMARY' ]] || {
  echo 'Protected execution is not authorized.' >&2
  exit 77
}

EXPECTED_PW='6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca'
EXPECTED_UPF='39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282'
EXPECTED_RUN_ROOT_ID='9d84848b4abb0db89e70fa8f6af2dc5f94b122d9574397e60398986638b91bb5'
EXPECTED_INPUT_MANIFEST='cdb6a41cf266034dc7e7b3ed5f48006bbd7caef3ca815849919f1732934407be'
PSEUDO_RELATIVE='pseudodojo/1.0/pbe/nc-sr-04-standard/Si/Si.upf'

ROOT=${KSD_PRODUCTION_CONVERGENCE_ROOT:?Set the canonical campaign root}
PW=${KSD_QE_PW_X:?Set the canonical pw.x path}
REPOSITORY_ROOT=${KSD_REPOSITORY_ROOT:?Set the canonical repository root}
BOUNDARY_COMMIT=${KSD_BOUNDARY_COMMIT:?Set the exact committed preflight boundary}

ROOT=$(cd -- "$ROOT" && pwd -P)
PW_DIR=$(cd -- "$(dirname -- "$PW")" && pwd -P)
PW="$PW_DIR/$(basename -- "$PW")"
REPOSITORY_ROOT=$(cd -- "$REPOSITORY_ROOT" && pwd -P)
HOME_CANONICAL=$(cd -- "$HOME" && pwd -P)
USER_OPT="$HOME_CANONICAL/opt"
[[ -d "$USER_OPT" && ! -L "$HOME/opt" ]]
USER_OPT=$(cd -- "$USER_OPT" && pwd -P)
for component in pseudodojo 1.0 pbe nc-sr-04-standard Si; do
  [[ ! -L "$USER_OPT/$component" ]]
  USER_OPT="$USER_OPT/$component"
done
USER_OPT_ROOT=$(cd -- "$HOME_CANONICAL/opt" && pwd -P)
INSTALLED_UPF="$USER_OPT_ROOT/$PSEUDO_RELATIVE"
INSTALLED_DIR=$(cd -- "$(dirname -- "$INSTALLED_UPF")" && pwd -P)
INSTALLED_UPF="$INSTALLED_DIR/$(basename -- "$INSTALLED_UPF")"
case "$INSTALLED_UPF" in
  "$USER_OPT_ROOT"/*) ;;
  *) echo 'PseudoDojo path escapes user_opt.' >&2; exit 78 ;;
esac
[[ ! -L "$INSTALLED_UPF" ]]
[[ -z "$(find "$USER_OPT" -type l -print -quit)" ]]
COMMITTED_RUNNER="$REPOSITORY_ROOT/calculations/bulk-silicon/production-convergence-preflight/run-primary.sh"
[[ -f "$COMMITTED_RUNNER" && ! -L "$COMMITTED_RUNNER" ]]
[[ -f "$0" && ! -L "$0" ]]
cmp -s "$COMMITTED_RUNNER" "$0"

[[ -f "$PW" && ! -L "$PW" ]]
[[ "$(git -C "$REPOSITORY_ROOT" rev-parse HEAD)" == "$BOUNDARY_COMMIT" ]]
[[ "$(git -C "$REPOSITORY_ROOT" rev-parse origin/dev)" == "$BOUNDARY_COMMIT" ]]
[[ -z "$(git -C "$REPOSITORY_ROOT" status --porcelain)" ]]
RUN_ROOT_DESCRIPTOR=$(basename -- "$(dirname -- "$ROOT")")/$(basename -- "$ROOT")
[[ "$(printf '%s' "$RUN_ROOT_DESCRIPTOR" | shasum -a 256 | awk '{print $1}')" == \
  "$EXPECTED_RUN_ROOT_ID" ]]
[[ "$(shasum -a 256 "$PW" | awk '{print $1}')" == "$EXPECTED_PW" ]]
[[ "$(shasum -a 256 "$INSTALLED_UPF" | awk '{print $1}')" == "$EXPECTED_UPF" ]]
[[ "$(shasum -a 256 "$ROOT/pseudo/Si.upf" | awk '{print $1}')" == \
  "$EXPECTED_UPF" ]]
[[ "$(shasum -a 256 "$ROOT/INPUTS.sha256" | awk '{print $1}')" == \
  "$EXPECTED_INPUT_MANIFEST" ]]
cd -- "$ROOT"
sed 's#  inputs/#  input/#' INPUTS.sha256 | shasum -a 256 -c -

run_one() {
  local label="$1" input="$2" output="$3" diagnostics="$4"
  if ! /usr/bin/time -l "$PW" < "$input" > "$output" 2> "$diagnostics"; then
    echo "STOP: $label invocation failed; no later invocation was attempted." >&2
    exit 1
  fi
  if ! grep -Fq 'JOB DONE.' "$output"; then
    echo "STOP: $label lacks JOB DONE.; no later invocation was attempted." >&2
    exit 1
  fi
}

run_pair() {
  local series="$1" case="$2"
  run_one "$case SCF" \
    "$ROOT/input/$series/$case.scf.in" \
    "$ROOT/output/$case.scf.out" \
    "$ROOT/output/$case.scf.time-and-stderr"

  # Preserve the SCF native state; the NSCF mutates only this isolated copy.
  if [[ -e "$ROOT/scratch/$case-diagnostic" ]]; then
    echo "STOP: $case diagnostic scratch already exists." >&2
    exit 1
  fi
  mkdir "$ROOT/scratch/$case-diagnostic"
  cp -R "$ROOT/scratch/$case/si_$case.save" \
    "$ROOT/scratch/$case-diagnostic/"

  run_one "$case NSCF" \
    "$ROOT/input/$series/$case.diagnostic.nscf.in" \
    "$ROOT/output/$case.diagnostic.nscf.out" \
    "$ROOT/output/$case.diagnostic.nscf.time-and-stderr"
}

for case in C30 C36 C42 C48 C54 C60; do
  run_pair cutoff "$case"
done

# K8 at 48 Ry is C48 and is reused without another invocation.
for case in K6 K10 K12; do
  run_pair mesh "$case"
done
