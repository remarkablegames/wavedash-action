#!/usr/bin/env bash
set -euo pipefail

# Get the current pinned SDK version from action.yml
CURRENT_VERSION=$(grep -oE 'default: [0-9]+\.[0-9]+\.[0-9]+' action.yml | head -1 | awk '{print $2}')

if [ -z "$CURRENT_VERSION" ]; then
  echo "Could not find current SDK version in action.yml" >&2
  exit 1
fi

# Fetch the latest version from the npm registry
LATEST_VERSION=$(curl -s https://registry.npmjs.org/@wvdsh/sdk-js/latest | grep -oE '"version":"[0-9]+\.[0-9]+\.[0-9]+"' | cut -d'"' -f4)

if [ -z "$LATEST_VERSION" ]; then
  echo "Could not fetch latest SDK version from npm registry" >&2
  exit 1
fi

if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
  echo "SDK version is up to date: $CURRENT_VERSION"
  exit 0
fi

echo "Updating SDK version from $CURRENT_VERSION to $LATEST_VERSION"

# Update the version in-place in action.yml and README.md
python3 - "$CURRENT_VERSION" "$LATEST_VERSION" action.yml README.md << 'PY'
import sys

old = sys.argv[1]
new = sys.argv[2]

for path in sys.argv[3:]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    updated = content.replace(old, new)

    if updated != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
PY

echo "Updated SDK version to $LATEST_VERSION"

if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "version=$LATEST_VERSION" >> "$GITHUB_OUTPUT"
fi
