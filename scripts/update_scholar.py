#!/usr/bin/env python3
"""Refresh publications and citation metrics in index.html from Google Scholar.

Reads the public Google Scholar profile, merges hand-edited formatting from
data/publication-overrides.json, and rewrites the marked regions of index.html
(data-scholar="..." elements and <!-- scholar:...:start/end --> blocks) using the
same markup as the rest of the site. Also writes data/scholar.json.

If Scholar blocks the request or returns suspicious data, nothing is changed.

Usage:
  python3 scripts/update_scholar.py            # fetch live
  python3 scripts/update_scholar.py --html f   # parse a saved profile page
"""
import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

USER_ID = "x6gjq2cAAAAJ"
HIGHLIGHT_SURNAME = "Bhati"
PROFILE_URL = f"https://scholar.google.com/citations?user={USER_ID}&hl=en&cstart=0&pagesize=100"
ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
OVERRIDES = ROOT / "data" / "publication-overrides.json"
DATA = ROOT / "data" / "scholar.json"
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "with", "via"}


def warn(msg):
    print(f"::warning::{msg}")


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).replace("\xa0", " ").strip()


def parse_profile(page):
    if 'id="gsc_prf_in"' not in page:
        raise ValueError("profile not found in response (likely a CAPTCHA or block page)")
    stats = [int(n) for n in re.findall(r'class="gsc_rsb_std">(\d+)<', page)]
    if len(stats) < 6:
        raise ValueError("citation metrics table not found")
    pubs = []
    for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S):
        link = re.search(r'citation_for_view=([^"&]+)[^>]*class="gsc_a_at">(.*?)</a>', row, re.S)
        grays = re.findall(r'class="gs_gray">(.*?)</div>', row, re.S)
        cites = re.search(r'class="gsc_a_ac[^"]*">(\d*)<', row)
        year = re.search(r'class="gsc_a_h gsc_a_hc gs_ibl">(\d*)<', row)
        if not link:
            continue
        pubs.append({
            "id": html.unescape(link.group(1)),
            "title": text(link.group(2)),
            "authors_raw": text(grays[0]) if grays else "",
            "venue_raw": text(grays[1]) if len(grays) > 1 else "",
            "citations": int(cites.group(1)) if cites and cites.group(1) else 0,
            "year": int(year.group(1)) if year and year.group(1) else 0,
        })
    return {"citations": stats[0], "h_index": stats[2], "i10_index": stats[4], "publications": pubs}


def format_authors(raw):
    out = []
    for name in [a.strip() for a in raw.split(",") if a.strip()]:
        if name in ("...", "…"):
            out.append("et al.")
            continue
        parts = name.split()
        if len(parts) > 1 and re.fullmatch(r"[A-Z]{1,4}", parts[0]):
            name = " ".join(f"{c}." for c in parts[0]) + " " + " ".join(parts[1:])
        out.append(name)
    return ", ".join(out)


def title_case(name):
    words = name.split(" ")
    result = []
    for i, w in enumerate(words):
        if i > 0 and w.lower() in SMALL_WORDS:
            result.append(w.lower())
        elif w[:1].islower():
            result.append(w[:1].upper() + w[1:])
        else:
            result.append(w)
    return " ".join(result)


def split_venue(raw, title, year):
    """Turn Scholar's 'Journal name 26 (10), 667-674, 2021' into (venue, details)."""
    v = raw.strip()
    if year:
        v = re.sub(rf",?\s*{year}$", "", v).strip()
    if not v or v.endswith("…") and title.lower().startswith(v.rstrip("… ").lower()[:30]):
        return "", ""
    m = re.match(r"^(.*?)\s+(\d+)\s*\(([^)]+)\)\s*,\s*([\d\-–]+)$", v)
    if m:
        return title_case(m.group(1)), f"{m.group(2)}({m.group(3)}), {m.group(4).replace('-', '–')}"
    m = re.match(r"^(.*?)\s+(\d+)\s*\(([^)]+)\)$", v)
    if m:
        return title_case(m.group(1)), f"{m.group(2)}({m.group(3)})"
    m = re.match(r"^(.*?)\s+(Vol\.?\s*\d+)\s*,\s*([\d\-–]+)$", v)
    if m:
        return title_case(m.group(1)), f"{m.group(2)}, {m.group(3).replace('-', '–')}"
    m = re.match(r"^(.*?)\s*,\s*([\d\-–]+)$", v)
    if m and "-" in m.group(2):
        return title_case(m.group(1)), m.group(2).replace("-", "–")
    return title_case(v), ""


def build(profile, overrides):
    pubs = []
    for p in profile["publications"]:
        o = overrides.get(p["id"], {})
        if o.get("hide"):
            continue
        venue, details = split_venue(p["venue_raw"], p["title"], p["year"])
        pubs.append({
            "id": p["id"],
            "title": o.get("title", p["title"]),
            "authors": o.get("authors", format_authors(p["authors_raw"])),
            "prefix": o.get("prefix", ""),
            "venue": o.get("venue", venue),
            "details": o.get("details", details),
            "year": p["year"],
            "citations": p["citations"],
        })
    # Scholar lists by citations; a stable sort keeps that order within a year.
    pubs.sort(key=lambda p: (-p["year"], -p["citations"]))
    return pubs


def esc(s):
    return html.escape(s, quote=False)


def authors_html(authors):
    parts = []
    for a in authors.split(", "):
        parts.append(f"<strong>{esc(a)}</strong>" if a.split()[-1:] == [HIGHLIGHT_SURNAME] else esc(a))
    return ", ".join(parts)


def source_html(p):
    """Prefix, italic venue and details, e.g. 'Book chapter, <em>Venue</em>, Vol. 9, 1–2'."""
    bits = [esc(p["prefix"])] if p["prefix"] else []
    if p["venue"]:
        bits.append(f"<em>{esc(p['venue'])}</em>")
    if p["details"]:
        bits.append(esc(p["details"]))
    return ", ".join(bits)


def render_list(pubs):
    items = []
    for p in pubs:
        meta = [m for m in (source_html(p), f'<span class="pub-year">{p["year"]}</span>' if p["year"] else "") if m]
        if p["citations"]:
            meta.append(f"Cited by {p['citations']}")
        items.append(
            f'          <li data-year="{p["year"]}" data-cites="{p["citations"]}">\n'
            f'            <p class="pub-title">{esc(p["title"])}</p>\n'
            f'            <p class="pub-authors">{authors_html(p["authors"])}</p>\n'
            f'            <p class="pub-meta">{" · ".join(meta)}</p>\n'
            f"          </li>\n"
        )
    return "".join(items)


def render_featured(pubs):
    top = max(pubs, key=lambda p: p["citations"])
    source = ", ".join(x for x in (source_html(top), str(top["year"]) if top["year"] else "") if x)
    label = "citation" if top["citations"] == 1 else "citations"
    return (
        '        <article class="featured-pub">\n'
        f'          <span class="tag">Most cited · {top["citations"]} {label}</span>\n'
        f'          <h3>{esc(top["title"])}</h3>\n'
        f'          <p class="pub-authors">{authors_html(top["authors"])} · {source}</p>\n'
        "        </article>\n"
    )


def replace_block(page, name, content):
    pattern = re.compile(rf"(<!-- scholar:{name}:start -->\n)(.*?)(\s*<!-- scholar:{name}:end -->)", re.S)
    if not pattern.search(page):
        raise ValueError(f"marker scholar:{name} missing from index.html")
    return pattern.sub(lambda m: m.group(1) + content.rstrip("\n") + m.group(3), page, count=1)


def replace_values(page, values):
    for key, value in values.items():
        pattern = re.compile(rf'(<(\w+)[^>]*data-scholar="{key}"[^>]*>)(.*?)(</\2>)', re.S)
        page = pattern.sub(lambda m: m.group(1) + esc(str(value)) + m.group(4), page)
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", help="parse a saved Scholar profile page instead of fetching")
    args = ap.parse_args()

    try:
        page = Path(args.html).read_text(encoding="utf-8") if args.html else fetch(PROFILE_URL)
        profile = parse_profile(page)
    except Exception as exc:  # network errors, HTTP 429, CAPTCHA pages
        warn(f"Google Scholar fetch failed, keeping existing data: {exc}")
        return 0

    previous = json.loads(DATA.read_text()) if DATA.exists() else None
    if not profile["publications"] or profile["citations"] == 0:
        warn("Scholar returned no publications or zero citations, keeping existing data")
        return 0
    if previous and len(profile["publications"]) < 0.8 * len(previous["publications"]):
        warn(f"Scholar returned {len(profile['publications'])} publications vs {len(previous['publications'])} before, keeping existing data")
        return 0

    overrides = {k: v for k, v in json.loads(OVERRIDES.read_text()).items() if not k.startswith("_")}
    pubs = build(profile, overrides)
    new_ids = [p["id"] for p in pubs if p["id"] not in overrides]
    if previous:
        known = {p["id"] for p in previous["publications"]}
        for p in pubs:
            if p["id"] not in known:
                print(f"New publication: {p['title']} (id {p['id']}). Add an entry to data/publication-overrides.json to adjust its formatting.")

    today = dt.date.today()
    page = INDEX.read_text(encoding="utf-8")
    updated = replace_values(page, {
        "citations": profile["citations"],
        "h-index": profile["h_index"],
        "i10-index": profile["i10_index"],
        "pub-count": len(pubs),
        "updated": today.strftime("%B %Y"),
    })
    updated = replace_block(updated, "featured", render_featured(pubs))
    updated = replace_block(updated, "list", render_list(pubs))

    data = {
        "source": PROFILE_URL,
        "citations": profile["citations"],
        "h_index": profile["h_index"],
        "i10_index": profile["i10_index"],
        "publications": pubs,
    }
    if previous and {k: v for k, v in previous.items() if k != "fetched"} == data:
        print("No changes from Google Scholar.")
        if updated != page:
            INDEX.write_text(updated, encoding="utf-8")
        return 0
    data["fetched"] = today.isoformat()
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    INDEX.write_text(updated, encoding="utf-8")
    print(f"Updated: {profile['citations']} citations, h-index {profile['h_index']}, {len(pubs)} publications"
          + (f"; {len(new_ids)} without formatting overrides" if new_ids else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
