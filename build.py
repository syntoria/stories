"""Wrap a page source from src/ into a standalone HTML file for GitHub Pages.

The sources in src/ are Claude artifact bodies: no doctype, no <head>, no
<body>, because claude.ai supplies that wrapper at publish time. This script
supplies the same wrapper so the deployed page renders identically, and adds
the noindex directive the artifact has no way to carry.

    python3 build.py src/josh.html josh/index.html
"""

import os
import re
import sys

# The minimal reset claude.ai applies around every artifact. The pages are
# designed against it, so it has to be reproduced here verbatim.
RESET = (
    ":root{color-scheme:light}"
    "body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;"
    "background:#faf9f5;color:#141413}"
    "img{max-width:100%}"
)

# Absolute paths so the icons resolve the same from /josh/ as from the root.
ICONS = """<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title}</title>
{icons}
<style>{reset}</style>
</head>
<body>
{body}
</body>
</html>
"""


def main(src, dest):
    body = open(src, encoding="utf-8").read()

    # A full document was passed in — take just what is inside <body>.
    if "<body>" in body:
        body = body[body.find("<body>") + len("<body>") : body.rfind("</body>")]

    # Artifacts carry their <title> inside the body; lift it into <head>.
    match = re.search(r"<title>(.*?)</title>", body, re.S)
    if not match:
        sys.exit(f"{src}: no <title> found")
    title = match.group(1).strip()
    body = (body[: match.start()] + body[match.end() :]).strip()

    page = TEMPLATE.format(title=title, icons=ICONS, reset=RESET, body=body)

    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    open(dest, "w", encoding="utf-8").write(page)

    links = [h for h in re.findall(r'href="([^"]+)"', body) if not h.startswith("data:")]
    print(f"{src} -> {dest}")
    print(f"  title: {title}")
    print(f"  bytes: {len(page):,}")
    print(f"  links: {', '.join(links) or 'none'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
