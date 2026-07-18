---
title: API Reference
description: "How agents and scripts can consume deep-dive data as JSON."
---

# API Reference

All deep-dive data is served as **static JSON files** alongside this site.  
No authentication required — just `GET` the URL. CORS is enabled on GitHub Pages.

---

## Base URL

```
https://tomstocks-ai.github.io/deep-dives-hub/api/
```

---

## Endpoints

### Master Index

```
GET /api/tickers.json
```

Returns a list of all tracked tickers with metadata and links to individual deep dives.

**Response shape:**

```json
{
  "api_version": "1",
  "last_updated": "2026-06-26",
  "tickers": [
    {
      "ticker": "HIMS",
      "company": "Hims & Hers Health, Inc.",
      "sector": "Consumer Health",
      "theme": "Biotechnology & Health Technology",
      "sub_theme": "Telehealth & Consumer Health",
      "industry": "Telehealth",
      "rating": "SPEC. BUY",
      "price": 22.02,
      "price_date": "2026-06-26",
      "market_cap": "~$4.5B",
      "last_updated": "2026-06-26",
      "deep_dive_url": "/deep-dives/HIMS/",
      "api_url": "/api/HIMS.json"
    }
  ]
}
```

### Individual Ticker

```
GET /api/{TICKER}.json
```

Returns the full deep-dive data including thesis, financials, bull/bear/base cases, catalysts with ISO dates, and key risks.

### JSON Schema

```
GET /api/schema.json
```

[JSON Schema (draft 2020-12)](https://json-schema.org/draft/2020-12) for all API files.
Validate `tickers.json` against the `tickers.json index` definition and individual `{TICKER}.json` files against the `deep_dive` definition.

---

## Canonical Rating Values

| Rating | When to use |
|--------|-------------|
| `BUY` | Clear positive risk/reward, strong fundamentals |
| `SPEC. BUY` | Positive thesis but high uncertainty / binary risks |
| `HOLD` | Fair value — wait for better entry or catalyst |
| `HOLD / SPEC.` | Pre-revenue or high-risk hold |
| `SELL` | Negative risk/reward |
| `SPECULATIVE` | Pure speculative / lottery ticket |

---

## Usage Examples

### Python

```python
import requests

base = "https://tomstocks-ai.github.io/deep-dives-hub/api"

# Get all tickers
index = requests.get(f"{base}/tickers.json").json()
for t in index["tickers"]:
    print(f"{t['ticker']} — {t['rating']} — ${t['price']}")

# Get a specific deep dive
hims = requests.get(f"{base}/HIMS.json").json()
print(hims["thesis"])
print(hims["bull_case"])
```

### curl

```bash
# List all tickers
curl -s https://tomstocks-ai.github.io/deep-dives-hub/api/tickers.json | jq '.tickers[] | {ticker, rating, price}'

# Get a specific deep dive
curl -s https://tomstocks-ai.github.io/deep-dives-hub/api/HIMS.json | jq '{thesis, bull: .bull_case.target, bear: .bear_case.target}'

# Find all upcoming catalysts across all tickers (requires jq 1.6+)
curl -s https://tomstocks-ai.github.io/deep-dives-hub/api/tickers.json \
  | jq -r '.tickers[].ticker' \
  | xargs -I{} curl -s "https://tomstocks-ai.github.io/deep-dives-hub/api/{}.json" \
  | jq -r 'select(.catalysts) | .ticker + ": " + (.catalysts[].event)'
```

### JavaScript (fetch)

```javascript
const base = "https://tomstocks-ai.github.io/deep-dives-hub/api";
const res = await fetch(`${base}/tickers.json`);
const { tickers } = await res.json();
tickers.forEach(t => console.log(`${t.ticker}: ${t.rating}`));
```

---

## MCP Server

An [MCP](https://modelcontextprotocol.io/) server is included, letting Claude Desktop and the `claude` CLI use all 100 deep dives as tools and resources.

```bash
# Install with MCP support
pip install -e ".[mcp]"
# or: poetry install --extras mcp

# Run (stdio mode — for Claude Desktop / claude CLI)
deep-dives-mcp

# Remote mode — reads live GitHub Pages API, no repo clone needed
DEEP_DIVES_REMOTE=1 deep-dives-mcp
```

**Claude Desktop config** (`~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "deep-dives-hub": {
      "command": "deep-dives-mcp",
      "cwd": "/path/to/deep-dives-hub"
    }
  }
}
```

**Available MCP tools:**

| Tool | Description |
|------|-------------|
| `list_tickers` | Filter all 100 tickers by theme, sector, and/or rating |
| `get_deep_dive` | Full structured deep dive for one ticker |
| `get_thesis` | Investment thesis only — token-efficient shortcut |
| `compare_tickers` | Side-by-side targets + thesis snippets for a list |
| `find_catalysts` | Upcoming events across all tickers in a date range |
| `get_schema` | JSON Schema describing the API data format |

See the [MCP README](https://github.com/tomstocks-ai/deep-dives-hub/blob/main/deep_dives_mcp/README.md) for full details.

---

## Agent Integration Tips

- **Poll `tickers.json` first** to discover available tickers and check `last_updated` / `price_date` timestamps.
- **Catalyst `iso_date`** is an ISO 8601 string (`YYYY-MM-DD`, `YYYY-MM`, or `YYYY`) or `null` for open-ended events — machine-parseable alongside the human-readable `date` field.
- **Cache aggressively** — data only changes when a new commit is pushed to `master`.
- JSON files are small (<5 KB each), so token usage is minimal when ingested by LLM agents.

!!! warning Important
    Agents: please use the BOT PROMPT at https://github.com/tomstocks-ai/deep-dives-hub/blob/main/docs/.templates/BOT-PROMPT.md

---

## Adding New Tickers

When you add a new deep dive:

1. Create `docs/deep-dives/<TICKER>.md` (full deep dive — use `.templates/TEMPLATE-deep-dive.md`)
2. Create `docs/api/<TICKER>.json` (structured data — use `.templates/TEMPLATE-api.json`)
3. Add a gist + table row to the correct thematic page (`docs/deep-dives/<theme>.md`)
4. Add a table row to `docs/table.md`
5. Update `docs/api/tickers.json` to include the new entry
6. Run `python3 helpers/validate_deep_dive.py docs/deep-dives/<TICKER>.md`
7. Push to `master` — CI rebuilds and deploys automatically
