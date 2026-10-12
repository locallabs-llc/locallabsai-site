#!/usr/bin/env python3
"""Builds the static pages from _src/ fragments into the repo root.

Run: python3 build.py   (no dependencies). Commit the generated files;
GitHub Pages serves them as-is.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://locallabsai.com"

# (source fragment, output file, canonical path, page title, meta description, nav key)
PAGES = [
    ("index.html", "index.html", "/", "Local Labs LLC",
     "Local Labs LLC is a small company that runs The Nani Company, an Etsy shop of digital planners, printable calendars and spreadsheet tools.",
     "home"),
    ("nani-company.html", "nani-company/index.html", "/nani-company/", "The Nani Company – Local Labs LLC",
     "The Nani Company sells digital planners, printable calendars and budgeting spreadsheets on Etsy. This page also explains our internal Pinterest integration.",
     "nani"),
    ("privacy.html", "privacy/index.html", "/privacy/", "Privacy Policy – Local Labs LLC",
     "How Local Labs LLC handles data for its website, its Etsy shop The Nani Company, and its internal Pinterest app.",
     "privacy"),
    ("terms.html", "terms/index.html", "/terms/", "Terms of Use – Local Labs LLC",
     "Terms of use for the locallabsai.com website.",
     "terms"),
    ("contact.html", "contact/index.html", "/contact/", "Contact – Local Labs LLC",
     "How to contact Local Labs LLC.",
     "contact"),
    ("404.html", "404.html", None, "Page not found – Local Labs LLC",
     "Page not found.",
     None),
]

NAV = [
    ("home", "/", "Home"),
    ("nani", "/nani-company/", "The Nani Company"),
    ("privacy", "/privacy/", "Privacy"),
    ("contact", "/contact/", "Contact"),
]

LOGO = ('<svg width="28" height="28" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<rect width="32" height="32" rx="7" fill="#1f5c4a"/>'
        '<path d="M9 8v16h7M18 8v16h6" fill="none" stroke="#fbfaf7" stroke-width="3" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{canonical}<meta name="color-scheme" content="light dark">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">{logo}<span>Local Labs</span></a>
    <nav class="site-nav" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>
<main id="main">
  <div class="wrap">
{body}
  </div>
</main>
<footer class="site-footer">
  <div class="wrap">
    <ul>
      <li><a href="/privacy/">Privacy Policy</a></li>
      <li><a href="/terms/">Terms of Use</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a href="mailto:support@locallabsai.com">support@locallabsai.com</a></li>
    </ul>
    <p>&copy; 2026 Local Labs LLC. This site uses no cookies and no analytics.</p>
  </div>
</footer>
</body>
</html>
"""


def nav_html(active):
    items = []
    for key, href, label in NAV:
        current = ' aria-current="page"' if key == active else ""
        items.append(f'        <li><a href="{href}"{current}>{label}</a></li>')
    return "\n".join(items)


def main():
    for src, out, path, title, description, key in PAGES:
        body = (ROOT / "_src" / src).read_text().rstrip()
        body = "\n".join(("    " + line) if line else "" for line in body.splitlines())
        canonical = f'<link rel="canonical" href="{SITE}{path}">\n' if path else ""
        html = TEMPLATE.format(title=title, description=description, canonical=canonical,
                               logo=LOGO, nav=nav_html(key), body=body)
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)
        print("built", out)


if __name__ == "__main__":
    main()
