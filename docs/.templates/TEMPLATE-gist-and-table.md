# Gist & Table Row Template
#
# This template produces TWO snippets you need to paste:
#   1. A table row     → into docs/index.md AND docs/deep-dives/{sector}.md
#   2. A gist section  → into docs/deep-dives/{sector}.md only
#
# ─────────────────────────────────────────────

## ① TABLE ROW — for docs/index.md
#
# Paste this row into the Summary Table in index.md.
# Note: the link path from index.md is deep-dives/{TICKER}.md

| **{TICKER}** | {COMPANY_NAME} | <span class="badge badge-{BADGE_CLASS}">{SECTOR_LABEL}</span> | <span class="rating-{RATING_CLASS}">{RATING_TEXT}</span> | ${PRICE} | {DATE} | [:material-file-document: Read](deep-dives/{TICKER}.md) |


## ② TABLE ROW — for docs/deep-dives/{sector}.md
#
# Paste this row into the Summary Table in the sector page.
# Note: the link path from sector page is just {TICKER}.md (same directory)

| **{TICKER}** | {COMPANY_NAME} | <span class="rating-{RATING_CLASS}">{RATING_TEXT}</span> | ${PRICE} | {DATE} | [:material-file-document: Read]({TICKER}.md) |


## ③ GIST SECTION — for docs/deep-dives/{sector}.md
#
# Paste this below the last "---" separator in the Gists section.

### {TICKER} — {COMPANY_NAME} · <span class="rating-{RATING_CLASS}">{RATING_TEXT}</span> · ${PRICE}

{GIST_PARAGRAPH}

**Bull:** ${BULL_TARGET} · **Base:** ${BASE_TARGET} · **Bear:** ${BEAR_TARGET}

[:material-arrow-right: Full Deep Dive]({TICKER}.md)


# ─────────────────────────────────────────────
# REFERENCE: Available badge classes
#
#   badge-tech       → Technology
#   badge-space      → Space
#   badge-energy     → Energy
#   badge-materials  → Materials
#   badge-health     → Health
#   badge-fintech    → Fintech
#   badge-consumer   → Consumer
#
# REFERENCE: Available rating classes
#
#   rating-buy        → BUY
#   rating-spec-buy   → SPEC. BUY
#   rating-hold       → HOLD
#   rating-spec-hold  → HOLD / SPEC.
#   rating-sell       → SELL
#   rating-spec       → SPECULATIVE
