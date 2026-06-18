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
│       ├── semiconductors.md              # Semiconductors
│       ├── memory-storage.md              # Memory & Storage
│       ├── networking-connectivity.md     # Networking & Connectivity
│       ├── photonics.md                   # Photonics & Optical Interconnects
│       ├── semiconductor-equipment.md     # Semiconductor Equipment
│       ├── data-center-infrastructure.md  # Data Center Infrastructure
│       ├── data-centers-hpc.md            # Data Centers & HPC
│       ├── cloud-enterprise-software.md   # Cloud & Enterprise Software
│       ├── cybersecurity.md               # Cybersecurity
│       ├── defense.md                     # Defense
│       ├── robotics-automation.md         # Robotics & Automation
│       ├── space-economy.md               # Space Economy
│       ├── quantum-computing.md           # Quantum Computing
│       ├── nuclear-energy.md              # Nuclear Energy
│       ├── grid-power.md                  # Grid & Power
│       ├── critical-minerals.md           # Critical Minerals & Strategic Materials
│       ├── biotech-health.md              # Biotechnology & Health Technology
│       ├── fintech.md                     # Fintech & Digital Payments
│       ├── evtol.md                       # eVTOL & Advanced Air Mobility
│       ├── natural-gas.md                 # Natural Gas & AI Power Demand
│       └── {TICKER}.md                    # Full deep dive (hidden from nav)
└── zensical.toml                  # Site configuration
```

## How It Works

- **Homepage** → overview and links
- **All tab** → master summary table across all themes
- **Theme tabs** → theme-specific table + gist paragraphs (with sub-theme sections)
- **Full DDs** → dedicated pages, linked from theme gists (not in nav)
- **JSON API** → `/api/` endpoints for agents

## Contributing

1. Add `docs/deep-dives/{TICKER}.md` (full DD — use `.templates/TEMPLATE-deep-dive.md`)
2. Add `docs/api/{TICKER}.json` (use `.templates/TEMPLATE-api.json`)
3. Add gist + table row to thematic page (use `.templates/TEMPLATE-gist-and-table.md`)
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
