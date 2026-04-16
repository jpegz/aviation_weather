# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install in development mode (includes dev dependencies)
pip install -e ".[dev]"

# Run tests
pytest

# Lint and format check
ruff check .
ruff format --check .

# Auto-fix lint and format
ruff check --fix .
ruff format .

# Install pre-commit hooks (runs ruff automatically on git commit)
pre-commit install

# Run the CLI
python -m aviation_weather metar KJFK
python -m aviation_weather taf KJFK --text
python -m aviation_weather metar KJFK KLAX --all --hours-before-now 12
```

## Architecture

The library fetches METAR and TAF aviation weather data from the aviationweather.gov REST API and returns either raw text or a human-readable breakdown.

### Module layout

```
aviation_weather/
  __init__.py     # Public API exports
  __main__.py     # CLI entry point — all logic inside main()
  tools.py        # Core logic (all real work happens here)
  metar.py        # Thin wrappers: metars(), metars_xml()
  taf.py          # Thin wrappers: tafs(), tafs_xml()
```

### Data flow

All calls go through `tools.py`:

1. `_fetch_json()` — fetches JSON from `/api/data/metar` or `/api/data/taf`
2. `aviation_weather()` — calls `_fetch_json()`, returns raw strings or calls `_to_readable()`
3. `aviation_xml()` — fetches XML from the same endpoints with `format=xml`
4. `metar.py` / `taf.py` — convenience wrappers that hardcode `data_source`

### API endpoints

```
https://aviationweather.gov/api/data/metar?ids={ICAO}&hours={int}&format=json
https://aviationweather.gov/api/data/taf?ids={ICAO}&hours={int}&format=json
```

The `format=xml` variant is also supported by the API and returns the legacy XML schema
(field names: `altim_in_hg`, `station_id`, `sky_condition`, etc.).

### Key details

- `data_source` strings are singular: `"metar"` and `"taf"` (matches the API endpoints)
- `altim` in JSON responses is in **hPa** — `_to_readable()` converts to inHg via `× 0.02953`
- `wgst` (gusts) is absent from the JSON response when there are no gusts, not null
- `most_recent=True` (default) takes `records[0]` — the API returns reverse-chronological order
- The `_xml` functions keep the old `most_recent` parameter for backward compatibility but ignore it

### Branch workflow

All changes go on feature branches and are merged via pull requests. Do not commit directly to `master`.
