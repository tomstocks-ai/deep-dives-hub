---
title: Deep Dives Hub
---

# Deep Dives Hub

Welcome to the **Deep Dives Hub** - a collaborative, open-source repository of stock deep-dive research.

Each ticker gets a concise summary on its sector page and a full deep-dive page. 

All data is also available as JSON for AI agents.

--- 

!!! warning "Disclaimer"
    The information on this page is not financial advice, and you should not consider it to be financial advice

---


## For Agents

All deep-dive data is available as static JSON:

```
GET /api/tickers.json          → master index of all tickers
GET /api/{TICKER}.json         → full deep-dive data for a specific stock
```

Base URL: `https://tomstocks-ai.github.io/deep-dives-hub/api/`

See the [API Reference](api-docs.md) for details.

---

## Contributing

1. Fork the repo
2. Add a Markdown deep dive at `docs/deep-dives/<TICKER>.md`
3. Add the corresponding JSON at `docs/api/<TICKER>.json`
4. Add the gist & table row to the sector page (`docs/deep-dives/<sector>.md`)
5. Add the table row to `docs/index.md`
6. Update `docs/api/tickers.json`
7. Open a PR — the site redeploys automatically on merge to `master`
