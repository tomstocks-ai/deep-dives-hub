#!/usr/bin/env python3
"""
Deep Dive Consistency Validator
Run BEFORE git add/commit to catch mismatches across artifacts.

Usage:
    python3 scripts/validate_dd.py TICKER [SECTOR]

Example:
    python3 scripts/validate_dd.py P technology
"""

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"


def fail(msg: str):
    print(f"  ❌ {msg}")
    return False


def ok(msg: str):
    print(f"  ✅ {msg}")
    return True


def warn(msg: str):
    print(f"  ⚠️  {msg}")
    return True


def check_files(ticker: str) -> bool:
    print(f"\n📁 File Existence Checks for {ticker}")
    all_ok = True
    required = {
        f"docs/deep-dives/{ticker}.md": "Deep dive markdown",
        f"docs/api/{ticker}.json": "Per-ticker JSON",
        f"docs/assets/images/{ticker}_rsi.png": "RSI chart PNG",
    }
    for rel_path, desc in required.items():
        path = REPO_ROOT / rel_path
        if path.exists():
            ok(f"{desc}: {rel_path}")
        else:
            all_ok = fail(f"{desc} MISSING: {rel_path}")
    return all_ok


def check_table_refs(ticker: str) -> bool:
    print(f"\n📋 Table Reference Checks")
    all_ok = True
    table_md = DOCS / "table.md"
    if table_md.exists():
        content = table_md.read_text()
        if ticker in content:
            ok(f"{ticker} found in docs/table.md")
        else:
            all_ok = fail(f"{ticker} MISSING from docs/table.md")
    else:
        all_ok = fail("docs/table.md not found")

    tickers_json = DOCS / "api" / "tickers.json"
    if tickers_json.exists():
        content = tickers_json.read_text()
        if f'"{ticker}"' in content:
            ok(f'{ticker} found in docs/api/tickers.json')
        else:
            all_ok = fail(f'{ticker} MISSING from docs/api/tickers.json')
    else:
        all_ok = fail("docs/api/tickers.json not found")
    return all_ok


def extract_price_targets(text: str) -> dict:
    """Extract Bull/Base/Bear targets from markdown text."""
    targets = {}
    # Handle two formats:
    # 1. Gist: **Bull:** $108–116 · **Base:** $76–82 · **Bear:** $51–56
    # 2. Table: | **Bull** | ... | $108 — $116 |
    # 3. Inline: Bull: $108-$116
    patterns = {
        'bull': r'\*\*Bull:?\*\*.*?[$]?([0-9]+)[\s]*[–—\-]+[\s]*[$]?([0-9]+)',
        'base': r'\*\*Base:?\*\*.*?[$]?([0-9]+)[\s]*[–—\-]+[\s]*[$]?([0-9]+)',
        'bear': r'\*\*Bear:?\*\*.*?[$]?([0-9]+)[\s]*[–—\-]+[\s]*[$]?([0-9]+)',
    }
    for key, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            # Normalize: remove spaces, use en-dash, drop duplicate $
            low = m.group(1).strip()
            high = m.group(2).strip()
            targets[key] = f"{low}–{high}"
    return targets


def extract_json_targets(data: dict) -> dict:
    """Extract Bull/Base/Bear targets from JSON."""
    targets = {}
    for case in ['bull_case', 'base_case', 'bear_case']:
        if case in data and 'target' in data[case]:
            # Remove $ and normalize dashes to en-dash
            raw = data[case]['target'].replace('$', '').replace(' ', '')
            raw = raw.replace('—', '–').replace('-', '–')
            # Split on en-dash to get low/high
            parts = raw.split('–')
            if len(parts) == 2:
                key = case.replace('_case', '')
                targets[key] = f"{parts[0]}–{parts[1]}"
    return targets


def check_price_targets(ticker: str, sector: str | None) -> bool:
    print(f"\n🎯 Price Target Consistency")
    all_ok = True

    # 1. From deep dive markdown
    dd_path = DOCS / "deep-dives" / f"{ticker}.md"
    dd_targets = {}
    if dd_path.exists():
        dd_text = dd_path.read_text()
        dd_targets = extract_price_targets(dd_text)
        if dd_targets:
            ok(f"Deep dive targets: {dd_targets}")
        else:
            all_ok = fail("Could not extract price targets from deep dive markdown")
    else:
        all_ok = fail(f"Deep dive file missing: {dd_path}")

    # 2. From JSON
    json_path = DOCS / "api" / f"{ticker}.json"
    json_targets = {}
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text())
            json_targets = extract_json_targets(data)
            if json_targets:
                ok(f"JSON targets: {json_targets}")
            else:
                all_ok = fail("Could not extract price targets from JSON")
        except json.JSONDecodeError as e:
            all_ok = fail(f"Invalid JSON in {json_path}: {e}")
    else:
        all_ok = fail(f"JSON file missing: {json_path}")

    # 3. From sector page gist
    if sector:
        sector_path = DOCS / "deep-dives" / f"{sector}.md"
        if sector_path.exists():
            sector_text = sector_path.read_text()
            # Find the gist block for this ticker
            gist_pattern = rf'### {re.escape(ticker)} .*?\n\n.*?(?=\n---|\Z)'
            m = re.search(gist_pattern, sector_text, re.DOTALL)
            if m:
                gist_text = m.group(0)
                gist_targets = extract_price_targets(gist_text)
                if gist_targets:
                    ok(f"Sector gist targets: {gist_targets}")
                else:
                    all_ok = fail(f"Could not extract price targets from {sector}.md gist")
            else:
                all_ok = fail(f"Could not find gist block for {ticker} in {sector}.md")
        else:
            warn(f"Sector file not found: {sector_path} (skipping gist check)")
            gist_targets = {}
    else:
        warn("No sector provided (skipping gist check)")
        gist_targets = {}

    # Compare all available
    refs = {'deep_dive': dd_targets, 'json': json_targets, 'sector_gist': gist_targets}
    active = {k: v for k, v in refs.items() if v}
    if len(active) >= 2:
        first_key = list(active.keys())[0]
        first_targets = active[first_key]
        for source, targets in active.items():
            if targets != first_targets:
                all_ok = fail(
                    f"MISMATCH: {first_key} targets {first_targets} != {source} targets {targets}"
                )
        if all_ok:
            ok("All price targets match across artifacts")
    return all_ok


def check_rating_consistency(ticker: str, sector: str | None) -> bool:
    print(f"\n⭐ Rating Consistency")
    all_ok = True
    ratings = {}

    dd_path = DOCS / "deep-dives" / f"{ticker}.md"
    if dd_path.exists():
        text = dd_path.read_text()
        # Look for rating in recommendation section or front matter
        m = re.search(r'rating-(\w+)', text)
        if m:
            ratings['deep_dive'] = m.group(1)

    json_path = DOCS / "api" / f"{ticker}.json"
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text())
            if 'rating' in data:
                # Normalize: HOLD -> hold, SPEC. BUY -> spec-buy
                r = data['rating'].lower().replace('.', '').replace(' ', '-')
                ratings['json'] = r
        except json.JSONDecodeError:
            pass

    if sector:
        sector_path = DOCS / "deep-dives" / f"{sector}.md"
        if sector_path.exists():
            text = sector_path.read_text()
            # Find gist block
            gist_pattern = rf'### {re.escape(ticker)} .*?\n\n.*?(?=\n---|\Z)'
            m = re.search(gist_pattern, text, re.DOTALL)
            if m:
                gist_text = m.group(0)
                m2 = re.search(r'rating-(\w+)', gist_text)
                if m2:
                    ratings['sector_gist'] = m2.group(1)

    if ratings:
        values = set(ratings.values())
        if len(values) == 1:
            ok(f"Rating consistent: {list(values)[0]} across {list(ratings.keys())}")
        else:
            all_ok = fail(f"Rating MISMATCH across files: {ratings}")
    else:
        all_ok = fail("Could not extract rating from any file")
    return all_ok


def check_json_validity(ticker: str) -> bool:
    print(f"\n🔧 JSON Validity")
    all_ok = True
    json_path = DOCS / "api" / f"{ticker}.json"
    if json_path.exists():
        try:
            json.loads(json_path.read_text())
            ok(f"{ticker}.json is valid JSON")
        except json.JSONDecodeError as e:
            all_ok = fail(f"Invalid JSON: {e}")
    else:
        all_ok = fail(f"Missing {json_path}")

    tickers_json = DOCS / "api" / "tickers.json"
    if tickers_json.exists():
        try:
            json.loads(tickers_json.read_text())
            ok("tickers.json is valid JSON")
        except json.JSONDecodeError as e:
            all_ok = fail(f"Invalid tickers.json: {e}")
    else:
        all_ok = fail("Missing tickers.json")
    return all_ok


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    sector = sys.argv[2].lower() if len(sys.argv) > 2 else None

    print(f"\n{'='*60}")
    print(f"🔍 Validating Deep Dive: {ticker}")
    print(f"{'='*60}")

    results = []
    results.append(check_files(ticker))
    results.append(check_table_refs(ticker))
    results.append(check_json_validity(ticker))
    results.append(check_rating_consistency(ticker, sector))
    results.append(check_price_targets(ticker, sector))

    print(f"\n{'='*60}")
    if all(results):
        print("✅ ALL CHECKS PASSED — safe to commit")
        print(f"{'='*60}\n")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED — fix issues before committing")
        print(f"{'='*60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
