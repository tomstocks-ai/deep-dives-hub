---
title: Deep Dives Hub
---

# Deep Dives Hub

Welcome to the **Deep Dives Hub** — a collaborative, open-source repository of stock deep-dive research.

91 tickers across 9 investment themes. Each ticker gets a concise summary on its thematic page and a full deep-dive page. All data is also available as structured JSON for AI agents and as an MCP server for Claude.

--- 

!!! warning "Disclaimer"
    The information on this page is not financial advice, and you should not consider it to be financial advice

---


## For Agents

All deep-dive data is available as static JSON (no auth, CORS enabled):

```
GET /api/tickers.json          → master index of all 91 tickers
GET /api/{TICKER}.json         → full deep-dive data for a specific stock
GET /api/schema.json           → JSON Schema (v1) for all API files
```

Base URL: `https://tomstocks-ai.github.io/deep-dives-hub/api/`

See the [API Reference](api-docs.md) for details, usage examples, and MCP server setup.

---

## Contributing

1. Fork the repo
2. Add a Markdown deep dive at `docs/deep-dives/<TICKER>.md`
3. Add the corresponding JSON at `docs/api/<TICKER>.json`
4. Add the gist & table row to the thematic page (`docs/deep-dives/<theme>.md`)
5. Add the table row to `docs/table.md`
6. Update `docs/api/tickers.json`
7. Run `python3 helpers/validate_deep_dive.py docs/deep-dives/<TICKER>.md`
8. Open a PR — the site redeploys automatically on merge to `master`

