---
title: "GLD — SPDR Gold Shares"
hide:
  - navigation
---

[← Back to Summary](../index.md)

<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/AMEX-GLD/" rel="noopener nofollow" target="_blank"><span class="blue-text">GLD stock chart</span></a><span class="trademark"> by TradingView</span></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {
    "allow_symbol_change": true,
    "calendar": false,
    "details": false,
    "hide_side_toolbar": true,
    "hide_top_toolbar": false,
    "hide_legend": false,
    "hide_volume": false,
    "hotlist": false,
    "interval": "D",
    "locale": "en",
    "save_image": true,
    "style": "1",
    "symbol": "AMEX:GLD",
    "theme": "dark",
    "timezone": "Etc/UTC",
    "backgroundColor": "#0F0F0F",
    "gridColor": "rgba(242, 242, 242, 0.06)",
    "watchlist": [],
    "withdateranges": false,
    "compareSymbols": [],
    "studies": [
      "STD;RSI",
      "STD;EMA"
    ],
    "autosize": true,
    "height": 500
  }
  </script>
</div>


# GLD — SPDR Gold Shares

SPDR Gold Shares is the world's largest physically backed gold ETF: \$141.0B of assets, ~34.0M ounces of bullion in London vaults, and a 0.40% expense ratio. Shares closed at \$377.91 on 2026-09-28 against a \$379.97 NAV, with spot gold (LBMA PM) at \$4,144.55/oz — roughly 26% below the record set in late January 2026. The structural bid is intact and arguably stronger than ever: central banks bought a record 289 tonnes in Q2 2026 and global gold-ETF holdings just passed 4,250 tonnes for the first time. What has changed is the macro driver. The Fed raised rates on 2026-09-16 for the first time since 2023, the 30-year Treasury yield hit its highest level since 2004, and markets now price better-than-even odds of another hike in October. That combination argues for holding the position, not adding aggressively into it.

## Company Overview

GLD is not an operating company. It is a passive grantor trust, launched 2004-11-18, whose sole purpose is for its shares to track the price of gold bullion less the trust's expenses.

**Structure and counterparties**

| Role | Entity |
|---|---|
| Sponsor | World Gold Trust Services, LLC |
| Trustee | The Bank of New York Mellon |
| Gold custodians | HSBC Bank plc and JPMorgan Chase Bank, N.A. |
| Marketing agent | State Street Global Advisors Funds Distributors, LLC |
| Listing | NYSE Arca, ticker GLD, CUSIP 78463V107 |
| Benchmark | LBMA Gold Price PM |

**Scale as of 2026-09-28**

- Assets under management: **\$141.05B**
- Shares outstanding: **371.20M**
- NAV per share: **\$379.97**; closing price **\$377.91** (premium/discount 0.04%)
- Implied gold per share: **~0.0917 oz**, or roughly **34.0M oz / ~1,059 tonnes** in trust (derived from AUM ÷ LBMA PM price — not a directly quoted figure)
- 30-day median bid/ask spread: **0.01%** — among the tightest in the entire ETF market

**Where the moat is, and where it is not.** GLD's advantage is liquidity and options depth, not cost. It is the oldest and by far the most heavily traded gold wrapper, which makes it the default vehicle for institutions, hedgers, and options strategies. Its disadvantage is the 0.40% fee, which is 4x SPDR's own GLDM (0.10%), 1.6x iShares IAU (0.25%), and 4.4x IAUM (0.09%) — all of which hold allocated physical bullion and track the same benchmark. That fee gap is now being arbitraged at scale: in the week to 2026-09-12, GLD shed \$603M while GLDM, IAU and IAUM together took in \$403M. Investors were not leaving gold; they were changing seats.

**What holders actually own.** GLD shares are a claim on a trust that holds bullion. No specific bar is allocated in a shareholder's name, and shares are not individually redeemable — only authorized participants can redeem, in Creation Unit baskets (NAV per basket was \$37,997,260.80 on 2026-09-28). The trust is not registered under the Investment Company Act of 1940 and is not regulated under the Commodity Exchange Act, so holders lack those statutory protections.

## Financial Analysis

A commodity trust has no income statement. There is no revenue, no margin, no EPS and no free cash flow. The analogous framework is AUM, the expense ratio, ounces held, flows, and tracking versus spot gold. The JSON `financials` block for this ticker carries labelled analogues rather than company metrics.

**Balance sheet — the only line that matters**

| Item | Value (2026-09-28) |
|---|---|
| Gold bullion held | ~34.0M oz / ~1,059 t (derived) |
| Cash | \$0 — the trust holds no cash buffer |
| Liabilities | Accrued sponsor fee only |
| Net assets (AUM) | \$141.05B |
| NAV / share | \$379.97 |

**"Cost of goods sold" — the fee drag.** The 0.40% gross expense ratio applied to \$141.0B of AUM implies roughly **\$564M of annual fees**, paid by selling bullion. This is the structural erosion built into the product: gold per share declines over time. Each share represented ~0.0936 oz at the time of this note's prior revision and ~0.0917 oz now. Over a decade that compounds to a ~4% shortfall versus holding metal outright, before any tracking error.

**AUM trajectory.** AUM was \$152.9B in early September 2026 and \$141.05B on 2026-09-28 — a ~7.8% decline driven almost entirely by the gold price, not redemptions. Separately, GLD is losing wallet share within the category even as the category grows.

**Tracking quality.** GLD tracks the LBMA Gold Price PM closely and the gap is almost exactly the fee. State Street reports NAV returns to 2026-08-31 of +5.64% YTD, +32.54% for one year, +19.76% annualized over five years and +10.86% annualized since inception, against benchmark figures of +4.46%, +33.06%, +20.24% and +11.30%. The consistent ~40–50bp annual lag is the expense ratio doing exactly what it says.

**Where the price sits now.** The September selloff has been sharp. Gold gained ~9% in August, peaked near \$4,696/oz on 2026-08-25, then fell ~8% through September, closing near \$4,149/oz on 2026-09-28 after a ~3% single-session drop. On the Yahoo Finance quote used for this note, GLD is +7.2% over the trailing year, sits 26% below its 52-week high of \$509.70, 7.8% above its 52-week low of \$350.87, and below both its 50-day (\$395.62) and 200-day (\$416.39) moving averages. Both averages are declining. That is a downtrend, not a dip.

## Valuation

Gold has no cash flows, so there is no multiple and no DCF. Valuation is a macro call on real yields, the dollar, and official-sector demand, cross-checked against published bank forecasts. Targets below are 12-month GLD share-price ranges, with the implied gold price at the current ~0.0917 oz/share conversion.

| Scenario | GLD target | Implied gold | Rationale |
|----------|-----------|--------------|-----------|
| **Bull** | \$495–550 | ~\$5,400–6,000/oz | Fed hiking cycle ends by early 2027 and reverses; central bank buying stays near record; ETF holdings keep compounding. Goldman Sachs reiterates \$5,400/oz for end-2027; J.P. Morgan's 2027 average forecast is \$6,263/oz. |
| **Base** | \$420–460 | ~\$4,600–5,000/oz | Rates peak near 4.25%, then plateau; official-sector demand persists; Asian investment demand offsets weak jewellery. ICICI Bank sees \$4,200–4,600/oz through end-2026 and \$4,600–5,000/oz in H1 2027; UBS reiterates \$5,000/oz by H1 2027. |
| **Bear** | \$320–360 | ~\$3,500–3,900/oz | Fed hikes in both October and December and signals more; 30-year yield pushes through 5.75%; dollar rallies; the momentum cohort that drove 2025–26 unwinds. Macquarie is the bearish outlier at a ~\$4,323/oz average. |

**Bull \$495–550 · Base \$420–460 · Bear \$320–360**

Base case implies roughly +11% to +22% from \$377.91. Bear case implies -5% to -15%. The asymmetry is mildly favourable, but every bank in the consensus cut its 2026 target during the year — J.P. Morgan to \$4,500, Goldman from \$5,400 to \$4,900, with Wells Fargo at \$4,900–5,100 and UBS at \$5,500 — and forecasts that keep getting revised downward are weak support for an entry.

## Growth Catalysts

- **Central bank accumulation at record pace.** Net official-sector purchases were 289t in Q2 2026, up 62% year over year and the strongest second quarter in World Gold Council records — bought *while* gold posted its worst quarterly decline since 2013. Poland added 51t, China 33t (its largest quarterly addition since late 2023). This is the price-insensitive buyer that did not exist a decade ago.
- **ETF holdings at all-time highs.** Global gold-ETF holdings rose 121t in August to a then-record 4,189t with category AUM up 16% to ~\$615B, August being the second-largest monthly inflow on record in dollar terms (~\$18B). Holdings then passed **4,250t for the first time ever** in the week to ~2026-09-19 — eleven consecutive weeks of inflows, including 27.1t (~\$3.9B) in one week — despite rising real rates.
- **Asian demand rotation.** North America was the only region in net ETF outflow across H1 2026 while Asia recorded its strongest first half on record. A US-centric read of flows understates global demand.
- **End of the hiking cycle.** The single largest swing variable cited by multiple banks is the Fed path. Goldman has pushed its first expected cut to June 2027; any data that pulls that forward is directly gold-positive.
- **Fiscal and term-premium stress.** The 30-year Treasury yield at 5.53%, its highest since 2004, cuts both ways: it raises gold's opportunity cost near term, but a disorderly term-premium repricing is historically a reserve-diversification catalyst.
- **Record demand value.** First-half 2026 total gold demand including OTC reached 2,522t (+2% y/y) at a record value of US\$380B.

## Risk Factors

- **A hiking Fed.** The FOMC raised the target range 25bp to 3.75–4.00% on 2026-09-16 — the first increase since 2023, a unanimous 12-0 vote — and signalled one more this year. Markets price better-than-even odds of an October hike. Rising nominal and real yields are the textbook headwind for a zero-yield asset.
- **Dollar strength.** Gold's short-run correlation to the dollar and front-end yields tightened to roughly -0.97 to -0.99 over the five sessions into 2026-09-28. Macro, not demand, is setting the price right now.
- **Momentum unwind.** Gold is ~26% below its late-January 2026 record. GLD trades below both its 50-day and 200-day averages, and independent technical work flagged near-term sell signals across major gold instruments as of 2026-09-26.
- **Fee drag and wrapper competition.** 0.40% versus 0.09–0.25% for functionally identical funds costs roughly \$564M a year in aggregate and is driving persistent share rotation out of GLD. This is a permanent relative-return handicap regardless of where gold goes.
- **Zero income.** With cash yielding near 4%, the opportunity cost of holding GLD is now material and rising.
- **Price-elastic demand destruction.** Q2 jewellery demand fell to 278t, one of the weakest quarters on record, as high prices curbed consumer buying. Mine supply and recycling also respond to price with a lag.
- **Structural / counterparty.** Shares are a claim on a trust, not allocated metal. No 1940 Act or CEA protection. Custody concentrates in HSBC and JPMorgan London vaults.
- **Forced-liquidation reflexivity.** In a broad deleveraging, GLD's liquidity makes it a first source of funds — the trust sells bullion into a falling market to meet redemptions.

## Recommendation

- **Rating:** **HOLD**

**Why HOLD and not BUY.** The structural case for gold is the strongest it has been in this cycle — record central bank buying, record ETF tonnage, record demand value. But the cyclical driver has flipped hard against it. A Fed that is raising rates with another hike better than even for October, a 30-year yield at a 22-year high, and a price below both major moving averages is not an environment in which to be adding to a non-yielding asset. The base case offers +11% to +22% over twelve months, which is a fair reward, but the entry can very likely be improved. Existing core allocations should be kept; new money should be staged.

- **Position sizing:** 3–7% of portfolio as a core diversifier. Trim toward the low end of any existing overweight.
- **Entry strategy:** Scale in thirds. Do not chase. First tranche on a hold of the \$370–378 area, second below \$360, third only on a reclaim of the 50-day (\$395.62) on volume. A confirmed close back above the 200-day (\$416.39) would be the signal that the September regime break has failed.
- **Stop loss / invalidation:** A weekly close below \$348 breaks the 52-week low (\$350.87) and invalidates the base case. For fundamental invalidation, watch two quarters of sub-150t central bank net purchases plus sustained global ETF outflows.
- **Cheaper expression:** For buy-and-hold exposure with no options or intraday liquidity requirement, GLDM (0.10%) or IAUM (0.09%) deliver the identical trade at a quarter to a tenth of the annual cost. GLD is worth its fee for traders and options users, not for a ten-year hold.
- **Time horizon:** 12–24 months.
- **Catalyst calendar:**
  - **2026-10** — September core CPI. Citi's economist argues this is the one data point that could stop an October hike.
  - **2026-10-28** — FOMC decision and statement. Markets price better-than-even odds of a second consecutive 25bp hike.
  - **Late 2026-10** — World Gold Council *Gold Demand Trends* Q3 2026, with Q3 central bank net purchases.
  - **2026-11** — GLD Form 10-K for the fiscal year ended 2026-09-30.
  - **2026-12-09** — FOMC decision. The Fed signalled one more hike in 2026 at the September meeting.
  - **H1 2027** — the window in which UBS sees \$5,000/oz and Goldman's first expected rate cut (June 2027) falls.

## Sentiment Analysis

**Analyst and bank positioning — bullish but repeatedly marked down.** Every major bank cut its 2026 gold forecast during the year. As of September 2026: J.P. Morgan \$4,500 year-end 2026, Goldman Sachs \$4,900 (down from \$5,400 in June, when it removed all 2026 rate cuts from its base case), Wells Fargo \$4,900–5,100, UBS \$5,500. Every one of those sits above the \$4,145 spot — the consensus is directionally positive. For 2027 the cluster is \$5,000–6,300: Goldman \$5,400 end-2027 (reiterated after the September hike), UBS \$5,000 by H1 2027, J.P. Morgan a \$6,263 average, with Macquarie the bearish outlier near a \$4,323 average. A consensus that is uniformly above spot *and* has been revised down four times is a mixed signal, not a clean bullish one.

**Flows — the most constructive datapoint.** Eleven consecutive weeks of global gold-ETF inflows through ~2026-09-19, holdings above 4,250t for the first time ever, August the second-largest inflow month on record. BullionVault framed it as demand "defying rising real rates." Investors are buying this drawdown.

**Fund-level flows — GLD specifically is losing share.** The \$603M single-week redemption in the week to 2026-09-12 against \$403M of inflows into GLDM, IAU and IAUM is fee arbitrage, not a gold verdict, but it is a real headwind for GLD's own AUM. Category-wide precious-metals ETFs were down only \$182M that week.

**Regional split.** North America was the only region in net ETF outflow across H1 2026; Asia had its strongest first half on record.

**Technical tone — negative.** Price below a declining 50-day and 200-day. Independent cycle analysis characterised the August-to-September decline as mean reversion after price extended far above the 34-day average, with an 85–90% reversion probability — i.e. structurally expected rather than thesis-breaking. Separate analysis on 2026-09-26 flagged near-term sell signals across major gold instruments.

**News tone.** Mixed-to-cautious. The dominant narrative into month-end is dollar and yields, not demand: a record flash composite PMI of 58.4 in September (fastest US business activity growth in over five years) pushed spot to \$4,280 on 2026-09-23, and the 30-year yield print did further damage.

**Retail and social, options flow.** Not independently verified in this session — no social-sentiment or options-positioning data source was available. Treat the absence as unknown rather than neutral. GLD does have deep listed options, so positioning data exists; it simply was not sourced here.

**Composite score: 5/10 — neutral.** Strong and improving physical and fund-flow demand, offset by a hostile rate path, a strengthening dollar, negative price structure, and fund-specific share loss.

## Readability Pass

- **ETF (Exchange-Traded Fund):** a fund whose shares trade on a stock exchange. GLD's shares are backed by gold bars sitting in London vaults.
- **Grantor trust:** the legal structure. GLD is not a company with employees and profits; it is a pot of gold with shares issued against it. There is nothing to analyse in the usual income-statement sense.
- **NAV (Net Asset Value):** the value of the gold in the trust divided by the number of shares — \$379.97 on 2026-09-28. The market price (\$377.91) can drift slightly above or below it.
- **AUM (Assets Under Management):** the total value of the trust's gold, \$141.05B. It moves with the gold price and with investor creations and redemptions.
- **Expense ratio:** the annual fee. GLD's 0.40% means \$40 a year on a \$10,000 position, paid by the trust selling a sliver of its gold. That is why each share represents slightly less gold every year.
- **LBMA Gold Price PM:** the London benchmark gold price set each afternoon. GLD uses it to calculate NAV. It was \$4,144.55/oz on 2026-09-28.
- **Real interest rate:** the interest rate after subtracting inflation. Gold pays nothing, so when real rates rise, holding gold costs more in forgone interest. The Fed raising rates pushes real rates up — the core reason gold has fallen.
- **Basis point (bp):** one hundredth of a percent. A 25bp hike is 0.25%.
- **Central bank net purchases:** how much gold governments bought minus what they sold. At 289t in Q2 2026 this is a large, price-insensitive source of demand.
- **Drawdown:** the fall from a peak. Gold is ~26% below its late-January 2026 record, which is a normal-sized correction inside a multi-year uptrend but painful if you bought the top.
- **Moving average (50-day / 200-day):** the average price over the last 50 or 200 trading days. Price below both, with both falling, is the standard definition of a downtrend.
- **Fee arbitrage:** moving money from an expensive fund to a cheap one that does the same thing. That is what GLD's outflows to GLDM and IAU are — not investors selling gold.

## Appendix — Quick Reference

| Metric | Value |
|---|---|
| Price (2026-09-28) | \$377.91 |
| NAV (2026-09-28) | \$379.97 |
| LBMA Gold Price PM (2026-09-28) | \$4,144.55/oz |
| AUM | \$141.05B |
| Shares outstanding | 371.20M |
| Gold per share (implied) | ~0.0917 oz |
| Gold held (derived) | ~34.0M oz / ~1,059 t |
| Gross expense ratio | 0.40% |
| Implied annual fee | ~\$564M |
| 52-week range | \$350.87 – \$509.70 |
| 50-day / 200-day MA | \$395.62 / \$416.39 |
| 1-year return | +7.2% |
| Inception | 2004-11-18 |
| Exchange | NYSE Arca |
| Benchmark | LBMA Gold Price PM |
| Cheaper alternatives | GLDM 0.10%, IAU 0.25%, IAUM 0.09% |
| Rating | HOLD |
| Targets | Bull \$495–550 · Base \$420–460 · Bear \$320–360 |

## Sources Consulted

1. [State Street Investment Management — SPDR Gold Shares (GLD) fund page](https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-shares-gld) — NAV, AUM, shares outstanding, expense ratio, LBMA PM price, custodians, trustee, listing details, and NAV vs benchmark performance to 2026-08-31. Accessed 2026-09-29.
2. [World Gold Council — Gold Demand Trends Q2 2026](https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026) — central bank net purchases of 289t, H1 demand of 2,522t, jewellery demand.
3. [World Gold Council — Gold Demand Trends Q2 2026, Central Banks](https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026/central-banks) — Poland and China purchase detail, revised Q1 estimate.
4. [World Gold Council — Global gold-backed ETF holdings and flows](https://www.gold.org/goldhub/data/global-gold-backed-etf-holdings-and-flows) — August 2026 holdings of 4,189t, AUM +16% to US\$615B.
5. [BullionVault — Gold ETFs Shrink from Record But Demand Defies Rising Real Rates (2026-09-23)](https://www.bullionvault.com/gold-news/gold-price-news/gold-etfs-gld-real-rates-092320261) — global ETF holdings passing 4,250t for the first time.
6. [GoldSilver — \$603 Million Left the World's Biggest Gold ETF (2026-09-16)](https://goldsilver.com/industry-news/goldsilver-news/gold-etf-outflow-fee-arbitrage-gld-gldm-iau/5/) — GLD weekly redemption, GLDM/IAU/IAUM inflows, competing expense ratios.
7. [GoldSilver — Gold Price Forecast 2026 to 2027: Predictions from Top Analysts](https://goldsilver.com/industry-news/article/gold-price-forecast-2026-2027-key-predictions-from-top-analysts/) — September 2026 bank targets: J.P. Morgan \$4,500, Goldman \$4,900, Wells Fargo \$4,900–5,100, UBS \$5,500.
8. [GoldSilver — Goldman Sachs Gold Target Cut](https://goldsilver.com/industry-news/goldsilver-news/goldman-sachs-gold-target-cut-jpmorgan-divergence/) — Goldman's June 2026 cut from \$5,400 to \$4,900 and removal of 2026 rate cuts.
9. [GoldSilver — Gold Price Forecast 2026–2027](https://goldsilver.com/industry-news/article/gold-price-forecast-predictions/) — all-time high of \$5,589.38/oz on 2026-01-28 and the subsequent Q2 decline.
10. [Yahoo Finance — What Fed rate hikes mean for gold prices in 2027, according to Goldman](https://uk.finance.yahoo.com/news/fed-rate-hikes-mean-gold-110610215.html) — Goldman's reiterated \$5,400/oz end-2027 target after the September hike.
11. [Yahoo Finance — UBS sees gold rising to \$5,000/oz by first half of 2027](https://finance.yahoo.com/markets/commodities/articles/ubs-sees-gold-rising-5-123943338.html)
12. [Federal Reserve — FOMC statement, 2026-09-16](https://www.federalreserve.gov/monetarypolicy/files/monetary20260916a1.pdf) and [Chair Warsh press conference transcript](https://www.federalreserve.gov/mediacenter/files/FOMCpresconf20260916.pdf) — 25bp increase to a 3.75–4.00% target range.
13. [CNBC — Fed approves interest rate hike, signals one more to come this year (2026-09-16)](https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html) — unanimous 12-0 vote, first hike since 2023.
14. [Yahoo Finance / Investing.com — October Fed meeting hinges on this key economic data, Citi says](https://ca.finance.yahoo.com/news/october-fed-meeting-hinges-key-114812796.html) — better-than-even market odds of an October hike and the role of September core CPI.
15. [Federal Reserve — FOMC tentative meeting schedule for 2025 and 2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20240809a.htm) — October 27–28 and December 8–9, 2026 meeting dates.
16. [Kitco — Spot gold drops to \$4,280/oz as flash S and P composite PMI improves to 58.4 (2026-09-23)](https://www.kitco.com/news/article/2026-09-23/spot-gold-drops-4280oz-flash-sp-composite-pmi-improves-584-september)
17. [Times Now — Gold's September Correction May Not Last: ICICI Bank Sees Prices Up To \$5,000/Oz](https://www.timesnownews.com/business-economy/markets/golds-september-correction-may-not-last-icici-bank-sees-prices-up-to-5000-oz-article-156229118) — \$4,200–4,600/oz through end-2026, \$4,600–5,000/oz H1 2027.
18. [DiscoveryAlert — Three Gold Price Cycles Explain the Correction](https://discoveryalert.com/analysis/gold-price-cycles-correction-rally/) — the \$4,696.18 peak on 2026-08-25 and mean-reversion framing.
19. [DiscoveryAlert — Gold Sector Outlook, September 2026](https://discoveryalert.com/analysis/gold-sector-outlook-september-2026/) — near-term sell signals as of 2026-09-26 and the Macquarie-to-J.P. Morgan forecast range.
20. [DiscoveryAlert — Precious Metals Market Analysis, September 2026](https://discoveryalert.com/analysis/precious-metals-market-analysis-september-2026/) — the 30-year Treasury yield at 5.53%, highest since 2004.
21. [Forex.com — XAU/USD hit hard as US yields, dollar resume ascent](https://www.forex.com/en-ca/news-and-analysis/gold-outlook-xau-usd-hit-hard-as-us-yields-dollar-resume-ascent/) — five-session gold correlations of roughly -0.97 to -0.99 to the dollar and yields.
22. [The National — Central banks' gold rush hits record in Q2](https://www.thenationalnews.com/business/markets/2026/07/30/central-banks-gold-buying-hits-record-in-q2-as-geopolitical-risks-persist/) — Poland 51t, China 33t, jewellery demand 278t.
23. [Motley Fool — Best Gold ETFs for 2026](https://www.fool.com/investing/stock-market/market-sectors/materials/gold-stocks/gold-etfs/) — GLD AUM of \$152.9B in early September 2026.
24. Yahoo Finance quote for GLD, pre-verified for this session — close of \$377.91 on 2026-09-28, 52-week range \$350.87–509.70, 50-day \$395.62, 200-day \$416.39, trailing one-year return +7.2%.

**Data notes and limitations.** The all-time high is reported inconsistently across sources — \$5,589.38/oz intraday on 2026-01-28 per GoldSilver, ~\$5,608 per one secondary source; the note uses "late January 2026" and the ~26% drawdown figure, which both sources agree on. Ounces and tonnes held are derived from AUM divided by the LBMA PM price rather than taken from State Street's daily holdings disclosure, so treat ~1,059t as an estimate. No social-sentiment or options-positioning data source was available this session, so those sentiment inputs are marked unknown rather than estimated. Scenario targets are the author's conversion of published bank gold-price forecasts into GLD share prices at the current ounces-per-share ratio; they are not fund-provided or analyst price targets on GLD itself.
