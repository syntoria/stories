# stories.syntoria.co

Client-facing pages for The Syntoria Institute's case-study service.
One directory per coach engagement, served by GitHub Pages.

- `/josh/` — Beta 1, Josh Dietrich. The page his client reads before saying yes.

## Before adding anything here

These pages are **public to anyone holding the link**. GitHub Pages has no
password protection, and this repository is public. `noindex,nofollow` and
`robots.txt` keep the pages out of search results — that is unlisted, not
private. Never publish anything a stranger should not see.

## Editing a page

`src/` holds the source; the built page at `<name>/index.html` is generated and
should not be hand-edited. Edit the source, rebuild, commit both:

    python3 build.py src/josh.html josh/index.html

The sources are Claude artifact bodies — no doctype, no `<head>`, no `<body>`,
because claude.ai adds that wrapper at publish time. `build.py` adds the same
wrapper plus the `noindex` directive, so the deployed page renders as the
artifact does.

`/josh/` began as artifact `a19ab16b-6bd5-4d82-9969-f1a948a0e1a6`. That artifact
is **no longer in sync**: the deployed page carries a 125% scale rule the
artifact does not have. Treat `src/` as authoritative.

## The Tally CTA link

Every coach page's CTA must link the participation form **with tracking
parameters** — they fill the form's hidden `coach` and `case` fields so each
submission arrives tagged with the engagement it belongs to:

    https://tally.so/r/Bzq7QY?coach=Full%20Name&case=<story-id>

`coach` is the coach's full name (URL-encode spaces and accents); `case` is the
case's story ID from Notion, e.g. `SYN-2026-001` — per the service playbook
(Step 2), which is authoritative. A bare `https://tally.so/r/Bzq7QY` loses the
tracking. Same rule applies when sharing the form link directly (email,
LinkedIn) instead of the story page.

## Icons

The favicon set is generated from the brand's rising-sun mark, kept in
`brand/logo-mark-white.png` (pulled from the Syntoria Design System). Rebuild
it with:

    python3 make_favicon.py

Do not hand-edit the generated `favicon*`, `apple-touch-icon.png` or `icon-*`
files. If the mark itself changes, replace the file in `brand/` and rerun.

## Caching

GitHub Pages serves with a ten-minute cache. After a push, a browser that
already has the page may keep showing the old one for a few minutes. Append
`?v=2` to the URL to force a fresh copy when checking a change.
