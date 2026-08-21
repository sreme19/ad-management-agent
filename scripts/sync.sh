#!/usr/bin/env bash
# Keep this working directory in parity with GitHub.
#
# Meant to run ON WHATEVER MACHINE HOLDS A CLONE — most usefully on your
# laptop, on a cron/launchd schedule (see README.md "Keeping your laptop in
# sync"). It cannot reach any other machine; it only ever syncs the clone it
# runs inside against the `origin` remote.
#
# Safe to run at any time: never force-pushes, never discards uncommitted
# work. If it can't fast-forward cleanly it stops and leaves the working
# tree alone rather than guessing.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

branch="$(git rev-parse --abbrev-ref HEAD)"

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "sync: local changes $(date -u +%Y-%m-%dT%H:%M:%SZ)"
fi

git fetch origin "$branch"
git pull --rebase origin "$branch"
git push origin "$branch"
