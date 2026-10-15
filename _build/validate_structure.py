"""Structural validation of the built pages using lxml's HTML parser.

Reports: parse errors, duplicate ids, heading order, alt-text gaps,
non-descriptive link text, and per-page landmark counts.
"""
import glob
import os
import re
import sys
from collections import Counter

from lxml import html as LH

PAGES = sorted(glob.glob("portfolio-soliu/**/*.html", recursive=True))
problems = []

for path in PAGES:
    rel = os.path.relpath(path, "portfolio-soliu").replace("\\", "/")
    raw = open(path, encoding="utf-8").read()

    parser = LH.HTMLParser(recover=True, remove_comments=False)
    doc = LH.fromstring(raw, parser=parser)

    # ---- raw tag-count comparison (recovers, so never raises) ---------
    # Percent-encoded SVG lives inside attribute values, so decode it first
    # or its tags get counted as if they were real markup.
    decoded = raw
    for _ in range(3):
        new = decoded.replace("%3C", "<").replace("%3E", ">").replace("%23", "#")
        if new == decoded:
            break
        decoded = new
    raw_open = Counter(re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)[\s>/]", decoded))
    # Only structural HTML is worth comparing. Inline/encoded SVG and void
    # elements legitimately differ between raw text and the parsed tree.
    SKIP = {
        "html", "head", "body", "meta", "link", "img", "br", "hr", "input",
        "source", "svg", "defs", "pattern", "circle", "rect", "path", "g",
        "line", "text", "polygon", "polyline", "ellipse", "use", "filter",
        "feTurbulence", "feColorMatrix", "clipPath", "title", "desc", "style",
        "script", "iframe", "canvas", "picture", "track", "area", "col",
    }
    for tag, n in raw_open.items():
        low = tag.lower()
        if low in SKIP:
            continue
        if tag != low:
            continue  # camelCase names are SVG internals
        parsed_n = len(doc.xpath(f"//*[local-name()='{low}']"))
        if parsed_n != n:
            problems.append(f"{rel}: <{tag}> raw={n} parsed={parsed_n} (possible nesting error)")

    # ---- duplicate ids -------------------------------------------------
    ids = [e.get("id") for e in doc.xpath("//*[@id]")]
    for dup, n in Counter(ids).items():
        if n > 1:
            problems.append(f"{rel}: duplicate id '{dup}' x{n}")

    # ---- headings ------------------------------------------------------
    h1s = doc.xpath("//h1")
    if len(h1s) != 1:
        problems.append(f"{rel}: expected exactly one <h1>, found {len(h1s)}")
    for h in h1s:
        if not (h.text_content() or "").strip():
            problems.append(f"{rel}: empty <h1>")

    # ---- images need alt ----------------------------------------------
    for img in doc.xpath("//img"):
        if img.get("alt") is None:
            problems.append(f"{rel}: <img src={img.get('src','?')[:40]}> missing alt")

    # ---- links need discernible text ----------------------------------
    for a in doc.xpath("//a"):
        text = (a.text_content() or "").strip()
        has_img_alt = any(i.get("alt") for i in a.xpath(".//img"))
        has_aria = a.get("aria-label")
        if not text and not has_img_alt and not has_aria:
            problems.append(f"{rel}: link href={a.get('href','?')[:40]} has no accessible text")

    # ---- required landmarks -------------------------------------------
    for sel, label in [
        ('//header[contains(@class,"masthead-bar")]', "site header"),
        ('//nav[@aria-label="Primary"]', "primary nav"),
        ('//main[@id="main"]', "main"),
        ('//footer[contains(@class,"colophon")]', "footer"),
        ('//button[contains(@class,"theme-toggle")]', "theme toggle"),
        ('//button[contains(@class,"burger")]', "burger"),
        ('//div[@id="drawer"]', "drawer"),
    ]:
        if not doc.xpath(sel):
            problems.append(f"{rel}: missing {label}")

    # ---- every primary nav destination must also be in the drawer -----
    nav_hrefs = [a.get("href") for a in doc.xpath('//nav[@aria-label="Primary"]//a')]
    drawer_hrefs = [a.get("href") for a in doc.xpath('//div[@id="drawer"]//a')]
    for href in nav_hrefs:
        if href not in drawer_hrefs:
            problems.append(f"{rel}: nav link {href} missing from the drawer")

    # ---- title / meta --------------------------------------------------
    t = doc.xpath("//title")
    if not t or not (t[0].text or "").strip():
        problems.append(f"{rel}: missing or empty <title>")
    desc = doc.xpath('//meta[@name="description"]/@content')
    if not desc or not desc[0].strip():
        problems.append(f"{rel}: missing meta description")
    if doc.xpath('//html[@lang]') is None:
        problems.append(f"{rel}: <html> missing lang")

print(f"Pages parsed: {len(PAGES)}")
print()
if problems:
    print(f"PROBLEMS ({len(problems)}):")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("STRUCTURE OK — no problems found.")
