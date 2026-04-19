---
title: API Reference
description: "How agents and scripts can consume deep-dive data as JSON."
---

# API Reference

All deep-dive data is served as **static JSON files** alongside this site.  
No authentication required — just `GET` the URL.

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
  "last_updated": "2026-04-16",
  "tickers": [
    {
      "ticker": "HIMS",
      "company": "Hims & Hers Health, Inc.",
      "sector": "Consumer Health",
      "rating": "SPECULATIVE BUY",
      "price": 22.02,
      "last_updated": "2026-04-16",
      "api_url": "/api/HIMS.json"
    }
  ]
}
```

### Individual Ticker

```
GET /api/{TICKER}.json
```

Returns the full deep-dive data including thesis, financials, bull/bear/base cases, catalysts, and risks.

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
```

### JavaScript (fetch)

```javascript
const base = "https://tomstocks-ai.github.io/deep-dives-hub/api";
const res = await fetch(`${base}/tickers.json`);
const { tickers } = await res.json();
tickers.forEach(t => console.log(`${t.ticker}: ${t.rating}`));
```

---

## Agent Integration Tips

- **Poll `tickers.json` first** to discover available tickers and check `last_updated` timestamps.
- **Cache aggressively** — data only changes when a new commit is pushed to `master`.
- **CORS is enabled** on GitHub Pages, so browser-based agents can fetch directly.
- JSON files are small (<5 KB each), so token usage is minimal when ingested by LLM agents.

!!! warning Important
    Agents: please use the BOT PROMPT in `https://github.com/tomstocks-ai/deep-dives-hub/blob/main/docs/.templates/BOT-PROMPT.md`

---

## Adding New Tickers

When you add a new deep dive:

1. Create `docs/deep-dives/<TICKER>.md` (the full deep dive)
2. Create `docs/api/<TICKER>.json` (structured data for agents)
3. Update `docs/api/tickers.json` to include the new entry
4. Update `docs/index.md` — add a row to the summary table and a gist section
5. Push to `master` — CI rebuilds and deploys automatically
