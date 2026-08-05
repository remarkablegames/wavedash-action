#!/usr/bin/env python3
"""Inject the Wavedash SDK modulepreload and script into the entrypoint HTML."""

import re
import sys


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <entrypoint.html> <sdk-version>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    version = sys.argv[2]

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    if "@wvdsh/sdk-js" in html:
        return

    sdk_url = f"https://esm.sh/@wvdsh/sdk-js@{version}"

    preload_link = f'<link rel="modulepreload" href="{sdk_url}">'

    sdk_script = (
        f'<script type="module">'
        f"import('{sdk_url}').then"
        f'(({{default:Wavedash}})=>{{'
        f'Wavedash.updateLoadProgressZeroToOne(1);'
        f'Wavedash.init();'
        f'}});'
        f'</script>'
    )

    new_html, head_count = re.subn(
        r"(</head>)",
        preload_link + "\n" + r"\1",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    new_html, body_count = re.subn(
        r"(</body>)",
        sdk_script + "\n" + r"\1",
        new_html,
        count=1,
        flags=re.IGNORECASE,
    )

    if body_count == 0:
        new_html = new_html + sdk_script

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)


if __name__ == "__main__":
    main()
