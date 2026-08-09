#!/usr/bin/env python3
"""Refresh the ``price`` / ``price_date`` snapshot in each ticker JSON.

The per-ticker files ``docs/api/{TICKER}.json`` carry a static ``price`` and
``price_date``. Those are the designed *staleness marker* for the JSON API
(the human-facing tables render live quotes via the TradingView widgets, so
they are never stale on the site — but the API snapshot drifts over time).

This tool pulls the current regular-market price from Yahoo Finance's public
chart endpoint (no API key) and writes it back, touching only the ``price``
and ``price_date`` fields so diffs stay minimal.

Safety: prices are never fabricated. A quote is only written when
  * the HTTP fetch succeeds and returns a positive price, AND
  * the quote currency matches the exchange's expected currency, AND
  * the returned instrument name overlaps the JSON ``company`` name
    (guards single-letter tickers like P / V / U / TE from matching the
    wrong Yahoo instrument).
Anything that fails a check is skipped and reported, leaving the file
untouched.

Usage:
    python3 helpers/refresh_prices.py                # refresh all tickers
    python3 helpers/refresh_prices.py --dry-run      # report, write nothing
    python3 helpers/refresh_prices.py NVDA OKLO SMR  # refresh a subset

After a refresh, regenerate the derived files:
    python3 helpers/build_derived.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_DIR = ROOT / "docs" / "api"

# JSON "exchange" -> Yahoo Finance symbol suffix. US venues use the bare
# ticker; only foreign listings need a suffix.
EXCHANGE_YF_SUFFIX = {
    "NYSE": "",
    "NYSEAMERICAN": "",
    "AMEX": "",
    "NYSE Arca": "",
    "NASDAQ": "",
    "NasdaqCM": "",
    "NASDAQ / TSX": "",
    "OMXSTO": ".ST",   # Nasdaq Stockholm
    "KRX": ".KS",      # Korea Exchange
}

# Expected quote currency per exchange — used to reject a mismatched quote.
EXCHANGE_CCY = {
    "NYSE": "USD",
    "NYSEAMERICAN": "USD",
    "AMEX": "USD",
    "NYSE Arca": "USD",
    "NASDAQ": "USD",
    "NasdaqCM": "USD",
    "NASDAQ / TSX": "USD",
    "OMXSTO": "SEK",
    "KRX": "KRW",
}

CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
_STOPWORDS = {
    "inc", "incorporated", "corp", "corporation", "co", "company", "plc",
    "ltd", "limited", "group", "holdings", "holding", "the", "ag", "nv",
    "sa", "ab", "spa", "se", "class", "and",
}


class QuoteError(Exception):
    """Raised when a quote can't be trusted; the ticker is skipped."""


# Tickers whose JSON company name legitimately differs from Yahoo's current
# instrument name (usually a rebrand). The name-overlap guard is skipped for
# these — each entry is a verified same-company case.
NAME_MATCH_OVERRIDE = {
    "IREN",  # Iris Energy Limited rebranded to "IREN Limited"
}


def yf_symbol(ticker: str, exchange: str) -> str:
    if exchange not in EXCHANGE_YF_SUFFIX:
        raise QuoteError(f"no Yahoo mapping for exchange {exchange!r}")
    return ticker + EXCHANGE_YF_SUFFIX[exchange]


def fetch_quote(symbol: str, timeout: int = 15) -> dict:
    """Return the Yahoo chart ``meta`` block for a symbol."""
    url = CHART_URL.format(sym=urllib.parse.quote(symbol))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last_exc: Exception | None = None
    for _ in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_exc = exc
            time.sleep(1.0)
    else:
        raise QuoteError(f"fetch failed: {last_exc}")

    chart = payload.get("chart") or {}
    if chart.get("error"):
        raise QuoteError(f"API error: {chart['error']}")
    results = chart.get("result") or []
    if not results:
        raise QuoteError("empty result")
    meta = results[0].get("meta") or {}
    if "regularMarketPrice" not in meta:
        raise QuoteError("no regularMarketPrice in response")
    return meta


def _norm_tokens(name: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", (name or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}


def name_matches(json_company: str, yahoo_name: str) -> bool:
    """Lenient overlap check between the JSON company and Yahoo's name."""
    a, b = _norm_tokens(json_company), _norm_tokens(yahoo_name)
    if not a or not b:
        return True  # nothing to compare on; don't block
    return bool(a & b)


def price_date_from_meta(meta: dict) -> str:
    ts = meta.get("regularMarketTime")
    offset = meta.get("gmtoffset", 0) or 0
    if ts is None:
        return dt.datetime.now(dt.timezone.utc).date().isoformat()
    local = dt.datetime.fromtimestamp(ts + offset, tz=dt.timezone.utc)
    return local.date().isoformat()


def round_price(value: float) -> float:
    return round(value, 4) if value < 1 else round(value, 2)


def apply_update(text: str, price: float, price_date: str) -> str:
    """Rewrite only the *top-level* price / price_date fields.

    Some ticker files carry stray ``price_date`` keys nested inside
    ``catalysts`` objects, so we anchor on the indentation of the top-level
    ``price`` key (the sole ``price`` key in the document) and only touch the
    ``price_date`` at that same indentation. This keeps the edit minimal and
    never disturbs nested fields.
    """
    new_price = f"{price:g}"
    m = re.search(r'^([ \t]*)"price"\s*:\s*(-?\d+(?:\.\d+)?)', text, re.M)
    if not m:
        raise QuoteError('could not locate top-level "price" field to update')
    indent = m.group(1)
    text = text[:m.start(2)] + new_price + text[m.end(2):]

    pd_re = re.compile(r'^' + re.escape(indent) + r'"price_date"\s*:\s*"[^"]*"', re.M)
    if pd_re.search(text):
        text = pd_re.sub(f'{indent}"price_date": "{price_date}"', text, count=1)
    else:
        # No top-level price_date — insert one right after the price line.
        line_re = re.compile(
            r'^(' + re.escape(indent) + r'"price"\s*:\s*-?\d+(?:\.\d+)?),?$', re.M
        )
        text = line_re.sub(
            lambda mm: f'{mm.group(1)},\n{indent}"price_date": "{price_date}"',
            text, count=1,
        )
    return text


def ticker_files(selected: list[str]) -> list[Path]:
    files = sorted(f for f in API_DIR.glob("*.json")
                   if f.name not in ("tickers.json", "schema.json"))
    if selected:
        want = {s.upper() for s in selected}
        files = [f for f in files if f.stem.upper() in want]
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("tickers", nargs="*", help="only refresh these tickers")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--delay", type=float, default=0.4, help="seconds between requests")
    args = ap.parse_args()

    files = ticker_files(args.tickers)
    if not files:
        print("no matching ticker JSON files", file=sys.stderr)
        return 1

    updated, unchanged, skipped = [], [], []

    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        ticker, exchange = data.get("ticker", f.stem), data.get("exchange", "")
        try:
            symbol = yf_symbol(ticker, exchange)
            meta = fetch_quote(symbol)

            ccy = meta.get("currency")
            expected_ccy = EXCHANGE_CCY.get(exchange)
            if expected_ccy and ccy and ccy != expected_ccy:
                raise QuoteError(f"currency {ccy} != expected {expected_ccy}")

            yahoo_name = meta.get("longName") or meta.get("shortName") or ""
            if ticker.upper() not in NAME_MATCH_OVERRIDE and \
                    not name_matches(data.get("company", ""), yahoo_name):
                raise QuoteError(
                    f"name mismatch: JSON {data.get('company','')!r} vs Yahoo {yahoo_name!r}"
                )

            new_price = round_price(float(meta["regularMarketPrice"]))
            if new_price <= 0:
                raise QuoteError(f"non-positive price {new_price}")
            new_date = price_date_from_meta(meta)
        except QuoteError as exc:
            skipped.append((ticker, str(exc)))
            print(f"  SKIP  {ticker:8s} {exc}", file=sys.stderr)
            time.sleep(args.delay)
            continue

        old_price, old_date = data.get("price"), data.get("price_date")
        if old_price == new_price and old_date == new_date:
            unchanged.append(ticker)
        else:
            if not args.dry_run:
                f.write_text(apply_update(f.read_text(encoding="utf-8"), new_price, new_date),
                             encoding="utf-8")
            updated.append((ticker, old_price, new_price, old_date, new_date))
            tag = "DRY " if args.dry_run else "OK  "
            print(f"  {tag}  {ticker:8s} {old_price} @ {old_date}  ->  {new_price} @ {new_date}")

        time.sleep(args.delay)

    print(
        f"\nsummary: {len(updated)} updated, {len(unchanged)} unchanged, "
        f"{len(skipped)} skipped"
        + (" (dry-run — nothing written)" if args.dry_run else "")
    )
    if skipped:
        print("skipped: " + ", ".join(t for t, _ in skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
