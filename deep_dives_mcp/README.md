# Deep Dives Hub — MCP Server

Exposes 97 structured stock deep dives as MCP tools and resources, consumable
by Claude Desktop, the `claude` CLI, and any MCP-compatible agent.

## Install

```bash
# Option A — pip
pip install fastmcp
pip install -e .            # installs the deep-dives-mcp script

# Option B — Poetry extras
poetry install --extras mcp
```

## Run

```bash
# stdio mode (Claude Desktop / claude CLI)
deep-dives-mcp

# or without installing the script:
python -m deep_dives_mcp.server

# Remote mode — no repo clone needed, reads live GitHub Pages API
DEEP_DIVES_REMOTE=1 deep-dives-mcp
```

## Claude Desktop config

`~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "deep-dives-hub": {
      "command": "deep-dives-mcp",
      "cwd": "/path/to/deep-dives-hub"
    }
  }
}
```

Remote mode (no repo clone needed):

```json
{
  "mcpServers": {
    "deep-dives-hub": {
      "command": "deep-dives-mcp",
      "env": { "DEEP_DIVES_REMOTE": "1" }
    }
  }
}
```

## Tools

| Tool | Description |
|---|---|
| `list_tickers` | Filter all 97 tickers by theme, sector, and/or rating |
| `get_deep_dive` | Full structured deep dive for one ticker |
| `get_thesis` | Investment thesis only — token-efficient shortcut |
| `compare_tickers` | Side-by-side targets + thesis snippets for a list |
| `find_catalysts` | Upcoming events across all tickers in a date range |
| `get_schema` | JSON Schema describing the API data format |

## Resources

| URI | Contents |
|---|---|
| `deep-dives://index` | Full `tickers.json` master index |
| `deep-dives://{TICKER}` | Full `{TICKER}.json` deep dive |

## Runtime modes

| Mode | Source | When to use |
|---|---|---|
| LOCAL (default) | `docs/api/*.json` on disk | Development, fastest |
| REMOTE (`DEEP_DIVES_REMOTE=1`) | Live GitHub Pages API | No repo clone needed |

`tickers.json` is cached in memory in LOCAL mode. Individual ticker files are
re-read on every call so edits take effect immediately.
