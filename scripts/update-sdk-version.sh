#!/usr/bin/env bash
set -euo pipefail

# Get the current pinned SDK version from action.yml
CURRENT_SDK_VERSION=$(grep -oE 'default: [0-9]+\.[0-9]+\.[0-9]+' action.yml | head -1 | awk '{print $2}')

if [ -z "$CURRENT_SDK_VERSION" ]; then
  echo "Could not find current SDK version in action.yml" >&2
  exit 1
fi

# Fetch the latest version from the npm registry
LATEST_SDK_VERSION=$(
  curl -s https://registry.npmjs.org/@wvdsh/sdk-js/latest |
    python3 -c "import sys, json; print(json.load(sys.stdin)['version'])"
)

if [ -z "$LATEST_SDK_VERSION" ]; then
  echo "Could not fetch latest SDK version from npm registry" >&2
  exit 1
fi

if [ "$CURRENT_SDK_VERSION" = "$LATEST_SDK_VERSION" ]; then
  echo "SDK version is up to date: $CURRENT_SDK_VERSION"
  exit 0
fi

# Bump the action's patch version for this dependency update
CURRENT_ACTION_VERSION=$(cat version.txt)
BUMPED_ACTION_VERSION=$(
  python3 - "$CURRENT_ACTION_VERSION" << 'PY'
import re
import sys

version = sys.argv[1]
match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
if not match:
    print(f"Invalid action version: {version}", file=sys.stderr)
    sys.exit(1)

major, minor, patch = match.groups()
print(f"{major}.{minor}.{int(patch) + 1}")
PY
)

echo "Updating SDK version from $CURRENT_SDK_VERSION to $LATEST_SDK_VERSION"
echo "Bumping action version from $CURRENT_ACTION_VERSION to $BUMPED_ACTION_VERSION"

# Update the SDK version in action.yml and README.md, and bump version.txt
python3 - "$CURRENT_SDK_VERSION" "$LATEST_SDK_VERSION" "$BUMPED_ACTION_VERSION" << 'PY'
import sys

old_sdk = sys.argv[1]
new_sdk = sys.argv[2]
new_action_version = sys.argv[3]

for path in ("action.yml", "README.md"):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    updated = content.replace(old_sdk, new_sdk)

    if updated != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)

with open("version.txt", "w", encoding="utf-8") as f:
    f.write(new_action_version + "\n")

print(f"SDK: {old_sdk} -> {new_sdk}")
print(f"Action: {new_action_version}")
PY

if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "old-sdk-version=$CURRENT_SDK_VERSION" >> "$GITHUB_OUTPUT"
  echo "sdk-version=$LATEST_SDK_VERSION" >> "$GITHUB_OUTPUT"
  echo "action-version=$BUMPED_ACTION_VERSION" >> "$GITHUB_OUTPUT"
fi
