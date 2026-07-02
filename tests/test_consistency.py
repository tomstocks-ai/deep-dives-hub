"""Cross-artifact consistency checks.

Guards the single-source-of-truth contract: docs/api/{TICKER}.json is
canonical, everything mechanical is generated from it by
helpers/build_derived.py, and the editorial artifacts (deep-dive pages,
thematic gists) must stay cross-referenced with it.

Known pre-existing issues are tracked in the allowlists below, following the
NEEDS_REGEN pattern from test_deep_dives.py: they xfail so CI stays green
while remaining visible. Burn them down; don't add to them.
"""

import json
import re
from pathlib import Path

import jsonschema
import pytest

import build_derived
from build_derived import GIST_HEADER_RE, ROOT

API_DIR = ROOT / "docs" / "api"
DD_DIR = ROOT / "docs" / "deep-dives"

# --- known pre-existing issues (burn-down lists) ---------------------------

# Gist and/or table rows exist on the site, but the API JSON was never
# created — the ticker 404s for agents. Fix: create docs/api/{T}.json.
MISSING_JSON = {"U", "UUUU", "VELO"}

# JSON exists but the ticker has no gist on any thematic page, so it is
# unreachable from the human-facing theme navigation. Fix: add a gist.
NO_THEME_HOME = {"MRVL"}

# (page, ticker) pairs with more than one gist on the same page. The second
# P gist on AI_buildout.md carries SK hynix's KRW price targets — delete it.
DUPLICATE_GISTS = {("AI_buildout.md", "P")}

# JSONs that fail schema validation (missing theme/sub_theme). Fix: add the
# two fields, then remove from this set.
SCHEMA_ISSUES = {"CBRS", "MRVL", "NOK"}


# --- fixtures ---------------------------------------------------------------

def json_files() -> list[Path]:
    return sorted(f for f in API_DIR.glob("*.json")
                  if f.name not in ("tickers.json", "schema.json"))


def ticker_md_files() -> list[Path]:
    return sorted(f for f in DD_DIR.glob("*.md") if re.fullmatch(r"[A-Z0-9]+", f.stem))


def gists_by_page() -> dict[str, list[str]]:
    pages = {}
    for page in build_derived.theme_pages():
        pages[page.name] = GIST_HEADER_RE.findall(page.read_text(encoding="utf-8"))
    return pages


SCHEMA = json.loads((API_DIR / "schema.json").read_text(encoding="utf-8"))
DEEP_DIVE_SCHEMA = {"$defs": SCHEMA["$defs"], **SCHEMA["$defs"]["deep_dive"]}


# --- tests ------------------------------------------------------------------

@pytest.mark.parametrize("f", json_files(), ids=lambda f: f.stem)
def test_json_matches_schema(f: Path) -> None:
    if f.stem in SCHEMA_ISSUES:
        pytest.xfail(f"{f.name} known schema violation — add missing fields")
    errors = sorted(
        jsonschema.Draft202012Validator(DEEP_DIVE_SCHEMA).iter_errors(json.loads(f.read_text())),
        key=lambda e: str(e.path),
    )
    assert not errors, "\n".join(
        f"  • {'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors
    )


@pytest.mark.parametrize("md", ticker_md_files(), ids=lambda f: f.stem)
def test_deep_dive_has_json(md: Path) -> None:
    if md.stem in MISSING_JSON:
        pytest.xfail(f"create docs/api/{md.stem}.json — ticker is invisible to the API")
    assert (API_DIR / f"{md.stem}.json").exists(), (
        f"docs/deep-dives/{md.name} has no docs/api/{md.stem}.json — "
        f"the ticker will 404 for agents and be dropped from tickers.json/table.md"
    )


@pytest.mark.parametrize("f", json_files(), ids=lambda f: f.stem)
def test_json_has_deep_dive(f: Path) -> None:
    assert (DD_DIR / f"{f.stem}.md").exists(), (
        f"docs/api/{f.name} has no docs/deep-dives/{f.stem}.md — "
        f"deep_dive_url in the API points at a 404"
    )


@pytest.mark.parametrize("f", json_files(), ids=lambda f: f.stem)
def test_json_has_theme_gist(f: Path) -> None:
    if f.stem in NO_THEME_HOME:
        pytest.xfail(f"{f.stem} has no gist on any thematic page — add one")
    pages = [p for p, tickers in gists_by_page().items() if f.stem in tickers]
    assert pages, f"{f.stem} has no gist on any thematic page"
    assert len(pages) == 1, f"{f.stem} has gists on multiple pages: {pages}"


def test_no_duplicate_gists() -> None:
    dups = {
        (page, t)
        for page, tickers in gists_by_page().items()
        for t in set(tickers)
        if tickers.count(t) > 1
    }
    new = dups - DUPLICATE_GISTS
    fixed = DUPLICATE_GISTS - dups
    assert not new, f"duplicate gists introduced: {sorted(new)}"
    assert not fixed, (
        f"duplicate gists fixed: {sorted(fixed)} — remove them from "
        f"DUPLICATE_GISTS in {__file__}"
    )


@pytest.mark.parametrize("f", json_files(), ids=lambda f: f.stem)
def test_exchange_mappable(f: Path) -> None:
    exch = json.loads(f.read_text()).get("exchange")
    assert exch in build_derived.EXCHANGE_TV, (
        f"exchange {exch!r} has no TradingView prefix mapping — "
        f"add it to EXCHANGE_TV in helpers/build_derived.py"
    )


def test_derived_files_fresh() -> None:
    """tickers.json, table.md, theme-page rows/gist trailers, and counters
    must match what build_derived.py generates from the ticker JSONs."""
    rep = build_derived.Reporter()
    build_derived.build(rep)
    assert not rep.changes, (
        "derived files are stale: "
        + ", ".join(rep.changes)
        + "\n  → run: python3 helpers/build_derived.py"
    )
