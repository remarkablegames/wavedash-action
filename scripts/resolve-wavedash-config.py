#!/usr/bin/env python3
"""Resolve upload_dir and entrypoint from wavedash.toml for later steps.

The config is the source of truth for wavedash build push, so later steps read
the values from it rather than from the action inputs. Inputs are only a
fallback for a missing or blank key, which the CLI also treats as unset.
"""

import os
import sys
import tomllib


def read_config(path: str) -> dict:
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError) as error:
        print(f"Could not read {path}, using action inputs: {error}", file=sys.stderr)
        return {}


def main() -> None:
    if len(sys.argv) != 4:
        print(
            f"Usage: {sys.argv[0]} <config> <upload-dir> <entrypoint>", file=sys.stderr
        )
        sys.exit(1)

    config = read_config(sys.argv[1])

    def resolve(key: str, fallback: str) -> str:
        value = config.get(key)
        return value if isinstance(value, str) and value else fallback

    lines = [
        f"upload-dir={resolve('upload_dir', sys.argv[2])}",
        f"entrypoint={resolve('entrypoint', sys.argv[3])}",
    ]

    destination = os.environ.get("GITHUB_OUTPUT")
    if destination:
        with open(destination, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()
