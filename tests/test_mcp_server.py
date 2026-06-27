"""
Unit tests for the Deep Dives Hub MCP server tools.

Imports the tool functions directly — no MCP protocol overhead needed.
All tests use the local docs/api/ fixture data (no mocking).
"""

import os

import pytest

# Ensure LOCAL mode (no network calls)
os.environ.pop("DEEP_DIVES_REMOTE", None)

from deep_dives_mcp.server import (  # noqa: E402  (import after env setup)
    compare_tickers,
    find_catalysts,
    get_deep_dive,
    get_schema,
    get_thesis,
    list_tickers,
)


# ---------------------------------------------------------------------------
# list_tickers
# ---------------------------------------------------------------------------


class TestListTickers:
    def test_no_filter_returns_all(self):
        results = list_tickers()
        assert len(results) >= 80, "Expected at least 80 tickers"

    def test_filter_by_theme(self):
        results = list_tickers(theme="Software")
        assert all("software" in r["theme"].lower() for r in results)
        assert len(results) > 0

    def test_theme_partial_match(self):
        # "AI" should match "AI Buildout"
        results = list_tickers(theme="AI")
        assert all("ai" in r["theme"].lower() for r in results)
        assert len(results) > 0

    def test_filter_by_sector(self):
        results = list_tickers(sector="Technology")
        assert all("technology" in r["sector"].lower() for r in results)
        assert len(results) > 0

    def test_filter_by_rating(self):
        results = list_tickers(rating="BUY")
        assert all("buy" in r["rating"].lower() for r in results)
        assert len(results) > 0

    def test_combined_filters(self):
        results = list_tickers(theme="Software", rating="SPEC. BUY")
        for r in results:
            assert "software" in r["theme"].lower()
            assert "spec" in r["rating"].lower()

    def test_case_insensitive_theme(self):
        lower = list_tickers(theme="software")
        upper = list_tickers(theme="Software")
        assert len(lower) == len(upper)

    def test_case_insensitive_rating(self):
        lower = list_tickers(rating="buy")
        upper = list_tickers(rating="BUY")
        assert len(lower) == len(upper)

    def test_no_match_returns_empty(self):
        results = list_tickers(theme="NonExistentThemeXYZ")
        assert results == []

    def test_result_fields(self):
        results = list_tickers(theme="Software")
        required_keys = {
            "ticker", "company", "sector", "theme", "sub_theme",
            "rating", "price", "price_date", "market_cap", "last_updated",
        }
        for r in results:
            assert required_keys.issubset(r.keys()), f"Missing keys in {r}"


# ---------------------------------------------------------------------------
# get_deep_dive
# ---------------------------------------------------------------------------


class TestGetDeepDive:
    def test_known_ticker(self):
        result = get_deep_dive("ADBE")
        assert result["ticker"] == "ADBE"
        assert result["company"] == "Adobe Inc."
        assert "thesis" in result
        assert "financials" in result
        assert "bull_case" in result
        assert "base_case" in result
        assert "bear_case" in result
        assert "catalysts" in result
        assert "key_risks" in result

    def test_case_insensitive(self):
        upper = get_deep_dive("NVDA")
        lower = get_deep_dive("nvda")
        assert upper["ticker"] == lower["ticker"]

    def test_unknown_ticker_raises(self):
        with pytest.raises(ValueError, match="not found"):
            get_deep_dive("ZZZZUNKNOWN")

    def test_returns_dict(self):
        result = get_deep_dive("AVGO")
        assert isinstance(result, dict)

    def test_staleness_warning_absent_for_recent(self):
        # Any ticker with a recent price_date should NOT have the warning
        # (We test that the key is absent, not its presence, since dates change)
        result = get_deep_dive("NVDA")
        # If price_date is within 90 days of today, no warning expected
        from datetime import date
        from deep_dives_mcp.server import STALE_DAYS
        pd = result.get("price_date")
        if pd:
            age = (date.today() - date.fromisoformat(pd)).days
            if age <= STALE_DAYS:
                assert "price_staleness_warning" not in result


# ---------------------------------------------------------------------------
# get_thesis
# ---------------------------------------------------------------------------


class TestGetThesis:
    def test_returns_thesis_string(self):
        result = get_thesis("ADBE")
        assert isinstance(result["thesis"], str)
        assert len(result["thesis"]) > 20

    def test_has_required_fields(self):
        result = get_thesis("AVGO")
        assert "ticker" in result
        assert "company" in result
        assert "rating" in result
        assert "price_date" in result
        assert "thesis" in result

    def test_no_financials_in_result(self):
        result = get_thesis("NVDA")
        assert "financials" not in result
        assert "bull_case" not in result
        assert "catalysts" not in result

    def test_case_insensitive(self):
        r1 = get_thesis("NVDA")
        r2 = get_thesis("nvda")
        assert r1["thesis"] == r2["thesis"]

    def test_unknown_ticker_raises(self):
        with pytest.raises(ValueError, match="not found"):
            get_thesis("ZZZZUNKNOWN")


# ---------------------------------------------------------------------------
# compare_tickers
# ---------------------------------------------------------------------------


class TestCompareTickers:
    def test_basic_comparison(self):
        results = compare_tickers(["NVDA", "AVGO"])
        assert len(results) == 2
        tickers_out = {r["ticker"] for r in results}
        assert tickers_out == {"NVDA", "AVGO"}

    def test_required_fields(self):
        results = compare_tickers(["ADBE"])
        r = results[0]
        assert "ticker" in r
        assert "company" in r
        assert "rating" in r
        assert "price" in r
        assert "price_date" in r
        assert "bull_target" in r
        assert "base_target" in r
        assert "bear_target" in r
        assert "thesis_snippet" in r

    def test_thesis_snippet_length(self):
        results = compare_tickers(["ADBE"])
        snippet = results[0]["thesis_snippet"]
        # snippet is max 123 chars (120 + "...")
        assert len(snippet) <= 123

    def test_thesis_snippet_ends_with_ellipsis_when_long(self):
        # Get a ticker known to have a long thesis
        results = compare_tickers(["NVDA"])
        snippet = results[0]["thesis_snippet"]
        full = get_deep_dive("NVDA")["thesis"]
        if len(full) > 120:
            assert snippet.endswith("...")

    def test_unknown_ticker_graceful(self):
        results = compare_tickers(["NVDA", "ZZZZUNKNOWN"])
        errors = [r for r in results if "error" in r]
        assert len(errors) == 1
        assert errors[0]["ticker"] == "ZZZZUNKNOWN"
        assert errors[0]["error"] == "not found"

    def test_all_unknown(self):
        results = compare_tickers(["AAAA", "BBBB"])
        assert all("error" in r for r in results)

    def test_case_insensitive(self):
        results = compare_tickers(["nvda", "avgo"])
        tickers_out = {r["ticker"] for r in results}
        assert "NVDA" in tickers_out
        assert "AVGO" in tickers_out


# ---------------------------------------------------------------------------
# find_catalysts
# ---------------------------------------------------------------------------


class TestFindCatalysts:
    def test_returns_list(self):
        results = find_catalysts("2026-01")
        assert isinstance(results, list)

    def test_result_fields(self):
        results = find_catalysts("2026-01")
        if results:
            r = results[0]
            assert "ticker" in r
            assert "company" in r
            assert "catalyst_date" in r
            assert "iso_date" in r
            assert "event" in r

    def test_sorted_by_iso_date(self):
        results = find_catalysts("2026-01")
        dates = [r["iso_date"] for r in results]
        # Pad and check ascending
        from deep_dives_mcp.server import _pad_iso_date
        padded = [_pad_iso_date(d) for d in dates]
        assert padded == sorted(padded)

    def test_null_iso_dates_excluded(self):
        results = find_catalysts("2026-01")
        assert all(r["iso_date"] is not None for r in results)

    def test_before_date_filter(self):
        narrow = find_catalysts("2026-07", "2026-09")
        # All narrow results must be within the range
        from deep_dives_mcp.server import _pad_iso_date
        for r in narrow:
            assert _pad_iso_date(r["iso_date"]) >= "2026-07-01"
            assert _pad_iso_date(r["iso_date"]) <= "2026-09-01"

    def test_after_date_excludes_earlier(self):
        results = find_catalysts("2030-01")
        # No catalysts should be in 2030+ given current data
        assert results == []

    def test_year_only_date(self):
        # "2026" should be padded to "2026-01-01"
        results = find_catalysts("2026")
        assert isinstance(results, list)

    def test_full_date_format(self):
        results = find_catalysts("2026-01-01")
        assert isinstance(results, list)


# ---------------------------------------------------------------------------
# get_schema
# ---------------------------------------------------------------------------


class TestGetSchema:
    def test_returns_dict(self):
        result = get_schema()
        assert isinstance(result, dict)

    def test_has_schema_key(self):
        result = get_schema()
        assert "$schema" in result

    def test_has_defs(self):
        result = get_schema()
        assert "$defs" in result

    def test_has_rating_def(self):
        result = get_schema()
        assert "rating" in result.get("$defs", {})

    def test_has_catalyst_def(self):
        result = get_schema()
        assert "catalyst" in result.get("$defs", {})
