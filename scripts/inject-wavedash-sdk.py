#!/usr/bin/env python3
"""Inject the Wavedash SDK script before the closing </body> tag."""

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

    sdk_script = f'''    <script type="module">
        import('https://esm.sh/@wvdsh/sdk-js@{version}').then(
          ({{ default: Wavedash }}) => {{
            Wavedash.updateLoadProgressZeroToOne(1);
            Wavedash.init();
          }},
        );
    </script>'''

    new_html, count = re.subn(
        r"(</body>)",
        sdk_script + "\n" + r"\1",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    if count == 0:
        new_html = html + sdk_script

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)


if __name__ == "__main__":
    main()
