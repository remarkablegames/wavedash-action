#!/usr/bin/env python3
"""Inject the Wavedash init script into the entrypoint HTML or JavaScript."""

import os
import re
import sys

MARKER = "Wavedash.init("

INIT_CALL = (
    "window.Wavedash&&(window.Wavedash.updateLoadProgressZeroToOne(1),"
    "window.Wavedash.init());"
)

INIT_SCRIPT = f"<script>{INIT_CALL}</script>"

ENTRYPOINTS = (".html", ".htm", ".js")


def calls_init(directory: str) -> bool:
    """Report whether any file under directory already calls Wavedash.init().

    The call may live in the entrypoint or in a script it loads, and bundlers
    do not rename globals, so the marker survives minification. The marker
    stops at the open paren so that init() calls with a config argument are
    matched too.
    """
    for root, _, files in os.walk(directory):
        for name in files:
            try:
                with open(
                    os.path.join(root, name), encoding="utf-8", errors="ignore"
                ) as f:
                    if MARKER in f.read():
                        return True
            except OSError:
                continue
    return False


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <upload-dir> <entrypoint>", file=sys.stderr)
        sys.exit(1)

    upload_dir = sys.argv[1]
    path = os.path.join(upload_dir, sys.argv[2])

    if not os.path.isfile(path):
        return

    extension = os.path.splitext(path)[1].lower()
    if extension not in ENTRYPOINTS:
        print(
            f"Entrypoint must be an HTML or JavaScript file: {sys.argv[2]}",
            file=sys.stderr,
        )
        sys.exit(1)

    if calls_init(upload_dir):
        return

    with open(path, encoding="utf-8") as f:
        content = f.read()

    if MARKER in content:
        return

    if extension == ".js":
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{content.rstrip()}\n{INIT_CALL}")
        return

    new_content, body_count = re.subn(
        r"(</body>)",
        INIT_SCRIPT + "\n" + r"\1",
        content,
        count=1,
        flags=re.IGNORECASE,
    )

    if body_count == 0:
        new_content = new_content + INIT_SCRIPT

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
