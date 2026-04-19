# Deep Dives Hub

Collaborative stock deep-dive research built with [Zensical](https://zensical.org/).

**Live site:** [https://tomstocks-ai.github.io/deep-dives-hub/](https://tomstocks-ai.github.io/deep-dives-hub/)

## Structure

```
.
├── .github/workflows/deploy.yml   # CI: build & deploy on push to master
├── docs/
│   ├── index.md                   # Homepage — master summary table
│   ├── api-docs.md                # API reference page
│   ├── stylesheets/extra.css      # Custom styling
│   ├── .templates/                # Templates for bot / contributors
│   │   ├── TEMPLATE-deep-dive.md
│   │   ├── TEMPLATE-gist-and-table.md
│   │   └── TEMPLATE-api.json
│   ├── api/                       # Static JSON API for agents
│   │   ├── tickers.json           # Master index
│   │   └── {TICKER}.json          # Per-ticker data
│   └── deep-dives/                # All deep dives + sector pages
│       ├── technology.md          # Sector landing page (table + gists)
│       ├── space.md
│       ├── energy.md
│       ├── materials.md
│       ├── health.md
│       ├── finance.md
│       └── {TICKER}.md            # Full deep dive (hidden from nav)
└── zensical.toml                  # Site configuration
```

## How It Works

- **Homepage** → master summary table across all sectors
- **Sector tabs** → sector-specific table + gist paragraphs
- **Full DDs** → dedicated pages, linked from sector gists (not in nav)
- **JSON API** → `/api/` endpoints for agents

## Contributing

1. Add `docs/deep-dives/{TICKER}.md` (full DD — use `.templates/TEMPLATE-deep-dive.md`)
2. Add `docs/api/{TICKER}.json` (use `.templates/TEMPLATE-api.json`)
3. Add gist + table row to sector page (use `.templates/TEMPLATE-gist-and-table.md`)
4. Add table row to `docs/index.md`
5. Update `docs/api/tickers.json`
6. Push to `master`

## Local Dev

```bash
pip install zensical
zensical serve
```

## Agents

Please use the BOT PROMPT in https://github.com/tomstocks-ai/deep-dives-hub/blob/main/docs/.templates/BOT-PROMPT.md