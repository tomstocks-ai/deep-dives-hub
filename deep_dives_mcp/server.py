"""Deep Dives Hub MCP Server.

Exposes the Deep Dives Hub stock research API as MCP tools and resources.

Runtime modes (set via env var):
  LOCAL  (default) — reads from docs/api/*.json on disk
  REMOTE           — fetches from the live GitHub Pages API
                     (set DEEP_DIVES_REMOTE=1)
"""

from __future__ import annotations

import json
import os
import urllib.request
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REMOTE: bool = os.environ.get("DEEP_DIVES_REMOTE", "").strip() in ("1", "true", "yes")
API_BASE_URL = "https://tomstocks-ai.github.io/deep-dives-hub/api"
LOCAL_API_DIR = Path(__file__).parent.parent / "docs" / "api"

TODAY = date.today()
STALE_DAYS = 90

# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "Deep Dives Hub",
    instructions=(
        "Stock research tools for the Deep Dives Hub — structured deep dives "
        "covering AI infrastructure, energy, space, software, critical minerals, and more. "
        "Use list_tickers to discover tickers by theme/sector/rating, get_deep_dive for "
        "full analysis, get_thesis for a quick investment summary, compare_tickers for "
        "side-by-side comparison, find_catalysts for upcoming events, and get_schema to "
        "understand the data structure."
    ),
)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_tickers_cache: dict | None = None


def _fetch_json(filename: str) -> dict:
    """Load a JSON file from LOCAL disk or REMOTE HTTP."""
    if REMOTE:
        url = f"{API_BASE_URL}/{filename}"
        with urllib.request.urlopen(url) as resp:
            return json.load(resp)
    path = LOCAL_API_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(path.read_text())


def _load_tickers() -> dict:
    """Return tickers.json, using an in-memory cache (LOCAL mode only)."""
    global _tickers_cache
    if _tickers_cache is None or REMOTE:
        _tickers_cache = _fetch_json("tickers.json")
    return _tickers_cache


def _load_ticker_file(ticker: str) -> dict:
    """Load {TICKER}.json; raises ValueError with a clear message if missing."""
    upper = ticker.upper()
    try:
        return _fetch_json(f"{upper}.json")
    except (FileNotFoundError, urllib.error.HTTPError):
        raise ValueError(f"Ticker '{upper}' not found in the Deep Dives Hub.")


def _staleness_warning(data: dict) -> dict:
    """Add price_staleness_warning if price_date is more than 90 days old."""
    price_date_str = data.get("price_date")
    if not price_date_str:
        return data
    try:
        price_date = date.fromisoformat(price_date_str)
    except ValueError:
        return data
    if TODAY - price_date > timedelta(days=STALE_DAYS):
        data = dict(data)
        data["price_staleness_warning"] = (
            f"Price data is from {price_date_str} — more than {STALE_DAYS} days old. "
            "Fetch the latest price before making trading decisions."
        )
    return data


def _pad_iso_date(iso_date: str) -> str:
    """Pad a partial ISO date string to YYYY-MM-DD for comparison."""
    parts = iso_date.split("-")
    if len(parts) == 1:
        return f"{iso_date}-01-01"
    if len(parts) == 2:
        return f"{iso_date}-01"
    return iso_date


def _matches(field_value: str, filter_value: str) -> bool:
    """Case-insensitive substring match."""
    return filter_value.lower() in field_value.lower()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool
def list_tickers(
    theme: Optional[str] = None,
    sector: Optional[str] = None,
    rating: Optional[str] = None,
) -> list[dict]:
    """List tracked tickers, with optional filters for theme, sector, and rating.

    All filters are combined with AND logic; omitting a filter means "any".
    Matching is case-insensitive and substring-based, so "software" matches
    "Software" and "AI" matches "AI Buildout".

    Args:
        theme: Filter by investment theme. Partial match supported.
               Known themes: AI Buildout, Biotechnology & Health Technology,
               Critical Minerals, Defense, Energy, Fintech & Digital Payments,
               Grid & Power, Nuclear, Quantum Computing, Software, Space, Space Economy.
        sector: Filter by sector. Partial match supported.
                Known sectors: Commodities, Consumer Health, Defense, Energy,
                Fintech, Health, Health Technology, Materials, Space, Technology.
        rating: Filter by analyst rating. Partial match supported.
                Known ratings: BUY, SPEC. BUY, HOLD, HOLD / SPEC., SPECULATIVE.

    Returns:
        List of ticker entries with fields:
        ticker, company, sector, theme, sub_theme, rating, price, price_date,
        market_cap, last_updated.
    """
    index = _load_tickers()
    results = []
    for entry in index.get("tickers", []):
        if theme and not _matches(entry.get("theme", ""), theme):
            continue
        if sector and not _matches(entry.get("sector", ""), sector):
            continue
        if rating and not _matches(entry.get("rating", ""), rating):
            continue
        results.append(
            {
                "ticker": entry.get("ticker"),
                "company": entry.get("company"),
                "sector": entry.get("sector"),
                "theme": entry.get("theme"),
                "sub_theme": entry.get("sub_theme"),
                "rating": entry.get("rating"),
                "price": entry.get("price"),
                "price_date": entry.get("price_date"),
                "market_cap": entry.get("market_cap"),
                "last_updated": entry.get("last_updated"),
            }
        )
    return results


@mcp.tool
def get_deep_dive(ticker: str) -> dict:
    """Return the full structured deep dive for a single ticker.

    Includes thesis, financials, bull/base/bear case price targets, catalysts,
    and key risks. Ticker lookup is case-insensitive.

    Adds a 'price_staleness_warning' key if the stored price_date is more than
    90 days old — check it before using the price in any calculation.

    Args:
        ticker: Stock ticker symbol (e.g. "NVDA", "adbe"). Case-insensitive.

    Returns:
        Full deep dive object. Fields: ticker, company, sector, theme, sub_theme,
        industry, exchange, price, price_date, market_cap, rating, last_updated,
        thesis, financials, bull_case, base_case, bear_case, catalysts, key_risks.
        May also include 'price_staleness_warning'.
    """
    data = _load_ticker_file(ticker)
    return _staleness_warning(data)


@mcp.tool
def get_thesis(ticker: str) -> dict:
    """Return only the investment thesis for a ticker — a token-efficient shortcut.

    Skips loading financials, price targets, and catalysts. Use this when you only
    need the 2-4 sentence thesis summary, not the full deep dive.

    Adds a 'price_staleness_warning' if price_date is more than 90 days old.

    Args:
        ticker: Stock ticker symbol (e.g. "NVDA", "adbe"). Case-insensitive.

    Returns:
        Dict with 'ticker', 'company', 'rating', 'price_date', 'thesis', and
        optionally 'price_staleness_warning'.
    """
    data = _load_ticker_file(ticker)
    result = {
        "ticker": data.get("ticker"),
        "company": data.get("company"),
        "rating": data.get("rating"),
        "price_date": data.get("price_date"),
        "thesis": data.get("thesis", ""),
    }
    return _staleness_warning(result)


@mcp.tool
def compare_tickers(tickers: list[str]) -> list[dict]:
    """Compare multiple tickers side-by-side with ratings, targets, and thesis snippets.

    Useful for quickly evaluating a shortlist of stocks against each other.
    Unknown tickers are included with an 'error' key rather than raising.

    Args:
        tickers: List of ticker symbols to compare (e.g. ["NVDA", "AVGO", "MRVL"]).
                 Case-insensitive. Up to ~20 tickers is practical.

    Returns:
        List of comparison entries (one per ticker), each with:
        ticker, company, rating, price, price_date,
        bull_target, base_target, bear_target, thesis_snippet (first 120 chars + "...").
        Failed lookups include {"ticker": X, "error": "not found"}.
    """
    results = []
    for symbol in tickers:
        try:
            data = _load_ticker_file(symbol)
        except ValueError:
            results.append({"ticker": symbol.upper(), "error": "not found"})
            continue

        thesis = data.get("thesis", "")
        snippet = thesis[:120] + "..." if len(thesis) > 120 else thesis

        results.append(
            {
                "ticker": data.get("ticker"),
                "company": data.get("company"),
                "rating": data.get("rating"),
                "price": data.get("price"),
                "price_date": data.get("price_date"),
                "bull_target": data.get("bull_case", {}).get("target"),
                "base_target": data.get("base_case", {}).get("target"),
                "bear_target": data.get("bear_case", {}).get("target"),
                "thesis_snippet": snippet,
            }
        )
    return results


@mcp.tool
def find_catalysts(
    after_date: str,
    before_date: Optional[str] = None,
) -> list[dict]:
    """Find upcoming catalysts across all tracked tickers within a date range.

    Scans every ticker's catalyst list and returns events whose iso_date falls
    within the specified window. Catalysts with iso_date = null are skipped.

    Date comparison pads partial ISO strings: "2026" → 2026-01-01,
    "2026-07" → 2026-07-01, so coarse dates are treated as the start of
    their period.

    Args:
        after_date: Inclusive lower bound, ISO format: YYYY, YYYY-MM, or YYYY-MM-DD.
                    Example: "2026-07" returns catalysts in July 2026 onward.
        before_date: Optional inclusive upper bound, same format as after_date.
                     If omitted, no upper bound is applied.

    Returns:
        List of catalyst entries sorted by iso_date ascending, each with:
        ticker, company, catalyst_date (human-readable), iso_date, event.
    """
    index = _load_tickers()
    after_padded = _pad_iso_date(after_date)
    before_padded = _pad_iso_date(before_date) if before_date else None

    results = []
    for entry in index.get("tickers", []):
        symbol = entry.get("ticker", "")
        company = entry.get("company", "")
        try:
            data = _load_ticker_file(symbol)
        except ValueError:
            continue

        for catalyst in data.get("catalysts", []):
            iso = catalyst.get("iso_date")
            if iso is None:
                continue
            padded = _pad_iso_date(iso)
            if padded < after_padded:
                continue
            if before_padded and padded > before_padded:
                continue
            results.append(
                {
                    "ticker": symbol,
                    "company": company,
                    "catalyst_date": catalyst.get("date"),
                    "iso_date": iso,
                    "event": catalyst.get("event"),
                }
            )

    results.sort(key=lambda c: _pad_iso_date(c["iso_date"]))
    return results


@mcp.tool
def get_schema() -> dict:
    """Return the JSON Schema that defines the Deep Dives Hub API structure.

    Useful for agents that want to understand or validate the data format before
    calling other tools. The schema covers both tickers.json (the index) and
    individual {TICKER}.json deep dive files.

    Returns:
        The full contents of docs/api/schema.json as a dict.
    """
    return _fetch_json("schema.json")


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


@mcp.resource("deep-dives://index")
def resource_index() -> dict:
    """The full tickers.json master index — all tracked tickers with metadata."""
    return _load_tickers()


@mcp.resource("deep-dives://{ticker}")
def resource_ticker(ticker: str) -> dict:
    """Full deep dive JSON for a single ticker (e.g. deep-dives://NVDA)."""
    return _load_ticker_file(ticker)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
