#!/usr/bin/env bash
# Clones the 20 audited repositories at the commits read on 8 October 2026.
# Run from this folder: bash setup.sh
set -euo pipefail
mkdir -p repos
while read -r sha repo; do
  d="repos/${repo/\//__}"
  if [ ! -d "$d" ]; then
    git clone -q --filter=blob:none "https://github.com/$repo" "$d"
  fi
  git -C "$d" checkout -q "$sha"
  echo "ok $repo $sha"
done < repos-at-sha.txt
