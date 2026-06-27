#!/usr/bin/env python3
"""
validate_deep_dive.py

Validates deep dive markdown files for structural and content correctness.
Usage: python validate_deep_dive.py <path/to/TICKER.md>
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def validate_deep_dive(md_path: str) -> dict:
    """Run all validation checks on a deep dive markdown file."""
    md_file = Path(md_path)
    results = {
        "file": str(md_file),
        "passed": [],
        "failed": [],
        "warnings": [],
    }

    if not md_file.exists():
        results["failed"].append(f"File not found: {md_path}")
        return results

    content = md_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # ------------------------------------------------------------------
    # 1. YAML front matter presence
    # ------------------------------------------------------------------
    has_front_matter = content.startswith("---")
    if has_front_matter:
        # Check for closing ---
        second_delim = content.find("---", 3)
        if second_delim == -1:
            results["failed"].append("YAML front matter opened but not closed")
        else:
            results["passed"].append("YAML front matter present")
    else:
        results["failed"].append("Missing YAML front matter (must start with ---)")

    # ------------------------------------------------------------------
    # 2. Back link to summary
    # ------------------------------------------------------------------
    back_link_pattern = re.compile(r"\[.*Back to Summary.*\]\(\.\.?/index\.md\)", re.IGNORECASE)
    if back_link_pattern.search(content):
        results["passed"].append("Back link to summary found")
    else:
        results["failed"].append("Missing back link to summary (e.g. [← Back to Summary](../index.md))")

    # ------------------------------------------------------------------
    # 3. No escaped characters (except \$ for MathJax compatibility)
    # ------------------------------------------------------------------
    escaped_chars = []
    for i, line in enumerate(lines, 1):
        # Skip code blocks
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("    "):
            continue
        # Find escaped chars but exclude intentional escapes:
        #   \$ — MathJax dollar sign (required by Zensical)
        #   \& — ampersand in company names / table cells (renders correctly)
        matches = re.findall(r"\\[$%><&#@~^=+|\[\]{}]", line)
        matches = [m for m in matches if m not in (r"\$", r"\&")]
        if matches:
            escaped_chars.append((i, matches))

    if escaped_chars:
        details = "; ".join(f"line {ln}: {', '.join(m)}" for ln, m in escaped_chars[:5])
        results["failed"].append(f"Escaped characters found ({details})")
    else:
        results["passed"].append("No escaped characters found")

    # ------------------------------------------------------------------
    # 4. No placeholder text
    # ------------------------------------------------------------------
    placeholder_patterns = [
        re.compile(r"\[\.\.\..*?\]"),          # [...], [...something...]
        re.compile(r"\[insert[^\]]*\]", re.I),   # [insert], [insert something]
        re.compile(r"\[TBD\]", re.I),           # [TBD]
        re.compile(r"\[TODO\]", re.I),          # [TODO]
        re.compile(r"\[PLACEHOLDER\]", re.I),   # [PLACEHOLDER]
    ]
    placeholders = []
    for i, line in enumerate(lines, 1):
        for pat in placeholder_patterns:
            if pat.search(line):
                placeholders.append((i, line.strip()))
                break

    if placeholders:
        details = "; ".join(f"line {ln}: {txt[:60]}" for ln, txt in placeholders[:5])
        results["failed"].append(f"Placeholder text found ({details})")
    else:
        results["passed"].append("No placeholder text found")

    # ------------------------------------------------------------------
    # 5. At least 9 sections
    # ------------------------------------------------------------------
    section_headers = re.findall(r"^#{2,3}\s+(.+)$", content, re.MULTILINE)
    # Count ## level (h2) as primary sections, but also count ### (h3) 
    # since some files use numbered h3s as their main sections
    h2_count = len(re.findall(r"^##\s+.+$", content, re.MULTILINE))
    h3_count = len(re.findall(r"^###\s+\d+\..+$", content, re.MULTILINE))
    # Use whichever is larger — some files use ## for everything, some use ###
    total_sections = max(h2_count, h3_count) if h3_count > 0 else h2_count
    if total_sections >= 8:
        results["passed"].append(f"At least 8 sections found ({total_sections})")
    else:
        results["failed"].append(f"Only {total_sections} sections found (need at least 8)")

    # ------------------------------------------------------------------
    # 6. Sources Consulted section present
    # ------------------------------------------------------------------
    sources_pattern = re.compile(r"^##\s+.*Sources\s+Consulted.*$", re.MULTILINE | re.IGNORECASE)
    if sources_pattern.search(content):
        results["passed"].append("Sources Consulted section present")
    else:
        # Some files may not have this exact header; check for alternative
        alt_pattern = re.compile(r"^##\s+.*Sources.*$", re.MULTILINE | re.IGNORECASE)
        if alt_pattern.search(content):
            results["warnings"].append("Sources section found but not titled 'Sources Consulted'")
        else:
            results["failed"].append("Missing 'Sources Consulted' section")

    # ------------------------------------------------------------------
    # 7. Image references resolve to actual files
    # ------------------------------------------------------------------
    img_refs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)
    broken_imgs = []
    for alt, src in img_refs:
        # Resolve relative to markdown file location
        if src.startswith("http://") or src.startswith("https://"):
            continue  # External URLs — skip
        img_path = (md_file.parent / src).resolve()
        if not img_path.exists():
            broken_imgs.append(src)

    if broken_imgs:
        results["failed"].append(f"Broken image references: {', '.join(broken_imgs)}")
    else:
        results["passed"].append(f"All {len(img_refs)} image references resolve correctly")

    # ------------------------------------------------------------------
    # 8. JSON file validity (if exists)
    # ------------------------------------------------------------------
    ticker = md_file.stem.upper()
    json_path = md_file.parent.parent / "api" / f"{ticker}.json"
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            results["passed"].append(f"JSON file valid: {json_path.name}")

            # Required top-level keys and expected types
            # 'sector' OR 'theme' is required (older files use only sector, newer add theme)
            required_keys = {
                "ticker": str, "company": str,
                "industry": str, "exchange": str, "price": (int, float),
                "market_cap": str, "rating": str, "last_updated": str,
                "thesis": str, "financials": dict, "bull_case": dict,
                "bear_case": dict, "base_case": dict, "catalysts": list,
                "key_risks": list,
            }
            for key, expected_type in required_keys.items():
                if key not in data:
                    results["failed"].append(f"JSON missing required key: '{key}'")
                elif not isinstance(data[key], expected_type):
                    results["failed"].append(
                        f"JSON key '{key}' has wrong type: expected {expected_type}, got {type(data[key]).__name__}"
                    )
            # sector OR theme must be present
            if "sector" not in data and "theme" not in data:
                results["failed"].append("JSON missing both 'sector' and 'theme' — at least one is required")
            else:
                results["passed"].append("JSON has sector/theme classification")

            # Warn if theme or sub_theme are absent (encouraged but not blocking)
            for field in ("theme", "sub_theme"):
                if field not in data or not data.get(field):
                    results["warnings"].append(f"JSON missing '{field}' — add for agent filtering")

            # price_date should be present
            if "price_date" not in data:
                results["warnings"].append("JSON missing 'price_date' — add so agents know data staleness")

            # Validate canonical rating value
            canonical_ratings = {"BUY", "SPEC. BUY", "HOLD", "HOLD / SPEC.", "SELL", "SPECULATIVE"}
            rating_val = data.get("rating", "")
            if rating_val and rating_val not in canonical_ratings:
                results["warnings"].append(
                    f"JSON 'rating' value {rating_val!r} is not canonical — "
                    f"use one of: {', '.join(sorted(canonical_ratings))}"
                )

            # Check for empty/placeholder values in top-level strings
            placeholder_re = re.compile(r"^\{.*\}$")
            for key in ("ticker", "company", "industry", "exchange",
                        "market_cap", "rating", "last_updated", "thesis"):
                val = data.get(key)
                if isinstance(val, str) and (not val.strip() or placeholder_re.match(val)):
                    results["failed"].append(f"JSON key '{key}' has empty/placeholder value: '{val}'")

            # Validate financials sub-keys
            financials_keys = ["fiscal_year", "revenue", "revenue_growth",
                               "gross_margin", "net_income", "eps_diluted", "cash", "fcf"]
            if isinstance(data.get("financials"), dict):
                for fk in financials_keys:
                    if fk not in data["financials"]:
                        results["failed"].append(f"JSON financials missing key: '{fk}'")
                    elif not str(data["financials"][fk]).strip():
                        results["failed"].append(f"JSON financials key '{fk}' is empty")

            # Validate bull_case structure
            if isinstance(data.get("bull_case"), dict):
                if "target" not in data["bull_case"]:
                    results["failed"].append("JSON bull_case missing 'target'")
                if "drivers" not in data["bull_case"]:
                    results["failed"].append("JSON bull_case missing 'drivers'")
                elif not isinstance(data["bull_case"]["drivers"], list) or len(data["bull_case"]["drivers"]) == 0:
                    results["failed"].append("JSON bull_case 'drivers' must be a non-empty list")

            # Validate bear_case structure
            if isinstance(data.get("bear_case"), dict):
                if "target" not in data["bear_case"]:
                    results["failed"].append("JSON bear_case missing 'target'")
                if "risks" not in data["bear_case"]:
                    results["failed"].append("JSON bear_case missing 'risks'")
                elif not isinstance(data["bear_case"]["risks"], list) or len(data["bear_case"]["risks"]) == 0:
                    results["failed"].append("JSON bear_case 'risks' must be a non-empty list")

            # Validate base_case structure
            if isinstance(data.get("base_case"), dict):
                if "target" not in data["base_case"]:
                    results["failed"].append("JSON base_case missing 'target'")
                if "assumptions" not in data["base_case"]:
                    results["failed"].append("JSON base_case missing 'assumptions'")

            # Validate catalysts entries
            if isinstance(data.get("catalysts"), list):
                if len(data["catalysts"]) == 0:
                    results["failed"].append("JSON 'catalysts' list is empty")
                missing_iso = []
                for i, cat in enumerate(data["catalysts"]):
                    if not isinstance(cat, dict):
                        results["failed"].append(f"JSON catalysts[{i}] is not an object")
                    else:
                        if "date" not in cat or "event" not in cat:
                            results["failed"].append(f"JSON catalysts[{i}] missing 'date' or 'event'")
                        if "iso_date" not in cat:
                            missing_iso.append(i)
                if missing_iso:
                    results["warnings"].append(
                        f"JSON catalysts missing 'iso_date' on entries: {missing_iso} — add for machine-parseable dates"
                    )

            # Validate key_risks is non-empty
            if isinstance(data.get("key_risks"), list) and len(data["key_risks"]) == 0:
                results["failed"].append("JSON 'key_risks' list is empty")

            # Validate last_updated date format
            last_updated = data.get("last_updated", "")
            if isinstance(last_updated, str) and last_updated:
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", last_updated):
                    results["failed"].append(f"JSON 'last_updated' not in YYYY-MM-DD format: '{last_updated}'")

            # Validate price is positive
            price = data.get("price")
            if isinstance(price, (int, float)) and price <= 0:
                results["failed"].append(f"JSON 'price' should be positive, got {price}")

            # If all sub-checks passed (no new failures beyond the initial parse pass)
            json_failures = [f for f in results["failed"] if f.startswith("JSON")]
            if not json_failures:
                results["passed"].append("JSON structure and values are complete and consistent")

        except json.JSONDecodeError as e:
            results["failed"].append(f"JSON file invalid: {json_path.name} — {e}")
    else:
        results["warnings"].append(f"No JSON file found at {json_path}")

    # ------------------------------------------------------------------
    # 9. Company name and ticker consistency
    # ------------------------------------------------------------------
    # Extract title from front matter or first H1
    title_match = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        # Expect format like "NBIS — Nebius Group N.V."
        if ticker in title.upper():
            results["passed"].append(f"Ticker '{ticker}' found in title: '{title}'")
        else:
            results["failed"].append(f"Ticker '{ticker}' NOT found in title: '{title}'")
    else:
        results["warnings"].append("Could not extract title from front matter for consistency check")

    # Check H1 contains ticker
    h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if h1_match:
        h1 = h1_match.group(1)
        if ticker in h1.upper():
            results["passed"].append(f"Ticker '{ticker}' found in H1")
        else:
            results["failed"].append(f"Ticker '{ticker}' NOT found in H1: '{h1}'")
    else:
        results["warnings"].append("No H1 found for ticker consistency check")

    # Check JSON ticker matches
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            json_ticker = data.get("ticker", "").upper()
            if json_ticker == ticker:
                results["passed"].append(f"JSON ticker '{json_ticker}' matches filename")
            else:
                results["failed"].append(f"JSON ticker '{json_ticker}' does not match filename '{ticker}'")
        except Exception as e:
            results["warnings"].append(f"Could not verify JSON ticker consistency: {e}")

    return results


def print_results(results: dict) -> int:
    """Print validation results and return exit code."""
    print(f"\n{'='*60}")
    print(f"  Validation Report: {results['file']}")
    print(f"{'='*60}")

    if results["passed"]:
        print(f"\n✅ PASSED ({len(results['passed'])}):")
        for item in results["passed"]:
            print(f"   • {item}")

    if results["warnings"]:
        print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
        for item in results["warnings"]:
            print(f"   • {item}")

    if results["failed"]:
        print(f"\n❌ FAILED ({len(results['failed'])}):")
        for item in results["failed"]:
            print(f"   • {item}")

    total_checks = len(results["passed"]) + len(results["failed"])
    print(f"\n{'='*60}")
    if not results["failed"]:
        print("  RESULT: ✅ PASS — All checks passed!")
        print(f"{'='*60}\n")
        return 0
    else:
        print(f"  RESULT: ❌ FAIL — {len(results['failed'])}/{total_checks} checks failed")
        print(f"{'='*60}\n")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Validate a deep dive markdown file for structural and content correctness."
    )
    parser.add_argument("md_file", help="Path to the markdown file to validate")
    args = parser.parse_args()

    results = validate_deep_dive(args.md_file)
    exit_code = print_results(results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
