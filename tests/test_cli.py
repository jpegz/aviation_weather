"""Tests for aviation_weather/__main__.py (the CLI entry point).

Verifies that the CLI correctly parses arguments, constructs the right API
request, and prints the expected output. HTTP calls are mocked with responses.
"""

import sys

import pytest
import responses as rsps

from aviation_weather.__main__ import main

from .conftest import METAR_KJFK, METAR_KLAX, TAF_KJFK

BASE = "https://aviationweather.gov/api/data"


@rsps.activate
def test_cli_metar_raw_default(capsys):
    """Default output is the raw METAR string."""
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK])
    sys.argv = ["aviation_weather", "metar", "KJFK"]
    main()
    out = capsys.readouterr().out.strip()
    assert out == METAR_KJFK["rawOb"]


@rsps.activate
def test_cli_taf_raw_default(capsys):
    """Default output for taf is the raw TAF string."""
    rsps.add(rsps.GET, f"{BASE}/taf", json=[TAF_KJFK])
    sys.argv = ["aviation_weather", "taf", "KJFK"]
    main()
    out = capsys.readouterr().out.strip()
    assert out == TAF_KJFK["rawTAF"]


@rsps.activate
def test_cli_metar_text_flag(capsys):
    """--text flag produces human-readable output."""
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK])
    sys.argv = ["aviation_weather", "metar", "KJFK", "--text"]
    main()
    out = capsys.readouterr().out
    assert "Station: KJFK" in out
    assert "Temperature:" in out
    assert "Flight category:" in out


@rsps.activate
def test_cli_all_flag_returns_multiple(capsys):
    """--all returns every record in the time window, not just the most recent."""
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK, METAR_KLAX])
    sys.argv = ["aviation_weather", "metar", "KJFK,KLAX", "--all"]
    main()
    out = capsys.readouterr().out
    assert METAR_KJFK["rawOb"] in out
    assert METAR_KLAX["rawOb"] in out


@rsps.activate
def test_cli_multiple_stations_joined(capsys):
    """Multiple station arguments are joined with a comma in the API request."""
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK, METAR_KLAX])
    sys.argv = ["aviation_weather", "metar", "KJFK", "KLAX"]
    main()
    url = rsps.calls[0].request.url
    assert "ids=KJFK%2CKLAX" in url or "ids=KJFK,KLAX" in url


@rsps.activate
def test_cli_hours_before_now(capsys):
    """--hours-before-now is forwarded to the API request."""
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK])
    sys.argv = ["aviation_weather", "metar", "KJFK", "--hours-before-now", "6"]
    main()
    assert "hours=6" in rsps.calls[0].request.url


def test_cli_invalid_data_source():
    """Passing an unknown data source should exit with an error."""
    sys.argv = ["aviation_weather", "metars", "KJFK"]
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
