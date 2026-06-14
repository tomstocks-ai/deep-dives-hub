#!/usr/bin/env python3
"""
generate_widget.py

Generates TradingView Advanced Chart widget HTML for a given ticker.
Usage:
    python generate_widget.py NBIS NASDAQ
    python generate_widget.py FCX NYSE
"""

import argparse
import json
import sys
from pathlib import Path

WIDGET_TEMPLATE = """\
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/{exchange}-{ticker}/" rel="noopener nofollow" target="_blank"><span class="blue-text">{ticker} stock chart</span></a><span class="trademark"> by TradingView</span></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {{
  "allow_symbol_change": true,
  "calendar": false,
  "details": false,
  "hide_side_toolbar": true,
  "hide_top_toolbar": false,
  "hide_legend": false,
  "hide_volume": false,
  "hotlist": false,
  "interval": "D",
  "locale": "en",
  "save_image": true,
  "style": "1",
  "symbol": "{exchange}:{ticker}",
  "theme": "dark",
  "timezone": "Etc/UTC",
  "backgroundColor": "#0F0F0F",
  "gridColor": "rgba(242, 242, 242, 0.06)",
  "watchlist": [],
  "withdateranges": false,
  "compareSymbols": [],
  "studies": [
    "STD;RSI",
    "STD;EMA"
  ],
  "autosize": true,
  "height": 500
}}
  </script>
</div>"""

# Map exchange names from JSON files to TradingView format
EXCHANGE_MAP = {
    "NASDAQ": "NASDAQ",
    "NasdaqCM": "NASDAQ",
    "NYSE": "NYSE",
    "NYSE Arca": "AMEX",
    "NYSE American": "AMEX",
    "AMEX": "AMEX",
    "TSX": "TSX",
}


def get_exchange_from_json(ticker: str) -> str | None:
    """Try to read exchange from the API JSON file."""
    json_path = Path(__file__).parent.parent / "docs" / "api" / f"{ticker}.json"
    if json_path.exists():
        data = json.loads(json_path.read_text())
        return data.get("exchange")
    return None


def normalize_exchange(exchange: str) -> str:
    """Normalize exchange name to TradingView format."""
    return EXCHANGE_MAP.get(exchange, exchange)


def generate_widget(ticker: str, exchange: str) -> str:
    """Generate the TradingView widget HTML."""
    tv_exchange = normalize_exchange(exchange)
    return WIDGET_TEMPLATE.format(ticker=ticker.upper(), exchange=tv_exchange)


def main():
    parser = argparse.ArgumentParser(description="Generate TradingView widget HTML for a ticker.")
    parser.add_argument("ticker", help="Stock ticker (e.g. NBIS)")
    parser.add_argument("exchange", nargs="?", help="Exchange (e.g. NASDAQ, NYSE). Auto-detected from JSON if omitted.")
    args = parser.parse_args()

    ticker = args.ticker.upper()
    exchange = args.exchange

    if not exchange:
        exchange = get_exchange_from_json(ticker)
        if not exchange:
            print(f"Error: No exchange provided and could not find {ticker}.json", file=sys.stderr)
            sys.exit(1)

    print(generate_widget(ticker, exchange))


if __name__ == "__main__":
    main()
