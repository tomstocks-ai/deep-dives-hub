---
title: Deep Dives Hub
---

# Deep Dives Hub

Welcome to the **Deep Dives Hub** — a collaborative, open-source repository of stock deep-dive research.  
Each ticker gets a concise summary on its sector page and a full deep-dive page. All data is also available as JSON for AI agents.

---

## Summary Table

| Ticker | Company | Sector | Rating | Price | Last Updated | Full DD |
|--------|---------|--------|--------|-------|--------------|---------|
| **HIMS** | Hims & Hers Health | <span class="badge badge-health">Health</span> | <span class="rating-spec-buy">SPEC. BUY</span> | $22.02 | 2026-04-16 | [:material-file-document: Read](deep-dives/HIMS.md) |
| **STAA** | STAAR Surgical | <span class="badge badge-health">Health</span> | — | — | 2026-04-09 | [:material-file-document: Read](deep-dives/STAA.md) |
| **SLDP** | Solid Power | <span class="badge badge-tech">Technology</span> | <span class="rating-spec-hold">HOLD / SPEC.</span> | $3.15 | 2026-04-14 | [:material-file-document: Read](deep-dives/SLDP.md) |
| **AEHR** | Aehr Test Systems | <span class="badge badge-tech">Technology</span> | — | — | 2026-04-06 | [:material-file-document: Read](deep-dives/AEHR.md) |
| **SNOW** | Snowflake | <span class="badge badge-tech">Technology</span> | — | — | 2026-04-10 | [:material-file-document: Read](deep-dives/SNOW.md) |
| **U** | Unity Software | <span class="badge badge-tech">Technology</span> | — | — | 2026-04-10 | [:material-file-document: Read](deep-dives/U.md) |
| **TSSI** | TSS Inc. | <span class="badge badge-tech">Technology</span> | — | — | 2026-04-03 | [:material-file-document: Read](deep-dives/TSSI.md) |
| **VELO** | VELO3D | <span class="badge badge-tech">Technology</span> | — | — | 2026-04-02 | [:material-file-document: Read](deep-dives/VELO.md) |
| **SATS** | EchoStar | <span class="badge badge-tech">Technology</span> | — | — | 2026-04-04 | [:material-file-document: Read](deep-dives/SATS.md) |
| **ASTS** | AST SpaceMobile | <span class="badge badge-space">Space</span> | — | — | 2026-04-02 | [:material-file-document: Read](deep-dives/ASTS.md) |
| **PL** | Planet Labs | <span class="badge badge-space">Space</span> | — | — | 2026-04-03 | [:material-file-document: Read](deep-dives/PL.md) |
| **SATL** | Satellogic | <span class="badge badge-space">Space</span> | — | — | 2026-04-02 | [:material-file-document: Read](deep-dives/SATL.md) |
| **NN** | NextNav | <span class="badge badge-space">Space</span> | — | — | 2026-04-17 | [:material-file-document: Read](deep-dives/NN.md) |
| **EOSE** | Eos Energy Enterprises | <span class="badge badge-energy">Energy</span> | — | — | 2026-04-05 | [:material-file-document: Read](deep-dives/EOSE.md) |
| **OKLO** | Oklo Inc. | <span class="badge badge-energy">Energy</span> | — | — | 2026-04-15 | [:material-file-document: Read](deep-dives/OKLO.md) |
| **IMSR** | Terrestrial Energy | <span class="badge badge-energy">Energy</span> | — | — | 2026-04-04 | [:material-file-document: Read](deep-dives/IMSR.md) |
| **TE** | T1 Energy | <span class="badge badge-energy">Energy</span> | — | — | 2026-03-16 | [:material-file-document: Read](deep-dives/TE.md) |
| **UUUU** | Energy Fuels | <span class="badge badge-energy">Energy</span> | — | — | 2026-04-03 | [:material-file-document: Read](deep-dives/UUUU.md) |
| **FCX** | Freeport-McMoRan | <span class="badge badge-materials">Materials</span> | — | — | 2026-04-03 | [:material-file-document: Read](deep-dives/FCX.md) |
| **TECK** | Teck Resources | <span class="badge badge-materials">Materials</span> | — | — | 2026-04-03 | [:material-file-document: Read](deep-dives/TECK.md) |
| **CRML** | Critical Metals | <span class="badge badge-materials">Materials</span> | — | — | 2026-03-24 | [:material-file-document: Read](deep-dives/CRML.md) |
| **CRCL** | Circle Internet Group | <span class="badge badge-fintech">Fintech</span> | <span class="rating-buy">BUY</span> | $94.44 | 2026-04-09 | [:material-file-document: Read](deep-dives/CRCL.md) |

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
