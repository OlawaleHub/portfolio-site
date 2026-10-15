"""Verify every page of the site over HTTP.

Checks:
  1. Every HTML page returns 200.
  2. Every local href/src referenced anywhere resolves to 200 or 404.
  3. Every served page has the expected landmarks (nav, main, footer, title).
  4. Reports the exact failing URL for anything broken.

Run with the bundled Python while the local server is running.
"""
import collections
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8899/"

PAGES = [
    "index.html",
    "about.html",
    "portfolio.html",
    "notebook.html",
    "contact.html",
    "work/lagos-emergency.html",
    "work/ifeoluwa-medical.html",
    "work/token-gated-voting.html",
    "work/refcrypt-labs.html",
    "work/portfolio-builds.html",
    "work/mobile-flutter.html",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "site-verifier/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # noqa: BLE001
        return None, str(e).encode()


def is_local(ref):
    if not ref:
        return False
    if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#", "//")):
        return False
    return True


def normalise(page, ref):
    """Resolve ref relative to the *absolute* URL of page."""
    ref = ref.split("#")[0].strip()
    if not ref:
        return None
    return urllib.parse.urljoin(BASE + page, ref)


problems = []
page_status = {}

# ---------------------------------------------------------------- 1. pages
for page in PAGES:
    status, body = fetch(BASE + page)
    page_status[page] = (status, len(body))
    if status != 200:
        problems.append(f"PAGE {page} -> HTTP {status}")
        continue
    text = body.decode("utf-8", "replace")

    checks = {
        "doctype": text.lstrip().lower().startswith("<!doctype html>"),
        "title": "<title>" in text,
        "nav": 'aria-label="Primary"' in text,
        "main": 'id="main"' in text,
        "colophon": 'class="colophon"' in text,
        "stylesheet": "assets/css/site.css" in text or "../assets/css/site.css" in text,
        "script": "assets/js/site.js" in text or "../assets/js/site.js" in text,
        "viewport": 'name="viewport"' in text,
        "skip-link": 'class="skip-link"' in text,
    }
    for name, ok in checks.items():
        if not ok:
            problems.append(f"PAGE {page} missing: {name}")

    # balanced tag sanity for the main structural elements
    for tag in ("html", "head", "body", "main", "header", "footer"):
        opens = len(re.findall(rf"<{tag}[\s>]", text))
        closes = len(re.findall(rf"</{tag}>", text))
        if opens != closes:
            problems.append(f"PAGE {page}: <{tag}> open={opens} close={closes}")

# ---------------------------------------------------------------- 2. links
checked = {}
broken = []
for page in PAGES:
    status, body = fetch(BASE + page)
    if status != 200:
        continue
    text = body.decode("utf-8", "replace")
    refs = set(re.findall(r'(?:href|src)="([^"]+)"', text))
    for ref in refs:
        if not is_local(ref):
            continue
        url = normalise(page, ref)
        if url is None:
            continue
        if url in checked:
            st = checked[url]
        else:
            st, _ = fetch(url)
            checked[url] = st
        if st != 200:
            broken.append((page, ref, url, st))

for page, ref, url, st in broken:
    problems.append(f"LINK {page}: {ref} -> HTTP {st} ({url})")

# ---------------------------------------------------------------- 3. report
print("=" * 66)
print("PAGE STATUS")
print("=" * 66)
for page in PAGES:
    st, size = page_status.get(page, (None, 0))
    flag = "OK " if st == 200 else "FAIL"
    print(f"  {flag} {page:34} HTTP {st}  {size:>6} bytes")

print()
print("=" * 66)
print(f"LOCAL ASSETS/LINKS CHECKED: {len(checked)}")
print("=" * 66)
for url in sorted(checked, key=lambda u: (checked[u] != 200, u)):
    st = checked[url]
    flag = "OK  " if st == 200 else "FAIL"
    print(f"  {flag} HTTP {st}  {url.replace(BASE, '')}")

print()
print("=" * 66)
if problems:
    print(f"PROBLEMS: {len(problems)}")
    print("=" * 66)
    for p in problems:
        print("  -", p)
else:
    print("ALL CHECKS PASSED — no problems found.")
    print("=" * 66)

sys.exit(1 if problems else 0)
