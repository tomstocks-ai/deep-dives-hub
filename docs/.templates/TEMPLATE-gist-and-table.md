# Gist & Table Row Template
#
# This template produces TWO snippets you need to paste:
#   1. A table row     → into docs/table.md AND docs/deep-dives/{theme}.md
#   2. A gist entry    → into docs/deep-dives/{theme}.md only
#
# NOTE: The TradingView ticker widget shows live prices, so we no longer need a Price column.
#
# ─────────────────────────────────────────────

## ① TABLE ROW — for docs/table.md
#
# Paste this row into the All Stocks table in table.md.
# Note: the link path from table.md is deep-dives/{TICKER}.md

| <tv-ticker-tag symbol="{EXCHANGE}:{TICKER}" hide-background></tv-ticker-tag> | {COMPANY_NAME} | <span class="badge badge-{BADGE_CLASS}">{THEME_LABEL}</span> | <span class="rating-{RATING_CLASS}">{RATING_TEXT}</span> | {DATE} | [:material-file-document: Read](deep-dives/{TICKER}.md) |


## ② TABLE ROW — for docs/deep-dives/{theme}.md
#
# Paste this row into the relevant ## section's table in the thematic page.
# Note: the link path from theme page is just {TICKER}.md (same directory)

| <tv-ticker-tag symbol="{EXCHANGE}:{TICKER}" hide-background></tv-ticker-tag> | {COMPANY_NAME} | <span class="rating-{RATING_CLASS}">{RATING_TEXT}</span> | {DATE} | [:material-file-document: Read]({TICKER}.md) |


## ③ GIST ENTRY — for docs/deep-dives/{theme}.md
#
# Paste this below the last "---" separator in the relevant section.
# If the ticker belongs to a sub-theme, place it under the relevant ### heading.
#
# ⚠️ IMPORTANT: Stock gists use BOLD text, NOT ### headers.
#    Only sub-themes use ### headers.

**{TICKER} — {COMPANY_NAME} · <span class="rating-{RATING_CLASS}">{RATING_TEXT}</span>**

{GIST_PARAGRAPH}

**Bull:** ${BULL_TARGET} · **Base:** ${BASE_TARGET} · **Bear:** ${BEAR_TARGET}

[:material-arrow-right: Full Deep Dive]({TICKER}.md)


# ─────────────────────────────────────────────
# PAGE HIERARCHY (how the thematic page is structured):
#
#   ## Section Title          ← top-level theme section (e.g., ## Semiconductors)
#   | table... |              ← summary table for that section
#   ---                       ← separator
#   ### Sub-theme             ← optional sub-theme heading (e.g., ### Analog / Power)
#   **TICKER — Company...**  ← bold gist entry (NOT a ### header)
#   ...gist text...
#   ---                       ← separator before next gist
#   **TICKER — Company...**  ← next gist
#   ---
#   ## Next Section           ← next theme section
#
# ─────────────────────────────────────────────
# REFERENCE: Consolidated Thematic Files
#
#   AI_buildout.md      → Semiconductors, Semiconductor Equipment, Photonics,
#                         Networking & Connectivity, Memory & Storage,
#                         Grid & Power, Data Center Infrastructure
#   energy.md           → Nuclear, Solar, Natural Gas & AI Power Demand
#   software.md         → Cloud & Enterprise Software, Cybersecurity
#   space.md            → Space Economy
#   defense.md          → Defense
#   critical-minerals.md → Critical Minerals & Strategic Materials
#   biotech-health.md   → Biotechnology & Health Technology
#   fintech.md          → Fintech & Digital Payments
#   quantum-computing.md → Quantum Computing
#   evtol.md            → eVTOL & Advanced Air Mobility
#
# ─────────────────────────────────────────────
# REFERENCE: TradingView Exchange Codes
#
#   NASDAQ    → NASDAQ-listed stocks (NasdaqGS, NasdaqCM, NasdaqGM)
#   NYSE      → NYSE-listed stocks
#   AMEX      → NYSE Arca / NYSE American (ETFs like GLD, SLV, URA, COPX)
#   OMXSTO    → Stockholm Stock Exchange (e.g., SIVE)
#
# REFERENCE: Available badge classes (theme-based)
#
#   badge-semi        → Semiconductors
#   badge-networking  → Networking & Connectivity
#   badge-photonics   → Photonics & Optical Interconnects
#   badge-semi-equip  → Semiconductor Equipment
#   badge-dc-infra    → Data Center Infrastructure
#   badge-cloud       → Cloud & Enterprise Software
#   badge-cyber       → Cybersecurity
#   badge-defense     → Defense
#   badge-robotics    → Robotics & Automation
#   badge-space       → Space Economy
#   badge-quantum     → Quantum Computing
#   badge-nuclear     → Nuclear Energy
#   badge-grid        → Grid & Power
#   badge-minerals    → Critical Minerals & Strategic Materials
#   badge-health      → Biotechnology & Health Technology
#   badge-fintech     → Fintech & Digital Payments
#   badge-evtol       → eVTOL & Advanced Air Mobility
#   badge-natgas      → Natural Gas & AI Power Demand
#   badge-memory      → Memory & Storage
#
# REFERENCE: Available rating classes
#
#   rating-buy        → BUY
#   rating-spec-buy   → SPEC. BUY
#   rating-hold       → HOLD
#   rating-spec-hold  → HOLD / SPEC.
#   rating-sell       → SELL
#   rating-spec       → SPECULATIVE
