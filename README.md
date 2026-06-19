# Deep Dives Hub

Collaborative stock deep-dive research built with [Zensical](https://zensical.org/).

**Live site:** [https://tomstocks-ai.github.io/deep-dives-hub/](https://tomstocks-ai.github.io/deep-dives-hub/)

## Structure

```
.
├── .github/workflows/deploy.yml   # CI: build & deploy on push to master
├── docs/
│   ├── index.md                   # Homepage
│   ├── table.md                   # Master summary table (ALL tickers)
│   ├── api-docs.md                # API reference page
│   ├── stylesheets/extra.css      # Custom styling
│   ├── .templates/                # Templates for bot / contributors
│   │   ├── TEMPLATE-deep-dive.md
│   │   ├── TEMPLATE-gist-and-table.md
│   │   ├── TEMPLATE-api.json
│   │   └── BOT-PROMPT.md
│   ├── api/                       # Static JSON API for agents
│   │   ├── tickers.json           # Master index
│   │   └── {TICKER}.json          # Per-ticker data
│   └── deep-dives/                # All deep dives + thematic pages
│       ├── AI_buildout.md                 # Consolidated: Semiconductors, Semi Equipment,
│       │                                    #   Photonics, Networking, Memory & Storage,
│       │                                    #   Grid & Power, Data Center Infrastructure
│       ├── energy.md                      # Consolidated: Nuclear, Solar, Natural Gas & AI Power Demand
│       ├── software.md                    # Consolidated: Cloud & Enterprise Software, Cybersecurity
│       ├── space.md                       # Space Economy
│       ├── defense.md                     # Defense
│       ├── critical-minerals.md             # Critical Minerals & Strategic Materials
│       ├── biotech-health.md              # Biotechnology & Health Technology
│       ├── fintech.md                     # Fintech & Digital Payments
│       ├── quantum-computing.md             # Quantum Computing
│       ├── evtol.md                       # eVTOL & Advanced Air Mobility
│       └── {TICKER}.md                    # Full deep dive (hidden from nav)
└── zensical.toml                  # Site configuration
```

## How It Works

- **Homepage** → overview and links
- **All tab** → master summary table across all themes (`docs/table.md`)
- **Theme tabs** → theme-specific table + gist paragraphs (with sub-theme sections)
- **Full DDs** → dedicated pages, linked from theme gists (not in nav)
- **JSON API** → `/api/` endpoints for agents

## Contributing

1. Add `docs/deep-dives/{TICKER}.md` (full DD — use `.templates/TEMPLATE-deep-dive.md`)
2. Add `docs/api/{TICKER}.json` (use `.templates/TEMPLATE-api.json`)
3. Add gist + table row to the correct **consolidated** thematic page (see `.templates/BOT-PROMPT.md` for sector mapping)
4. Add table row to `docs/table.md`
5. Update `docs/api/tickers.json`
6. Push to `master`

## Local Dev

```bash
pip install zensical
zensical serve
```

## Agents

Please use the BOT PROMPT in https://github.com/tomstocks-ai/deep-dives-hub/blob/main/docs/.templates/BOT-PROMPT.md
