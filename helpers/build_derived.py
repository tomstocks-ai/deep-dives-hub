#!/usr/bin/env python3
"""Generate all derived artifacts from the per-ticker JSON files.

The per-ticker files ``docs/api/{TICKER}.json`` are the single source of
truth. Everything mechanical is (re)generated from them:

  1. ``docs/api/tickers.json``      — fully generated master index
  2. ``docs/table.md``              — master table, generated between markers
  3. thematic pages                 — summary-table rows and the mechanical
                                      parts of each gist (rating span,
                                      Bull/Base/Bear line) are rewritten
                                      in place; prose and ticker membership
                                      are left untouched
  4. ticker/theme counters          — in docs/index.md and docs/api-docs.md

Usage:
    python3 helpers/build_derived.py           # rewrite derived files
    python3 helpers/build_derived.py --check   # exit 1 if anything is stale
                                               # (used by CI)

Design notes:
  * Ticker membership of a thematic page is an editorial decision. It is
    inferred from the gists present on the page and never changed here —
    adding a ticker to a theme means adding its gist.
  * A ticker appears in tickers.json / table.md iff docs/api/{T}.json
    exists. A gist or table row without a JSON file is preserved as-is and
    reported as a warning (tests/test_consistency.py tracks these).
  * Output is deterministic: no timestamps are invented. The top-level
    ``last_updated`` of tickers.json is the max of the per-ticker values.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_DIR = ROOT / "docs" / "api"
DD_DIR = ROOT / "docs" / "deep-dives"
TABLE_MD = ROOT / "docs" / "table.md"
COUNTER_FILES = [ROOT / "docs" / "index.md", ROOT / "docs" / "api-docs.md",
                 ROOT / "README.md", ROOT / "deep_dives_mcp" / "README.md"]

BEGIN = "<!-- BEGIN GENERATED: {name} — do not edit, run helpers/build_derived.py -->"
END = "<!-- END GENERATED: {name} -->"

# --- presentation config ----------------------------------------------------

# Thematic pages in display order. (file stem, fallback badge label, css class)
THEME_PAGES = [
    ("AI_buildout", "AI Buildout", "badge-tech"),
    ("software", "Software", "badge-cloud"),
    ("energy", "Energy", "badge-energy"),
    ("critical-minerals", "Minerals", "badge-minerals"),
    ("fintech", "Fintech", "badge-fintech"),
    ("space", "Space", "badge-space"),
    ("defense", "Defense", "badge-defense"),
    ("biotech-health", "Biotech & Health", "badge-health"),
    ("quantum-computing", "Quantum", "badge-quantum"),
    ("evtol", "eVTOL", "badge-evtol"),
]

RATING_CLASS = {
    "BUY": "rating-buy",
    "SPEC. BUY": "rating-spec-buy",
    "HOLD": "rating-hold",
    "HOLD / SPEC.": "rating-spec-hold",
    "SELL": "rating-sell",
    "SPECULATIVE": "rating-spec",
}

# JSON "exchange" -> TradingView symbol prefix.
EXCHANGE_TV = {
    "NYSE": "NYSE",
    "NYSEAMERICAN": "NYSEAMERICAN",
    "AMEX": "AMEX",
    "NYSE Arca": "AMEX",
    "NASDAQ": "NASDAQ",
    "NasdaqCM": "NASDAQ",
    "NASDAQ / TSX": "NASDAQ",
    "OMXSTO": "OMXSTO",
    "KRX": "KRX",
}

# sub_theme -> (badge label, css class). Classes must exist in
# docs/stylesheets/extra.css. Unmapped sub-themes fall back to the badge of
# the thematic page the ticker's gist lives on.
SUBTHEME_BADGE = {
    "AI Compute": ("Semiconductors", "badge-semi"),
    "Analog / Power": ("Semiconductors", "badge-semi"),
    "Memory & Storage": ("Memory & Storage", "badge-memory"),
    "Semiconductor Equipment": ("Semi Equipment", "badge-semi-equip"),
    "Photonics & Optical Interconnects": ("Photonics", "badge-photonics"),
    "Networking & Connectivity": ("Networking", "badge-networking"),
    "Data Center Infrastructure": ("DC Infra", "badge-dc-infra"),
    "Electrical Contractors": ("DC Infra", "badge-dc-infra"),
    "Servers & Systems": ("DC Infra", "badge-dc-infra"),
    "AI / HPC Operators": ("DC & HPC", "badge-dc-hpc"),
    "Cloud Storage / Data Infrastructure": ("Cloud & Software", "badge-cloud"),
    "Cloud & Enterprise Software": ("Software", "badge-cloud"),
    "Game Engines & Marketing": ("Cloud & Software", "badge-cloud"),
    "Enterprise Software": ("Software", "badge-cloud"),
    "Data & Analytics": ("Cloud & Software", "badge-cloud"),
    "UX": ("Cloud & Software", "badge-cloud"),
    "Cybersecurity": ("Cybersecurity", "badge-cyber"),
    "Robotics & Automation": ("Robotics", "badge-robotics"),
    "Solid-State Batteries": ("Grid & Power", "badge-grid"),
    "Marine & Wave Energy": ("Grid & Power", "badge-grid"),
    "Grid-Scale Energy Storage": ("Grid & Power", "badge-grid"),
    "Grid-Scale Energy Storage / Grid & Power": ("Grid & Power", "badge-grid"),
    "Fuel Cells": ("Grid & Power", "badge-grid"),
    "Solar": ("Grid & Power", "badge-grid"),
    "Natural Gas & AI Power Demand": ("Grid & Power", "badge-grid"),
    "Reactor Developers": ("Nuclear", "badge-nuclear"),
    "Enrichment": ("Nuclear", "badge-nuclear"),
    "Enrichment / Fuel Cycle": ("Nuclear", "badge-nuclear"),
    "Uranium & Nuclear Fuel": ("Minerals", "badge-minerals"),
    "Specialty Metals": ("Nuclear", "badge-nuclear"),
    "Specialty Metals (Silver)": ("Minerals", "badge-minerals"),
    "Rare Earths / Specialty Metals": ("Minerals", "badge-minerals"),
    "Copper": ("Minerals", "badge-minerals"),
    "Gold": ("Minerals", "badge-minerals"),
    "Rare Earths": ("Minerals", "badge-minerals"),
    "Stablecoins / Crypto Finance": ("Fintech", "badge-fintech"),
    "Brokerage / Trading": ("Fintech", "badge-fintech"),
    "Payments / Digital Banking": ("Fintech", "badge-fintech"),
    "Banking / Diversified Financials": ("Fintech", "badge-fintech"),
    "Consumer Finance": ("Fintech", "badge-fintech"),
    "Satellite Connectivity": ("Space", "badge-space"),
    "Launch Vehicles": ("Space", "badge-space"),
    "Geospatial Intelligence": ("Space", "badge-space"),
    "Satellite Connectivity / Geospatial Intelligence": ("Space", "badge-space"),
    "Lunar / Deep Space": ("Space", "badge-space"),
    "Prime Contractors": ("Defense", "badge-defense"),
    "Telehealth & Digital Health": ("Biotech & Health", "badge-health"),
    "Medical Devices": ("Biotech & Health", "badge-health"),
    "Precision Medicine & Diagnostics": ("Biotech & Health", "badge-health"),
    "Pure Plays": ("Quantum", "badge-quantum"),
}

TICKER_ENTRY_FIELDS = [
    "ticker", "company", "sector", "industry", "rating", "price",
    "market_cap", "last_updated", "deep_dive_url", "api_url",
    "theme", "sub_theme", "price_date",
]

GIST_HEADER_RE = re.compile(r"^\*\*([A-Z0-9]{1,7}) — .*\*\*\s*$", re.M)
TARGETS_LINE_RE = re.compile(r"^\*\*Bull:\*\* .*\*\*Bear:\*\* .*$", re.M)
SUMMARY_HEADER_RE = re.compile(r"^\|\s*Ticker\s*\|\s*Company\s*\|", re.M)
ROW_TICKER_RE = re.compile(r'symbol="[^":]+:([A-Z0-9]{1,7})"')


class Reporter:
    def __init__(self) -> None:
        self.warnings: list[str] = []
        self.changes: dict[str, tuple[str, str]] = {}  # path -> (old, new)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def propose(self, path: Path, new: str) -> None:
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if old != new:
            self.changes[str(path.relative_to(ROOT))] = (old, new)


# --- data loading -----------------------------------------------------------

def load_tickers(rep: Reporter) -> dict[str, dict]:
    data: dict[str, dict] = {}
    for f in sorted(API_DIR.glob("*.json")):
        if f.name in ("tickers.json", "schema.json"):
            continue
        try:
            data[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:  # hard error: source of truth broken
            sys.exit(f"error: {f} is not valid JSON: {exc}")
    return data


def theme_pages() -> list[Path]:
    return [DD_DIR / f"{stem}.md" for stem, _, _ in THEME_PAGES if (DD_DIR / f"{stem}.md").exists()]


def gist_membership(rep: Reporter) -> dict[str, str]:
    """ticker -> theme page stem, inferred from gist headers."""
    member: dict[str, str] = {}
    for page in theme_pages():
        for t in GIST_HEADER_RE.findall(page.read_text(encoding="utf-8")):
            if t in member and member[t] != page.stem:
                rep.warn(f"{t}: gist on both {member[t]}.md and {page.stem}.md")
            elif t in member:
                rep.warn(f"{page.stem}.md: duplicate gist for {t}")
            member.setdefault(t, page.stem)
    return member


# --- rendering helpers ------------------------------------------------------

def rating_span(rating: str, rep: Reporter, ctx: str) -> str:
    cls = RATING_CLASS.get(rating)
    if cls is None:
        rep.warn(f"{ctx}: rating {rating!r} not in canonical set, using generic style")
        cls = "rating-spec"
    return f'<span class="{cls}">{rating}</span>'


def tv_symbol(d: dict, rep: Reporter) -> str:
    exch = d.get("exchange", "")
    prefix = EXCHANGE_TV.get(exch)
    if prefix is None:
        prefix = exch.split(" / ")[0].split()[0].upper() if exch else "NYSE"
        rep.warn(f"{d['ticker']}: unknown exchange {exch!r}, guessing TV prefix {prefix!r}")
    return f"{prefix}:{d['ticker']}"


def badge(d: dict, member: dict[str, str], rep: Reporter) -> tuple[str, str]:
    sub = d.get("sub_theme")
    if sub in SUBTHEME_BADGE:
        return SUBTHEME_BADGE[sub]
    page = member.get(d["ticker"])
    for stem, label, cls in THEME_PAGES:
        if stem == page:
            if sub:
                rep.warn(f"{d['ticker']}: sub_theme {sub!r} has no badge mapping, "
                         f"using {label!r} (add it to SUBTHEME_BADGE)")
            return label, cls
    rep.warn(f"{d['ticker']}: no badge mapping and no gist on any theme page")
    return d.get("theme") or d.get("sector") or "—", "badge-tech"


def esc_money(s: str) -> str:
    """Escape $ for markdown the way the existing pages do."""
    return re.sub(r"(?<!\\)\$", r"\\$", s)


def target_of(d: dict, case: str) -> str | None:
    v = d.get(case)
    if isinstance(v, dict):
        t = v.get("target")
        return str(t) if t is not None else None
    return None


# --- generators -------------------------------------------------------------

def gen_tickers_json(data: dict[str, dict], member: dict[str, str], rep: Reporter) -> str:
    entries = []
    for t in sorted(data):
        d = data[t]
        page_label = next((label for stem, label, _ in THEME_PAGES if stem == member.get(t)), None)
        entry = {
            "ticker": t,
            "company": d.get("company", ""),
            "sector": d.get("sector", ""),
            "industry": d.get("industry", ""),
            "rating": d.get("rating", ""),
            "price": d.get("price"),
            "market_cap": d.get("market_cap", ""),
            "last_updated": d.get("last_updated", ""),
            "deep_dive_url": f"/deep-dives/{t}/",
            "api_url": f"/api/{t}.json",
            "theme": d.get("theme") or page_label or d.get("sector", ""),
            "sub_theme": d.get("sub_theme") or d.get("industry") or d.get("sector", ""),
            "price_date": d.get("price_date", ""),
        }
        entries.append({k: entry[k] for k in TICKER_ENTRY_FIELDS})
        if not d.get("theme"):
            rep.warn(f"{t}: missing 'theme' in JSON, tickers.json falls back to {entry['theme']!r}")
        if not d.get("sub_theme"):
            rep.warn(f"{t}: missing 'sub_theme' in JSON, tickers.json falls back to {entry['sub_theme']!r}")
    doc = {
        "$schema": "/api/schema.json",
        "api_version": "1",
        "last_updated": max((e["last_updated"] for e in entries), default=""),
        "count": len(entries),
        "tickers": entries,
    }
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def table_row(d: dict, member: dict[str, str], rep: Reporter, with_theme: bool) -> str:
    t = d["ticker"]
    cells = [f'<tv-ticker-tag symbol="{tv_symbol(d, rep)}" hide-background></tv-ticker-tag>',
             d.get("company", "")]
    if with_theme:
        label, cls = badge(d, member, rep)
        cells.append(f'<span class="badge {cls}">{label}</span>')
    cells += [rating_span(d.get("rating", ""), rep, t),
              d.get("last_updated", ""),
              f"[:material-file-document: Read]({'deep-dives/' if with_theme else ''}{t}.md)"]
    return "| " + " | ".join(cells) + " |"


def gen_master_table(data: dict[str, dict], member: dict[str, str], rep: Reporter) -> str:
    page_order = {stem: i for i, (stem, _, _) in enumerate(THEME_PAGES)}

    def key(t: str) -> tuple:
        d = data[t]
        return (page_order.get(member.get(t), len(page_order)),
                d.get("sub_theme") or "", t)

    lines = ["| Ticker | Company | Theme | Rating | Last Updated | Full DD |",
             "|--------|---------|-------|--------|--------------|---------|"]
    lines += [table_row(data[t], member, rep, with_theme=True) for t in sorted(data, key=key)]
    return "\n".join(lines)


def splice_generated(text: str, name: str, body: str, locate: re.Pattern, path: Path) -> str:
    begin, end = BEGIN.format(name=name), END.format(name=name)
    block = f"{begin}\n{body}\n{end}"
    marked = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if marked.search(text):
        return marked.sub(lambda _: block, text)
    m = locate.search(text)
    if not m:
        sys.exit(f"error: cannot find where to place generated block {name!r} in {path}")
    # adopt: replace the existing contiguous table starting at the located header
    start = m.start()
    tail = text[start:]
    stop = re.search(r"\n(?!\|)", tail)
    end_idx = start + (stop.start() if stop else len(tail))
    return text[:start] + block + text[end_idx:]


def gen_table_md(data: dict, member: dict, rep: Reporter) -> str:
    text = TABLE_MD.read_text(encoding="utf-8")
    return splice_generated(text, "all-stocks-table", gen_master_table(data, member, rep),
                            SUMMARY_HEADER_RE, TABLE_MD)


def regen_theme_page(page: Path, data: dict, member: dict, rep: Reporter) -> str:
    """Rewrite mechanical parts of a thematic page, preserving prose/membership."""
    lines = page.read_text(encoding="utf-8").split("\n")
    current_gist: str | None = None
    out: list[str] = []
    for line in lines:
        row = ROW_TICKER_RE.search(line)
        if line.startswith("|") and row:
            t = row.group(1)
            if t in data:
                line = table_row(data[t], member, rep, with_theme=False)
            else:
                rep.warn(f"{page.name}: table row for {t} kept as-is (no docs/api/{t}.json)")
        elif (m := GIST_HEADER_RE.match(line)):
            t = m.group(1)
            current_gist = t if t in data else None
            if current_gist:
                d = data[t]
                line = f"**{t} — {d.get('company', '')} · {rating_span(d.get('rating', ''), rep, f'{page.name}:{t}')}**"
            else:
                rep.warn(f"{page.name}: gist for {t} kept as-is (no docs/api/{t}.json)")
        elif TARGETS_LINE_RE.match(line) and current_gist:
            d = data[current_gist]
            bull, base, bear = (target_of(d, c) for c in ("bull_case", "base_case", "bear_case"))
            if None in (bull, base, bear):
                rep.warn(f"{page.name}:{current_gist}: missing scenario target in JSON, targets line kept as-is")
            else:
                line = f"**Bull:** {esc_money(bull)} · **Base:** {esc_money(base)} · **Bear:** {esc_money(bear)}"
            current_gist = None
        out.append(line)
    return "\n".join(out)


def update_counters(text: str, n_tickers: int, n_themes: int) -> str:
    text = re.sub(r"\b\d+ tickers across \d+ investment themes\b",
                  f"{n_tickers} tickers across {n_themes} investment themes", text)
    text = re.sub(r"\b\d+ structured (stock )?deep dives across \d+ investment themes\b",
                  lambda m: f"{n_tickers} structured {m.group(1) or ''}deep dives "
                            f"across {n_themes} investment themes", text)
    text = re.sub(r"\b\d+ structured (stock )?deep dives\b",
                  lambda m: f"{n_tickers} structured {m.group(1) or ''}deep dives", text)
    text = re.sub(r"\ball \d+ (tickers|deep dives|tracked tickers)\b",
                  lambda m: f"all {n_tickers} {m.group(1)}", text)
    return text


# --- entry point ------------------------------------------------------------

def build(rep: Reporter) -> None:
    data = load_tickers(rep)
    member = gist_membership(rep)

    for t in sorted(set(data) - set(member)):
        rep.warn(f"{t}: docs/api/{t}.json exists but no gist on any theme page — "
                 f"listed in tickers.json/table.md without a theme home")
    for t in sorted(set(member) - set(data)):
        rep.warn(f"{t}: gist on {member[t]}.md but no docs/api/{t}.json — "
                 f"excluded from tickers.json until the JSON exists")

    rep.propose(API_DIR / "tickers.json", gen_tickers_json(data, member, rep))
    rep.propose(TABLE_MD, gen_table_md(data, member, rep))
    for page in theme_pages():
        rep.propose(page, regen_theme_page(page, data, member, rep))

    n_themes = sum(1 for stem, _, _ in THEME_PAGES
                   if any(member.get(t) == stem for t in member))
    for f in COUNTER_FILES:
        rep.propose(f, update_counters(f.read_text(encoding="utf-8"), len(data), n_themes))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="don't write; exit 1 if any derived file is stale")
    ap.add_argument("--diff", action="store_true", help="print full diffs")
    args = ap.parse_args()

    rep = Reporter()
    build(rep)

    for w in rep.warnings:
        print(f"warning: {w}", file=sys.stderr)

    if not rep.changes:
        suffix = f" ({len(rep.warnings)} warning(s))" if rep.warnings else ""
        print(f"derived files up to date{suffix}")
        return 0

    for path, (old, new) in rep.changes.items():
        if args.check or args.diff:
            diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(),
                                             fromfile=f"a/{path}", tofile=f"b/{path}", lineterm=""))
            shown = diff if args.diff else diff[:30]
            print("\n".join(shown))
            if len(diff) > len(shown):
                print(f"... ({len(diff) - len(shown)} more diff lines, use --diff)")
        if not args.check:
            (ROOT / path).write_text(new, encoding="utf-8")
            print(f"wrote {path}")

    if args.check:
        print(f"\nSTALE: {len(rep.changes)} derived file(s) out of date: "
              + ", ".join(rep.changes))
        print("run: python3 helpers/build_derived.py")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # e.g. piped to head
        sys.exit(0)
