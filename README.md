# Deep Dives Hub

Collaborative stock deep-dive research built with [Zensical](https://zensical.org/).  
97 structured deep dives across 9 investment themes, served as a static JSON API and an MCP server.

**Live site:** [https://tomstocks-ai.github.io/deep-dives-hub/](https://tomstocks-ai.github.io/deep-dives-hub/)

## Structure

```
.
├── .github/workflows/deploy.yml   # CI: build & deploy on push to master
├── deep_dives_mcp/                # MCP server (Claude Desktop / claude CLI)
│   ├── server.py                  # FastMCP server — tools + resources
│   └── README.md                  # MCP install & usage guide
├── docs/
│   ├── index.md                   # Homepage
│   ├── table.md                   # Master summary table (ALL tickers)
│   ├── api-docs.md                # API reference page
│   ├── llms.txt                   # LLM-readable site summary
│   ├── stylesheets/extra.css      # Custom styling
│   ├── .templates/                # Templates for bot / contributors
│   │   ├── TEMPLATE-deep-dive.md
│   │   ├── TEMPLATE-gist-and-table.md
│   │   ├── TEMPLATE-api.json
│   │   └── BOT-PROMPT.md
│   ├── api/                       # Static JSON API for agents
│   │   ├── tickers.json           # Master index (api_version: "1")
│   │   ├── schema.json            # JSON Schema for all API files
│   │   └── {TICKER}.json          # Per-ticker data
│   └── deep-dives/                # All deep dives + thematic pages
│       ├── AI_buildout.md         # Semiconductors, Semi Equipment,
│       │                          #   Photonics, Networking, Memory & Storage,
│       │                          #   Grid & Power, Data Center Infrastructure
│       ├── energy.md              # Nuclear, Solar, Natural Gas & AI Power Demand
│       ├── software.md            # Cloud & Enterprise Software, Cybersecurity
│       ├── space.md               # Space Economy
│       ├── defense.md             # Defense
│       ├── critical-minerals.md   # Critical Minerals & Strategic Materials
│       ├── biotech-health.md      # Biotechnology & Health Technology
│       ├── fintech.md             # Fintech & Digital Payments
│       ├── quantum-computing.md   # Quantum Computing
│       ├── evtol.md               # eVTOL & Advanced Air Mobility
│       └── {TICKER}.md            # Full deep dive (hidden from nav)
├── helpers/
│   └── validate_deep_dive.py      # Validation script (run before committing)
├── tests/
│   ├── test_deep_dives.py         # Validates all markdown + JSON files
│   └── test_mcp_server.py         # MCP server tool integration tests
├── pyproject.toml                 # Project deps; `mcp` extra for MCP server
└── zensical.toml                  # Site configuration
```

## How It Works

- **Homepage** → overview and links
- **All tab** → master summary table across all themes (`docs/table.md`)
- **Theme tabs** → theme-specific table + gist paragraphs (with sub-theme sections)
- **Full DDs** → dedicated pages, linked from theme gists (not in nav)
- **JSON API** → `/api/` endpoints for agents (schema at `/api/schema.json`)
- **MCP server** → exposes all tickers as tools/resources for Claude Desktop and the `claude` CLI

## Contributing

1. Add `docs/deep-dives/{TICKER}.md` (full DD — use `.templates/TEMPLATE-deep-dive.md`)
2. Add `docs/api/{TICKER}.json` (use `.templates/TEMPLATE-api.json`)
3. Add gist + table row to the correct **consolidated** thematic page (see `.templates/BOT-PROMPT.md` for sector mapping)
4. Add table row to `docs/table.md`
5. Update `docs/api/tickers.json`
6. Run validation: `python3 helpers/validate_deep_dive.py docs/deep-dives/{TICKER}.md`
7. Push to `master`

## Local Dev

```bash
pip install zensical
zensical serve
```

## MCP Server

Exposes all 97 deep dives as MCP tools and resources for Claude Desktop / the `claude` CLI.

```bash
# Install with MCP support
pip install -e ".[mcp]"
# or: poetry install --extras mcp

# Run (stdio mode)
deep-dives-mcp

# Remote mode — reads live GitHub Pages API, no repo clone needed
DEEP_DIVES_REMOTE=1 deep-dives-mcp
```

See [deep_dives_mcp/README.md](deep_dives_mcp/README.md) for Claude Desktop config and full tool reference.

## Agents

Please use the BOT PROMPT in https://github.com/tomstocks-ai/deep-dives-hub/blob/main/docs/.templates/BOT-PROMPT.md
