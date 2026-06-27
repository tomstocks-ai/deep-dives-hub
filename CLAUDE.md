# Deep Dives Hub — Agent Context

This repo is a collaborative stock research site built with [Zensical](https://zensical.org/). It hosts structured deep dives and a static JSON API consumed by agents.

**Live site:** https://tomstocks-ai.github.io/deep-dives-hub/
**API base:** https://tomstocks-ai.github.io/deep-dives-hub/api/

---

## Key Files

| Path | Purpose |
|------|---------|
| `docs/api/tickers.json` | Master index of all tracked tickers |
| `docs/api/{TICKER}.json` | Per-ticker structured data (thesis, financials, bull/base/bear, catalysts) |
| `docs/api/schema.json` | JSON Schema for both `tickers.json` and individual ticker files |
| `docs/deep-dives/{TICKER}.md` | Full deep dive markdown page (hidden from nav) |
| `docs/deep-dives/{theme}.md` | Thematic index pages (AI_buildout, energy, software, etc.) |
| `docs/table.md` | Master summary table across all tickers |
| `docs/.templates/BOT-PROMPT.md` | Full instructions for generating a new deep dive |
| `helpers/validate_deep_dive.py` | Validation script for deep dive markdown + JSON |

---

## Adding a New Ticker — The 4-Artifact Workflow

Every new ticker requires **exactly 4 artifacts**. See `docs/.templates/BOT-PROMPT.md` for complete instructions and templates.

1. **`docs/deep-dives/{TICKER}.md`** — Full deep dive with TradingView widget
2. **`docs/api/{TICKER}.json`** — Structured data (see schema below)
3. **Thematic page additions** — table row + gist in `docs/deep-dives/{theme}.md`
4. **`docs/table.md` row** — one row in the master All Stocks table
5. **Update `docs/api/tickers.json`** — add entry with all required fields

After generating, run:
```bash
python3 helpers/validate_deep_dive.py docs/deep-dives/{TICKER}.md
```

---

## JSON API Schema

All ticker JSON files must have these fields (defined in `docs/api/schema.json`):

```
ticker, company, sector, theme, sub_theme, industry, exchange,
price, price_date, market_cap, rating, last_updated,
thesis, financials, bull_case, base_case, bear_case, catalysts, key_risks
```

### Canonical Rating Values

| Value | When to use |
|-------|-------------|
| `BUY` | Clear positive risk/reward, strong fundamentals |
| `SPEC. BUY` | Positive thesis but high uncertainty / binary risks |
| `HOLD` | Fair value — wait for better entry or catalyst |
| `HOLD / SPEC.` | Pre-revenue or high-risk hold |
| `SELL` | Negative risk/reward |
| `SPECULATIVE` | Pure speculative / lottery ticket |

### Catalyst Dates

Every catalyst entry must have both a human-readable `date` AND a machine-parseable `iso_date`:
```json
{ "date": "Q3 2026", "iso_date": "2026-07", "event": "..." }
```
`iso_date` should be `YYYY-MM-DD`, `YYYY-MM`, `YYYY`, or `null` for open-ended entries.

---

## Sector → Theme Mapping

Use this table to assign `theme` and `sub_theme` for a new ticker:

| If the company primarily… | Theme | Sub-theme |
|---|---|---|
| Designs/manufactures chips (GPUs, logic, SiC) | AI Buildout | AI Compute / Analog / Power |
| Makes chip testing/lithography/wafer equipment | AI Buildout | Semiconductor Equipment |
| Makes optical transceivers, photonic ICs, lasers | AI Buildout | Photonics & Optical Interconnects |
| Builds networking gear, fiber, 5G/mmWave | AI Buildout | Networking & Connectivity |
| Makes DRAM, NAND, SSDs, storage platforms | AI Buildout | Memory & Storage |
| Builds/services data centers, racks, cooling | AI Buildout | Servers & Systems |
| Operates HPC / GPU cloud / AI data centers | AI Buildout | AI / HPC Operators |
| Does electrical grid / data center contracting | AI Buildout | Electrical Contractors |
| Makes BESS / grid-scale battery storage | AI Buildout | Grid-Scale Energy Storage |
| Makes solid-state batteries | AI Buildout | Solid-State Batteries |
| Makes 3D printers / additive manufacturing | AI Buildout | Robotics & Automation |
| Sells cloud/SaaS, enterprise analytics, dev tools | Software | Enterprise Software / Data & Analytics / UX |
| Provides cybersecurity (network, endpoint, cloud) | Software | Cybersecurity |
| Builds/operates nuclear reactors | Energy | Reactor Developers |
| Enriches/mines uranium or nuclear fuel | Energy | Enrichment / Fuel Cycle |
| Manufactures solar panels, inverters | Energy | Solar |
| Produces/transports natural gas for power | Energy | Natural Gas & AI Power Demand |
| Operates satellites, provides space connectivity | Space Economy | Satellite Connectivity |
| Builds launch vehicles, lunar/deep-space systems | Space Economy | Lunar / Deep Space |
| Provides geospatial intelligence / Earth obs | Space Economy | Geospatial Intelligence |
| Makes defense systems, drones, autonomous weapons | Defense | Prime Contractors / Next-Gen Defense / Drones |
| Mines/processes copper, gold, silver, rare earths | Critical Minerals | Copper / Gold / Specialty Metals / Rare Earths |
| Mines/holds uranium | Critical Minerals | Uranium & Nuclear Fuel |
| Develops biotech, medical devices, telehealth | Biotechnology & Health Technology | varies |
| Provides fintech, payments, crypto infrastructure | Fintech & Digital Payments | varies |
| Develops quantum hardware or software | Quantum Computing | Pure Plays / Diversified Exposure |

---

## Critical Formatting Rules (Markdown files)

- **Escape all `$` signs** as `\$` in markdown (prevents LaTeX math mode). JSON files are exempt.
- **Dollar sign rule applies to:** price targets, market caps, revenue figures, table cells, gist summaries.
- **Gist entries use bold text** (`**TICKER — Company · Rating**`), NOT `###` headers.
- **Thematic page links** use relative path `{TICKER}.md` (not `deep-dives/{TICKER}.md`).

---

## Local Dev

```bash
pip install zensical
zensical serve
```

## Running Validation

```bash
python3 helpers/validate_deep_dive.py docs/deep-dives/{TICKER}.md
```

CI runs this automatically for all ticker deep dives on push to `main`/`master`.
